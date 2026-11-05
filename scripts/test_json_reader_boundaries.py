"""F03-SEC-03: exercise actual JSON reader modules at the file-system boundary.

RED/GREEN adversarial fixtures; all writes remain in temporary roots.
"""
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import validate_institutional_register as register_module
import verify_status_evidence as evidence_module
import verify_nvidia_2026_11_05 as nvidia_module


READERS = (
    ("register", register_module),
    ("dated_status", evidence_module),
    ("nvidia", nvidia_module),
)
VALID = b'{"valid":{"nested":[1,2,3]},"identity":"in-root"}'


class JsonReaderBoundaryTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.workspace = pathlib.Path(directory.name)
        self.root = self.workspace / "approved"
        self.root.mkdir()
        self.other_root = self.workspace / "other"
        self.other_root.mkdir()
        self.external = self.workspace / "outside.json"
        self.external.write_bytes(VALID)
        self.in_root = self.root / "inside" / "valid.json"
        self.in_root.parent.mkdir()
        self.in_root.write_bytes(VALID)
        (self.other_root / "other.json").write_bytes(VALID)

    def readers(self):
        for name, module in READERS:
            with mock.patch.object(module, "ROOT", self.root):
                yield name, module.read

    def assert_rejected(self, relative):
        for name, reader in self.readers():
            with self.subTest(reader=name, input=relative):
                with self.assertRaises(AssertionError):
                    reader(relative)

    def test_positive_in_root_json_for_every_real_reader(self):
        for name, reader in self.readers():
            with self.subTest(reader=name):
                self.assertEqual(reader("inside/valid.json")["identity"], "in-root")

    def test_negative_parent_traversal(self):
        self.assert_rejected("../outside.json")

    def test_negative_absolute_path(self):
        self.assert_rejected(str(self.external))

    def test_negative_symlinked_file(self):
        link = self.root / "linked.json"
        try:
            link.symlink_to(self.external)
        except (NotImplementedError, OSError) as exc:
            self.skipTest("symlink unavailable: " + str(exc))
        self.assert_rejected("linked.json")

    def test_negative_symlinked_parent_directory(self):
        external_dir = self.workspace / "outside-dir"
        external_dir.mkdir()
        (external_dir / "source.json").write_bytes(VALID)
        link = self.root / "linked-dir"
        try:
            link.symlink_to(external_dir, target_is_directory=True)
        except (NotImplementedError, OSError) as exc:
            self.skipTest("symlink unavailable: " + str(exc))
        self.assert_rejected("linked-dir/source.json")

    def test_negative_cross_temporary_root(self):
        self.assert_rejected("../other/other.json")

    def test_noncanonical_input_rejected(self):
        for path in ("./inside/valid.json", "inside//valid.json",
                     "inside\\valid.json", "C:/outside.json"):
            self.assert_rejected(path)

    def test_nested_and_escaped_duplicate_keys_rejected_all_readers(self):
        path = self.root / "inside" / "dup.json"
        for raw in (
            b'{"records":[{"id":1,"id":2}]}',
            b'{"records":[{"id":1,"\\u0069d":2}]}',
        ):
            path.write_bytes(raw)
            for name, reader in self.readers():
                with self.subTest(reader=name, raw=raw):
                    with self.assertRaises(AssertionError):
                        reader("inside/dup.json")

    def test_nvidia_explicit_root_isolated_from_repository_and_sibling(self):
        self.assertEqual(nvidia_module.read("inside/valid.json", root=self.root)["identity"], "in-root")
        with self.assertRaises(AssertionError):
            nvidia_module.read("../other/other.json", root=self.root)
        with self.assertRaises(AssertionError):
            nvidia_module.read(str(self.external), root=self.root)


    @unittest.skipUnless(os.name == "posix" and hasattr(os, "mkfifo"),
                         "FIFO regression requires POSIX")
    def test_fifo_is_rejected_without_blocking_in_subprocess(self):
        """A special file must fail closed before a blocking read; bound the probe."""
        fifo = self.root / "pipe.json"
        os.mkfifo(fifo)
        script = (
            "import pathlib, sys\n"
            "sys.path.insert(0, sys.argv[1])\n"
            "from append_only_updates import read_bounded_json\n"
            "try:\n"
            "    read_bounded_json(pathlib.Path(sys.argv[2]), 'pipe.json')\n"
            "except AssertionError:\n"
            "    print('FIFO_REJECTED')\n"
            "else:\n"
            "    raise AssertionError('FIFO_WAS_ACCEPTED')\n"
        )
        try:
            result = subprocess.run(
                [sys.executable, "-c", script,
                 str(pathlib.Path(__file__).resolve().parent), str(self.root)],
                capture_output=True, text=True, check=False, timeout=2,
            )
        except subprocess.TimeoutExpired:
            self.fail("FIFO read blocked longer than 2 seconds")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("FIFO_REJECTED", result.stdout)

if __name__ == "__main__":
    unittest.main()
