"""Runtime integrity primitives: always enforce, including under python -O."""
import pathlib
import re

SCANNED_EXTENSIONS = frozenset({".md", ".json", ".csv", ".go", ".tcl", ".sh", ".py", ".yml", ".yaml", ".toml", ".txt"})
TOKEN_PATTERN = re.compile(
    r"(?:ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,}|"
    r"AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)"
)

def require(condition, detail="integrity requirement violated"):
    """Never use Python assert for security or release gates."""
    if not condition:
        raise AssertionError(detail)
    return True

def scan_public_secrets(root):
    """Review-safe targeted scan, not a complete DLP or secret attestation."""
    root = pathlib.Path(root)
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SCANNED_EXTENSIONS:
            continue
        require(not path.is_symlink(), ("symlink not allowed in public scan", str(path)))
        text = path.read_text(encoding="utf-8")
        require(TOKEN_PATTERN.search(text) is None, ("possible credential in public file", str(path.relative_to(root))))
    return True
