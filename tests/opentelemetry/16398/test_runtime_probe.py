import unittest
import runtime_probe as p

class HarnessTests(unittest.TestCase):
    def test_shared_storage(self):
        s=p.config()
        self.assertEqual(s.count("processors: [queue_batch]"), 2)
        self.assertEqual(s.count("    storage: file_storage"), 1)

    def test_distinct_ids(self):
        s=p.config(distinct_ids=True)
        self.assertIn("queue_batch/1:", s)
        self.assertIn("queue_batch/2:", s)
        self.assertEqual(s.count("    storage: file_storage"), 2)

    def test_no_storage(self):
        self.assertNotIn("file_storage", p.config(storage=False))

    def test_red_match_strict(self):
        self.assertEqual(p.classify("shared_storage",1,
            'failed to start "queue_batch" processor: timeout',False), "RED_REPRODUCED")
        self.assertEqual(p.classify("shared_storage",1,
            'failed to pull Docker image',False), "INCONCLUSIVE_NO_MATCH")

    def test_control_ready_strict(self):
        self.assertEqual(p.classify("single_storage",-9,p.READY,True), "CONTROL_READY")
        self.assertEqual(p.classify("single_storage",1,"failed",False), "CONTROL_NOT_READY")

if __name__ == "__main__":
    unittest.main()
