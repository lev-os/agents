import importlib.machinery
import importlib.util
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("LEV_SKILLS_TEST_SOURCE", ROOT / "lev-skills.sh")).resolve()
LOADER = importlib.machinery.SourceFileLoader("lev_skills", str(SOURCE))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
LEV_SKILLS = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(LEV_SKILLS)


class CatalogRootsTest(unittest.TestCase):
    def test_direct_and_repository_skills_share_category_semantics(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skills_db = root / "skills-db"
            skill_repos = root / "_repos"
            direct = skills_db / "video" / "direct" / "SKILL.md"
            lower = skills_db / "video" / "lowercase" / "skill.md"
            external = skill_repos / "video" / "vendor" / "external" / "SKILL.md"
            malformed = skill_repos / "video" / "SKILL.md"

            for path, name in (
                (direct, "direct"),
                (lower, "lowercase"),
                (external, "external"),
                (malformed, "malformed"),
            ):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f"---\nname: {name}\ndescription: test\n---\n")

            with (
                patch.object(LEV_SKILLS, "SKILLS_DB_DIR", skills_db),
                patch.object(LEV_SKILLS, "SKILL_REPOS_DIR", skill_repos),
            ):
                rows = {row["name"]: row for row in LEV_SKILLS.catalog_rows()}
                repo_row = LEV_SKILLS.build_skill_row(
                    "_repos", external, external.relative_to(skill_repos).parts
                )

            self.assertEqual({"direct", "external", "lowercase"}, set(rows))
            self.assertEqual("skill.md", Path(rows["lowercase"]["path"]).name)
            self.assertEqual(("skills-db", "video", None), (
                rows["direct"]["base"], rows["direct"]["category"], rows["direct"]["source_repo"]
            ))
            self.assertEqual(("_repos", "video", "vendor"), (
                rows["external"]["base"], rows["external"]["category"], rows["external"]["source_repo"]
            ))
            self.assertEqual(("video", "vendor", "catalog-repo"), (
                repo_row["category"], repo_row["source_repo"], repo_row["surface"]
            ))
            self.assertEqual(1, LEV_SKILLS.parse_usage_markers(
                f"{Path.home()}/.agents/_repos/video/vendor/nested/SKILL.md"
            )["repos-video-vendor-nested"])

    def test_missing_parser_is_distinct_from_headerless_source_without_salvage(self):
        with patch.object(LEV_SKILLS, "yaml", None):
            parsed, _, _, _ = LEV_SKILLS.parse_source_metadata(
                b"---\nname: Nested Value\n  tags: [one, two]\n---\n",
                markdown=True,
            )
            headerless, _, _, _ = LEV_SKILLS.parse_source_metadata(
                b"# Headerless\nbody\n",
                markdown=True,
            )

        self.assertEqual("parser_unavailable", parsed["status"])
        self.assertIsNone(parsed["value"])
        self.assertEqual("absent", headerless["status"])


class SourceIdentityAndBundleTest(unittest.TestCase):
    def write(self, root, relative, content):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return path

    def scan(self, root):
        skills_db = root / "skills-db"
        skills = root / "skills"
        repos = root / "_repos"
        skills_db.mkdir(parents=True, exist_ok=True)
        skills.mkdir(parents=True, exist_ok=True)
        repos.mkdir(parents=True, exist_ok=True)
        with (
            patch.object(LEV_SKILLS, "SKILLS_DB_DIR", skills_db),
            patch.object(LEV_SKILLS, "SKILLS_DIR", skills),
            patch.object(LEV_SKILLS, "SKILL_REPOS_DIR", repos),
        ):
            return LEV_SKILLS.scan_source_inputs(include_bytes=True)[1]

    def test_identity_uses_namespace_and_complete_filename_across_edit_and_move(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write(root / "skills-db", "thinking/hidden-gems/murphyjitsu.md", b"same bytes")
            self.write(root / "skills-db", "thinking/hidden-gems/alders-razor.md", b"same bytes")
            self.write(root / "skills-db", "dev/convex/SKILL.md", b"same entrypoint")
            self.write(root / "skills-db", "convex/skills/convex/SKILL.md", b"same entrypoint")
            self.write(root / "skills-db", "engineering/wayfinder/SKILL.md", b"same wayfinder")
            self.write(root / "skills-db", "planning/wayfinder/SKILL.md", b"same wayfinder")

            before = self.scan(root)
            by_path = {row["relative_path"]: row for row in before if row["base"] == "skills-db"}
            source_ids = {
                path: LEV_SKILLS.source_id_for("skills-db", path)
                for path in by_path
            }
            self.assertNotEqual(
                source_ids["thinking/hidden-gems/murphyjitsu.md"],
                source_ids["thinking/hidden-gems/alders-razor.md"],
            )
            self.assertEqual(
                by_path["thinking/hidden-gems/murphyjitsu.md"]["sha256"],
                by_path["thinking/hidden-gems/alders-razor.md"]["sha256"],
            )
            self.assertNotEqual(
                source_ids["dev/convex/SKILL.md"],
                source_ids["convex/skills/convex/SKILL.md"],
            )
            self.assertEqual(
                by_path["dev/convex/SKILL.md"]["sha256"],
                by_path["convex/skills/convex/SKILL.md"]["sha256"],
            )
            self.assertNotEqual(
                source_ids["engineering/wayfinder/SKILL.md"],
                source_ids["planning/wayfinder/SKILL.md"],
            )
            self.assertEqual(
                by_path["engineering/wayfinder/SKILL.md"]["sha256"],
                by_path["planning/wayfinder/SKILL.md"]["sha256"],
            )
            package_catalog, bundle_assignments = LEV_SKILLS.build_bundle_catalog(before)
            package_by_id = {item["bundle_id"]: item for item in package_catalog}
            for first_path, second_path in (
                ("dev/convex/SKILL.md", "convex/skills/convex/SKILL.md"),
                ("engineering/wayfinder/SKILL.md", "planning/wayfinder/SKILL.md"),
            ):
                first_id = source_ids[first_path]
                second_id = source_ids[second_path]
                first_bundle_id = bundle_assignments[first_id]
                second_bundle_id = bundle_assignments[second_id]
                self.assertNotEqual(first_bundle_id, second_bundle_id)
                self.assertEqual(
                    package_by_id[first_bundle_id]["sha256"],
                    package_by_id[second_bundle_id]["sha256"],
                )

            edited = root / "skills-db" / "thinking/hidden-gems/murphyjitsu.md"
            edited.write_bytes(b"changed bytes")
            after_edit = self.scan(root)
            edit_row = next(row for row in after_edit if row["relative_path"] == "thinking/hidden-gems/murphyjitsu.md")
            self.assertEqual(source_ids["thinking/hidden-gems/murphyjitsu.md"],
                             LEV_SKILLS.source_id_for(edit_row["base"], edit_row["relative_path"]))
            self.assertNotEqual(by_path["thinking/hidden-gems/murphyjitsu.md"]["sha256"], edit_row["sha256"])

            edited.rename(root / "skills-db" / "thinking/hidden-gems/murphyjitsu-renamed.md")
            after_move = self.scan(root)
            moved_paths = {row["relative_path"] for row in after_move}
            self.assertNotIn("thinking/hidden-gems/murphyjitsu.md", moved_paths)
            self.assertIn("thinking/hidden-gems/murphyjitsu-renamed.md", moved_paths)
            self.assertNotEqual(
                source_ids["thinking/hidden-gems/murphyjitsu.md"],
                LEV_SKILLS.source_id_for("skills-db", "thinking/hidden-gems/murphyjitsu-renamed.md"),
            )

    def test_package_bundle_tracks_assets_and_stops_at_nested_skill_boundary(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.write(root / "skills-db", "convex/skills/convex/SKILL.md", b"entrypoint")
            self.write(root / "skills-db", "convex/skills/convex/references/guide.md", b"guide one")
            self.write(root / "skills-db", "convex/skills/convex/scripts/check.sh", b"check")
            self.write(root / "skills-db", "convex/skills/convex/plugins/child/SKILL.md", b"child")
            self.write(root / "skills-db", "convex/skills/convex/plugins/child/config.json", b"{}")
            self.write(root / "skills-db", "thinking/hidden-gems/murphyjitsu.md", b"flat")
            self.write(root / "skills-db", "thinking/hidden-gems/alders-razor.md", b"flat")
            self.write(root / "skills", "lev/SKILL.md", b"active entrypoint")
            self.write(root / "skills", "lev/references/guide.md", b"not in the admitted active-source scan")
            self.write(root / "_repos", "video/vendor/SKILL.md", b"repo entrypoint")
            self.write(root / "_repos", "video/vendor/scripts/check.sh", b"repo script")

            before_records = self.scan(root)
            before_catalog, before_assignments = LEV_SKILLS.build_bundle_catalog(before_records)
            entry_id = LEV_SKILLS.source_id_for("skills-db", "convex/skills/convex/SKILL.md")
            bundle_id = before_assignments[entry_id]
            bundle = next(item for item in before_catalog if item["bundle_id"] == bundle_id)
            members = {item["relative_path"] for item in bundle["members"]}
            self.assertEqual(
                {"SKILL.md", "references/guide.md", "scripts/check.sh"},
                members,
            )
            self.assertNotIn("plugins/child/SKILL.md", members)
            self.assertEqual("package_snapshot", bundle["scope"])

            flat_ids = [
                LEV_SKILLS.source_id_for("skills-db", path)
                for path in (
                    "thinking/hidden-gems/murphyjitsu.md",
                    "thinking/hidden-gems/alders-razor.md",
                )
            ]
            self.assertNotEqual(before_assignments[flat_ids[0]], before_assignments[flat_ids[1]])
            for source_id in flat_ids:
                flat_bundle = next(item for item in before_catalog if item["bundle_id"] == before_assignments[source_id])
                self.assertEqual("standalone_file", flat_bundle["scope"])
                self.assertEqual("unknown_no_package_marker", flat_bundle["boundary_status"])
                self.assertEqual(1, len(flat_bundle["members"]))

            active_id = LEV_SKILLS.source_id_for("skills", "lev/SKILL.md")
            active_bundle = next(item for item in before_catalog if item["bundle_id"] == before_assignments[active_id])
            self.assertEqual("unknown_unenumerated_assets", active_bundle["boundary_status"])

            repo_id = LEV_SKILLS.source_id_for("_repos", "video/vendor/SKILL.md")
            repo_bundle = next(item for item in before_catalog if item["bundle_id"] == before_assignments[repo_id])
            self.assertEqual("standalone_file", repo_bundle["scope"])
            self.assertEqual("unknown_unenumerated_assets", repo_bundle["boundary_status"])
            self.assertEqual({"SKILL.md"}, {item["relative_path"] for item in repo_bundle["members"]})
            self.assertNotIn("video/vendor/scripts/check.sh", {item["relative_path"] for item in before_records})

            self.write(root / "skills-db", "convex/skills/convex/references/guide.md", b"guide two")
            after_catalog, after_assignments = LEV_SKILLS.build_bundle_catalog(self.scan(root))
            after_bundle = next(item for item in after_catalog if item["bundle_id"] == after_assignments[entry_id])
            self.assertEqual(entry_id, LEV_SKILLS.source_id_for("skills-db", "convex/skills/convex/SKILL.md"))
            self.assertNotEqual(bundle["sha256"], after_bundle["sha256"])


class TaxonomyProjectionTest(unittest.TestCase):
    def setUp(self):
        self.taxonomy_state = LEV_SKILLS.load_taxonomy_config()

    def node_labels(self):
        return {node["id"]: node["label"] for node in self.taxonomy_state["config"]["nodes"]}

    def row(self, relative_path, collection, *, base="skills-db", metadata=None, source_id=None,
            name=None, description=""):
        entrypoint = Path(relative_path).name.casefold() == "skill.md"
        doc_type = "skill" if entrypoint else ("markdown" if Path(relative_path).suffix.lower() == ".md" else "asset")
        directory = Path(relative_path).parent.as_posix()
        if directory == ".":
            directory = ""
        source_path = f"/fixture/{base}/{relative_path}"
        return {
            "source_id": source_id or LEV_SKILLS.source_id_for(base, relative_path),
            "base": base,
            "name": name or Path(relative_path).stem,
            "description": description,
            "doc_type": doc_type,
            "path": source_path,
            "path_key": f"{base}/{directory}" if directory else base,
            "lifecycle": "catalog",
            "rotation_role": "none",
            "structure": {
                "entrypoint_candidate": entrypoint,
                "declared_skill_type": metadata.get("skill_type") if isinstance(metadata, dict) and isinstance(metadata.get("skill_type"), str) else None,
                "role_status": "needs_semantic_review",
            },
            "source": {
                "collection": collection,
                "relative_path": relative_path,
                "sha256": "a" * 64,
                "real_path": source_path,
            },
            "original_metadata": {"status": "parsed" if metadata is not None else "absent",
                                  "value": metadata},
            "quality": {"runtime_status": "untested"},
        }

    def test_config_represents_accepted_tree_and_all_collection_policies(self):
        config = self.taxonomy_state["config"]
        labels_by_id = self.node_labels()
        labels = set(labels_by_id.values())
        for label in (
            "Software & systems", "Architecture", "Development", "Operations & release",
            "Security", "Testing", "Platforms & integrations", "Convex", "Current collection",
            "Preserved extras", "Apple", "Lev", "SDKs & tools", "AI & agents",
            "Prompting & retrieval", "Orchestration & memory", "Thinking & decisions",
            "Frameworks & methods", "Domain guides", "Axioms, concepts & skill chains",
            "Design & media", "UI & experience", "Diagrams & visual communication",
            "Video & animation", "Marketing & growth", "Search visibility", "Generative Engine Optimization",
            "Conversion & analytics", "Writing & editing", "Business & finance", "Law & compliance",
            "Health & clinical", "Investigation & OSINT", "Maritime & logistics", "By task",
            "Planning", "Building", "Reviewing", "Debugging", "By form", "Skills", "Routers",
            "Workflows", "References", "Concepts", "Weird / experimental",
            "By original collection / upstream source", "Acquisition & intake", "Retained history / archive",
            "Workshop scaffolding", "Uncategorized / unresolved",
        ):
            self.assertIn(label, labels)
        collections = [item for item in config["source_collections"] if item["namespace"] == "skills-db"]
        self.assertGreaterEqual(len(collections), 27)
        self.assertEqual(len(collections) - 3, sum(item["policy"] == "regular" for item in collections))
        self.assertEqual(3, sum(item["policy"] == "administrative" for item in collections))
        policy_by_name = {item["name"]: item["policy"] for item in collections}
        self.assertEqual("regular", policy_by_name["other"])
        self.assertEqual("regular", policy_by_name["creative"])
        self.assertEqual("administrative", policy_by_name["_workshop"])
        collection_ids = {item["name"]: item["node_id"] for item in collections}
        self.assertEqual("source.collection.skills-db.design-ux", collection_ids["design-ux"])
        self.assertEqual("source.collection.skills-db.video", collection_ids["video"])
        other = LEV_SKILLS.project_taxonomy_row(self.row("other/record.txt", "other"), self.taxonomy_state)
        other_memberships = {labels_by_id[item["node_id"]]: item for item in other["memberships"]}
        self.assertIn("Uncategorized / unresolved", other_memberships)
        self.assertTrue(any(
            basis.get("policy") == "regular"
            for basis in other_memberships["other"]["basis"]
        ))

    def test_cross_domain_legal_examples_are_overlapping_views_and_unknowns_stay_unresolved(self):
        labels = self.node_labels()
        cases = (
            ("legal/conducting-growth-due-diligence/SKILL.md", "Business & finance"),
            ("legal/coding-medical-encounters/SKILL.md", "Health & clinical"),
            ("legal/maritime-expert/SKILL.md", "Maritime & logistics"),
            ("legal/osint/SKILL.md", "Investigation & OSINT"),
        )
        for relative_path, expected_view in cases:
            with self.subTest(relative_path=relative_path):
                projected = LEV_SKILLS.project_taxonomy_row(self.row(relative_path, "legal"), self.taxonomy_state)
                membership_labels = {labels[item["node_id"]] for item in projected["memberships"]}
                self.assertIn(expected_view, membership_labels)
                self.assertNotIn("Law & compliance", membership_labels)
                self.assertTrue(all(item["status"] == "projected" and item.get("basis") for item in projected["memberships"]))
                self.assertEqual("projected", projected["semantic_status"])

        unknown = LEV_SKILLS.project_taxonomy_row(self.row("legal/unreviewed/SKILL.md", "legal"), self.taxonomy_state)
        self.assertIn("subject", unknown["unresolved_views"])
        unknown_labels = {labels[item["node_id"]] for item in unknown["memberships"]}
        self.assertNotIn("Law & compliance", unknown_labels)
        self.assertNotIn("Business & finance", unknown_labels)
        self.assertNotIn("confidence", json.dumps(unknown).lower())

    def test_convex_current_and_preserved_extras_share_platform_parent_without_merging(self):
        labels = self.node_labels()
        current_sources = (
            ("dev/convex/SKILL.md", "dev"),
            ("convex/skills/convex/SKILL.md", "convex"),
        )
        current_ids = []
        for path, collection in current_sources:
            row = self.row(path, collection)
            current_ids.append(row["source_id"])
            projected = LEV_SKILLS.project_taxonomy_row(row, self.taxonomy_state)
            membership_labels = {labels[item["node_id"]] for item in projected["memberships"]}
            self.assertIn("Convex", membership_labels)
            self.assertIn("Current collection", membership_labels)
        self.assertNotEqual(current_ids[0], current_ids[1])

        extras = LEV_SKILLS.project_taxonomy_row(
            self.row("convex-extras/convex-check-updates/SKILL.md", "convex-extras"),
            self.taxonomy_state,
        )
        extras_labels = {labels[item["node_id"]] for item in extras["memberships"]}
        self.assertIn("Convex", extras_labels)
        self.assertIn("Preserved extras", extras_labels)
        self.assertNotIn("Current collection", extras_labels)

    def test_weird_view_is_separate_from_maturity_and_view_totals_deduplicate_source_ids(self):
        labels = self.node_labels()
        experimental = self.row("experimental/unusual/SKILL.md", "experimental")
        first = LEV_SKILLS.project_taxonomy_row(experimental, self.taxonomy_state)
        experimental["classification"] = first
        membership_labels = {labels[item["node_id"]] for item in first["memberships"]}
        self.assertIn("Weird / experimental", membership_labels)
        self.assertEqual("catalog", experimental["lifecycle"])
        self.assertEqual("none", experimental["rotation_role"])
        self.assertNotIn("maturity", first)
        self.assertNotIn("readiness", first)

        tools_collection = LEV_SKILLS.project_taxonomy_row(
            self.row("tools/provider-host/SKILL.md", "tools"), self.taxonomy_state
        )
        tools_labels = {labels[item["node_id"]] for item in tools_collection["memberships"]}
        self.assertNotIn("SDKs & tools", tools_labels)
        self.assertIn("Platforms & integrations", tools_labels)
        self.assertTrue(any(
            basis.get("basis_status") == "provisional"
            for membership in tools_collection["memberships"]
            if labels[membership["node_id"]] == "Platforms & integrations"
            for basis in membership["basis"]
        ))

        convex = self.row("convex/skills/convex/SKILL.md", "convex")
        convex["taxonomy"] = LEV_SKILLS.project_taxonomy_row(convex, self.taxonomy_state)
        repeated = dict(convex)
        repeated["taxonomy"] = convex["taxonomy"]
        catalog = LEV_SKILLS.build_taxonomy_catalog([convex, repeated], self.taxonomy_state)
        convex_label_ids = {
            node_id for node_id, label in labels.items()
            if label in {"Current collection", "Convex", "convex"}
        }
        self.assertTrue(convex_label_ids)
        self.assertEqual(1, catalog["distinct_resource_count"])
        for node_id in convex_label_ids:
            if node_id in catalog["view_counts"]:
                self.assertEqual(1, catalog["view_counts"][node_id])

    def test_resolvable_capture_examples_have_path_rules_and_unmapped_examples_stay_diagnostic(self):
        config = self.taxonomy_state["config"]
        path_rules = config["rules"]["path_views"]
        mapped_examples = {
            (target, rule["example"])
            for rule in path_rules
            if rule.get("basis_kind") in {"accepted_example", "accepted_structure"}
            for target in rule["target_node_ids"]
        }
        nodes = {node["id"]: node for node in config["nodes"]}
        source_group_examples = set()
        declared_examples = set()
        for node in config["nodes"]:
            for example in node.get("examples", []):
                if node["view_kind"] == "source_group":
                    source_group_examples.add((node["id"], example))
                else:
                    declared_examples.add((node["id"], example))
        unresolved = declared_examples - mapped_examples
        self.assertEqual(
            {
                ("view.administration.acquisition-intake", "Metadata-only candidates"),
                ("view.administration.acquisition-intake", "Packages awaiting review"),
                ("view.administration.retained-history-archive", "Absorbed packages"),
                ("view.administration.retained-history-archive", "Previous variants"),
            },
            unresolved,
        )
        root_required = {
            ("view.thinking-decisions.frameworks-methods", "murphyjitsu"),
            ("view.thinking-decisions.frameworks-methods", "ooda-loop"),
            ("view.design-media.ui-experience", "ui-ux-pro-max"),
            ("view.ai-agents.prompting-retrieval", "prompt-engineer"),
            ("view.software-systems.architecture", "software-architecture"),
            ("view.software-systems.development", "bun-development"),
            ("view.software-systems.operations-release", "gh-actions"),
            ("view.writing-editing", "de-slopify"),
        }
        self.assertTrue(root_required <= mapped_examples)
        collection_names = {item["name"] for item in config["source_collections"]}
        self.assertTrue(all(example in collection_names for _, example in source_group_examples))

        for rule in path_rules:
            if rule.get("basis_kind") != "accepted_example":
                continue
            relative_path = rule["path"]
            if rule["match"] == "prefix":
                relative_path = relative_path + "/fixture/SKILL.md"
            row = self.row(relative_path, relative_path.split("/", 1)[0])
            projected = LEV_SKILLS.project_taxonomy_row(row, self.taxonomy_state)
            projected_ids = {item["node_id"] for item in projected["memberships"]}
            self.assertTrue(set(rule["target_node_ids"]) <= projected_ids, rule["id"])

        example_rows = []
        for rule in path_rules:
            relative_path = rule["path"]
            if rule["match"] == "prefix":
                relative_path = relative_path + "/fixture/SKILL.md"
            row = self.row(relative_path, relative_path.split("/", 1)[0])
            row["taxonomy"] = LEV_SKILLS.project_taxonomy_row(row, self.taxonomy_state)
            example_rows.append(row)
        catalog = LEV_SKILLS.build_taxonomy_catalog(example_rows, self.taxonomy_state)
        diagnostic_pairs = {(item["node_id"], item["example"]) for item in catalog["example_diagnostics"]}
        self.assertEqual(unresolved, diagnostic_pairs)

    def test_proposed_collection_views_are_provisional_and_legal_stays_selective(self):
        labels = self.node_labels()
        cases = (
            ("ai-agents/prompt-engineer/SKILL.md", "ai-agents", "AI & agents"),
            ("architecture/software-architecture/SKILL.md", "architecture", "Architecture"),
            ("design-ux/unreviewed/SKILL.md", "design-ux", "Design & media"),
            ("dev/unreviewed/SKILL.md", "dev", "Software & systems"),
            ("devops/unreviewed/SKILL.md", "devops", "Software & systems"),
            ("engineering/unreviewed/SKILL.md", "engineering", "Software & systems"),
            ("geo/unreviewed/SKILL.md", "geo", "Generative Engine Optimization"),
            ("formatting/unreviewed/SKILL.md", "formatting", "Writing & editing"),
            ("lev/unreviewed/SKILL.md", "lev", "Lev"),
            ("marketing/unreviewed/SKILL.md", "marketing", "Marketing & growth"),
            ("planning/unreviewed/SKILL.md", "planning", "Planning"),
            ("sdk/unreviewed/SKILL.md", "sdk", "SDKs & tools"),
            ("security/unreviewed/SKILL.md", "security", "Software & systems"),
            ("testing/unreviewed/SKILL.md", "testing", "Software & systems"),
            ("thinking/unreviewed/SKILL.md", "thinking", "Thinking & decisions"),
            ("video/unreviewed/SKILL.md", "video", "Design & media"),
            ("workflow/unreviewed/SKILL.md", "workflow", "Workflows"),
            ("apple/unreviewed/SKILL.md", "apple", "Apple"),
            ("experimental/unusual/SKILL.md", "experimental", "Weird / experimental"),
        )
        for path, collection, expected_label in cases:
            with self.subTest(collection=collection):
                row = self.row(path, collection)
                projected = LEV_SKILLS.project_taxonomy_row(row, self.taxonomy_state)
                target_ids = {node_id for node_id, label in labels.items() if label == expected_label}
                memberships = [item for item in projected["memberships"] if item["node_id"] in target_ids]
                self.assertTrue(memberships, expected_label)
                self.assertTrue(any(
                    basis.get("basis_status") == "provisional"
                    for membership in memberships
                    for basis in membership["basis"]
                ))

        legal = LEV_SKILLS.project_taxonomy_row(self.row("legal/unreviewed/SKILL.md", "legal"), self.taxonomy_state)
        legal_labels = {labels[item["node_id"]] for item in legal["memberships"]}
        self.assertNotIn("Law & compliance", legal_labels)

    def test_structure_form_hints_preserve_role_and_runtime_uncertainty(self):
        labels = self.node_labels()
        cases = (
            (self.row("dev/example/SKILL.md", "dev", metadata={"skill_type": "router"}), {"Skills", "Routers"}),
            (self.row("dev/example/SKILL.md", "dev", metadata={"skill_type": "workflow"}), {"Skills", "Workflows"}),
            (self.row("dev/example/SKILL.md", "dev", metadata={"skill_type": "concept"}), {"Skills", "Concepts"}),
            (self.row("dev/example/references/guide.md", "dev"), {"References"}),
        )
        for row, expected_labels in cases:
            projected = LEV_SKILLS.project_taxonomy_row(row, self.taxonomy_state)
            actual_labels = {labels[item["node_id"]] for item in projected["memberships"]}
            self.assertTrue(expected_labels <= actual_labels)
            self.assertEqual("needs_semantic_review", row["structure"]["role_status"])
            self.assertEqual("untested", row["quality"]["runtime_status"])
            self.assertTrue(any(
                basis.get("basis_status") == "provisional"
                for membership in projected["memberships"]
                if labels[membership["node_id"]] in expected_labels
                for basis in membership["basis"]
            ))

        unknown = self.row("dev/plain/document.md", "dev", name="plain", description="A generic reference note")
        unknown_projection = LEV_SKILLS.project_taxonomy_row(unknown, self.taxonomy_state)
        self.assertIn("form", unknown_projection["unresolved_views"])

    def test_task_cues_are_provisional_and_unsupported_items_stay_unknown(self):
        labels = self.node_labels()
        cases = (
            (self.row("misc/planner/SKILL.md", "misc", name="sprint planner", description="Plan a release roadmap"), "Planning"),
            (self.row("misc/build/SKILL.md", "misc", name="code builder", description="Implement application modules"), "Building"),
            (self.row("misc/review/SKILL.md", "misc", name="contract review", description="Audit a proposed agreement"), "Reviewing"),
            (self.row("misc/debug/SKILL.md", "misc", name="stack debugger", description="Troubleshoot and diagnose failures"), "Debugging"),
        )
        for row, expected_label in cases:
            projected = LEV_SKILLS.project_taxonomy_row(row, self.taxonomy_state)
            target_ids = {node_id for node_id, label in labels.items() if label == expected_label}
            memberships = [item for item in projected["memberships"] if item["node_id"] in target_ids]
            self.assertTrue(memberships, expected_label)
            self.assertTrue(any(
                basis.get("basis_status") == "provisional"
                for membership in memberships
                for basis in membership["basis"]
            ))
            self.assertTrue(any(
                basis.get("field") in {"name", "description"}
                and basis.get("token")
                and basis.get("basis_source") == "source-fields"
                for membership in memberships
                for basis in membership["basis"]
            ))

        source_cue = LEV_SKILLS.project_taxonomy_row(
            self.row("planning/unmatched/SKILL.md", "planning", name="unmatched"),
            self.taxonomy_state,
        )
        self.assertIn("Planning", {labels[item["node_id"]] for item in source_cue["memberships"]})
        self.assertTrue(any(
            basis.get("basis_status") == "provisional"
            for item in source_cue["memberships"] if labels[item["node_id"]] == "Planning"
            for basis in item["basis"]
        ))

        authored = self.row("misc/authored/SKILL.md", "misc", name="authored", metadata={"tasks": ["Reviewing"]})
        authored_projection = LEV_SKILLS.project_taxonomy_row(authored, self.taxonomy_state)
        self.assertIn("Reviewing", {labels[item["node_id"]] for item in authored_projection["memberships"]})

        unknown = self.row("misc/plain/SKILL.md", "misc", name="plain", description="A generic utility")
        unknown_projection = LEV_SKILLS.project_taxonomy_row(unknown, self.taxonomy_state)
        self.assertIn("task", unknown_projection["unresolved_views"])

    def test_disposed_trash_sources_keep_identity_but_receive_no_semantic_views(self):
        row = self.row(".trash/run/example/SKILL.md", "skills", base="skills", metadata={"skill_type": "router"})
        projected = LEV_SKILLS.project_taxonomy_row(row, self.taxonomy_state)
        self.assertEqual([], projected["semantic_memberships"])
        self.assertTrue(any(item["node_id"] == "source.namespace.skills" for item in projected["memberships"]))
        self.assertTrue(any(".trash" in item for item in projected["diagnostics"]))
        self.assertEqual(row["source_id"], LEV_SKILLS.source_id_for("skills", row["source"]["relative_path"]))


class RelationshipProjectionTest(unittest.TestCase):
    def row(self, relative_path, name, metadata, *, base="skills-db"):
        return {
            "source_id": LEV_SKILLS.source_id_for(base, relative_path),
            "base": base,
            "name": name,
            "slug": LEV_SKILLS.normalize_name(name),
            "source": {"relative_path": relative_path, "collection": relative_path.split("/")[0]},
            "original_metadata": {"status": "parsed", "value": metadata},
            "lifecycle": "catalog",
        }

    def test_relative_missing_ambiguous_external_and_subsumes_keep_authored_context(self):
        source = self.row(
            "legal/source/SKILL.md",
            "source",
            {
                "base": ".",
                "related_skills": ["references/helper.md", "missing.md", "same-name"],
                "dependencies": "python>=3.10, claude-agent-sdk>=1.0.0",
                "subsumes": ["source:skills-db/legal/target/SKILL.md"],
            },
        )
        helper = self.row("legal/source/references/helper.md", "helper", {})
        first_same = self.row("legal/one/SKILL.md", "same-name", {})
        second_same = self.row("legal/two/SKILL.md", "same-name", {})
        target = self.row("legal/target/SKILL.md", "target", {})
        rows = [source, helper, first_same, second_same, target]

        relationships = LEV_SKILLS.project_relationships(rows)[source["source_id"]]
        related = next(item for item in relationships if item["declaration_key"] == "related_skills")
        self.assertEqual(source["source"]["relative_path"], related["source_ref"])
        self.assertEqual("legal/source", related["resolution_context"]["source_directory"])
        self.assertEqual(".", related["resolution_context"]["declared_base"])
        self.assertEqual(["references/helper.md", "missing.md", "same-name"], related["original_value"])
        item_statuses = {item["original_value"]: item["resolution_status"] for item in related["targets"]}
        self.assertEqual("resolved", item_statuses["references/helper.md"])
        self.assertEqual("missing", item_statuses["missing.md"])
        self.assertEqual("ambiguous", item_statuses["same-name"])

        dependencies = next(item for item in relationships if item["declaration_key"] == "dependencies")
        self.assertEqual("external_runtime", dependencies["resolution_status"])
        self.assertEqual("python>=3.10, claude-agent-sdk>=1.0.0", dependencies["original_value"])
        subsumes = next(item for item in relationships if item["declaration_key"] == "subsumes")
        self.assertEqual("resolved", subsumes["resolution_status"])
        self.assertEqual(target["source_id"], subsumes["targets"][0]["target_source_id"])
        self.assertEqual("authored_not_verified", subsumes["semantic_status"])
        self.assertEqual("catalog", source["lifecycle"])


class IsolatedProjectionIntegrationTest(unittest.TestCase):
    def make_fixture(self, root, *, with_taxonomy=True):
        def write(relative, content):
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            return path

        (root / "skills-db").mkdir(parents=True)
        (root / "skills").mkdir(parents=True)
        (root / "_repos").mkdir(parents=True)
        write("skills-db/convex/skills/convex/SKILL.md", b"# Convex\n")
        write("skills-db/convex/skills/convex/references/guide.md", b"guide one")
        write("skills-db/legal/conducting-growth-due-diligence/SKILL.md", b"# Finance\n")
        write("skills-db/legal/coding-medical-encounters/SKILL.md", b"# Health\n")
        write("skills-db/legal/maritime-expert/SKILL.md", b"# Maritime\n")
        write("skills-db/legal/osint/SKILL.md", b"# OSINT\n")
        write("skills-db/legal/unreviewed/SKILL.md", b"# Unreviewed\n")
        write("skills-db/other/other.txt", b"regular collection file without skill entrypoint")
        write("skills-db/thinking/hidden-gems/murphyjitsu.md", b"flat one")
        write("skills-db/thinking/hidden-gems/alders-razor.md", b"flat two")
        write("skills/lev/SKILL.md", b"# Active\n")
        write("skills/lev/references/guide.md", b"not enumerated by active source spec")
        write("_repos/video/vendor/SKILL.md", b"# Vendor\n")
        write("_repos/video/vendor/scripts/check.sh", b"check")
        write("skills-state.json", b'{"skills": {}}')
        write("skill-graph.json", b'{"nodes": {}, "edges": []}')
        taxonomy_path = root / "skills-taxonomy.json"
        if with_taxonomy:
            shutil.copyfile(ROOT / "skills-taxonomy.json", taxonomy_path)
        return write

    def bindings(self, root):
        return patch.multiple(
            LEV_SKILLS,
            ROOT=root,
            SKILLS_DB_DIR=root / "skills-db",
            SKILLS_DIR=root / "skills",
            SKILL_REPOS_DIR=root / "_repos",
            SKILLS_STATE_FILE=root / "skills-state.json",
            SKILL_GRAPH_FILE=root / "skill-graph.json",
            SKILLS_INVENTORY_FILE=root / "skills-inventory.jsonl",
            SKILLS_INVENTORY_SNAPSHOT_FILE=root / "skills-inventory.snapshot.json",
            TAXONOMY_CONFIG_FILE=root / "skills-taxonomy.json",
        )

    def test_rebuild_binds_all_projection_inputs_and_asset_edit_marks_snapshot_stale(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write = self.make_fixture(root)
            with self.bindings(root), patch.object(LEV_SKILLS, "ensure_complete_yaml_parser"):
                rows, snapshot = LEV_SKILLS.rebuild_inventory()
                entry = next(row for row in rows if row["source"]["relative_path"] == "convex/skills/convex/SKILL.md")
                self.assertEqual("skills-db/convex/skills/convex/SKILL.md", entry["source_id"])
                self.assertEqual(entry["source"]["sha256"], entry["digest"])
                self.assertEqual(entry["digest"], entry["content_revision"])
                old_revision = snapshot["revision"]
                old_bundle_revision = entry["bundle_revision"]
                collection_counts = {
                    item["name"]: item["resource_count"]
                    for item in snapshot["taxonomy"]["source_collections"]
                }
                self.assertEqual(1, collection_counts["other"])
                self.assertEqual(0, collection_counts["_workshop"])
                write("skills-db/convex/skills/convex/references/guide.md", b"guide two")
                with self.assertRaisesRegex(RuntimeError, "stale"):
                    LEV_SKILLS.read_validated_inventory()

                rows_after, snapshot_after = LEV_SKILLS.rebuild_inventory()
                entry_after = next(row for row in rows_after if row["source"]["relative_path"] == "convex/skills/convex/SKILL.md")
                self.assertEqual(entry["source_id"], entry_after["source_id"])
                self.assertEqual(entry["digest"], entry_after["digest"])
                self.assertNotEqual(old_bundle_revision, entry_after["bundle_revision"])
                self.assertNotEqual(old_revision, snapshot_after["revision"])

                taxonomy_path = root / "skills-taxonomy.json"
                taxonomy_config = json.loads(taxonomy_path.read_text())
                taxonomy_config["rules"]["collection_views"][0]["basis_description"] += " Updated rule evidence."
                taxonomy_path.write_text(json.dumps(taxonomy_config, indent=2) + "\n")
                with self.assertRaisesRegex(RuntimeError, "stale"):
                    LEV_SKILLS.read_validated_inventory()

    def test_missing_taxonomy_is_explicit_and_malformed_taxonomy_fails_before_output(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_fixture(root, with_taxonomy=False)
            with self.bindings(root), patch.object(LEV_SKILLS, "ensure_complete_yaml_parser"):
                rows, snapshot = LEV_SKILLS.rebuild_inventory()
                row = next(row for row in rows if row["source"]["relative_path"] == "legal/unreviewed/SKILL.md")
                self.assertEqual("unconfigured", row["taxonomy"]["status"])
                self.assertTrue(row["taxonomy"]["diagnostics"])
                self.assertEqual("unconfigured", snapshot["taxonomy"]["status"])

        valid_config = json.loads((ROOT / "skills-taxonomy.json").read_text())
        invalid_rule = json.loads(json.dumps(valid_config))
        invalid_rule["rules"]["collection_views"][0]["target_node_ids"] = ["missing-node"]
        invalid_structure = json.loads(json.dumps(valid_config))
        invalid_structure["rules"]["structural_views"][0]["target_node_id"] = "missing-node"
        invalid_task = json.loads(json.dumps(valid_config))
        invalid_task["rules"]["task_cues"][0]["target_node_id"] = "missing-node"
        invalid_schema = {**valid_config, "unexpected": True}
        malformed_configs = (
            "{broken json",
            json.dumps(invalid_schema),
            json.dumps(invalid_rule),
            json.dumps(invalid_structure),
            json.dumps(invalid_task),
        )
        for config_text in malformed_configs:
            with self.subTest(config_text=config_text[:24]), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                self.make_fixture(root)
                (root / "skills-taxonomy.json").write_text(config_text)
                with (
                    self.bindings(root),
                    patch.object(LEV_SKILLS, "ensure_complete_yaml_parser"),
                    patch.object(LEV_SKILLS, "read_state_input") as read_state,
                    patch.object(LEV_SKILLS, "read_graph_input") as read_graph,
                    patch.object(LEV_SKILLS, "atomic_write") as atomic_write,
                ):
                    with self.assertRaisesRegex(RuntimeError, "taxonomy"):
                        LEV_SKILLS.rebuild_inventory()
                    read_state.assert_not_called()
                    read_graph.assert_not_called()
                    atomic_write.assert_not_called()
                    self.assertFalse((root / "skills-inventory.jsonl").exists())
                    self.assertFalse((root / "skills-inventory.snapshot.json").exists())

    def test_taxonomy_accepts_dynamic_regular_collections_and_keeps_admin_and_historical_ids(self):
        config = json.loads((ROOT / "skills-taxonomy.json").read_text())
        corpus = {item["name"]: item for item in config["source_collections"] if item["namespace"] == "skills-db"}
        self.assertEqual(corpus["creative"]["policy"], "regular")
        self.assertEqual(corpus["video"]["node_id"], "source.collection.skills-db.video")
        self.assertEqual(corpus["design-ux"]["node_id"], "source.collection.skills-db.design-ux")

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.make_fixture(root)
            (root / "skills-db/creative").mkdir()
            self.assertFalse((root / "skills-db/video").exists(), "declared empty historical collections stay valid")
            with self.bindings(root):
                validated = LEV_SKILLS.validate_taxonomy_config(config)
                self.assertEqual(validated["source_collections"], config["source_collections"])

                bad_admin = json.loads(json.dumps(config))
                next(item for item in bad_admin["source_collections"] if item["name"] == ".archive")["policy"] = "regular"
                with self.assertRaisesRegex(RuntimeError, "administrative collections"):
                    LEV_SKILLS.validate_taxonomy_config(bad_admin)

                undeclared = json.loads(json.dumps(config))
                undeclared["source_collections"] = [
                    item for item in undeclared["source_collections"]
                    if not (item["namespace"] == "skills-db" and item["name"] == "creative")
                ]
                with self.assertRaisesRegex(RuntimeError, "undeclared: creative"):
                    LEV_SKILLS.validate_taxonomy_config(undeclared)

                unsafe_path = json.loads(json.dumps(config))
                next(item for item in unsafe_path["source_collections"] if item["name"] == "creative")["name"] = "../creative"
                with self.assertRaisesRegex(RuntimeError, "source collection"):
                    LEV_SKILLS.validate_taxonomy_config(unsafe_path)


if __name__ == "__main__":
    unittest.main()
