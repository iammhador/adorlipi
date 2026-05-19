import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RepositoryPolicyTests(unittest.TestCase):
    def test_forbidden_external_name_not_in_tracked_files(self):
        forbidden = "".join(chr(x) for x in (107, 104, 105, 112, 114, 111))
        tracked = subprocess.run(
            ["git", "ls-files"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.splitlines()

        offenders = []
        for rel in tracked:
            path = ROOT / rel
            if not path.is_file():
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if forbidden in content.lower():
                offenders.append(rel)

        self.assertEqual([], offenders, msg=f"Forbidden token found in tracked files: {offenders}")


if __name__ == "__main__":
    unittest.main()
