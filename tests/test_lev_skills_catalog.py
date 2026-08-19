import importlib.machinery
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
LOADER = importlib.machinery.SourceFileLoader("lev_skills", str(ROOT / "lev-skills.sh"))
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
            external = skill_repos / "video" / "vendor" / "nested" / "SKILL.md"
            malformed = skill_repos / "video" / "SKILL.md"

            for path, name in ((direct, "direct"), (external, "external"), (malformed, "malformed")):
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

            self.assertEqual({"direct", "external"}, set(rows))
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


if __name__ == "__main__":
    unittest.main()
