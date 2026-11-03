"""Offline tests for public-activity URL and contributor identity validation."""
import unittest
from discover_public_activity import ACCOUNT, normalize, valid_public_url

class DiscoveryTests(unittest.TestCase):
    def test_public_github_url(self):
        self.assertTrue(valid_public_url("https://github.com/redis/redis/issues/4#issuecomment-10", "redis/redis"))
        self.assertFalse(valid_public_url("http://github.com/redis/redis/issues/4", "redis/redis"))
        self.assertFalse(valid_public_url("https://github.com.attacker.example/redis/redis/issues/4", "redis/redis"))
        self.assertFalse(valid_public_url("https://github.com/other/repo/issues/4", "redis/redis"))

    def test_exact_public_author(self):
        original = {"id": 10, "user": {"login": ACCOUNT},
                    "html_url": "https://github.com/redis/redis/issues/4#issuecomment-10",
                    "created_at": "2026-10-02T12:00:00Z"}
        item = normalize(original, "redis/redis", 4,
                         "https://github.com/redis/redis/issues/4", "issue_comment")
        self.assertEqual(item["author"], ACCOUNT)
        self.assertEqual(item["comment_id"], 10)
        self.assertIn("TECHNICAL_REVIEW_PENDING", item["evidence_state"])

    def test_wrong_author_rejected(self):
        original = {"id": 11, "user": {"login": "upstream-maintainer"},
                    "html_url": "https://github.com/redis/redis/issues/4#issuecomment-11"}
        self.assertIsNone(normalize(original, "redis/redis", 4,
                                   "https://github.com/redis/redis/issues/4", "issue_comment"))

    def test_wrong_url_fails_closed(self):
        original = {"id": 12, "user": {"login": ACCOUNT},
                    "html_url": "https://malicious.example/redis/redis/issues/4"}
        with self.assertRaises(RuntimeError):
            normalize(original, "redis/redis", 4,
                      "https://github.com/redis/redis/issues/4", "issue_comment")

if __name__ == "__main__":
    unittest.main()
