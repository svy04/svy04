import tempfile
import unittest
from pathlib import Path

from scripts import check_public_github_surface_hygiene as hygiene


class PublicGitHubSurfaceHygieneTests(unittest.TestCase):
    def test_scan_repo_tree_catches_local_paths_and_secret_shaped_placeholders(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            bad_path = "C:" + "\\Users\\admin\\Desktop\\private\\README.md"
            placeholder = "OPENAI_API_KEY=" + "sk-" + "example-placeholder"
            (root / "README.md").write_text(
                f"Bad path: {bad_path}\n{placeholder}\n",
                encoding="utf-8",
            )

            findings = hygiene.scan_repo_tree("demo", root)

        labels = {finding.label for finding in findings}
        self.assertIn("windows-user-path", labels)
        self.assertIn("openai-key-assignment", labels)
        self.assertTrue(all(finding.repo == "demo" for finding in findings))

    def test_scan_repo_tree_catches_auth_state_log_disclosures(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            log_text = "\n".join(
                [
                    "Loaded cached " + "credentials for local provider",
                    "Auth" + "Required: reconnect account",
                    "error=invalid" + "_token",
                    "Missing or invalid " + "access token",
                ]
            )
            (root / "run-log.txt").write_text(log_text, encoding="utf-8")

            findings = hygiene.scan_repo_tree("demo", root)

        labels = {finding.label for finding in findings}
        self.assertIn("auth-cache-disclosure", labels)
        self.assertIn("auth-required-disclosure", labels)
        self.assertIn("invalid-token-disclosure", labels)
        self.assertIn("missing-access-token-disclosure", labels)

    def test_scan_repo_tree_catches_raw_auth_transcript_markers(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "bench" / "task" / "runs").mkdir(parents=True)
            (root / "bench" / "task" / "runs" / "client.md").write_text(
                "\n".join(
                    [
                        "async function refreshAccessToken() {}",
                        "return { status: 'UNAUTHENTICATED' };",
                    ]
                ),
                encoding="utf-8",
            )

            findings = hygiene.scan_repo_tree("demo", root)

        labels = {finding.label for finding in findings}
        self.assertIn("raw-auth-transcript", labels)

    def test_scan_repo_tree_blocks_actual_looking_bearer_values_but_not_placeholders(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "README.md").write_text(
                "Authorization: Bearer <token>\n",
                encoding="utf-8",
            )
            (root / "raw.txt").write_text(
                "Authorization: Bearer "
                + "abcdefghijklmnopqrstuvwxyz1234567890"
                + "\n",
                encoding="utf-8",
            )

            findings = hygiene.scan_repo_tree("demo", root)

        labels = {finding.label for finding in findings}
        self.assertIn("bearer-token-disclosure", labels)
        self.assertFalse(
            any(
                finding.label == "bearer-token-disclosure"
                and finding.path == "README.md"
                for finding in findings
            )
        )

    def test_scan_repo_tree_ignores_binary_files_and_git_metadata(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / ".git").mkdir()
            (root / ".git" / "config").write_text(
                "C:" + "\\Users\\admin\\Desktop\\hidden\n",
                encoding="utf-8",
            )
            (root / "image.png").write_bytes(b"\x89PNG\r\n\x1a\n")
            (root / "README.md").write_text("clean public text\n", encoding="utf-8")

            findings = hygiene.scan_repo_tree("demo", root)

        self.assertEqual(findings, [])

    def test_scan_repo_tree_allows_generic_windows_path_examples(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "windows-paths.md").write_text(
                "Example: C:" + "\\Users\\example\\workspace\\file.txt\n",
                encoding="utf-8",
            )

            findings = hygiene.scan_repo_tree("demo", root)

        self.assertEqual(findings, [])

    def test_format_finding_redacts_secret_like_excerpt(self):
        finding = hygiene.Finding(
            repo="demo",
            path="README.md",
            line=7,
            label="openai-key-assignment",
            excerpt="OPENAI_API_KEY=" + "sk-" + "example-placeholder",
        )

        rendered = hygiene.format_finding(finding)

        self.assertIn("demo:README.md:7 [openai-key-assignment]", rendered)
        self.assertIn("OPENAI_API_KEY=<redacted>", rendered)
        self.assertNotIn("example-placeholder", rendered)


if __name__ == "__main__":
    unittest.main()
