#!/usr/bin/env python3
"""Isolated release-image reproduction for OTel #16398; never a patch GREEN test."""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

IMAGE = "otel/opentelemetry-collector-contrib:0.165.0"
BASE = Path("runtime_evidence")
READY = "Everything is ready. Begin running and processing data."
FAILURE = re.compile(r'failed to start ["\x27]queue_batch["\x27] processor: timeout', re.I)


def config(pipelines=2, storage=True, distinct_ids=False):
    lines = []
    if storage:
        lines += ["extensions:", "  file_storage:", "    directory: /tmp/otelcol-storage", "    create_directory: true", ""]
    lines += ["receivers:", "  nop:", "", "processors:"]
    names = [f"queue_batch/{i+1}" if distinct_ids else "queue_batch" for i in range(pipelines)]
    for n in dict.fromkeys(names):
        lines += [f"  {n}:"]
        if storage:
            lines += ["    storage: file_storage"]
    lines += ["", "exporters:", "  nop:", "", "service:"]
    if storage:
        lines += ["  extensions: [file_storage]"]
    lines += ["  pipelines:"]
    for i, n in enumerate(names, 1):
        lines += [f"    logs/{i}:", "      receivers: [nop]", f"      processors: [{n}]", "      exporters: [nop]"]
    return "\n".join(lines) + "\n"


def classify(name, code, output, timed_out):
    if name == "shared_storage":
        return "RED_REPRODUCED" if code not in (None, 0) and FAILURE.search(output) else "INCONCLUSIVE_NO_MATCH"
    return "CONTROL_READY" if timed_out and READY in output else "CONTROL_NOT_READY"


def run_case(name, yaml, seconds=30):
    container = f"axg-otel-16398-{name.replace('_','-')}-{os.environ.get('GITHUB_RUN_ID','local')}"
    cmd = ["docker", "run", "--rm", "--name", container, "--network", "none",
           "--cap-drop", "ALL", "--pids-limit", "128", "--memory", "768m",
           "--tmpfs", "/tmp:rw,uid=10001,gid=10001", IMAGE, "--config", "yaml:" + yaml]
    (BASE / f"{name}.yaml").write_text(yaml)
    start = time.monotonic()
    out = err = ""
    timeout = False
    code = None
    try:
        proc = subprocess.Popen(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            out, err = proc.communicate(timeout=seconds)
        except subprocess.TimeoutExpired:
            timeout = True
            proc.kill()
            out, err = proc.communicate(timeout=10)
        code = proc.returncode
    finally:
        subprocess.run(["docker", "rm", "-f", container], timeout=15,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    (BASE / f"{name}.stdout.log").write_text(out)
    (BASE / f"{name}.stderr.log").write_text(err)
    return {"scenario": name, "exit_code": code, "timed_out": timeout,
            "seconds": round(time.monotonic()-start, 2),
            "outcome": classify(name, code, out+"\n"+err, timeout)}


def main():
    BASE.mkdir(exist_ok=True)
    result = {"mission":"AXG-OTEL-QUEUE-BATCH-PERSISTENCE-R2",
              "source_scope":"Docker release image 0.165.0; NOT pinned-HEAD source build",
              "image": IMAGE, "patch_tested": False, "scenarios":[]}
    cases = [("shared_storage", config()),
             ("single_storage", config(pipelines=1)),
             ("shared_memory", config(storage=False)),
             ("distinct_storage", config(distinct_ids=True))]
    try:
        for name, yaml in cases:
            print("RUN_CASE", name, flush=True)
            item = run_case(name, yaml)
            result["scenarios"].append(item)
            print(json.dumps(item, sort_keys=True), flush=True)
    finally:
        (BASE / "runtime_results.json").write_text(json.dumps(result, sort_keys=True, indent=2)+"\n")
    outcomes = {i["scenario"]: i["outcome"] for i in result["scenarios"]}
    passed = outcomes.get("shared_storage") == "RED_REPRODUCED" and all(
        outcomes.get(n) == "CONTROL_READY" for n in
        ("single_storage", "shared_memory", "distinct_storage"))
    print("CLASSIFICATION:", "RED_WITH_CONTROLS" if passed else "INCONCLUSIVE", flush=True)
    return 0 if passed else 1

if __name__ == "__main__":
    sys.exit(main())
