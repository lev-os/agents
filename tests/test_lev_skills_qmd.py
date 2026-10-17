"""Focused public QMD CLI and refresh checks with isolated fake boundaries."""

import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
import time


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("LEV_SKILLS_TEST_SOURCE", ROOT / "lev-skills.sh")).resolve()
REFRESH_COLLECTIONS = (
    "skills-db",
    "skills-db-bundle-docs",
    "skills-db-archive",
    "skills-db-backlog",
    "skills-db-workshop",
)


class PublicLevSkillsQmdTest(unittest.TestCase):
    def setUp(self):
        self._temporary = tempfile.TemporaryDirectory(prefix="lev-skills-qmd-")
        self.output = Path(self._temporary.name).resolve()
        self.repo = self.output / "repo"
        self.repo.mkdir()
        self.script = self.repo / "lev-skills.sh"
        shutil.copy2(SOURCE, self.script)
        shutil.copy2(ROOT / "lev-skills-qmd.mjs", self.repo / "lev-skills-qmd.mjs")
        self.qmd_bin = self.output / "bin"
        self.qmd_bin.mkdir()
        self.config_dir = self.output / "qmd-config"
        self.config_dir.mkdir()
        self.cache_home = self.output / "cache-home"
        self.model_dir = self.cache_home / "qmd" / "models"
        self.model_dir.mkdir(parents=True)
        self.qmd_prefix = self.output / "qmd-prefix"
        package = self.qmd_prefix / "lib/node_modules/@tobilu/qmd/dist"
        package.mkdir(parents=True)
        (package / "index.js").write_text("export {};\n")
        self.cache_dir = self.output / "lev-cache"
        self.guard_dir = self.output / "guard"
        self.guard_dir.mkdir()
        self.qmd_output = self.output / "qmd-output.json"
        self.node_output = self.output / "node-output.json"
        self.node_args = self.output / "node-args.jsonl"
        self.index_manifest_path = self.output / "qmd-index-manifest.json"
        self._make_sources()
        self._make_qmd_config()
        self._make_fake_node()
        self._write_guard()
        self.write_qmd_results([])
        self.write_node_response(self.complete_refresh_response())

    def tearDown(self):
        self._temporary.cleanup()

    def _make_sources(self):
        self.active_path = self.repo / "skills-db/tools/qmd-sample/SKILL.md"
        self.active_path.parent.mkdir(parents=True)
        self.active_bytes = b"---\nname: qmd-sample\ndescription: local semantic retrieval fixture\n---\n\nBody text for this QMD result.\n"
        self.active_path.write_bytes(self.active_bytes)
        self.variant_path = self.repo / "skills-db/tools/qmd-variant/SKILL.md"
        self.variant_path.parent.mkdir(parents=True)
        self.variant_path.write_bytes(self.active_bytes)
        self.invalid_utf8_path = self.repo / "skills-db/tools/invalid-utf8.md"
        self.invalid_utf8_bytes = b"# Invalid UTF-8 fixture \xff\n"
        self.invalid_utf8_path.write_bytes(self.invalid_utf8_bytes)
        self.archived_path = self.repo / "skills-db/tools/qmd-archived/SKILL.md"
        self.archived_path.parent.mkdir(parents=True)
        self.archived_bytes = b"---\nname: qmd-archived\ndescription: retired retrieval fixture\n---\n\nArchived body.\n"
        self.archived_path.write_bytes(self.archived_bytes)
        self.unknown_path = self.repo / "skills-db/tools/unlisted.txt"
        self.unknown_path.write_text("not an eligible Markdown source\n")
        for relative in (
            "skills-db/.archive",
            "skills-db/_todo",
            "skills-db/_workshop",
            "skills-db/creative/roundtable-marvkr--better-design/source/.agents/skills",
        ):
            (self.repo / relative).mkdir(parents=True, exist_ok=True)
        for relative, data in (
            ("skills-db/.archive/archive-note.md", b"# Archive note\n"),
            ("skills-db/_todo/backlog-note.md", b"# Backlog note\n"),
            ("skills-db/_workshop/workshop-note.md", b"# Workshop note\n"),
            ("skills-db/creative/roundtable-marvkr--better-design/source/.agents/skills/bundle-member/SKILL.md", b"# Bundle member\n"),
        ):
            path = self.repo / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        state = {
            "skills": {
                "skills-db/tools/qmd-archived": {
                    "lifecycle": "archived",
                    "rotation_role": "none",
                }
            }
        }
        (self.repo / "skills-state.json").write_text(json.dumps(state))

    def _make_qmd_config(self):
        paths = {
            "skills-db": self.repo / "skills-db",
            "skills-db-bundle-docs": self.repo / "skills-db/creative/roundtable-marvkr--better-design/source/.agents/skills",
            "skills-db-archive": self.repo / "skills-db/.archive",
            "skills-db-backlog": self.repo / "skills-db/_todo",
            "skills-db-workshop": self.repo / "skills-db/_workshop",
        }
        config = {
            "collections": {
                name: {"path": str(path), "pattern": "**/*.md", "includeByDefault": name in {"skills-db", "skills-db-bundle-docs"}}
                for name, path in paths.items()
            },
            "models": {
                "embed": "hf:fixture/qmd/embedding.gguf",
                "generate": "hf:fixture/qmd/generate.gguf",
                "rerank": "hf:fixture/qmd/rerank.gguf",
            },
        }
        (self.config_dir / "index.yml").write_text(json.dumps(config, indent=2))
        for filename in (
            "hf_fixture_qmd_embedding.gguf",
            "hf_fixture_qmd_generate.gguf",
            "hf_fixture_qmd_rerank.gguf",
        ):
            (self.model_dir / filename).write_bytes(b"GGUF" + b"fixture")
        (self.output / "qmd-index.sqlite").write_bytes(b"isolated-index")
        self.write_index_manifest_snapshot()

    def write_index_manifest_snapshot(self):
        roots = {
            "skills-db": self.repo / "skills-db",
            "skills-db-bundle-docs": self.repo / "skills-db/creative/roundtable-marvkr--better-design/source/.agents/skills",
            "skills-db-archive": self.repo / "skills-db/.archive",
            "skills-db-backlog": self.repo / "skills-db/_todo",
            "skills-db-workshop": self.repo / "skills-db/_workshop",
        }
        documents = []
        for file_path in sorted((self.repo / "skills-db").rglob("*")):
            if not file_path.is_file() or file_path.suffix.lower() != ".md" or ".trash" in file_path.parts:
                continue
            canonical_relative = file_path.relative_to(self.repo / "skills-db").as_posix()
            collection = "skills-db"
            for name in ("skills-db-bundle-docs", "skills-db-archive", "skills-db-backlog", "skills-db-workshop"):
                try:
                    qmd_relative = file_path.relative_to(roots[name]).as_posix()
                    collection = name
                    break
                except ValueError:
                    continue
            else:
                qmd_relative = canonical_relative
            data = file_path.read_bytes()
            documents.append({
                "source_id": f"skills-db/{canonical_relative}",
                "source_relative_path": canonical_relative,
                "file_path": str(file_path.resolve()),
                "source_sha256": hashlib.sha256(data).hexdigest(),
                "collection": collection,
                "path": qmd_relative,
            })
        documents.sort(key=lambda item: (item["collection"], item["path"], item["source_id"]))
        self.index_manifest_path.write_text(json.dumps({"documents": documents}, sort_keys=True))

    def _make_fake_node(self):
        path = self.qmd_bin / "node"
        path.write_text(
            "#!/usr/bin/python3\n"
            "import json, os, sys\n"
            "from pathlib import Path\n"
            "if sys.argv[1:] == ['--version']:\n"
            " print('v24.3.0'); raise SystemExit(0)\n"
            "request=json.loads(sys.argv[2])\n"
            "with open(os.environ['SDB_NODE_ARGS'], 'a') as handle: handle.write(json.dumps({'request':request,'bridge':sys.argv[1]})+'\\n')\n"
            "if request.get('operation') == 'inspect':\n"
            " config=json.loads(Path(request['configPath']).read_text())\n"
            " names=['skills-db','skills-db-bundle-docs','skills-db-archive','skills-db-backlog','skills-db-workshop']\n"
            " collections={name: ({'path':config['collections'][name].get('path'),'pattern':config['collections'][name].get('pattern')} if name in config['collections'] else None) for name in names}\n"
            " model_uris={'embed':'hf:fixture/qmd/embedding.gguf','generate':'hf:fixture/qmd/generate.gguf','rerank':'hf:fixture/qmd/rerank.gguf'}\n"
            " model_files={'embed':'hf_fixture_qmd_embedding.gguf','generate':'hf_fixture_qmd_generate.gguf','rerank':'hf_fixture_qmd_rerank.gguf'}\n"
            " models={}\n"
            " for kind,uri in config.get('models',{}).items():\n"
            "  cached=Path(os.environ['XDG_CACHE_HOME'])/'qmd/models'/model_files.get(kind,'')\n"
            "  model_path=cached if uri==model_uris.get(kind) and cached.is_file() else (Path(uri) if isinstance(uri,str) and Path(uri).is_file() else None)\n"
            "  if model_path is not None:\n"
            "   stat=model_path.stat(); models[kind]={'uri':uri,'path':str(model_path.resolve()),'sizeBytes':stat.st_size,'mtimeMs':stat.st_mtime*1000,'dev':stat.st_dev,'ino':stat.st_ino}\n"
            " model=config.get('models',{}).get('embed'); model_path=models.get('embed',{}).get('path')\n"
            " if len(models)!=3:\n"
            "  print(json.dumps({'status':'error','code':'qmd_model_unavailable','error':'a configured model is not cached'})); raise SystemExit(1)\n"
            " print(json.dumps({'status':'inspected','collections':collections,'embedModel':model,'embedModelPath':model_path,'models':models}))\n"
            "elif request.get('operation') == 'integrity':\n"
            " expected=json.loads(sys.stdin.read())['documents']\n"
            " indexed=json.loads(Path(os.environ['SDB_QMD_INDEX_MANIFEST']).read_text())['documents']\n"
            " if expected != indexed:\n"
            "  print(json.dumps({'status':'error','code':'stale_qmd_index','error':'QMD canonical manifest does not match the isolated index'}))\n"
            " else:\n"
            "  print(json.dumps({'status':'integrity_checked','model':request['model'],'fingerprint':'abcdef','expectedDocuments':len(expected),'actualDocuments':len(indexed),'missingPaths':0,'extraPaths':0,'staleBodies':0,'pendingEmbeddingHashes':0,'missingVectorIds':0}))\n"
            "elif request.get('operation') == 'query':\n"
            " if os.environ.get('SDB_BRIDGE_QUERY_EXIT'):\n"
            "  print(json.dumps({'status':'error','code':'qmd_engine_failed','error':'isolated query failure'})); raise SystemExit(int(os.environ['SDB_BRIDGE_QUERY_EXIT']))\n"
            " raw=Path(os.environ['SDB_QMD_OUTPUT']).read_text()\n"
            " try: results=json.loads(raw)\n"
            " except json.JSONDecodeError: print(raw); raise SystemExit(0)\n"
            " print(json.dumps({'status':'queried','results':results}))\n"
            "else: print(Path(os.environ['SDB_NODE_OUTPUT']).read_text())\n"
        )
        path.chmod(0o755)
        self.node_path = path.resolve()

    def _write_guard(self):
        self.guard_dir.joinpath("sitecustomize.py").write_text(
            """
import os
from pathlib import Path
import sys
allowed = Path(os.environ['SDB_ALLOWED']).resolve()
def permitted(path):
    if isinstance(path, int) or str(path) == '/dev/null': return
    if not Path(path).resolve().is_relative_to(allowed):
        raise PermissionError('fixture guard blocked external write: ' + str(path))
def is_node(raw):
    return Path(raw).resolve() == Path(os.environ['SDB_TEST_NODE']).resolve()
def audit(event, args):
    if event == 'open':
        path, mode, flags = args
        if (mode and any(ch in mode for ch in 'wax+')) or flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND): permitted(path)
    elif event in {'os.mkdir','os.remove','os.rmdir','os.chmod','os.utime'}: permitted(args[0])
    elif event in {'os.rename','os.replace'}: permitted(args[0]); permitted(args[1])
    elif event == 'subprocess.Popen':
        command=args[1]
        if not isinstance(command,(list,tuple)) or not command: raise PermissionError('fixture guard blocked subprocess')
        if not is_node(str(command[0])): raise PermissionError('fixture guard blocked subprocess: '+str(command))
    elif event == 'os.exec':
        target=str(args[0])
        exec_argv=args[1] if len(args)>1 and isinstance(args[1],(list,tuple)) else []
        script_path=Path(exec_argv[1]).resolve() if len(exec_argv)>1 else Path('/')
        explicit_yaml_retry=(Path(target).resolve()==Path('/usr/bin/python3').resolve() and script_path.is_relative_to(allowed) and len(exec_argv)>2 and ((exec_argv[2]=='inventory' and '--rebuild' in exec_argv[3:]) or exec_argv[2]=='refresh'))
        if not (is_node(target) or explicit_yaml_retry): raise PermissionError('fixture guard blocked exec: '+target)
    elif event in {'os.system','socket.connect','sqlite3.connect'}: raise PermissionError('fixture guard blocked effect: '+event)
sys.addaudithook(audit)
"""
        )

    def env(self, overrides=None):
        environment = os.environ.copy()
        environment.update({
            "LEV_CACHE_DIR": str(self.cache_dir),
            "PYTHONPATH": str(self.guard_dir),
            "PYTHONDONTWRITEBYTECODE": "1",
            "SDB_ALLOWED": str(self.output),
            "PATH": str(self.qmd_bin) + os.pathsep + os.defpath,
            "QMD_CONFIG_DIR": str(self.config_dir),
            "XDG_CACHE_HOME": str(self.cache_home),
            "QMD_PREFIX": str(self.qmd_prefix),
            "QMD_NODE": str(self.node_path),
            "INDEX_PATH": str(self.output / "qmd-index.sqlite"),
            "SDB_TEST_NODE": str(self.node_path),
            "SDB_QMD_OUTPUT": str(self.qmd_output),
            "SDB_NODE_OUTPUT": str(self.node_output),
            "SDB_NODE_ARGS": str(self.node_args),
            "SDB_QMD_INDEX_MANIFEST": str(self.index_manifest_path),
        })
        if overrides:
            environment.update(overrides)
        return environment

    def run_cli(self, args, *, env_overrides=None, timeout=30):
        return subprocess.run(
            [sys.executable, str(self.script), *args],
            cwd=self.repo,
            env=self.env(env_overrides),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )

    def run_json(self, args, *, env_overrides=None):
        result = self.run_cli(args, env_overrides=env_overrides)
        self.assertEqual(result.returncode, 0, f"stdout={result.stdout}\nstderr={result.stderr}")
        return json.loads(result.stdout)

    def rebuild_inventory(self):
        result = self.run_cli(["inventory", "--rebuild", "--json"])
        self.assertEqual(result.returncode, 0, f"stdout={result.stdout}\nstderr={result.stderr}")
        return json.loads(result.stdout)

    def write_qmd_results(self, results):
        self.qmd_output.write_text(json.dumps(results, allow_nan=True))

    def write_node_response(self, response, *, exit_code=0):
        if exit_code:
            response = {**response, "test_exit_code": exit_code}
        self.node_output.write_text(json.dumps(response))

    def node_requests(self, operation=None):
        if not self.node_args.exists():
            return []
        requests = [json.loads(line)["request"] for line in self.node_args.read_text().splitlines()]
        return [request for request in requests if operation is None or request.get("operation") == operation]

    def qmd_result(self, path=None, body=None, score=0.86):
        path = path or self.active_path
        if body is None:
            body = path.read_bytes().decode("utf-8", errors="replace")
        display_path = str(path.relative_to(self.repo)) if path.resolve().is_relative_to(self.repo) else str(path)
        return {"file": display_path, "score": score, "body": body, "title": "fixture"}

    def complete_refresh_response(self):
        return {
            "status": "complete",
            "updatedCollections": list(REFRESH_COLLECTIONS),
            "embedCollections": list(REFRESH_COLLECTIONS),
            "force": False,
            "update": {"collections": 5, "indexed": 0, "updated": 0, "unchanged": 2, "removed": 0, "skipped": 0},
            "embeds": [
                {"collection": name, "force": False, "docsProcessed": 0, "chunksEmbedded": 0, "errors": 0}
                for name in REFRESH_COLLECTIONS
            ],
        }

    def load_product_module(self):
        loader = importlib.machinery.SourceFileLoader("lev_skills_qmd_runner_test", str(SOURCE))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        return module

    def assert_pid_exited(self, pid):
        deadline = time.monotonic() + 2
        while time.monotonic() < deadline:
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                return
            time.sleep(0.02)
        self.fail(f"owned process {pid} survived runner cleanup")

    def assert_error(self, args, code, *, env_overrides=None):
        result = self.run_cli(args, env_overrides=env_overrides)
        self.assertEqual(result.returncode, 1, f"stdout={result.stdout}\nstderr={result.stderr}")
        payload = json.loads(result.stdout)
        self.assertEqual(payload["error"]["code"], code)
        return payload

    def test_qmd_maps_canonical_source_and_returns_full_descriptor(self):
        rows = self.rebuild_inventory()
        self.write_qmd_results([self.qmd_result()])
        payload = self.run_json(["discover", "--query", "semantic retrieval", "--backend", "qmd", "--json"])

        self.assertEqual(payload["backend"], "qmd")
        self.assertEqual(payload["evaluation_origin"], "qmd_query")
        self.assertFalse(payload["_cache"]["hit"])
        self.assertFalse(payload["total_exact"])
        self.assertTrue(payload["query_groups"][0]["evaluated"])
        match = payload["matches"][0]
        expected = next(row for row in rows if row["source_id"] == "skills-db/tools/qmd-sample/SKILL.md")
        self.assertEqual(match["source_id"], expected["source_id"])
        self.assertEqual(match["digest"], hashlib.sha256(self.active_bytes).hexdigest())
        self.assertEqual(match["source_record"]["relative_path"], "tools/qmd-sample/SKILL.md")
        self.assertEqual(match["retrieval_backend"], "qmd")
        query_requests = self.node_requests("query")
        self.assertEqual(len(query_requests), 1)
        self.assertEqual(query_requests[0]["query"], "semantic retrieval")
        self.assertEqual(query_requests[0]["collections"], ["skills-db", "skills-db-bundle-docs"])
        self.assertEqual(query_requests[0]["candidateLimit"], 50)

    def test_duplicate_groups_are_evaluated_once_and_mapped_without_cache_reuse(self):
        self.rebuild_inventory()
        self.write_qmd_results([self.qmd_result()])
        payload = self.run_json([
            "discover", "--query", "qmd sample", "--query", "qmd-sample", "--backend", "qmd", "--json"
        ])
        self.assertEqual(len(self.node_requests("query")), 1)
        self.assertTrue(payload["query_groups"][0]["evaluated"])
        self.assertFalse(payload["query_groups"][1]["evaluated"])
        self.assertEqual(payload["query_groups"][1]["duplicate_of"], "group-1")
        self.assertEqual(payload["matches"][0]["matched_groups"], ["group-1", "group-2"])

    def test_long_task_queries_are_qmd_only_and_keep_lexical_limit(self):
        self.rebuild_inventory()
        self.write_qmd_results([self.qmd_result()])
        long_query = " ".join(f"taskterm{index:03d}" for index in range(60))
        payload = self.run_json(["discover", long_query, "--backend", "qmd", "--json"])
        self.assertTrue(payload["query_groups"][0]["evaluated"])
        self.assertEqual(len(payload["query_groups"][0]["tokens"]), 60)
        self.assertEqual(len(self.node_requests("query")), 1)

        too_many = " ".join(f"taskterm{index:03d}" for index in range(257))
        self.assert_error(["discover", too_many, "--backend", "qmd", "--json"], "invalid_request")
        lexical = self.assert_error(["discover", too_many, "--backend", "lexical", "--json"], "invalid_request")
        self.assertIn("32 searchable terms", lexical["error"]["message"])
        self.assertEqual(len(self.node_requests("query")), 1)

        too_many_bytes = "qmdterm " * 1100
        self.assert_error(["discover", too_many_bytes, "--backend", "qmd", "--json"], "invalid_request")
        self.assertEqual(len(self.node_requests("query")), 1)

    def test_qmd_rejects_malformed_engine_results_scores_paths_and_stale_bodies(self):
        self.rebuild_inventory()
        outside = self.output / "outside.md"
        outside.write_text("outside\n")
        cases = [
            ("malformed", b"{broken", "qmd_backend_error"),
            ("negative", json.dumps([self.qmd_result(score=-0.1)]).encode(), "qmd_backend_error"),
            ("nonfinite", b'[{"file":"skills-db/tools/qmd-sample/SKILL.md","score":NaN,"body":"x"}]', "qmd_backend_error"),
            ("oversized", json.dumps([self.qmd_result(score=10**400)]).encode(), "qmd_backend_error"),
            ("outside", json.dumps([self.qmd_result(path=self.output / "outside.md")]).encode(), "qmd_untrusted_source"),
            ("traversal", b'[{"file":"../outside.md","score":0.5,"body":"x"}]', "qmd_untrusted_source"),
            ("stale", json.dumps([self.qmd_result(body="old indexed body")]).encode(), "stale_qmd_index"),
        ]
        for name, raw, code in cases:
            with self.subTest(name=name):
                self.qmd_output.write_bytes(raw)
                self.assert_error(["discover", "qmd", "--backend", "qmd", "--json", "--no-cache"], code)
        self.write_qmd_results([self.qmd_result(path=self.unknown_path)])
        self.assert_error(["discover", "qmd", "--backend", "qmd", "--json", "--no-cache"], "qmd_untrusted_source")

    def test_qmd_engine_failure_and_missing_model_never_fall_back(self):
        self.rebuild_inventory()
        self.write_qmd_results([self.qmd_result()])
        payload = self.assert_error(
            ["discover", "qmd", "--backend", "qmd", "--json"],
            "qmd_engine_failed",
            env_overrides={"SDB_BRIDGE_QUERY_EXIT": "3"},
        )
        self.assertNotIn("matches", payload)
        query_count = len(self.node_requests("query"))
        model = next(self.model_dir.glob("*.gguf"))
        model.unlink()
        self.assert_error(["discover", "qmd", "--backend", "qmd", "--json"], "qmd_model_unavailable")
        self.assertEqual(len(self.node_requests("query")), query_count)

    def test_qmd_model_identity_uses_full_cached_uri_and_accepts_local_gguf(self):
        self.rebuild_inventory()
        self.write_qmd_results([self.qmd_result()])
        config_path = self.config_dir / "index.yml"
        config = json.loads(config_path.read_text())
        config["models"]["embed"] = "hf:uncached-owner/other-repository/embedding.gguf"
        config_path.write_text(json.dumps(config))
        self.assert_error(["discover", "qmd", "--backend", "qmd", "--json"], "qmd_model_unavailable")
        self.assertEqual(len(self.node_requests("query")), 0, "same-basename model from another repository must block before search")

        local_model = self.output / "local-embedding.gguf"
        local_model.write_bytes(b"GGUFlocal-fixture")
        config["models"]["embed"] = str(local_model)
        config_path.write_text(json.dumps(config))
        payload = self.run_json(["discover", "qmd", "--backend", "qmd", "--json"])
        self.assertEqual(payload["backend"], "qmd")
        self.assertEqual(len(self.node_requests("query")), 1)

    def test_missing_qmd_index_fails_before_engine_but_existing_empty_index_is_valid(self):
        self.rebuild_inventory()
        self.write_qmd_results([])
        index_path = self.output / "qmd-index.sqlite"
        index_path.unlink()
        self.assert_error(
            ["discover", "no-result", "--backend", "qmd", "--json"],
            "qmd_index_unavailable",
        )
        self.assertEqual(len(self.node_requests("query")), 0)

        index_path.write_bytes(b"isolated-index")
        payload = self.run_json(["discover", "no-result", "--backend", "qmd", "--json"])
        self.assertEqual(payload["status"], "empty")
        self.assertEqual(len(self.node_requests("query")), 1)

    def test_integrity_guard_blocks_noncandidate_edit_after_catalog_rebuild(self):
        self.rebuild_inventory()
        self.write_qmd_results([])
        self.active_path.write_bytes(self.active_bytes + b"\nnewuniquequerytoken\n")
        self.rebuild_inventory()
        self.assert_error(["discover", "newuniquequerytoken", "--backend", "qmd", "--json"], "stale_qmd_index")
        self.assertEqual(len(self.node_requests("query")), 0, "integrity failure must precede query launch")

    def test_integrity_guard_blocks_new_or_deleted_noncandidate_occurrences(self):
        self.rebuild_inventory()
        self.write_qmd_results([])
        new_path = self.repo / "skills-db/tools/new-noncandidate.md"
        new_path.write_text("# Brand new noncandidate markdown\n")
        self.rebuild_inventory()
        self.assert_error(["discover", "no-hit", "--backend", "qmd", "--json"], "stale_qmd_index")
        self.assertEqual(len(self.node_requests("query")), 0)

        new_path.unlink()
        self.archived_path.unlink()
        self.rebuild_inventory()
        self.assert_error(["discover", "no-hit", "--backend", "qmd", "--json"], "stale_qmd_index")
        self.assertEqual(len(self.node_requests("query")), 0)

    def test_integrity_manifest_keeps_same_body_occurrences_and_invalid_utf8_bytes(self):
        self.rebuild_inventory()
        original_invalid = self.invalid_utf8_path.read_bytes()
        self.write_qmd_results([])
        payload = self.run_json(["discover", "no-hit", "--backend", "qmd", "--json"])
        self.assertEqual(payload["status"], "empty")
        documents = json.loads(self.index_manifest_path.read_text())["documents"]
        active_occurrences = [
            item for item in documents
            if item["source_id"] in {
                "skills-db/tools/qmd-sample/SKILL.md",
                "skills-db/tools/qmd-variant/SKILL.md",
            }
        ]
        self.assertEqual(len(active_occurrences), 2)
        self.assertNotEqual(active_occurrences[0]["source_id"], active_occurrences[1]["source_id"])
        self.assertEqual(active_occurrences[0]["source_sha256"], active_occurrences[1]["source_sha256"])
        self.assertEqual(self.invalid_utf8_path.read_bytes(), original_invalid)

    def test_qmd_filters_ineligible_sources_and_rejects_other_namespaces(self):
        self.rebuild_inventory()
        self.write_qmd_results([self.qmd_result(), self.qmd_result(self.archived_path)])
        payload = self.run_json(["discover", "qmd", "--backend", "qmd", "--json"])
        self.assertEqual([item["skill_name"] for item in payload["matches"]], ["qmd-sample"])
        calls_before = len(self.node_requests("query"))
        self.assert_error(
            ["discover", "qmd", "--backend", "qmd", "--namespace", "skills", "--json"],
            "unsupported_namespace",
        )
        self.assertEqual(len(self.node_requests("query")), calls_before)

    def test_qmd_refresh_uses_exact_scope_no_force_and_rebuilds_only_after_success(self):
        self.rebuild_inventory()
        before_config = (self.config_dir / "index.yml").read_bytes()
        result = self.run_cli(["refresh", "--repo-local"], timeout=30)
        self.assertEqual(result.returncode, 0, f"stdout={result.stdout}\nstderr={result.stderr}")
        self.assertEqual((self.config_dir / "index.yml").read_bytes(), before_config)
        calls = [json.loads(line) for line in self.node_args.read_text().splitlines()]
        call = next(item for item in calls if item["request"].get("operation") == "refresh")
        request = call["request"]
        self.assertEqual(request["collections"], list(REFRESH_COLLECTIONS))
        self.assertEqual(request["embedCollections"], list(REFRESH_COLLECTIONS))
        self.assertFalse(request["force"])
        self.assertEqual(request["maxDocsPerBatch"], 50)

    def test_refresh_failure_preserves_inventory_and_absent_models_block_before_bridge(self):
        before = self.rebuild_inventory()
        inventory_bytes = (self.repo / "skills-inventory.jsonl").read_bytes()
        failed = self.complete_refresh_response()
        failed["status"] = "error"
        failed["error"] = "QMD embedding was incomplete"
        self.write_node_response(failed, exit_code=1)
        result = self.run_cli(["refresh"], timeout=30)
        self.assertEqual(result.returncode, 1)
        self.assertEqual((self.repo / "skills-inventory.jsonl").read_bytes(), inventory_bytes)
        self.node_args.unlink()
        model = next(self.model_dir.glob("*.gguf"))
        model.unlink()
        result = self.run_cli(["refresh"], timeout=30)
        self.assertEqual(result.returncode, 1)
        requests = [json.loads(line)["request"] for line in self.node_args.read_text().splitlines()]
        self.assertFalse(any(request.get("operation") == "refresh" for request in requests))
        self.assertEqual((self.repo / "skills-inventory.jsonl").read_bytes(), inventory_bytes)
        self.assertIn("skills-db/tools/qmd-sample/SKILL.md", {row["source_id"] for row in before})

    def test_integrity_guard_rejects_missing_owned_indexed_occurrence(self):
        self.rebuild_inventory()
        indexed = json.loads(self.index_manifest_path.read_text())
        indexed["documents"].pop()
        self.index_manifest_path.write_text(json.dumps(indexed, sort_keys=True))
        self.write_qmd_results([])
        self.assert_error(["discover", "no-hit", "--backend", "qmd", "--json"], "stale_qmd_index")
        self.assertEqual(len(self.node_requests("query")), 0, "missing indexed occurrence must block before query launch")

    def test_readonly_integrity_bridge_checks_synthetic_sqlite_snapshot(self):
        node = Path("/opt/homebrew/opt/node@24/bin/node")
        if not node.is_file():
            self.skipTest("installed Node 24 runtime is unavailable")
        qmd_prefix = Path.home() / ".local/share/qmd/npm"
        package_root = qmd_prefix / "lib/node_modules/@tobilu/qmd"
        self.assertTrue((package_root / "dist/store.js").is_file())
        manifest = json.loads(self.index_manifest_path.read_text())
        database = self.output / "synthetic-qmd.sqlite"
        setup = self.output / "setup-synthetic-qmd.mjs"
        setup.write_text(
            "import { createHash } from 'node:crypto';\n"
            "import { readFileSync } from 'node:fs';\n"
            "import { createRequire } from 'node:module';\n"
            "import { join } from 'node:path';\n"
            "import { pathToFileURL } from 'node:url';\n"
            "const root=process.env.TEST_QMD_PACKAGE_ROOT;\n"
            "const require=createRequire(join(root,'package.json'));\n"
            "const Database=require('better-sqlite3'); const sqliteVec=require('sqlite-vec');\n"
            "const {getEmbeddingFingerprint}=await import(pathToFileURL(join(root,'dist/store.js')).href);\n"
            "const db=new Database(process.env.TEST_QMD_DB); sqliteVec.load(db);\n"
            "db.exec(`CREATE TABLE content(hash TEXT PRIMARY KEY,doc TEXT NOT NULL,created_at TEXT NOT NULL);\n"
            "CREATE TABLE documents(id INTEGER PRIMARY KEY,collection TEXT NOT NULL,path TEXT NOT NULL,title TEXT NOT NULL,hash TEXT NOT NULL,created_at TEXT NOT NULL,modified_at TEXT NOT NULL,active INTEGER NOT NULL DEFAULT 1);\n"
            "CREATE TABLE content_vectors(hash TEXT NOT NULL,seq INTEGER NOT NULL DEFAULT 0,pos INTEGER NOT NULL DEFAULT 0,model TEXT NOT NULL,embed_fingerprint TEXT NOT NULL DEFAULT '',total_chunks INTEGER NOT NULL DEFAULT 1,embedded_at TEXT NOT NULL,PRIMARY KEY(hash,seq));\n"
            "CREATE VIRTUAL TABLE vectors_vec USING vec0(hash_seq TEXT PRIMARY KEY,embedding float[3] distance_metric=cosine)`);\n"
            "const model='hf:fixture/qmd/embedding.gguf'; const fingerprint=getEmbeddingFingerprint(model);\n"
            "const manifest=JSON.parse(readFileSync(process.env.TEST_QMD_MANIFEST,'utf8')); const inserted=new Set();\n"
            "const content=db.prepare('INSERT INTO content(hash,doc,created_at) VALUES(?,?,?)');\n"
            "const document=db.prepare('INSERT INTO documents(collection,path,title,hash,created_at,modified_at,active) VALUES(?,?,?,?,?,?,1)');\n"
            "const vector=db.prepare('INSERT INTO content_vectors(hash,seq,pos,model,embed_fingerprint,total_chunks,embedded_at) VALUES(?,0,0,?,?,1,?)');\n"
            "const vec=db.prepare('INSERT INTO vectors_vec(hash_seq,embedding) VALUES(?,?)');\n"
            "for (const item of manifest.documents) { const body=readFileSync(item.file_path).toString('utf8'); const hash=createHash('sha256').update(body,'utf8').digest('hex');\n"
            " if(!inserted.has(hash)){ content.run(hash,body,'fixture'); vector.run(hash,model,fingerprint,'fixture'); vec.run(`${hash}_0`,Buffer.from(new Float32Array([1,0,0]).buffer)); inserted.add(hash); }\n"
            " document.run(item.collection,item.path,item.path,hash,'fixture','fixture'); } db.close();\n"
        )
        environment = os.environ.copy()
        environment.update({
            "QMD_PREFIX": str(qmd_prefix),
            "TEST_QMD_PACKAGE_ROOT": str(package_root),
            "TEST_QMD_DB": str(database),
            "TEST_QMD_MANIFEST": str(self.index_manifest_path),
        })
        setup_result = subprocess.run([str(node), str(setup)], cwd=self.output, env=environment, capture_output=True, text=True, timeout=15, check=False)
        self.assertEqual(setup_result.returncode, 0, f"stdout={setup_result.stdout}\nstderr={setup_result.stderr}")
        config_path = self.config_dir / "index.yml"
        roots = {
            "skills-db": str(self.repo / "skills-db"),
            "skills-db-bundle-docs": str(self.repo / "skills-db/creative/roundtable-marvkr--better-design/source/.agents/skills"),
            "skills-db-archive": str(self.repo / "skills-db/.archive"),
            "skills-db-backlog": str(self.repo / "skills-db/_todo"),
            "skills-db-workshop": str(self.repo / "skills-db/_workshop"),
        }
        request = {
            "operation": "integrity", "dbPath": str(database), "configPath": str(config_path),
            "collections": list(REFRESH_COLLECTIONS), "roots": roots,
            "model": "hf:fixture/qmd/embedding.gguf", "expectedDocuments": len(manifest["documents"]),
        }
        bridge = self.repo / "lev-skills-qmd.mjs"
        def check_guard():
            return subprocess.run(
                [str(node), str(bridge), json.dumps(request)], cwd=self.repo,
                env=environment, input=json.dumps(manifest), capture_output=True,
                text=True, timeout=15, check=False,
            )
        before = hashlib.sha256(database.read_bytes()).hexdigest()
        healthy = check_guard()
        self.assertEqual(healthy.returncode, 0, f"stdout={healthy.stdout}\nstderr={healthy.stderr}")
        self.assertEqual(json.loads(healthy.stdout)["status"], "integrity_checked")
        self.assertEqual(hashlib.sha256(database.read_bytes()).hexdigest(), before, "read-only guard must not modify its index")
        with sqlite3.connect(database) as connection:
            connection.execute("DELETE FROM documents WHERE id=(SELECT MIN(id) FROM documents)")
        stale = check_guard()
        self.assertNotEqual(stale.returncode, 0)
        self.assertEqual(json.loads(stale.stdout).get("code"), "stale_qmd_index")
        database.write_bytes(b"corrupt isolated QMD database")
        corrupt = check_guard()
        self.assertNotEqual(corrupt.returncode, 0)
        self.assertEqual(json.loads(corrupt.stdout).get("code"), "qmd_index_integrity")

    def test_native_hybrid_binding_keeps_canonical_sql_readonly_and_cache_ephemeral(self):
        node = Path("/opt/homebrew/opt/node@24/bin/node")
        if not node.is_file():
            self.skipTest("installed Node 24 runtime is unavailable")
        package_root = Path.home() / ".local/share/qmd/npm/lib/node_modules/@tobilu/qmd"
        probe = self.repo / "skills-db/tools/qmd-quality-probe.md"
        probe.parent.mkdir(parents=True, exist_ok=True)
        probe.write_text("# Query expansion target\nfixtureneedle appears in this body.\n")
        database = self.output / "hybrid-readonly.sqlite"
        helper = self.output / "hybrid-readonly-probe.mjs"
        helper.write_text(
            "import { createRequire } from 'node:module';\n"
            "import { pathToFileURL } from 'node:url';\n"
            "import { join } from 'node:path';\n"
            "import { createHash } from 'node:crypto';\n"
            "import { readFileSync } from 'node:fs';\n"
            "if (process.platform === 'darwin') process.env.GGML_METAL_NO_RESIDENCY='1';\n"
            "process.env.LLAMA_LOG_LEVEL='error'; process.env.GGML_LOG_LEVEL='error'; process.env.GGML_BACKEND_SILENT='1';\n"
            "const root=process.env.TEST_QMD_PACKAGE_ROOT; const require=createRequire(join(root,'package.json'));\n"
            "const qmd=await import(pathToFileURL(join(root,'dist/index.js')).href);\n"
            "const qmdStore=await import(pathToFileURL(join(root,'dist/store.js')).href);\n"
            "const qmdLlm=await import(pathToFileURL(join(root,'dist/llm.js')).href);\n"
            "const bridge=await import(pathToFileURL(process.env.TEST_QMD_BRIDGE).href);\n"
            "const config={collections:{'skills-db':{path:process.env.TEST_QMD_CORPUS,pattern:'**/*.md'}},models:{embed:'hf:fixture/embed.gguf',generate:'hf:fixture/generate.gguf',rerank:'hf:fixture/rerank.gguf'}};\n"
            "const initializer=await qmd.createStore({dbPath:process.env.TEST_QMD_DB,config});\n"
            "await initializer.update({collections:['skills-db']}); await initializer.close();\n"
            "const Database=require('better-sqlite3'); const sqliteVec=require('sqlite-vec'); const setup=new Database(process.env.TEST_QMD_DB); sqliteVec.load(setup); setup.exec('DROP TABLE IF EXISTS vectors_vec; CREATE VIRTUAL TABLE vectors_vec USING vec0(hash_seq TEXT PRIMARY KEY,embedding float[3] distance_metric=cosine)'); setup.close();\n"
            "const before=createHash('sha256').update(readFileSync(process.env.TEST_QMD_DB)).digest('hex');\n"
            "const db=new Database(process.env.TEST_QMD_DB,{readonly:true,fileMustExist:true}); sqliteVec.load(db); db.pragma('query_only = ON');\n"
            "const cacheDb=new Database(':memory:'); cacheDb.exec('CREATE TABLE llm_cache(hash TEXT PRIMARY KEY,result TEXT NOT NULL,created_at TEXT NOT NULL)');\n"
            "const calls={expand:[],rerank:[],embed:0}; const llm={embedModelName:config.models.embed,generateModelName:config.models.generate,rerankModelName:config.models.rerank,\n"
            " async expandQuery(query){calls.expand.push(query);return [{type:'lex',text:'fixtureneedle'}]},\n"
            " async embedBatch(texts){calls.embed++;return texts.map(()=>({embedding:[1,0,0],model:config.models.embed}))},\n"
            " async rerank(query,docs){calls.rerank.push(query);return {results:docs.map(doc=>({file:doc.file,score:0.91})),model:config.models.rerank}}};\n"
            "const models={generate:{uri:config.models.generate},rerank:{uri:config.models.rerank}};\n"
            "const store=bridge.buildReadOnlyHybridStore({db,cacheDb,llm,models,qmdStore});\n"
            "const results=await qmdStore.hybridQuery(store,'quizzical opal',{collection:['skills-db'],limit:10,candidateLimit:50});\n"
            "async function runFault(kind){ const faultCache=new Database(':memory:'); faultCache.exec('CREATE TABLE llm_cache(hash TEXT PRIMARY KEY,result TEXT NOT NULL,created_at TEXT NOT NULL)');\n"
            " const faultLlm={embedModelName:config.models.embed,generateModelName:config.models.generate,rerankModelName:config.models.rerank,\n"
            "  async expandQuery(query){if(kind==='expand-swallowed'){const target={_ciMode:false,touchActivity(){},async ensureLlama(){return {async createGrammar(){throw new Error('fixture expansion context failure')}}},async ensureGenerateModel(){}};return qmdLlm.LlamaCpp.prototype.expandQuery.call(target,query)} if(kind==='expand-empty')return []; return [{type:'lex',text:'fixtureneedle'}]},\n"
            "  async embedBatch(texts){if(kind==='embed-context'){const target={_ciMode:false,touchActivity(){},async ensureEmbedContexts(){throw new Error('fixture embedding context failure')}};return qmdLlm.LlamaCpp.prototype.embedBatch.call(target,texts)} if(kind==='embed-incomplete')return []; if(kind==='embed-nonfinite')return texts.map(()=>({embedding:[NaN,0,0],model:config.models.embed})); return texts.map(()=>({embedding:[1,0,0],model:config.models.embed}))},\n"
            "  async rerank(query,docs){if(kind==='rerank-fallback'){const target={_ciMode:false,touchActivity(){},async ensureRerankContexts(){return []}};return qmdLlm.LlamaCpp.prototype.rerank.call(target,query,docs)} if(kind==='rerank-incomplete')return {model:config.models.rerank,results:[]}; if(kind==='rerank-nonfinite')return {model:config.models.rerank,results:docs.map(doc=>({file:doc.file,score:NaN}))}; return {model:config.models.rerank,results:docs.map(doc=>({file:doc.file,score:0.9}))}}};\n"
            " const faultStore=bridge.buildReadOnlyHybridStore({db,cacheDb:faultCache,llm:faultLlm,models,qmdStore}); let outcome;\n"
            " try {await qmdStore.hybridQuery(faultStore,'quizzical opal',{collection:['skills-db'],limit:10,candidateLimit:50});outcome={status:'success'}} catch(error){outcome={status:'error',code:error.code||null,message:String(error.message||error)}} finally {faultCache.close()} return outcome; }\n"
            "const faultResults={}; for(const kind of ['expand-swallowed','expand-empty','embed-context','embed-incomplete','embed-nonfinite','rerank-fallback','rerank-incomplete','rerank-nonfinite']) faultResults[kind]=await runFault(kind);\n"
            "const canonicalCache=db.prepare('SELECT COUNT(*) AS n FROM llm_cache').get().n;\n"
            "const memoryCache=cacheDb.prepare('SELECT COUNT(*) AS n FROM llm_cache').get().n;\n"
            "let canonicalWriteRejected=false; try { db.prepare(\"INSERT INTO llm_cache(hash,result,created_at) VALUES('probe','x','now')\").run(); } catch { canonicalWriteRejected=true; }\n"
            "await llm.dispose?.(); cacheDb.close(); db.close();\n"
            "const after=createHash('sha256').update(readFileSync(process.env.TEST_QMD_DB)).digest('hex');\n"
            "process.stdout.write(JSON.stringify({results,calls,faultResults,canonicalCache,memoryCache,canonicalWriteRejected,before,after})+'\\n');\n"
        )
        environment = os.environ.copy()
        environment.update({
            "QMD_PREFIX": str(Path.home() / ".local/share/qmd/npm"),
            "TEST_QMD_PACKAGE_ROOT": str(package_root),
            "TEST_QMD_DB": str(database),
            "TEST_QMD_CORPUS": str(self.repo / "skills-db"),
            "TEST_QMD_BRIDGE": str(self.repo / "lev-skills-qmd.mjs"),
        })
        result = subprocess.run([str(node), str(helper)], cwd=self.repo, env=environment, capture_output=True, text=True, timeout=30, check=False)
        self.assertEqual(result.returncode, 0, f"stdout={result.stdout}\nstderr={result.stderr}")
        payload = json.loads(result.stdout)
        self.assertEqual(len(payload["results"]), 1)
        self.assertEqual(payload["results"][0]["file"], "qmd://skills-db/tools/qmd-quality-probe.md")
        self.assertIn("fixtureneedle", payload["results"][0]["body"])
        self.assertEqual(payload["calls"]["expand"], ["quizzical opal"])
        self.assertEqual(payload["calls"]["rerank"], ["quizzical opal"])
        self.assertEqual(payload["calls"]["embed"], 1)
        self.assertEqual(payload["canonicalCache"], 0)
        self.assertGreater(payload["memoryCache"], 0)
        self.assertTrue(payload["canonicalWriteRejected"])
        self.assertEqual(payload["before"], payload["after"])
        self.assertEqual(set(payload["faultResults"]), {
            "expand-swallowed", "expand-empty", "embed-context", "embed-incomplete",
            "embed-nonfinite", "rerank-fallback", "rerank-incomplete", "rerank-nonfinite",
        })
        for name, outcome in payload["faultResults"].items():
            with self.subTest(native_stage=name):
                self.assertEqual(outcome["status"], "error", f"{name}: {outcome}")
                self.assertEqual(outcome["code"], "qmd_engine_failed", f"{name}: {outcome}")

    def test_installed_inspector_resolves_all_three_cached_models_without_downloads(self):
        node = Path("/opt/homebrew/opt/node@24/bin/node")
        if not node.is_file():
            self.skipTest("installed Node 24 runtime is unavailable")
        package_root = Path.home() / ".local/share/qmd/npm/lib/node_modules/@tobilu/qmd"
        installed_config = Path.home() / ".config/qmd/index.yml"
        self.assertTrue(installed_config.is_file())
        isolated_config = self.output / "installed-models-index.yml"
        isolated_config.write_bytes(installed_config.read_bytes())
        environment = os.environ.copy()
        environment["QMD_PREFIX"] = str(Path.home() / ".local/share/qmd/npm")
        environment.pop("XDG_CACHE_HOME", None)

        def inspect(path):
            return subprocess.run(
                [str(node), str(self.repo / "lev-skills-qmd.mjs"), json.dumps({"operation": "inspect", "configPath": str(path)})],
                cwd=self.repo,
                env=environment,
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )

        valid = inspect(isolated_config)
        self.assertEqual(valid.returncode, 0, f"stdout={valid.stdout}\nstderr={valid.stderr}")
        response = json.loads(valid.stdout)
        self.assertEqual(response["status"], "inspected")
        self.assertEqual(set(response["models"]), {"embed", "generate", "rerank"})
        model_state = {}
        for item in response["models"].values():
            model_path = Path(item["path"])
            stats = model_path.stat()
            self.assertGreater(stats.st_size, 4)
            with model_path.open("rb") as handle:
                self.assertEqual(handle.read(4), b"GGUF")
            model_state[model_path] = (stats.st_size, stats.st_mtime_ns, stats.st_ino)

        model_cache = next(iter(model_state)).parent
        cache_state = {
            path.name: (path.stat().st_size, path.stat().st_mtime_ns, path.stat().st_ino)
            for path in model_cache.iterdir()
            if path.is_file()
        }
        original = isolated_config.read_text()
        embed_uri = response["models"]["embed"]["uri"]
        wrong_config = self.output / "wrong-model-index.yml"
        wrong_config.write_text(original.replace(embed_uri, "hf:uncached-owner/other-repository/" + Path(response["models"]["embed"]["path"]).name, 1))
        wrong = inspect(wrong_config)
        self.assertNotEqual(wrong.returncode, 0)
        self.assertEqual(json.loads(wrong.stdout).get("code"), "qmd_model_unavailable")

        missing_config = self.output / "missing-model-index.yml"
        generate_uri = response["models"]["generate"]["uri"]
        missing_config.write_text(original.replace(generate_uri, "hf:uncached-owner/no-such-repository/missing.gguf", 1))
        missing = inspect(missing_config)
        self.assertNotEqual(missing.returncode, 0)
        self.assertEqual(json.loads(missing.stdout).get("code"), "qmd_model_unavailable")
        self.assertEqual(
            {path: (path.stat().st_size, path.stat().st_mtime_ns, path.stat().st_ino) for path in model_state},
            model_state,
            "model preflight must not download or change cached models",
        )
        self.assertEqual(
            {
                path.name: (path.stat().st_size, path.stat().st_mtime_ns, path.stat().st_ino)
                for path in model_cache.iterdir()
                if path.is_file()
            },
            cache_state,
            "wrong or missing model URIs must not create cache files",
        )

    def test_refresh_does_not_rebuild_when_final_index_integrity_fails(self):
        self.rebuild_inventory()
        inventory_before = (self.repo / "skills-inventory.jsonl").read_bytes()
        indexed = json.loads(self.index_manifest_path.read_text())
        indexed["documents"].pop()
        self.index_manifest_path.write_text(json.dumps(indexed, sort_keys=True))
        result = self.run_cli(["refresh"], timeout=30)
        self.assertEqual(result.returncode, 1)
        self.assertIn("stale_qmd_index", result.stderr)
        self.assertEqual((self.repo / "skills-inventory.jsonl").read_bytes(), inventory_before)

    def test_bounded_process_cleans_closed_pipe_timeout_and_output_overflow(self):
        runner = self.load_product_module()
        sleeper = self.output / "close-pipes.py"
        sleeper_pid = self.output / "close-pipes.pid"
        sleeper.write_text(
            "import os,sys,time\n"
            "from pathlib import Path\n"
            "Path(sys.argv[1]).write_text(str(os.getpid()))\n"
            "os.close(1); os.close(2); time.sleep(5)\n"
        )
        with self.assertRaisesRegex(runner.QmdBackendError, "timed out"):
            runner.run_bounded_process(
                [sys.executable, str(sleeper), str(sleeper_pid)],
                timeout=0.2,
                max_output_bytes=1024,
                cwd=self.repo,
            )
        self.assert_pid_exited(int(sleeper_pid.read_text()))

        leader = self.output / "exits-with-child.py"
        child_pid = self.output / "exits-with-child.pid"
        leader.write_text(
            "import subprocess,sys\n"
            "from pathlib import Path\n"
            "child=subprocess.Popen([sys.executable,'-c','import time; time.sleep(5)'],stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)\n"
            "Path(sys.argv[1]).write_text(str(child.pid))\n"
        )
        completed = runner.run_bounded_process(
            [sys.executable, str(leader), str(child_pid)],
            timeout=2,
            max_output_bytes=1024,
            cwd=self.repo,
        )
        self.assertEqual(completed.returncode, 0)
        self.assert_pid_exited(int(child_pid.read_text()))

        overflow = self.output / "overflow.py"
        overflow_pid = self.output / "overflow.pid"
        overflow.write_text(
            "import os,sys,time\n"
            "from pathlib import Path\n"
            "Path(sys.argv[1]).write_text(str(os.getpid()))\n"
            "print('x' * 1024, flush=True); time.sleep(5)\n"
        )
        with self.assertRaisesRegex(runner.QmdBackendError, "output exceeded 32 bytes"):
            runner.run_bounded_process(
                [sys.executable, str(overflow), str(overflow_pid)],
                timeout=2,
                max_output_bytes=32,
                cwd=self.repo,
            )
        self.assert_pid_exited(int(overflow_pid.read_text()))

    def test_sdk_close_failure_returns_one_error_without_complete_status(self):
        runner = self.load_product_module()
        package_root = self.qmd_prefix / "lib/node_modules/@tobilu/qmd"
        (package_root / "package.json").write_text(json.dumps({"name": "@tobilu/qmd", "type": "module"}))
        (package_root / "dist/index.js").write_text(
            "export async function createStore() {\n"
            "  return {\n"
            "    async update() { return {collections:5,indexed:0,updated:0,unchanged:1,removed:0,skipped:0}; },\n"
            "    async embed() { return {docsProcessed:0,chunksEmbedded:0,errors:0}; },\n"
            "    async close() { throw new Error('close failure sentinel'); },\n"
            "  };\n"
            "}\n"
        )
        request = {
            "operation": "refresh",
            "dbPath": str(self.output / "qmd-index.sqlite"),
            "configPath": str(self.config_dir / "index.yml"),
            "collections": list(REFRESH_COLLECTIONS),
            "embedCollections": list(REFRESH_COLLECTIONS),
            "force": False,
        }
        node = runner.qmd_node_executable()
        result = subprocess.run(
            [node, str(self.repo / "lev-skills-qmd.mjs"), json.dumps(request)],
            cwd=self.repo,
            env=self.env(),
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        lines = result.stdout.splitlines()
        self.assertEqual(len(lines), 1, result.stdout)
        response = json.loads(lines[0])
        self.assertEqual(response["status"], "error")
        self.assertIn("close failure sentinel", response["error"])
        self.assertNotIn("complete", response["status"])


if __name__ == "__main__":
    unittest.main()
