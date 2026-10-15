"""Public CLI checks over isolated, source-backed skills-db fixtures."""

import hashlib
import base64
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("LEV_SKILLS_TEST_SOURCE", ROOT / "lev-skills.sh")).resolve()
CANONICAL_NAMES = (
    "skills-state.json",
    "skills-inventory.jsonl",
    "skills-inventory.snapshot.json",
    "skill-graph.json",
)


def file_digest(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def yaml_scalar(value: str) -> str:
    """JSON quoted strings are valid YAML scalars and preserve fixture text."""
    return json.dumps(value, ensure_ascii=False)


class PublicLevSkillsCliTest(unittest.TestCase):
    def setUp(self) -> None:
        self._temporary = tempfile.TemporaryDirectory(prefix="lev-skills-cli-")
        self.output = Path(self._temporary.name).resolve()
        self.repo = self.output / "repo"
        self.repo.mkdir()
        self.script = self.repo / "lev-skills.sh"
        shutil.copy2(SOURCE, self.script)
        self.invocations: list[list[str]] = []
        self.cache_dir = self.output / "cache"
        self.guard_dir = self.output / "guard"
        self.guard_dir.mkdir()
        self._write_effect_guard()

    def tearDown(self) -> None:
        self._temporary.cleanup()

    def _write_effect_guard(self) -> None:
        (self.guard_dir / "sitecustomize.py").write_text(
            """
import os
from pathlib import Path
sys_dont_write_bytecode = True
import sys
sys.dont_write_bytecode = sys_dont_write_bytecode
allowed = Path(os.environ["SDB_CHARACTERIZATION_OUTPUT"]).resolve()
def permitted(path):
    if isinstance(path, int):
        return
    candidate = Path(path)
    normalized = str(candidate).replace("\\\\", "/")
    if "agent_search.db" in normalized or "/.lev/pm/handoffs/" in normalized:
        raise PermissionError("CLI fixture guard blocked usage-source read: " + str(path))
    if not candidate.resolve().is_relative_to(allowed):
        raise PermissionError("CLI fixture guard blocked external write: " + str(path))
def audit(event, args):
    if event == "open":
        path, mode, flags = args
        if (mode and any(char in mode for char in "wax+")) or flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND):
            permitted(path)
        elif isinstance(path, (str, bytes)) and (
            "agent_search.db" in str(path) or "/.lev/pm/handoffs/" in str(path).replace("\\\\", "/")
        ):
            raise PermissionError("CLI fixture guard blocked usage-source read: " + str(path))
    elif event in {"os.mkdir", "os.remove", "os.rmdir", "os.chmod", "os.utime"}:
        permitted(args[0])
    elif event in {"os.rename", "os.replace"}:
        permitted(args[0])
        permitted(args[1])
    elif event == "os.exec":
        target = Path(args[0]).resolve()
        exec_argv = [str(value) for value in args[1]] if len(args) > 1 and isinstance(args[1], (list, tuple)) else []
        explicit_producer = len(exec_argv) > 2 and (
            (exec_argv[2] == "inventory" and "--rebuild" in exec_argv[3:])
            or exec_argv[2] == "refresh"
            or (exec_argv[2] == "graph" and len(exec_argv) > 3 and exec_argv[3] == "rebuild")
        )
        explicit_producer = (
            explicit_producer
            and len(exec_argv) > 1
            and Path(exec_argv[1]).resolve().is_relative_to(allowed)
        )
        if target != Path("/usr/bin/python3").resolve() or not explicit_producer:
            raise PermissionError("CLI fixture guard blocked non-producer exec: " + str(args[0]))
    elif event == "subprocess.Popen":
        command = args[1]
        if not isinstance(command, (list, tuple)) or not command:
            raise PermissionError("CLI fixture guard blocked non-list subprocess")
        seed = os.environ.get("SDB_TEST_SEED")
        qmd = os.environ.get("SDB_TEST_QMD")
        seed_ok = (
            seed
            and len(command) > 1
            and str(command[1]) == seed
            and Path(command[0]).resolve() == Path(sys.executable).resolve()
        )
        path_head = os.environ.get("PATH", "").split(os.pathsep)[0]
        qmd_path = Path(path_head) / "qmd" if path_head else Path()
        qmd_ok = qmd and str(command[0]) == "qmd" and qmd_path.resolve() == Path(qmd).resolve()
        if not (seed_ok or qmd_ok):
            raise PermissionError("CLI fixture guard blocked unapproved subprocess: " + str(command))
    elif event in {"os.system", "socket.connect", "sqlite3.connect"}:
        raise PermissionError("CLI fixture guard blocked incidental effect: " + event)
sys.addaudithook(audit)
"""
        )

    def env(self, overrides: dict[str, str] | None = None) -> dict[str, str]:
        environment = os.environ.copy()
        environment.update(
            {
                "LEV_CACHE_DIR": str(self.cache_dir),
                "PYTHONPATH": str(self.guard_dir),
                "PYTHONDONTWRITEBYTECODE": "1",
                "SDB_CHARACTERIZATION_OUTPUT": str(self.output),
            }
        )
        if overrides:
            environment.update(overrides)
        return environment

    def run_cli(
        self,
        args: list[str],
        *,
        timeout: int = 30,
        env_overrides: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        self.invocations.append(list(args))
        return subprocess.run(
            [sys.executable, str(self.script), *args],
            cwd=str(self.repo),
            env=self.env(env_overrides),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )

    def install_taxonomy(self) -> dict:
        source = ROOT / "skills-taxonomy.json"
        self.assertEqual(
            file_digest(source),
            "5213d1b7f35ca20243ece0ddbf660585a6ac41ef91e6e932c4edae12d34997e3",
            "the accepted taxonomy is a read-only S04 regression input",
        )
        destination = self.repo / "skills-taxonomy.json"
        shutil.copy2(source, destination)
        return json.loads(destination.read_text(encoding="utf-8"))

    def flatten_nodes(self, items: list[dict]) -> list[dict]:
        output = []
        for item in items:
            output.append(item)
            output.extend(self.flatten_nodes(item.get("children", [])))
        return output

    def assert_cli_error(self, args: list[str], code: str) -> dict:
        result = self.run_cli(args)
        return self.assert_json_error_result(result, code)

    def assert_json_error_result(self, result: subprocess.CompletedProcess[str], code: str | None = None) -> dict:
        self.assertEqual(
            result.returncode,
            1,
            f"expected a structured error: {result.args}\nstdout={result.stdout}\nstderr={result.stderr}",
        )
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError as error:
            self.fail(f"expected a structured JSON error: {error}\n{result.stdout}\n{result.stderr}")
        self.assertEqual(payload.get("status"), "error")
        if code is not None:
            self.assertEqual(payload.get("error", {}).get("code"), code)
        return payload

    def encode_cursor(self, payload: dict) -> str:
        unsigned = dict(payload)
        unsigned.pop("checksum", None)
        unsigned["checksum"] = hashlib.sha256(
            json.dumps(
                {key: value for key, value in unsigned.items() if key != "checksum"},
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            ).encode("utf-8")
        ).hexdigest()
        raw = json.dumps(unsigned, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")

    def decode_cursor(self, token: str) -> dict:
        raw = base64.urlsafe_b64decode(token + "=" * ((-len(token)) % 4))
        return json.loads(raw.decode("utf-8"))

    def run_json(
        self, args: list[str], *, env_overrides: dict[str, str] | None = None
    ) -> object:
        result = self.run_cli(args, env_overrides=env_overrides)
        self.assertEqual(
            result.returncode,
            0,
            f"public command failed: {result.args}\nstdout={result.stdout}\nstderr={result.stderr}",
        )
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError as error:
            self.fail(f"public command returned invalid JSON: {error}\n{result.stdout}\n{result.stderr}")

    def run_inventory_json(self, *, rebuild: bool = False, no_cache: bool = False) -> list[dict]:
        args = ["inventory", "--json", "--include-hidden"]
        if rebuild:
            args.append("--rebuild")
        if no_cache:
            args.append("--no-cache")
        payload = self.run_json(args)
        self.assertIsInstance(payload, list)
        return payload

    def write_skill(
        self,
        name: str,
        *,
        category: str = "testing",
        root: str = "skills-db",
        description: str = "",
        filename: str = "SKILL.md",
        tags: list[str] | None = None,
        aliases: list[str] | None = None,
        raw_header: str | None = None,
        body: str = "",
    ) -> Path:
        path = self.repo / root / category / name / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        if raw_header is None:
            lines = ["---", f"name: {yaml_scalar(name)}"]
            if description:
                lines.append(f"description: {yaml_scalar(description)}")
            if tags is not None:
                lines.append("tags:")
                lines.extend(f"  - {yaml_scalar(tag)}" for tag in tags)
            if aliases is not None:
                lines.append("aliases:")
                lines.extend(f"  - {yaml_scalar(alias)}" for alias in aliases)
            lines.extend(["---", body])
            content = "\n".join(lines)
        else:
            content = raw_header + body
        path.write_text(content, encoding="utf-8")
        return path

    def write_flat_markdown(self, relative_path: str, content: str) -> Path:
        path = self.repo / "skills-db" / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def write_state(self, skills: dict | None = None) -> Path:
        path = self.repo / "skills-state.json"
        path.write_text(
            json.dumps({"_schema": 1, "taxonomy": {}, "skills": skills or {}}, indent=2) + "\n"
        )
        return path

    def write_graph(self, *, node_name: str = "graph-control") -> Path:
        path = self.repo / "skill-graph.json"
        path.write_text(
            json.dumps(
                {
                    "nodes": {
                        node_name: {
                            "id": node_name,
                            "kind": "skill",
                            "name": node_name,
                            "lane": "testing",
                        }
                    },
                    "edges": [],
                },
                indent=2,
            )
            + "\n"
        )
        return path

    def rebuild(self) -> list[dict]:
        return self.run_inventory_json(rebuild=True)

    def source_row(self, rows: list[dict], relative_path: str) -> dict:
        matches = [
            row for row in rows
            if row.get("source", {}).get("relative_path") == relative_path
        ]
        self.assertEqual(len(matches), 1, f"expected one row for source {relative_path}, got {len(matches)}")
        return matches[0]

    def tree_bytes(self, root: Path) -> dict[str, bytes]:
        if not root.exists():
            return {}
        return {
            path.relative_to(root).as_posix(): path.read_bytes()
            for path in sorted(root.rglob("*"))
            if path.is_file()
        }

    def canonical_bytes(self) -> dict[str, bytes | None]:
        return {
            name: (self.repo / name).read_bytes() if (self.repo / name).is_file() else None
            for name in CANONICAL_NAMES
        }

    def test_explicit_rebuild_accounts_all_files_and_preserves_typed_metadata_truth(self):
        entrypoint = self.write_skill(
            "fancy-skill",
            category="tools",
            filename="Skill.Md",
            raw_header=(
                "---\n"
                "name: FancyCamel\n"
                "description: >-\n"
                "  Folded first line\n"
                "  and second line\n"
                "metadata:\n"
                "  tags: [one, two]\n"
                "  options:\n"
                "    enabled: true\n"
                "    values: [1, false, null, nested]\n"
                "aliases:\n"
                "  - Fancy Alias\n"
                "---\n"
            ),
            body="# Searchable\nneedle-in-body\n",
        )
        lower_entrypoint = self.write_skill(
            "lower-entry",
            category="tools",
            filename="skill.md",
            description="lowercase filename control",
        )
        headerless = self.write_flat_markdown(
            "tools/Overview.MD",
            "# Headerless Overview\n\nSearchable constellation protocol.",
        )
        sibling_a = self.write_flat_markdown("tools/flat-a.md", "# Alpha sibling")
        sibling_b = self.write_flat_markdown("tools/flat-b.md", "# Beta sibling")
        asset = self.repo / "skills-db" / "tools" / "package" / "assets" / "logo.svg"
        asset.parent.mkdir(parents=True, exist_ok=True)
        asset.write_bytes(b"<svg><title>fixture</title></svg>\n")
        excluded_git = self.repo / "skills-db" / "tools" / "package" / ".git"
        excluded_git.write_text("repository marker\n", encoding="utf-8")
        excluded_finder = self.repo / "skills-db" / "tools" / "package" / ".DS_Store"
        excluded_finder.write_bytes(b"finder metadata")
        malformed = self.repo / "skills-db" / "languages" / "tla-plus" / "SKILL.md"
        malformed.parent.mkdir(parents=True, exist_ok=True)
        malformed.write_text("---\nname: [broken\n---\n", encoding="utf-8")
        bad_header = self.repo / "skills-db" / "tools" / "bad-header" / "SKILL.md"
        bad_header.parent.mkdir(parents=True, exist_ok=True)
        bad_header.write_bytes(b"---\nname: bad-\xff\n---\nbody\n")
        bad_body = self.repo / "skills-db" / "thinking" / "patterns" / "aria" / "SKILL.md"
        bad_body.parent.mkdir(parents=True, exist_ok=True)
        bad_body.write_bytes(
            b'---\nname: aria\ndescription: "valid header"\n---\nvalid text \xff tail\n'
        )
        unsupported = self.repo / "skills-db" / "tools" / "unsupported" / "SKILL.md"
        unsupported.parent.mkdir(parents=True, exist_ok=True)
        unsupported.write_text(
            "---\nname: unsupported\nmetadata:\n  values: !!set\n    unusual: null\n---\n",
            encoding="utf-8",
        )
        cyclic = self.repo / "skills-db" / "tools" / "cyclic" / "SKILL.md"
        cyclic.parent.mkdir(parents=True, exist_ok=True)
        cyclic.write_text(
            "---\nname: cyclic\nmetadata:\n  values: &values [*values]\n---\n",
            encoding="utf-8",
        )

        rows = self.rebuild()
        relative_paths = {row["source"]["relative_path"] for row in rows}
        expected = {
            "tools/fancy-skill/Skill.Md",
            "tools/lower-entry/skill.md",
            "tools/Overview.MD",
            "tools/flat-a.md",
            "tools/flat-b.md",
            "tools/package/assets/logo.svg",
            "languages/tla-plus/SKILL.md",
            "tools/bad-header/SKILL.md",
            "thinking/patterns/aria/SKILL.md",
            "tools/unsupported/SKILL.md",
            "tools/cyclic/SKILL.md",
        }
        self.assertTrue(expected.issubset(relative_paths))
        self.assertFalse(any(path.endswith("/.git") for path in relative_paths))
        self.assertFalse(any(path.endswith("/.DS_Store") for path in relative_paths))
        self.assertEqual(len(relative_paths), len(rows), "every source occurrence must remain distinct")

        fancy = self.source_row(rows, "tools/fancy-skill/Skill.Md")
        self.assertTrue(fancy["structure"]["entrypoint_candidate"])
        self.assertEqual(fancy["name"], "FancyCamel")
        self.assertEqual(fancy["description"], "Folded first line and second line")
        self.assertEqual(
            fancy["original_metadata"]["value"]["metadata"],
            {
                "tags": ["one", "two"],
                "options": {"enabled": True, "values": [1, False, None, "nested"]},
            },
        )
        self.assertIn("Folded first line", fancy["original_metadata"]["raw_yaml"])
        self.assertTrue(fancy["source"]["sha256"])
        self.assertEqual(fancy["source"]["bytes"], entrypoint.stat().st_size)
        self.assertEqual(fancy["quality"]["runtime_status"], "untested")
        self.assertEqual(fancy["structure"]["role_status"], "needs_semantic_review")
        self.assertEqual(fancy["source"]["relative_path"], "tools/fancy-skill/Skill.Md")
        self.assertEqual(fancy["path_key"], "skills-db/tools/fancy-skill")
        self.assertEqual(fancy["legacy_path_key"], fancy["path_key"])
        self.assertEqual(fancy["content_tokens"], [])

        lower = self.source_row(rows, "tools/lower-entry/skill.md")
        self.assertEqual(lower["source"]["relative_path"], "tools/lower-entry/skill.md")
        self.assertTrue(lower["structure"]["entrypoint_candidate"])
        lower_hits = self.run_json(["discover", "lower-entry", "--json", "--no-cache"])["matches"]
        self.assertTrue(any(item["local_path"] == str(lower_entrypoint.resolve()) for item in lower_hits))

        overview = self.source_row(rows, "tools/Overview.MD")
        self.assertEqual(overview["name"], "Overview")
        self.assertEqual(overview["original_metadata"]["status"], "absent")
        self.assertIn("constellation", overview["content_tokens"])
        markdown_hits = self.run_json(
            ["discover", "constellation", "--json", "--no-cache", "--limit=10"]
        )["matches"]
        self.assertTrue(
            any(
                item["skill_name"] == "Overview"
                and item["doc_type"] == "markdown"
                and item["local_path"] == str(headerless.resolve())
                for item in markdown_hits
            )
        )
        flat_a = self.source_row(rows, "tools/flat-a.md")
        flat_b = self.source_row(rows, "tools/flat-b.md")
        self.assertNotEqual(flat_a["path_key"], flat_b["path_key"])
        self.assertTrue(flat_a["path_key"].endswith("flat-a.md"))
        self.assertTrue(flat_b["path_key"].endswith("flat-b.md"))
        self.assertNotEqual(flat_a["occurrence_key"], flat_b["occurrence_key"])

        asset_row = self.source_row(rows, "tools/package/assets/logo.svg")
        self.assertEqual(asset_row["doc_type"], "asset")
        self.assertEqual(asset_row["source"]["sha256"], hashlib.sha256(asset.read_bytes()).hexdigest())
        self.assertNotIn("assets", asset_row, "asset membership is per-file, not an invented bundle field")

        bad_yaml_row = self.source_row(rows, "languages/tla-plus/SKILL.md")
        self.assertEqual(bad_yaml_row["original_metadata"]["status"], "malformed_yaml")
        self.assertEqual(bad_yaml_row["name"], "tla-plus", "malformed YAML must not line-parser salvage name")
        self.assertTrue(bad_yaml_row["original_metadata"]["error"])
        self.assertIn("name: [broken", bad_yaml_row["original_metadata"]["raw_yaml"])

        bad_header_row = self.source_row(rows, "tools/bad-header/SKILL.md")
        self.assertEqual(bad_header_row["original_metadata"]["status"], "invalid_utf8")
        self.assertTrue(bad_header_row["original_metadata"]["raw_header_base64"])
        self.assertTrue(bad_header_row["diagnostics"])

        bad_body_row = self.source_row(rows, "thinking/patterns/aria/SKILL.md")
        self.assertEqual(bad_body_row["original_metadata"]["status"], "parsed")
        self.assertEqual(bad_body_row["name"], "aria")
        self.assertEqual(bad_body_row["source"]["encoding_status"], "invalid_utf8_body")
        self.assertTrue(bad_body_row["diagnostics"])

        unsupported_row = self.source_row(rows, "tools/unsupported/SKILL.md")
        self.assertEqual(unsupported_row["original_metadata"]["status"], "unsupported_type")
        self.assertIsNone(unsupported_row["original_metadata"]["value"])
        self.assertTrue(unsupported_row["original_metadata"]["raw_yaml"])
        self.assertTrue(unsupported_row["diagnostics"])
        cyclic_row = self.source_row(rows, "tools/cyclic/SKILL.md")
        self.assertEqual(cyclic_row["original_metadata"]["status"], "unsupported_type")
        self.assertTrue(cyclic_row["original_metadata"]["raw_yaml"])

        snapshot = json.loads((self.repo / "skills-inventory.snapshot.json").read_text())
        self.assertEqual(snapshot["source_count"], len(rows))
        self.assertEqual(snapshot["skills_db_source_count"], len(rows))

    def test_missing_snapshot_fails_readers_and_defaults_are_not_persisted(self):
        self.write_skill("positive-control", description="needle target")
        before = self.canonical_bytes()
        self.assertTrue(all(value is None for value in before.values()))

        for args in (
            ["needle", "--json"],
            ["discover", "needle", "--json", "--no-cache"],
            ["find", "needle", "--json"],
            ["pick", "needle", "--json", "--no-cache"],
            ["inventory", "--json"],
            ["inventory", "--json", "--no-cache"],
        ):
            with self.subTest(args=args):
                result = self.run_cli(args)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                if args[0] == "inventory":
                    self.assertIn("requires rebuild", result.stderr.lower())
                else:
                    error = self.assert_json_error_result(result, "invalid_index")
                    self.assertIn("requires rebuild", error["error"]["message"].lower())
                self.assertEqual(before, self.canonical_bytes())
                self.assertFalse(self.cache_dir.exists())

        rows = self.rebuild()
        self.assertTrue(rows)
        self.assertFalse((self.repo / "skills-state.json").exists())
        payload = self.run_json(["discover", "needle", "--json"])
        self.assertTrue(payload["matches"], "a current positive control must be returned")

    def test_missing_approved_root_fails_before_writes_and_empty_root_stays_valid(self):
        installed = self.repo / "skills" / "existing" / "SKILL.md"
        installed.parent.mkdir(parents=True)
        installed.write_text("---\nname: existing\n---\n", encoding="utf-8")
        result = self.run_cli(["inventory", "--rebuild", "--json"])
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("skills-db", result.stderr.lower())
        self.assertTrue(all(value is None for value in self.canonical_bytes().values()))
        self.assertFalse((self.repo / "skills-db").exists())

        installed.unlink()
        installed.parent.rmdir()
        installed.parents[1].rmdir()
        (self.repo / "skills-db").mkdir()
        rows = self.run_inventory_json(rebuild=True)
        self.assertEqual(rows, [])
        self.assertFalse((self.repo / "skills").exists())
        self.assertFalse((self.repo / "_repos").exists())
        self.assertFalse((self.repo / "skills-state.json").exists())

        empty_lookup = self.run_json(["discover", "needle", "--json", "--no-cache"])
        self.assertEqual(empty_lookup["matches"], [])
        self.assertFalse(empty_lookup.get("_cache", {}).get("hit", False))

    def test_graph_and_refresh_preflight_state_before_isolated_producer_stubs(self):
        self.write_skill("writer-positive", description="needle writer")
        graph_dir = self.repo / "graph-scripts"
        graph_dir.mkdir()
        seed = graph_dir / "seed.py"
        graph_marker = graph_dir / "effect.marker"
        seed.write_text(
            "from pathlib import Path\n"
            "import json\n"
            "root = Path(__file__).parent.parent\n"
            "Path(__file__).with_name('effect.marker').write_text('graph producer ran')\n"
            "(root / 'skill-graph.json').write_text(json.dumps({'nodes': {}, 'edges': []}))\n",
            encoding="utf-8",
        )
        graph_env = {
            "LEV_SKILL_GRAPH_DIR": str(graph_dir),
            "SDB_TEST_SEED": str(seed),
        }
        state = self.repo / "skills-state.json"
        state.write_bytes(b"{broken state\n")
        graph_failure_before = self.canonical_bytes()

        result = self.run_cli(["graph", "rebuild"], env_overrides=graph_env)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("state", result.stderr.lower())
        self.assertNotIn("guard blocked", result.stderr.lower())
        self.assertFalse(graph_marker.exists())
        self.assertEqual(graph_failure_before, self.canonical_bytes())

        state.unlink()
        result = self.run_cli(["graph", "rebuild"], env_overrides=graph_env)
        self.assertEqual(
            result.returncode,
            0,
            f"isolated graph producer positive control failed:\n{result.stdout}\n{result.stderr}",
        )
        self.assertTrue(graph_marker.is_file())
        self.assertTrue((self.repo / "skill-graph.json").is_file())
        self.assertTrue((self.repo / "skills-inventory.snapshot.json").is_file())

        self.write_skill("refresh-positive", description="needle refresh")
        qmd_dir = self.repo / "fakebin"
        qmd_dir.mkdir()
        qmd = qmd_dir / "qmd"
        qmd_marker = qmd_dir / "effect.marker"
        qmd.write_text(
            "#!/usr/bin/python3\n"
            "from pathlib import Path\n"
            "import sys\n"
            "with Path(__file__).with_name('effect.marker').open('a') as handle:\n"
            "    handle.write(' '.join(sys.argv[1:]) + '\\n')\n",
            encoding="utf-8",
        )
        qmd.chmod(0o755)
        qmd_env = {
            "PATH": str(qmd_dir) + os.pathsep + os.environ.get("PATH", ""),
            "SDB_TEST_QMD": str(qmd),
        }
        state.write_bytes(b"{broken state\n")
        refresh_failure_before = self.canonical_bytes()

        result = self.run_cli(["refresh"], env_overrides=qmd_env)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("state", result.stderr.lower())
        self.assertNotIn("guard blocked", result.stderr.lower())
        self.assertFalse(qmd_marker.exists())
        self.assertEqual(refresh_failure_before, self.canonical_bytes())

        state.unlink()
        result = self.run_cli(["refresh"], env_overrides=qmd_env)
        self.assertEqual(
            result.returncode,
            0,
            f"isolated qmd producer positive control failed:\n{result.stdout}\n{result.stderr}",
        )
        self.assertEqual(qmd_marker.read_text().splitlines(), ["update", "embed -f"])
        self.assertTrue((self.repo / "skills-inventory.snapshot.json").is_file())

    def test_validated_reads_and_no_cache_variants_do_not_write_canonical_or_cache_files(self):
        skill = self.write_skill("target-skill", description="needle target")
        self.write_state(
            {
                "skills-db/testing/target-skill": {
                    "lifecycle": "active",
                    "rotation_role": "eligible",
                }
            }
        )
        self.rebuild()
        self.run_json(["discover", "needle", "--json"])
        canonical_before = self.canonical_bytes()
        cache_before = self.tree_bytes(self.cache_dir)
        source_before = skill.read_bytes()

        commands = (
            ["needle", "--json", "--no-cache"],
            ["discover", "needle", "--json", "--no-cache"],
            ["find", "needle", "--json", "--no-cache"],
            ["pick", "needle", "--json", "--rotation=all", "--no-cache"],
            ["inventory", "--json", "--no-cache"],
        )
        for args in commands:
            with self.subTest(args=args):
                payload = self.run_json(args)
                if isinstance(payload, dict) and "matches" in payload:
                    self.assertTrue(payload["matches"], "positive result prevents vacuous success")
                    self.assertFalse(payload.get("_cache", {}).get("hit", False))
                elif isinstance(payload, dict) and "candidates" in payload:
                    self.assertTrue(payload["candidates"], "pick positive control must return candidates")
                else:
                    self.assertIsInstance(payload, list)
                    self.assertTrue(payload)
                self.assertEqual(canonical_before, self.canonical_bytes())
                self.assertEqual(cache_before, self.tree_bytes(self.cache_dir))
                self.assertEqual(source_before, skill.read_bytes())

    def test_corrupt_and_legacy_snapshots_fail_diagnostically_without_replacement(self):
        self.write_skill("positive", description="needle")
        self.rebuild()
        snapshot_path = self.repo / "skills-inventory.snapshot.json"
        canonical_before = self.canonical_bytes()
        snapshot_path.write_bytes(b"{broken snapshot\n")
        corrupt_snapshot = snapshot_path.read_bytes()

        result = self.run_cli(["discover", "needle", "--json"])
        error = self.assert_json_error_result(result, "invalid_index")
        self.assertIn("snapshot", error["error"]["message"].lower())
        self.assertEqual(corrupt_snapshot, snapshot_path.read_bytes())

        self.rebuild()
        snapshot_path.write_bytes(b"\xff")
        invalid_snapshot = snapshot_path.read_bytes()
        result = self.run_cli(["discover", "needle", "--json"])
        error = self.assert_json_error_result(result, "invalid_index")
        self.assertIn("snapshot", error["error"]["message"].lower())
        self.assertEqual(invalid_snapshot, snapshot_path.read_bytes())

        self.rebuild()
        tampered = json.loads(snapshot_path.read_text())
        tampered["state_input"] = {"status": "present", "sha256": "wrong"}
        snapshot_path.write_text(json.dumps(tampered), encoding="utf-8")
        tampered_bytes = snapshot_path.read_bytes()
        result = self.run_cli(["find", "needle", "--json", "--no-cache"])
        error = self.assert_json_error_result(result, "invalid_index")
        self.assertIn("snapshot", error["error"]["message"].lower())
        self.assertEqual(tampered_bytes, snapshot_path.read_bytes())

        self.rebuild()
        snapshot_path.unlink()
        legacy_inventory = (self.repo / "skills-inventory.jsonl").read_bytes()
        result = self.run_cli(["inventory", "--json", "--no-cache"])
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("requires rebuild", result.stderr.lower())
        self.assertEqual(legacy_inventory, (self.repo / "skills-inventory.jsonl").read_bytes())
        self.assertIsNone(self.canonical_bytes()["skills-inventory.snapshot.json"])
        self.assertIsNotNone(canonical_before["skills-inventory.jsonl"])

    def test_corrupt_state_blocks_reader_and_writer_without_changing_projection(self):
        self.write_skill("positive", description="needle")
        state = self.write_state()
        self.rebuild()
        projection_before = {
            name: (self.repo / name).read_bytes()
            for name in ("skills-inventory.jsonl", "skills-inventory.snapshot.json")
        }
        corrupt_state = b'{"skills": [ malformed }\n'
        state.write_bytes(corrupt_state)

        for args in (["discover", "needle", "--json"], ["inventory", "--rebuild", "--json"]):
            with self.subTest(args=args):
                result = self.run_cli(args)
                self.assertNotEqual(result.returncode, 0, result.stdout)
                if args[0] == "discover":
                    error = self.assert_json_error_result(result, "invalid_index")
                    self.assertIn("state", error["error"]["message"].lower())
                else:
                    self.assertIn("state", result.stderr.lower())
                self.assertEqual(corrupt_state, state.read_bytes())
                self.assertEqual(projection_before["skills-inventory.jsonl"], (self.repo / "skills-inventory.jsonl").read_bytes())
                self.assertEqual(projection_before["skills-inventory.snapshot.json"], (self.repo / "skills-inventory.snapshot.json").read_bytes())

    def test_same_size_restored_mtime_membership_state_and_graph_changes_go_stale(self):
        source = self.write_skill("freshness", description="alpha target")
        self.write_graph()
        self.rebuild()
        self.assertTrue(self.run_json(["discover", "alpha", "--json"])["matches"])
        old_stat = source.stat()
        original = source.read_bytes()
        changed = original.replace(b"alpha", b"omega")
        self.assertEqual(len(original), len(changed))
        source.write_bytes(changed)
        os.utime(source, ns=(old_stat.st_atime_ns, old_stat.st_mtime_ns))

        result = self.run_cli(["discover", "alpha", "--json"])
        error = self.assert_json_error_result(result, "stale_index")
        self.assertIn("stale", error["error"]["message"].lower())
        no_cache = self.run_cli(["find", "alpha", "--json", "--no-cache"])
        error = self.assert_json_error_result(no_cache, "stale_index")
        self.assertIn("stale", error["error"]["message"].lower())

        self.rebuild()
        self.assertTrue(self.run_json(["discover", "omega", "--json"])["matches"])
        self.assertFalse(self.run_json(["discover", "alpha", "--json"])["matches"])
        source.unlink()
        result = self.run_cli(["inventory", "--json"])
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("stale", result.stderr.lower())

        self.rebuild()
        added = self.write_skill("added-after-snapshot", description="needle new")
        result = self.run_cli(["pick", "needle", "--json", "--no-cache"])
        error = self.assert_json_error_result(result, "stale_index")
        self.assertIn("stale", error["error"]["message"].lower())
        self.rebuild()
        self.assertTrue(self.run_json(["discover", "needle", "--json"])["matches"])

        self.write_state(
            {
                "skills-db/testing/added-after-snapshot": {
                    "lifecycle": "archived",
                    "rotation_role": "none",
                }
            }
        )
        state_result = self.run_cli(["discover", "needle", "--json"])
        error = self.assert_json_error_result(state_result, "stale_index")
        self.assertIn("stale", error["error"]["message"].lower())
        result = self.run_cli(["inventory", "--json", "--no-cache"])
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("stale", result.stderr.lower())

        self.rebuild()
        graph = self.write_graph(node_name="changed-graph-input")
        result = self.run_cli(["discover", "needle", "--json"])
        error = self.assert_json_error_result(result, "stale_index")
        self.assertIn("stale", error["error"]["message"].lower())
        self.assertTrue(added.exists())
        self.assertTrue(graph.exists())
        self.rebuild()
        current = self.run_json(["inventory", "--json", "--include-hidden", "--no-cache"])
        self.assertTrue(current)

    def test_optional_result_cache_missing_expired_and_corrupt_never_overrides_current_rows(self):
        self.write_skill("target-a", description="needle")
        self.write_skill("target-b", description="needle")
        self.rebuild()
        first = self.run_json(["discover", "needle", "--json", "--limit=1"])
        self.assertEqual(len(first["matches"]), 1)
        self.assertEqual(first["evaluation_origin"], "cli_evaluation")
        self.assertTrue(first["query_groups"][0]["evaluated"])
        repeated = self.run_json(["discover", "needle", "--json", "--limit=1"])
        self.assertTrue(repeated["_cache"]["hit"])
        self.assertEqual(repeated["evaluation_origin"], "cache")
        self.assertFalse(repeated["query_groups"][0]["evaluated"])
        self.assertEqual(repeated["query_groups"][0]["evaluation_origin"], "cache")
        self.assertEqual([item["skill_name"] for item in repeated["matches"]], ["target-a"])
        fresh = self.run_json(["discover", "needle", "--json", "--limit=1", "--no-cache"])
        self.assertFalse(fresh["_cache"]["hit"])
        self.assertEqual(fresh["evaluation_origin"], "cli_evaluation")
        self.assertTrue(fresh["query_groups"][0]["evaluated"])

        cache_files = list(self.cache_dir.glob("discover-v*.json"))
        self.assertTrue(cache_files)
        result_cache = cache_files[0]
        valid_document = json.loads(result_cache.read_text())

        result_cache.write_text(json.dumps({"matches": []}), encoding="utf-8")
        shape_invalid = self.run_json(["discover", "needle", "--json", "--limit=1"])
        self.assertFalse(shape_invalid["_cache"]["hit"])
        self.assertEqual(len(shape_invalid["matches"]), 1)

        damaged_document = json.loads(json.dumps(valid_document))
        damaged_document["result"]["matches"] = []
        result_cache.write_text(json.dumps(damaged_document), encoding="utf-8")
        recomputed = self.run_json(["discover", "needle", "--json", "--limit=1"])
        self.assertFalse(recomputed["_cache"]["hit"])
        self.assertEqual([m["skill_name"] for m in recomputed["matches"]], ["target-a"])

        request_mismatch = json.loads(json.dumps(valid_document))
        request_mismatch["request"]["revision"] = "wrong-revision"
        unsigned = {key: value for key, value in request_mismatch.items() if key != "integrity_sha256"}
        request_mismatch["integrity_sha256"] = hashlib.sha256(
            json.dumps(
                unsigned,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            ).encode("utf-8")
        ).hexdigest()
        result_cache.write_text(json.dumps(request_mismatch), encoding="utf-8")
        rebound = self.run_json(["discover", "needle", "--json", "--limit=1"])
        self.assertFalse(rebound["_cache"]["hit"])
        self.assertEqual([m["skill_name"] for m in rebound["matches"]], ["target-a"])

        result_cache.write_text("{bad cache", encoding="utf-8")
        malformed_json = self.run_json(["discover", "needle", "--json", "--limit=1"])
        self.assertFalse(malformed_json["_cache"]["hit"])

        result_cache.write_bytes(b"\xff")
        invalid_encoding = self.run_json(["discover", "needle", "--json", "--limit=1"])
        self.assertFalse(invalid_encoding["_cache"]["hit"])
        self.assertEqual([m["skill_name"] for m in invalid_encoding["matches"]], ["target-a"])

        os.utime(result_cache, (1, 1))
        expired = self.run_json(["discover", "needle", "--json", "--limit=1"])
        self.assertEqual([m["skill_name"] for m in expired["matches"]], ["target-a"])

    def test_cached_discovery_respects_limits_and_bypasses_legacy_cache(self):
        names = [f"item-{index:02d}" for index in range(10)]
        for name in names:
            self.write_skill(name, description="widget")
        self.rebuild()

        legacy_parts = ["discover", "widget", "", str(True)]
        legacy_digest = hashlib.sha256("|".join(legacy_parts).encode()).hexdigest()[:16]
        legacy_path = self.cache_dir / f"discover-{legacy_digest}.json"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        legacy_path.write_text(
            json.dumps(
                {
                    "query": "widget",
                    "category_filter": [],
                    "matches": [{"skill_name": "stale-legacy-result", "score": 999}],
                }
            )
        )

        for limits in ((1, 8, 1), (8, 1, 8)):
            payloads = [
                self.run_json(["discover", "widget", "--json", f"--limit={limit}"])
                for limit in limits
            ]
            names_by_request = [
                [item["skill_name"] for item in payload["matches"]]
                for payload in payloads
            ]
            self.assertEqual([len(items) for items in names_by_request], list(limits))
            self.assertEqual(names_by_request, [names[:limit] for limit in limits])
            self.assertNotIn("stale-legacy-result", names_by_request[0])

        clamped = self.run_json(["discover", "widget", "--json", "--limit=0"])
        self.assertEqual([item["skill_name"] for item in clamped["matches"]], names[:1])

    def test_partial_matches_keep_positive_candidates_and_sort_independently_of_source_order(self):
        fixtures = [
            ("feedback-loops", "feedback loops"),
            ("generic", "feedback loops systems"),
            ("one-term-a", "feedback"),
            ("one-term-b", "feedback"),
            ("irrelevant", "calendar"),
        ]
        for name, description in fixtures:
            self.write_skill(name, description=description)
        self.rebuild()
        first = self.run_json(["discover", "feedback loops systems", "--json", "--limit=10"])
        forward = [
            (item["skill_name"], item["adjusted_score"], item["matched_terms"])
            for item in first["matches"]
        ]
        self.assertEqual(
            forward,
            [
                ("feedback-loops", 34.0667, ["feedback", "loops"]),
                ("generic", 29.25, ["feedback", "loops", "systems"]),
                ("one-term-a", 1.325, ["feedback"]),
                ("one-term-b", 1.325, ["feedback"]),
            ],
        )

        # Rebuild from the same real source files created in reverse order in a second checkout.
        second = PublicLevSkillsCliTest()
        second.setUp()
        try:
            for name, description in reversed(fixtures):
                second.write_skill(name, description=description)
            second.rebuild()
            reverse_payload = second.run_json(
                ["discover", "feedback loops systems", "--json", "--limit=10"]
            )
            reverse = [
                (item["skill_name"], item["adjusted_score"], item["matched_terms"])
                for item in reverse_payload["matches"]
            ]
            self.assertEqual(forward, reverse)
        finally:
            second.tearDown()

    def test_discovery_excludes_exact_trash_ancestors_and_keeps_near_matches(self):
        self.write_skill("safe-storage", category="tools", description="storage management")
        self.write_skill("disposed-physical", category=".trash/physical", description="storage management")
        self.write_skill("disposed-nested", category="archive/.trash/nested", description="storage management")
        self.write_skill("near-trashcan", category=".trashcan", description="storage management")
        self.write_skill("near-foo-trash", category="foo.trash", description="storage management")
        self.write_skill("trash", category="tools", description="storage management")
        self.write_skill("safe-archived", category="tools", description="storage management")
        self.write_state(
            {
                "skills-db/tools/safe-archived": {
                    "lifecycle": "archived",
                    "rotation_role": "none",
                }
            }
        )
        self.rebuild()

        payload = self.run_json(["discover", "storage", "--json", "--limit=20"])
        actual_names = {item["skill_name"] for item in payload["matches"]}
        self.assertTrue(actual_names, "positive storage matches make absence checks meaningful")
        self.assertTrue({"safe-storage", "near-trashcan", "near-foo-trash", "trash"}.issubset(actual_names))
        self.assertTrue({"disposed-physical", "disposed-nested", "safe-archived"}.isdisjoint(actual_names))
        for item in payload["matches"]:
            for source_path in (item["local_path"], item["path_key"]):
                self.assertNotIn(".trash", source_path.replace("\\", "/").split("/"))

        inventory = self.run_json(["inventory", "--json", "--include-hidden"])
        inventory_names = {item["name"] for item in inventory}
        self.assertIn("safe-archived", inventory_names)
        self.assertTrue({"disposed-physical", "disposed-nested"}.isdisjoint(inventory_names))

    def test_query_and_discover_keep_legacy_match_fields_filters_and_pick(self):
        rows = (
            ("gh-actions", "workflow", "workflow automation", ["github", "actions"], "active", "eligible"),
            ("legacy-workflow-alias", "workflow", "legacy workflow automation", ["github", "actions"], "active", "eligible"),
            ("archived-workflow-alias", "workflow", "archived workflow automation", ["github", "actions"], "archived", "eligible"),
            ("other-category-alias", "other", "other workflow automation", ["github", "actions"], "active", "eligible"),
            ("picker-active", "workflow", "strategy selection", ["discovery"], "active", "eligible"),
            ("picker-archived", "workflow", "strategy selection", ["discovery"], "archived", "eligible"),
            ("picker-other-category", "other", "strategy selection", ["discovery"], "active", "eligible"),
            ("picker-not-eligible", "workflow", "strategy selection", ["discovery"], "active", "none"),
            ("picker-disposed", ".trash", "strategy selection", ["discovery"], "active", "eligible"),
        )
        overrides = {}
        for name, category, description, tags, lifecycle, rotation in rows:
            self.write_skill(name, category=category, description=description, tags=tags)
            overrides[f"skills-db/{category}/{name}"] = {
                "lifecycle": lifecycle,
                "rotation_role": rotation,
            }
        self.write_flat_markdown("workflow/strategy-notes.md", "# discovery strategy notes")
        self.write_state(overrides)
        self.rebuild()

        exact = self.run_json(["gh-actions", "--json", "--limit=5"])
        self.assertTrue(exact["matches"], "exact-name control must return a positive result")
        exact_match = exact["matches"][0]
        self.assertEqual(exact_match["skill_name"], "gh-actions")
        self.assertEqual(exact_match["local_path"], exact_match["path"])
        self.assertIn("source", exact_match)
        self.assertIn("anomaly", exact_match)

        legacy = self.run_json(["discover", "github actions", "--json", "--limit=10"])
        self.assertTrue(legacy["matches"], "legacy alias control must return a positive result")
        self.assertEqual(
            {item["skill_name"] for item in legacy["matches"]},
            {"gh-actions", "legacy-workflow-alias", "other-category-alias"},
        )
        self.assertTrue(all(item["local_path"] == item["path"] for item in legacy["matches"]))

        category_filtered = self.run_json(
            ["github actions", "--json", "--category=workflow", "--limit=10"]
        )
        category_names = {item["skill_name"] for item in category_filtered["matches"]}
        self.assertEqual(category_names, {"gh-actions", "legacy-workflow-alias"})

        picked = self.run_json(
            ["pick", "discovery", "--json", "--category=workflow", "--rotation=eligible"]
        )
        self.assertIsInstance(picked, dict)
        self.assertIn("candidates", picked)
        self.assertEqual({item["skill_name"] for item in picked["candidates"]}, {"picker-active"})
        all_rotations = self.run_json(
            ["pick", "discovery", "--json", "--category=workflow", "--rotation=all"]
        )
        self.assertTrue(all_rotations["candidates"])
        self.assertNotIn("strategy-notes", {item["skill_name"] for item in all_rotations["candidates"]})

    def test_s04_tree_browse_and_discover_return_openable_source_descriptors(self):
        taxonomy = self.install_taxonomy()
        source = self.write_skill(
            "software-architecture",
            category="architecture",
            description="navigationneedle source-backed fixture",
        )
        rows = self.rebuild()
        expected = self.source_row(rows, "architecture/software-architecture/SKILL.md")

        subjects = self.run_json(["tree", "--view", "subjects", "--depth", "20", "--json"])
        self.assertEqual(subjects["status"], "ok")
        subject_nodes = self.flatten_nodes(subjects["items"])
        expected_subject_ids = {node["id"] for node in taxonomy["nodes"] if node["id"].startswith("view.")}
        self.assertEqual({node["id"] for node in subject_nodes}, expected_subject_ids)
        self.assertIn("view.additional-views", expected_subject_ids)
        self.assertIn("view.administration", expected_subject_ids)
        self.assertTrue(all("path" not in node for node in subject_nodes), "virtual taxonomy nodes have no file path")
        roots_only = self.run_json(["tree", "--view", "subjects", "--depth", "0", "--json"])
        root_ids = {node["id"] for node in self.flatten_nodes(roots_only["items"])}
        expected_root_ids = {
            node["id"] for node in taxonomy["nodes"]
            if node["id"].startswith("view.") and node.get("parent_id") is None
        }
        self.assertEqual(root_ids, expected_root_ids)
        self.assertTrue(all(node["children"] == [] for node in roots_only["items"]))

        collections = self.run_json(["tree", "--view=collections", "--depth=20", "--json"])
        collection_nodes = self.flatten_nodes(collections["items"])
        expected_collection_ids = {
            item["node_id"] for item in taxonomy["source_namespaces"] + taxonomy["source_collections"]
        }
        self.assertEqual({node["id"] for node in collection_nodes}, expected_collection_ids)

        node_id = "view.software-systems.architecture"
        browsed = self.run_json(["browse", "--node", node_id, "--limit", "10", "--json"])
        self.assertEqual(browsed["status"], "ok")
        self.assertEqual(browsed["total"], 1)
        self.assertEqual(browsed["items"][0]["source_id"], expected["source_id"])
        self.assertEqual([crumb["id"] for crumb in browsed["breadcrumbs"]][-1], node_id)
        self.assertEqual(browsed["eligible_count"], 1)

        discovered = self.run_json(
            ["discover", "--query", "navigationneedle", "--namespace", "skills-db", "--json", "--no-cache"]
        )
        match = next(item for item in discovered["matches"] if item["source_id"] == expected["source_id"])
        browse_item = browsed["items"][0]
        for item in (browse_item, match):
            self.assertEqual(item["path"], str(source.resolve()))
            self.assertEqual(item["local_path"], str(source.resolve()))
            self.assertEqual(item["realpath"], str(source.resolve()))
            self.assertEqual(item["digest"], file_digest(source))
            self.assertEqual(item["content_revision"], file_digest(source))
            self.assertEqual(item["index_revision"], browsed["index_revision"])
            self.assertEqual(item["source_namespace"], "skills-db")
            self.assertEqual(item["source_collection"], "architecture")
            self.assertEqual(item["source_scope"]["relative_path"], "architecture/software-architecture/SKILL.md")
            self.assertEqual(item["source_record"]["real_path"], str(source.resolve()))
            self.assertIn("bundle_id", item)
            self.assertIn("bundle_revision", item)
            self.assertIn("bundle_scope", item)
            self.assertIn("bundle_boundary_status", item)
            self.assertIn("bundle_member_source_ids", item)
            self.assertIn("bundle", item)
            self.assertEqual(item["bundle"]["revision"], item["bundle_revision"])
            self.assertIn("relationship_uncertainty", item)
            self.assertTrue(item["diagnostics"] == [] or isinstance(item["diagnostics"], list))
        self.assertEqual(match["source_id"], browse_item["source_id"])
        self.assertEqual(Path(browse_item["path"]).read_bytes(), source.read_bytes())
        self.assertEqual(Path(match["path"]).read_bytes(), source.read_bytes())
        self.assertFalse(any(call and call[0] == "get" for call in self.invocations))

        empty = self.run_json(["browse", "--node", "source.collection.skills-db.tools", "--json"])
        self.assertEqual(empty["status"], "empty")
        self.assertEqual(empty["node_id"], "source.collection.skills-db.tools")
        self.assertEqual(empty["total"], 0)
        self.assertEqual(empty["items"], [])
        self.assertIsNone(empty["next_cursor"])
        self.assert_cli_error(["browse", "--node", "source.collection.skills-db.unknown", "--json"], "unknown_node")

    def test_s04_get_exact_ids_and_ambiguous_equal_byte_variants(self):
        self.install_taxonomy()
        header = (
            "---\n"
            "name: Shared Variant\n"
            "description: source variant lookup\n"
            "aliases:\n"
            "  - shared fixture alias\n"
            "---\n"
        )
        first = self.write_skill("variant-one", category="testing", raw_header=header, body="# Same bytes\n")
        second = self.write_skill("variant-two", category="architecture", raw_header=header, body="# Same bytes\n")
        unique = self.write_skill("unique-get-control", category="tools", description="unique source descriptor")
        self.assertEqual(first.read_bytes(), second.read_bytes())
        rows = self.rebuild()
        first_row = self.source_row(rows, "testing/variant-one/SKILL.md")
        second_row = self.source_row(rows, "architecture/variant-two/SKILL.md")
        self.assertNotEqual(first_row["source_id"], second_row["source_id"])
        self.assertEqual(first_row["digest"], second_row["digest"])

        exact = self.run_json(["get", first_row["source_id"], "--json"])
        item = exact["items"][0]
        self.assertEqual(exact["status"], "ok")
        self.assertEqual(item["source_id"], first_row["source_id"])
        self.assertEqual(item["path"], str(first.resolve()))
        self.assertEqual(item["digest"], file_digest(first))
        self.assertEqual(item["content_delivery"], {"mode": "descriptor_only", "content_loaded": False})
        browsed = self.run_json(["browse", "--node", "source.collection.skills-db.testing", "--limit", "10", "--json"])
        browse_item = next(value for value in browsed["items"] if value["source_id"] == first_row["source_id"])
        self.assertEqual(item["path"], browse_item["path"])
        self.assertEqual(item["digest"], browse_item["digest"])
        self.assertEqual(item["index_revision"], browse_item["index_revision"])
        unique_id = self.source_row(rows, "tools/unique-get-control/SKILL.md")["source_id"]
        named = self.run_json(["get", "unique-get-control", "--json"])["items"][0]
        self.assertEqual(named["source_id"], unique_id)
        self.assertEqual(named["path"], str(unique.resolve()))
        self.assertEqual(named["digest"], file_digest(unique))

        ambiguous = self.assert_cli_error(["get", "shared fixture alias", "--json"], "ambiguous_source")
        alternatives = ambiguous["alternatives"]
        self.assertEqual({value["source_id"] for value in alternatives}, {first_row["source_id"], second_row["source_id"]})
        self.assertEqual({value["path"] for value in alternatives}, {str(first.resolve()), str(second.resolve())})
        self.assertEqual({value["digest"] for value in alternatives}, {file_digest(first)})
        self.assert_cli_error(["get", "missing fixture name", "--json"], "source_not_found")

    def test_s04_grouped_discovery_maps_duplicates_and_reports_full_group_outcomes(self):
        self.install_taxonomy()
        self.write_skill("shared-a", category="testing", description="common aurora borealis")
        self.write_skill("shared-b", category="testing", description="common aurora borealis")
        self.write_skill("sun-only", category="testing", description="common aurora")
        self.write_skill("moon-only", category="testing", description="common borealis")
        self.rebuild()

        result = self.run_json(
            [
                "discover",
                "--query", "common",
                "--query", " COMMON ",
                "--query", "aurora",
                "--query", "absent-token",
                "--query", "aurora borealis",
                "--query", "borealis aurora",
                "--query", "aurora aurora",
                "--tags", "borealis, common",
                "--limit", "1",
                "--json",
                "--no-cache",
            ]
        )
        groups = result["query_groups"]
        self.assertEqual(len(groups), 8)
        self.assertEqual(groups[0]["raw"], "common")
        self.assertEqual(groups[1]["raw"], " COMMON ")
        self.assertEqual(groups[1]["duplicate_of"], groups[0]["id"])
        self.assertFalse(groups[1]["evaluated"])
        self.assertEqual(groups[1]["evaluation_origin"], "mapped_duplicate")
        self.assertEqual(groups[0]["predicate_fingerprint"], groups[1]["predicate_fingerprint"])
        self.assertEqual(groups[0]["status"], "ok")
        self.assertEqual(groups[0]["total"], 4)
        self.assertEqual(groups[3]["status"], "empty")
        self.assertEqual(groups[3]["total"], 0)
        self.assertEqual(groups[7]["kind"], "tags")
        self.assertEqual(groups[7]["raw"], "borealis, common")
        self.assertEqual(result["normalized_request"]["tags_raw"], "borealis, common")
        self.assertEqual(result["normalized_request"]["normalized_tags"], ["borealis", "common"])
        self.assertEqual(result["total"], 4)
        self.assertEqual(result["returned_count"], 1)
        self.assertEqual(len(result["matches"]), 1)
        self.assertEqual(len(set(result["matches"][0]["matched_groups"])), len(result["matches"][0]["matched_groups"]))

        forward, reverse = groups[4], groups[5]
        self.assertEqual(forward["predicate_fingerprint"], reverse["predicate_fingerprint"])
        self.assertNotEqual(forward["request_fingerprint"], reverse["request_fingerprint"])
        repeated = groups[6]
        self.assertEqual(groups[2]["predicate_fingerprint"], repeated["predicate_fingerprint"])
        self.assertNotEqual(groups[2]["request_fingerprint"], repeated["request_fingerprint"])
        self.assertGreater(groups[0]["total"], result["limit"], "group totals are full positive counts before union limit")

        ranking = self.run_json(
            ["discover", "--query", "aurora", "--query", "aurora aurora", "--limit", "10", "--json", "--no-cache"]
        )
        target_id = next(item["source_id"] for item in ranking["matches"] if item["skill_name"] == "shared-a")
        target_match = next(item for item in ranking["matches"] if item["source_id"] == target_id)
        single_value = target_match["group_scores"]["group-1"]
        repeated_value = target_match["group_scores"]["group-2"]
        self.assertGreater(repeated_value, single_value)
        self.assertEqual(target_match["adjusted_score"], repeated_value)

        unbounded = self.run_json(
            ["discover", "--query", "common", "--query", "absent-token", "--limit", "10", "--json", "--no-cache"]
        )
        self.assertEqual(unbounded["total"], 4)
        self.assertEqual(len(unbounded["matches"]), 4)
        self.assertEqual(len({item["source_id"] for item in unbounded["matches"]}), 4)
        all_empty = self.run_json(
            ["discover", "--query", "absent-token", "--query", "missing-token", "--json", "--no-cache"]
        )
        self.assertEqual(all_empty["status"], "empty")
        self.assertEqual([group["status"] for group in all_empty["query_groups"]], ["empty", "empty"])

    def test_s04_namespace_filters_before_scoring_and_preserves_legacy_noops(self):
        self.install_taxonomy()
        self.write_skill("corpus-control", category="testing", description="rare facet")
        self.write_skill("corpus-secondary", category="architecture", description="rare facet")
        self.write_skill("RareFacet", category="testing", root="skills", description="installed match")
        self.write_skill("repo-control", category="acme/repo", root="_repos", description="rare facet")
        self.rebuild()

        all_rows = self.run_json(["discover", "--query", "rare facet", "--json", "--no-cache"])
        self.assertEqual(all_rows["matches"][0]["source_namespace"], "skills")
        corpus = self.run_json(
            ["discover", "--query", "rare facet", "--namespace", "skills-db", "--limit", "1", "--json", "--no-cache"]
        )
        self.assertEqual(corpus["normalized_request"]["namespace"], "skills-db")
        self.assertEqual(corpus["matches"][0]["source_namespace"], "skills-db")
        self.assertEqual(corpus["matches"][0]["skill_name"], "corpus-control")
        self.assertTrue(all(item["source_namespace"] == "skills-db" for item in corpus["matches"]))

        shorthand = self.run_json(["rare facet", "--namespace=skills-db", "--json", "--no-cache"])
        self.assertTrue(shorthand["matches"])
        self.assertTrue(all(item["source_namespace"] == "skills-db" for item in shorthand["matches"]))
        picked = self.run_json(
            ["pick", "rare facet", "--namespace", "skills-db", "--rotation", "all", "--json", "--no-cache"]
        )
        self.assertTrue(picked["candidates"])
        self.assertTrue(all(item["source_namespace"] == "skills-db" for item in picked["candidates"]))

        default_ids = [item["source_id"] for item in self.run_json(["discover", "rare facet", "--json", "--no-cache"])["matches"]]
        all_ids = [item["source_id"] for item in self.run_json(["discover", "rare facet", "--all", "--json", "--no-cache"])["matches"]]
        primary_ids = [
            item["source_id"]
            for item in self.run_json(["discover", "rare facet", "--primary-only", "--json", "--no-cache"])["matches"]
        ]
        self.assertEqual(default_ids, all_ids)
        self.assertEqual(default_ids, primary_ids)
        physical_category = self.run_json(
            ["discover", "rare facet", "--namespace", "skills-db", "--category", "testing", "--json", "--no-cache"]
        )
        self.assertEqual({item["category"] for item in physical_category["matches"]}, {"testing"})

    def test_s04_strict_errors_and_group_bounds_fail_before_inventory_lookup(self):
        cases = [
            (["discover", "--query", "needle", "--unknown", "--json"], "invalid_request"),
            (["discover", "--query", "needle", "--namespace", "invalid", "--json"], "invalid_request"),
            (["discover", "--query", "needle", "--namespace", "skills-db", "--namespace", "skills", "--json"], "invalid_request"),
            (["find", "needle", "--limit", "--json"], "invalid_request"),
            (["needle", "--category", "--json"], "invalid_request"),
            (["discover", "old-query", "--query", "new-query", "--json"], "invalid_request"),
            (["tree", "--view", "unsupported", "--json"], "invalid_request"),
            (["tree", "--depth", "-1", "--json"], "invalid_request"),
            (["tree", "--depth", "shallow", "--json"], "invalid_request"),
            (["tree", "--view", "subjects", "--view", "collections", "--json"], "invalid_request"),
            (["browse", "--node", "source.collection.skills-db.tools", "--limit", "0", "--json"], "invalid_request"),
            (["browse", "--node", "source.collection.skills-db.tools", "--limit", "101", "--json"], "invalid_request"),
            (["get", "--json"], "invalid_request"),
            (["discover", "--query", "the and", "--json"], "invalid_request"),
            (["discover", "--query", "needle", "--tags", "one,,two", "--json"], "invalid_request"),
        ]
        for args, code in cases:
            with self.subTest(args=args):
                payload = self.assert_cli_error(args, code)
                self.assertNotIn("inventory", payload.get("error", {}).get("message", "").lower())

        too_many = ["discover", "--json"] + [part for _ in range(9) for part in ("--query", "needle")]
        self.assert_cli_error(too_many, "invalid_request")
        too_many_terms = " ".join(["needle"] * 33)
        self.assert_cli_error(["discover", "--query", too_many_terms, "--json"], "invalid_request")
        self.assertFalse((self.repo / "skills-inventory.snapshot.json").exists())

    def test_s04_browse_cursor_paging_exact_empty_stale_corrupt_and_changed_request(self):
        self.install_taxonomy()
        for name in ("page-a", "page-b", "page-c"):
            self.write_skill(name, category="testing", description="pagingfixture")
        self.rebuild()
        node_id = "source.collection.skills-db.testing"

        default_page = self.run_json(["browse", "--node", node_id, "--json"])
        self.assertEqual(default_page["limit"], 10)
        self.assertEqual(default_page["returned_count"], 3)

        first = self.run_json(["browse", "--node", node_id, "--limit", "2", "--json"])
        self.assertEqual(first["total"], 3)
        self.assertEqual(first["normalized_request"]["offset"], 0)
        self.assertEqual(first["returned_count"], 2)
        self.assertIsNotNone(first["next_cursor"])
        token = first["next_cursor"]
        cursor = self.decode_cursor(token)
        self.assertEqual(cursor["offset"], 2)
        second = self.run_json(["browse", "--cursor", token, "--json"])
        self.assertEqual(second["returned_count"], 1)
        self.assertEqual(second["total"], 3)
        self.assertIsNone(second["next_cursor"])

        exact = self.run_json(["browse", "--node", node_id, "--limit", "3", "--json"])
        self.assertEqual(exact["returned_count"], 3)
        self.assertIsNone(exact["next_cursor"], "an exact page boundary has no spurious cursor")

        at_total = dict(cursor)
        at_total["offset"] = 3
        at_total_token = self.encode_cursor(at_total)
        terminal = self.run_json(["browse", "--cursor", at_total_token, "--json"])
        self.assertEqual(terminal["status"], "empty")
        self.assertEqual(terminal["total"], 3)
        self.assertEqual(terminal["returned_count"], 0)
        beyond = dict(cursor)
        beyond["offset"] = 4
        self.assert_cli_error(["browse", "--cursor", self.encode_cursor(beyond), "--json"], "invalid_cursor")
        self.assert_cli_error(["browse", "--cursor", token + "x", "--json"], "invalid_cursor")
        self.assert_cli_error(["browse", "--cursor", token, "--node", node_id, "--json"], "invalid_cursor")
        self.assert_cli_error(["browse", "--cursor", token, "--limit", "1", "--json"], "invalid_cursor")
        self.assert_cli_error(["browse", "--cursor", token, "--node", "source.collection.skills-db.tools", "--json"], "invalid_cursor")

        self.write_skill("page-d", category="testing", description="pagingfixture")
        self.rebuild()
        self.assert_cli_error(["browse", "--cursor", token, "--json"], "stale_cursor")

    def test_s04_source_edit_rename_and_bundle_asset_descriptors_are_truthful(self):
        self.install_taxonomy()
        source = self.write_skill(
            "package",
            category="testing",
            raw_header=(
                "---\nname: package\ndescription: oldtag001\ndependencies:\n"
                "  - unresolved-fixture-target\n---\n"
            ),
        )
        near_marker = self.write_skill("near-marker", category="testing/.trashcan", description="near marker control")
        trashed = self.write_skill("trashed", category="testing/.trash", description="disposed control")
        archived = self.write_skill("archived-control", category="testing", description="archive marker")
        asset = self.repo / "skills-db" / "testing" / "package" / "assets" / "logo.svg"
        asset.parent.mkdir(parents=True, exist_ok=True)
        asset.write_bytes(b"<svg>assetonlyneedle</svg>\n")
        self.write_state(
            {"skills-db/testing/archived-control": {"lifecycle": "archived", "rotation_role": "none"}}
        )
        rows = self.rebuild()
        skill = self.source_row(rows, "testing/package/SKILL.md")
        asset_row = self.source_row(rows, "testing/package/assets/logo.svg")

        node_id = "source.collection.skills-db.testing"
        browse = self.run_json(["browse", "--node", node_id, "--limit", "20", "--json"])
        initial_revision = browse["index_revision"]
        browsed_ids = {item["source_id"] for item in browse["items"]}
        self.assertIn(self.source_row(rows, "testing/.trashcan/near-marker/SKILL.md")["source_id"], browsed_ids)
        self.assertTrue(trashed.exists())
        self.assertFalse(any(".trash" in Path(item["path"]).parts for item in browse["items"]))
        archived_item = next(item for item in browse["items"] if item["skill_name"] == "archived-control")
        self.assertEqual(archived_item["lifecycle"], "archived")
        self.assertTrue(all(isinstance(item["lifecycle"], str) for item in browse["items"]))
        asset_item = next(item for item in browse["items"] if item["source_id"] == asset_row["source_id"])
        skill_item = next(item for item in browse["items"] if item["source_id"] == skill["source_id"])
        self.assertEqual(asset_item["digest"], file_digest(asset))
        self.assertIn(asset_row["source_id"], {member["source_id"] for member in asset_item["bundle"]["members"]})
        self.assertIn(skill["source_id"], {member["source_id"] for member in asset_item["bundle"]["members"]})
        self.assertEqual(asset_item["bundle"]["scope"], "package_snapshot")
        self.assertEqual(asset_item["bundle"]["boundary_status"], "entrypoint_directory")
        self.assertTrue(
            any(item["resolution_status"] == "not_resolved" for item in skill_item["relationship_uncertainty"])
        )

        discovered = self.run_json(["discover", "assetonlyneedle", "--json", "--no-cache"])
        self.assertNotIn(asset_row["source_id"], {item["source_id"] for item in discovered["matches"]})
        got_asset = self.run_json(["get", asset_row["source_id"], "--json"])["items"][0]
        self.assertEqual(got_asset["path"], str(asset.resolve()))
        self.assertEqual(got_asset["digest"], file_digest(asset))

        original = source.read_bytes()
        original_stat = source.stat()
        edited = original.replace(b"oldtag001", b"newtag002")
        self.assertEqual(len(edited), len(original))
        source.write_bytes(edited)
        os.utime(source, ns=(original_stat.st_atime_ns, original_stat.st_mtime_ns))
        self.assert_cli_error(["discover", "newtag002", "--json", "--no-cache"], "stale_index")

        updated_rows = self.rebuild()
        updated_skill = self.source_row(updated_rows, "testing/package/SKILL.md")
        self.assertNotEqual(updated_skill["digest"], skill["digest"])
        updated = self.run_json(["discover", "newtag002", "--json", "--no-cache"])
        updated_match = next(item for item in updated["matches"] if item["source_id"] == skill["source_id"])
        self.assertEqual(updated_match["digest"], file_digest(source))
        self.assertNotEqual(updated_match["index_revision"], initial_revision)

        renamed = source.with_name("NOTES.md")
        source.rename(renamed)
        self.assert_cli_error(["get", skill["source_id"], "--json"], "stale_index")
        renamed_rows = self.rebuild()
        renamed_row = self.source_row(renamed_rows, "testing/package/NOTES.md")
        self.assertNotEqual(renamed_row["source_id"], skill["source_id"])
        self.assertEqual(renamed_row["digest"], file_digest(renamed))
        self.assert_cli_error(["get", skill["source_id"], "--json"], "source_not_found")
        new_get = self.run_json(["get", renamed_row["source_id"], "--json"])["items"][0]
        self.assertEqual(new_get["path"], str(renamed.resolve()))
        self.assertEqual(new_get["digest"], file_digest(renamed))

    def test_s04_no_cache_readers_preserve_canonical_and_optional_cache_bytes(self):
        self.install_taxonomy()
        source = self.write_skill("readonly-control", category="testing", description="readonlyneedle")
        rows = self.rebuild()
        row = self.source_row(rows, "testing/readonly-control/SKILL.md")
        before_canonical = self.canonical_bytes()

        self.run_json(["tree", "--view", "collections", "--json"])
        self.run_json(["browse", "--node", "source.collection.skills-db.testing", "--json"])
        self.run_json(["get", row["source_id"], "--json"])
        self.run_json(["discover", "readonlyneedle", "--json"])
        cache_files = list(self.cache_dir.glob("discover-v*.json"))
        self.assertTrue(cache_files)
        cache_file = cache_files[0]
        cache_document = json.loads(cache_file.read_text(encoding="utf-8"))
        cache_document["result"]["matches"][0]["skill_name"] = "poisoned-cache-result"
        unsigned = {key: value for key, value in cache_document.items() if key != "integrity_sha256"}
        cache_document["integrity_sha256"] = hashlib.sha256(
            json.dumps(unsigned, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
        ).hexdigest()
        cache_file.write_text(json.dumps(cache_document), encoding="utf-8")
        before_cache = self.tree_bytes(self.cache_dir)
        uncached = self.run_json(["discover", "readonlyneedle", "--json", "--no-cache"])
        self.assertNotEqual(uncached["matches"][0]["skill_name"], "poisoned-cache-result")
        self.assertEqual(uncached["matches"][0]["skill_name"], "readonly-control")
        self.assertEqual(uncached["evaluation_origin"], "cli_evaluation")
        self.assertTrue(uncached["query_groups"][0]["evaluated"])

        self.assertEqual(self.canonical_bytes(), before_canonical)
        self.assertEqual(self.tree_bytes(self.cache_dir), before_cache)
        self.assertEqual(file_digest(source), row["digest"])

    def test_s04_oversized_numeric_values_fail_structurally_before_inventory_lookup(self):
        self.write_skill("numeric-not-indexed", category="testing", description="numericneedle")
        before_canonical = self.canonical_bytes()
        before_cache = self.tree_bytes(self.cache_dir)
        oversized = "9" * 5000
        node_id = "source.collection.skills-db.testing"
        cases = [
            ("discover-equals", ["discover", "--query", "numericneedle", f"--limit={oversized}", "--json"]),
            ("discover-separated", ["discover", "--query", "numericneedle", "--limit", oversized, "--json"]),
            ("tree-equals", ["tree", f"--depth={oversized}", "--json"]),
            ("tree-separated", ["tree", "--depth", oversized, "--json"]),
            ("browse-equals", ["browse", "--node", node_id, f"--limit={oversized}", "--json"]),
            ("browse-separated", ["browse", "--node", node_id, "--limit", oversized, "--json"]),
            ("discover-positional-limit", ["discover", "numericneedle", oversized, "--json"]),
            ("shorthand-positional-limit", ["numericneedle", oversized, "--json"]),
        ]
        for case_name, args in cases:
            with self.subTest(case=case_name):
                result = self.run_cli(args)
                self.assertEqual(
                    result.returncode,
                    1,
                    f"oversized numeric input must fail before lookup: {result.args}\nstdout={result.stdout}\nstderr={result.stderr}",
                )
                self.assertNotIn("Traceback", result.stdout + result.stderr)
                try:
                    payload = json.loads(result.stdout)
                except json.JSONDecodeError as error:
                    self.fail(f"oversized numeric input did not return structured JSON: {error}\n{result.stdout}\n{result.stderr}")
                self.assertEqual(payload.get("status"), "error")
                self.assertEqual(payload.get("error", {}).get("code"), "invalid_request")
                self.assertEqual(self.canonical_bytes(), before_canonical)
                self.assertEqual(self.tree_bytes(self.cache_dir), before_cache)
                self.assertFalse((self.repo / "skills-inventory.snapshot.json").exists())
                self.assertFalse(self.cache_dir.exists())

        signed_browse_limit = self.run_cli(["browse", "--node", node_id, "--limit", "-1", "--json"])
        invalid = self.assert_json_error_result(signed_browse_limit, "invalid_request")
        self.assertNotIn("Traceback", json.dumps(invalid) + signed_browse_limit.stderr)
        self.assertEqual(self.canonical_bytes(), before_canonical)
        self.assertEqual(self.tree_bytes(self.cache_dir), before_cache)

    def test_s04_signed_and_legacy_discovery_limits_keep_clamp_and_exact_boundary(self):
        taxonomy = self.install_taxonomy()
        self.write_skill("numeric-a", category="testing", description="numericboundary")
        self.write_skill("numeric-b", category="testing", description="numericboundary")
        self.rebuild()

        for args in (
            ["discover", "numericboundary", "--limit=0", "--json", "--no-cache"],
            ["discover", "numericboundary", "--limit", "0", "--json", "--no-cache"],
            ["discover", "numericboundary", "--limit=-1", "--json", "--no-cache"],
            ["discover", "numericboundary", "--limit", "-1", "--json", "--no-cache"],
            ["discover", "numericboundary", "0", "--json", "--no-cache"],
            ["numericboundary", "1", "--json", "--no-cache"],
        ):
            with self.subTest(args=args):
                payload = self.run_json(args)
                self.assertEqual(payload["status"], "ok")
                self.assertEqual(payload["limit"], 1)
                self.assertEqual(payload["returned_count"], 1)

        exact_named = self.run_json(
            ["discover", "numericboundary", "--limit=2", "--json", "--no-cache"]
        )
        exact_positional = self.run_json(
            ["discover", "numericboundary", "2", "--json", "--no-cache"]
        )
        self.assertEqual(exact_named["limit"], 2)
        self.assertEqual(exact_named["total"], 2)
        self.assertEqual(exact_named["returned_count"], 2)
        self.assertEqual(exact_positional["limit"], 2)
        self.assertEqual([item["source_id"] for item in exact_named["matches"]], [
            item["source_id"] for item in exact_positional["matches"]
        ])

        tree = self.run_json(["tree", "--view", "subjects", "--depth", "0", "--json"])
        self.assertEqual(tree["depth"], 0)
        self.assertTrue(all(node["children"] == [] for node in tree["items"]))
        node_id = "source.collection.skills-db.testing"
        exact_browse = self.run_json(["browse", "--node", node_id, "--limit", "2", "--json"])
        self.assertEqual(exact_browse["total"], 2)
        self.assertEqual(exact_browse["returned_count"], 2)
        self.assertIsNone(exact_browse["next_cursor"])
        self.assertIn("source.collection.skills-db.testing", {node["id"] for node in taxonomy["nodes"]})

    def test_s04_all_and_primary_only_remain_composable_legacy_noops(self):
        self.write_skill("noop-control", category="testing", description="aurora compatibility")
        self.rebuild()
        forms = (
            (["aurora", "--json", "--no-cache"], ["aurora", "--all", "--primary-only", "--json", "--no-cache"]),
            (["find", "aurora", "--json", "--no-cache"], ["find", "aurora", "--all", "--primary-only", "--json", "--no-cache"]),
            (["discover", "aurora", "--json", "--no-cache"], ["discover", "aurora", "--all", "--primary-only", "--json", "--no-cache"]),
        )
        for baseline_args, combined_args in forms:
            with self.subTest(form=baseline_args[0]):
                baseline = self.run_cli(baseline_args)
                combined = self.run_cli(combined_args)
                self.assertEqual(baseline.returncode, 0, baseline.stderr)
                self.assertEqual(combined.returncode, 0, combined.stderr)
                self.assertEqual(combined.stdout, baseline.stdout)

    def test_s04_cached_source_descriptors_are_bound_to_current_rows_and_bundle(self):
        self.install_taxonomy()
        source = self.write_skill(
            "cachetruth",
            category="testing",
            raw_header=(
                "---\nname: cachetruth\ndescription: cachetruthneedle\ndependencies:\n"
                "  - unresolved-cache-fixture-target\n---\n"
            ),
        )
        assets_dir = source.parent / "assets"
        assets_dir.mkdir(parents=True, exist_ok=True)
        for index in range(14):
            (assets_dir / f"member-{index:02d}.svg").write_bytes(f"<svg>{index}</svg>\n".encode())
        rows = self.rebuild()
        row = self.source_row(rows, "testing/cachetruth/SKILL.md")
        asset_row = self.source_row(rows, "testing/cachetruth/assets/member-00.svg")

        first = self.run_json(["discover", "cachetruthneedle", "--json"])
        self.assertEqual(first["evaluation_origin"], "cli_evaluation")
        self.assertTrue(first["query_groups"][0]["evaluated"])
        first_match = first["matches"][0]
        self.assertEqual(first_match["source_id"], row["source_id"])
        self.assertEqual(first_match["bundle"]["member_count"], 15)
        self.assertEqual(len(first_match["bundle"]["members"]), 15)
        self.assertTrue(first_match["relationships"])
        self.assertTrue(first_match["relationship_uncertainty"])

        # Instrument only this disposable CLI copy. A valid cache hit must return
        # before the whole-query evaluator runs; no-cache and invalid-cache paths
        # must still evaluate once.
        marker = 'if __name__ == "__main__":\n    raise SystemExit(main())'
        script = self.script.read_text(encoding="utf-8")
        self.assertIn(marker, script)
        counter_hook = '''if os.environ.get("SDB_TEST_DISCOVERY_COUNTER"):
    _s04_original_discover_matches = discover_matches

    def discover_matches(*args, **kwargs):
        with open(os.environ["SDB_TEST_DISCOVERY_COUNTER"], "a", encoding="utf-8") as counter:
            counter.write("called\\n")
        return _s04_original_discover_matches(*args, **kwargs)


'''
        self.script.write_text(script.replace(marker, counter_hook + marker, 1), encoding="utf-8")
        discovery_counter = self.output / "discover-matcher-calls.log"
        counter_env = {"SDB_TEST_DISCOVERY_COUNTER": str(discovery_counter)}

        valid_hit = self.run_json(
            ["discover", "cachetruthneedle", "--json"], env_overrides=counter_env
        )
        self.assertTrue(valid_hit["_cache"]["hit"])
        self.assertEqual(valid_hit["evaluation_origin"], "cache")
        self.assertFalse(valid_hit["query_groups"][0]["evaluated"])
        self.assertEqual(valid_hit["matches"][0], first_match)
        valid_hit_invoked_matcher = discovery_counter.exists()
        if valid_hit_invoked_matcher:
            discovery_counter.unlink()

        cache_file = next(self.cache_dir.glob("discover-v*.json"))
        original_cache = json.loads(cache_file.read_text(encoding="utf-8"))
        cache_before_no_cache = cache_file.read_bytes()
        no_cache = self.run_json(
            ["discover", "cachetruthneedle", "--json", "--no-cache"],
            env_overrides=counter_env,
        )
        self.assertEqual(no_cache["evaluation_origin"], "cli_evaluation")
        self.assertTrue(no_cache["query_groups"][0]["evaluated"])
        self.assertFalse(no_cache["_cache"]["hit"])
        self.assertEqual(discovery_counter.read_text(encoding="utf-8").splitlines(), ["called"])
        self.assertEqual(cache_file.read_bytes(), cache_before_no_cache)

        def reseal(document: dict) -> bytes:
            unsigned = {key: value for key, value in document.items() if key != "integrity_sha256"}
            document["integrity_sha256"] = hashlib.sha256(
                json.dumps(
                    unsigned,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                    allow_nan=False,
                ).encode("utf-8")
            ).hexdigest()
            return json.dumps(document, ensure_ascii=False).encode("utf-8")

        def false_path(match: dict) -> None:
            path = str(self.repo / "skills-db" / "testing" / "fabricated" / "SKILL.md")
            match["path"] = match["local_path"] = match["realpath"] = path
            match["source_record"]["real_path"] = path
            match["path_key"] = "skills-db/testing/fabricated"

        def false_digest(match: dict) -> None:
            digest = "0" * 64
            match["digest"] = match["content_revision"] = digest
            match["source_record"]["sha256"] = digest

        def false_namespace(match: dict) -> None:
            match["source_namespace"] = "skills"
            match["source_scope"]["namespace"] = "skills"

        def false_scope(match: dict) -> None:
            relative = "testing/fabricated/SKILL.md"
            match["source_scope"]["relative_path"] = relative
            match["source_record"]["relative_path"] = relative

        def false_collection(match: dict) -> None:
            match["source_collection"] = "tools"
            match["source_scope"]["collection"] = "tools"
            match["source_record"]["collection"] = "tools"

        def false_metadata(match: dict) -> None:
            match["metadata"]["status"] = "verified"

        def false_runtime(match: dict) -> None:
            match["quality"]["runtime_status"] = "verified"

        def false_availability(match: dict) -> None:
            match["availability"] = False
            match["quality"]["source_available"] = False
            match["source_record"]["status"] = "unavailable"

        false_role_value = next(
            role for role in ("pinned", "eligible", "experimental", "none") if role != first_match["rotation_role"]
        )

        def false_role(match: dict) -> None:
            match["rotation_role"] = false_role_value
            match["lifecycle"] = "archived"

        def false_taxonomy(match: dict) -> None:
            match["taxonomy"] = {"status": "projected", "memberships": [], "unresolved": []}

        def false_relationships(match: dict) -> None:
            match["relationships"] = []
            match["relationship_uncertainty"] = []

        def false_delivery(match: dict) -> None:
            match["content_delivery"] = {"mode": "bytes_delivered", "content_loaded": True}

        def false_diagnostics(match: dict) -> None:
            match["diagnostics"] = ["fabricated cache diagnostic"]

        def wrong_doc_type(match: dict) -> None:
            match["doc_type"] = "markdown"

        def unknown_source_id(match: dict) -> None:
            match["source_id"] = "skills-db/testing/missing/SKILL.md"

        def ineligible_asset_id(match: dict) -> None:
            match["source_id"] = asset_row["source_id"]

        def incomplete_bundle(match: dict) -> None:
            match["bundle"]["members"].pop()
            match["bundle"]["member_count"] -= 1
            match["bundle_member_source_ids"].pop()

        def false_bundle_revision(match: dict) -> None:
            revision = "f" * 64
            match["bundle_revision"] = revision
            match["bundle"]["revision"] = revision

        def false_bundle_scope(match: dict) -> None:
            match["bundle_scope"] = "standalone_file"
            match["bundle"]["scope"] = "standalone_file"

        def false_bundle_boundary(match: dict) -> None:
            match["bundle_boundary_status"] = "unknown_no_package_marker"
            match["bundle"]["boundary_status"] = "unknown_no_package_marker"

        mutants = [
            ("path", false_path),
            ("digest-and-content-revision", false_digest),
            ("namespace", false_namespace),
            ("source-scope", false_scope),
            ("collection", false_collection),
            ("full-metadata", false_metadata),
            ("runtime-status", false_runtime),
            ("availability", false_availability),
            ("role-and-lifecycle", false_role),
            ("taxonomy", false_taxonomy),
            ("relationships", false_relationships),
            ("content-delivery", false_delivery),
            ("diagnostics", false_diagnostics),
            ("document-type", wrong_doc_type),
            ("unknown-source-id", unknown_source_id),
            ("ineligible-asset-id", ineligible_asset_id),
            ("bundle-member-closure", incomplete_bundle),
            ("bundle-revision", false_bundle_revision),
            ("bundle-scope", false_bundle_scope),
            ("bundle-boundary", false_bundle_boundary),
        ]
        canonical_before = self.canonical_bytes()
        for name, mutate in mutants:
            with self.subTest(cache_mutant=name):
                poisoned = json.loads(json.dumps(original_cache))
                mutate(poisoned["result"]["matches"][0])
                poisoned_bytes = reseal(poisoned)
                cache_file.write_bytes(poisoned_bytes)
                parsed_poison = json.loads(poisoned_bytes)
                self.assertEqual(
                    parsed_poison["integrity_sha256"],
                    hashlib.sha256(
                        json.dumps(
                            {key: value for key, value in parsed_poison.items() if key != "integrity_sha256"},
                            ensure_ascii=False,
                            sort_keys=True,
                            separators=(",", ":"),
                            allow_nan=False,
                        ).encode("utf-8")
                    ).hexdigest(),
                    "the cache envelope checksum is recomputed for each semantic mutation",
                )
                discovery_counter.write_text("", encoding="utf-8")
                result = self.run_json(
                    ["discover", "cachetruthneedle", "--json"], env_overrides=counter_env
                )
                self.assertEqual(result["evaluation_origin"], "cli_evaluation")
                self.assertFalse(result["_cache"]["hit"])
                self.assertEqual(
                    discovery_counter.read_text(encoding="utf-8").splitlines(),
                    ["called"],
                    "a rejected source mutation must fall through to one fresh group evaluation",
                )
                self.assertEqual(result["matches"][0]["source_id"], row["source_id"])
                current = result["matches"][0]
                self.assertEqual(current["path"], str(source.resolve()))
                self.assertEqual(current["realpath"], str(source.resolve()))
                self.assertEqual(current["digest"], file_digest(source))
                self.assertEqual(current["content_revision"], file_digest(source))
                self.assertEqual(current["source_record"], row["source"])
                self.assertEqual(current["metadata"], row["original_metadata"])
                self.assertEqual(current["quality"], row["quality"])
                self.assertEqual(current["taxonomy"], row["taxonomy"])
                self.assertEqual(current["relationships"], row["relationship_declarations"])
                self.assertEqual(current["content_delivery"], {"mode": "descriptor_only", "content_loaded": False})
                self.assertEqual(current["bundle"], first_match["bundle"])
                self.assertEqual(len(current["bundle"]["members"]), 15)
                self.assertEqual(current["bundle_member_source_ids"], first_match["bundle_member_source_ids"])
                self.assertEqual(self.canonical_bytes(), canonical_before)
                repaired_cache = json.loads(cache_file.read_text(encoding="utf-8"))
                self.assertEqual(repaired_cache["result"]["matches"], result["matches"])

        self.assertFalse(
            valid_hit_invoked_matcher,
            "a valid cache hit must not invoke the full-query matcher",
        )


if __name__ == "__main__":
    unittest.main()
