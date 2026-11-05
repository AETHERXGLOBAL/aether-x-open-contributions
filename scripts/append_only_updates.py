"""Reviewable append-only participation records; new links are never auto-qualified.

An editable manifest hash is only consistency evidence. Human source-identity
verification and Founder approval of the exact PR remain separate controls.
"""
import datetime
import hashlib
import json
import pathlib
import re

from integrity_runtime import require

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = "data/updates/manifest.json"
THREAD = re.compile(r"https://github\.com/([^/]+/[^/]+)/(issues|pull)/(\d+)")
SOURCE = re.compile(
    r"https://github\.com/([^/]+/[^/]+)/(issues|pull)/(\d+)"
    r"(?:#(?:issuecomment-\d+|discussion_r\d+))?"
)
EXPECTED_FIELDS = {"source_url", "project", "author", "kind", "thread_url", "observed_state"}

def read_unique_json(raw):
    def unique(pairs):
        result = {}
        for k, v in pairs:
            require(k not in result, ("duplicate JSON object key", k))
            result[k] = v
        return result
    return json.loads(raw, object_pairs_hook=unique)

def read_bounded_bytes(root, name):
    """Read a regular file inside an explicitly authorized root; never follow symlinks.

    POSIX uses descriptor-relative O_NOFOLLOW walks to resist path-swap races.
    Other platforms use a checked path fallback; see the documented TOCTOU limit.
    """
    import contextlib
    import os
    import stat

    require(isinstance(name, str) and bool(name) and "\x00" not in name
            and "\\" not in name, "unsafe JSON input path")
    relative = pathlib.PurePosixPath(name)
    require(bool(relative.parts) and not relative.is_absolute()
            and ".." not in relative.parts and relative.as_posix() == name
            and not pathlib.PureWindowsPath(name).drive,
            "unsafe JSON input path")
    root = pathlib.Path(root)
    require(root.is_dir() and not root.is_symlink(), "unsafe JSON root")

    nofollow = getattr(os, "O_NOFOLLOW", 0)
    directory_only = getattr(os, "O_DIRECTORY", 0)
    if nofollow and directory_only and os.open in getattr(os, "supports_dir_fd", ()):
        flags = os.O_RDONLY | nofollow | getattr(os, "O_CLOEXEC", 0)
        try:
            with contextlib.ExitStack() as opened:
                parent = os.open(root, flags | directory_only)
                opened.callback(os.close, parent)
                require(stat.S_ISDIR(os.fstat(parent).st_mode), "unsafe JSON root")
                for index, part in enumerate(relative.parts):
                    last = index == len(relative.parts) - 1
                    fd = os.open(part, flags if last else flags | directory_only,
                                 dir_fd=parent)
                    opened.callback(os.close, fd)
                    mode = os.fstat(fd).st_mode
                    require(stat.S_ISREG(mode) if last else stat.S_ISDIR(mode),
                            "non-regular JSON input or directory")
                    parent = fd
                with os.fdopen(os.dup(parent), "rb") as stream:
                    return stream.read()
        except (OSError, ValueError) as exc:
            raise AssertionError("unsafe or unavailable JSON input path") from exc

    # Windows/other fallback: reject links and junctions on every component,
    # verify confinement and type before opening. Not atomic against a hostile
    # concurrent path swap; use immutable, trusted checkouts on such platforms.
    current = root
    for index, part in enumerate(relative.parts):
        current = current / part
        linked = current.is_symlink() or (
            hasattr(current, "is_junction") and current.is_junction()
        )
        require(not linked, "linked JSON input path")
        require(current.is_file() if index == len(relative.parts) - 1
                else current.is_dir(), "missing or non-regular JSON input")
    require(current.resolve().is_relative_to(root.resolve()),
            "JSON input escaped authorized root")
    try:
        return current.read_bytes()
    except (OSError, ValueError) as exc:
        raise AssertionError("unsafe or unavailable JSON input path") from exc


def read_bounded_json(root, name):
    """Apply strict duplicate-key rejection to confined original JSON bytes."""
    return read_unique_json(read_bounded_bytes(root, name))


def verify_date(value):
    require(isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value), "invalid date")
    require(datetime.date.fromisoformat(value) > datetime.date(2026, 11, 4),
            "historical snapshots must not be rewritten")
    return True

def read_updates(root=None):
    root = pathlib.Path(root or ROOT)
    manifest = read_bounded_json(root, MANIFEST)
    require(set(manifest) == {"schema_version", "baseline_as_of", "snapshots", "notice"},
            "manifest schema drift")
    require(manifest["schema_version"] == "AX-APPEND-ONLY-PARTICIPATION-MANIFEST-v1")
    require(manifest["baseline_as_of"] == "2026-11-04")
    require(isinstance(manifest["snapshots"], list))
    result, paths, dates = [], [], []
    for item in manifest["snapshots"]:
        require(isinstance(item, dict) and set(item) == {"date", "path", "sha256"})
        date = item["date"]
        verify_date(date)
        path = "data/updates/" + date + ".json"
        require(item["path"] == path, "snapshot path must be canonical")
        require(re.fullmatch(r"[0-9a-f]{64}", item["sha256"]) is not None)
        require(date not in dates, "duplicate dated snapshot")
        require(not dates or date > dates[-1], "snapshot dates must increase")
        file = root / path
        require(file.is_file() and not file.is_symlink(), "missing or linked snapshot")
        raw = read_bounded_bytes(root, path)
        require(hashlib.sha256(raw).hexdigest() == item["sha256"],
                ("snapshot SHA-256 differs", date))
        snapshot = read_unique_json(raw)
        require(isinstance(snapshot, dict) and set(snapshot) ==
                {"schema_version", "snapshot_date", "source_account", "participations"},
                "snapshot schema drift")
        require(snapshot["schema_version"] == "AX-UNQUALIFIED-PARTICIPATION-v1")
        require(snapshot["snapshot_date"] == date)
        require(snapshot["source_account"] == "aetherxeg-source")
        require(isinstance(snapshot["participations"], list) and snapshot["participations"],
                "empty snapshot")
        require(len(snapshot["participations"]) <= 10000, "snapshot size limit")
        for entry in snapshot["participations"]:
            require(isinstance(entry, dict) and set(entry) == EXPECTED_FIELDS)
            require(entry["author"] == "aetherxeg-source", "wrong declared author")
            require(entry["kind"] in ("comment", "authored_issue", "authored_pull_request"),
                    "unqualified participation kind")
            require(entry["observed_state"] in ("open", "closed", "unknown"),
                    "invalid observed state")
            m = SOURCE.fullmatch(entry["source_url"])
            t = THREAD.fullmatch(entry["thread_url"])
            require(m is not None and t is not None, "non-canonical GitHub source link")
            require(entry["project"] == m.group(1) == t.group(1), "project mismatch")
            require(m.group(2) == t.group(2) and m.group(3) == t.group(3),
                    "source/thread identity mismatch")
            require(entry["kind"] != "comment" or "#" in entry["source_url"],
                    "comment requires exact authored comment permalink")
            require(entry["kind"] == "comment" or "#" not in entry["source_url"],
                    "authored discussion requires direct PR/issue URL")
            require(entry["kind"] != "authored_issue" or m.group(2) == "issues")
            require(entry["kind"] != "authored_pull_request" or m.group(2) == "pull")
            result.append(dict(entry, snapshot_date=date))
        dates.append(date)
        paths.append(path)
    disk_files = set()
    directory = root / "data/updates"
    for file in directory.iterdir():
        require(file.is_file() and not file.is_symlink(), "unexpected updates directory entry")
        if file.name != "manifest.json":
            require(file.suffix == ".json" and re.fullmatch(r"\d{4}-\d{2}-\d{2}\.json", file.name),
                    "unregistered update file")
            disk_files.add("data/updates/" + file.name)
    require(set(paths) == disk_files, "unmanifested or missing update snapshot")
    require(len({r["source_url"] for r in result}) == len(result),
            "duplicate participation across dated snapshots")
    return result, paths, dates

if __name__ == "__main__":
    participation, paths, dates = read_updates()
    print("APPEND_ONLY_UPDATES=PASS snapshots={} unqualified_sources={}".format(
        len(dates), len(participation)))
