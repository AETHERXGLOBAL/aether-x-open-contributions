# Redis Streams AOF consumer recovery — PR #15930

- Upstream: https://github.com/redis/redis/pull/15930
- Original source: [w07-aof-replay.tcl](w07-aof-replay.tcl), SHA-256 `bbe6b2ef4970a954f9fb095e818fafdb0f6ffdeb8a6cf482eadafc56c6687f62`.
- Pinned baseline: `558ef8fafb508adb276fb838442f7f202fc1d7e6`; candidate PR HEAD: `d32ad60a779540b18beae37954b8d6b2e3e9b830`.
- Founder-run native Tcl baseline two expected RED and positive-control PASS; candidate all three PASS. Original archive source/checksums independently byte-verified; not independently rerun in a second runtime.
- [Public engineering evidence](https://github.com/redis/redis/pull/15930#issuecomment-6605978538).

**Safety:** Requires Redis's own Tcl development test harness and invokes `DEBUG LOADAOF`. **NEVER run against a production Redis instance.** Integrate only into a disposable test checkout, under `tests/unit/type/w07-aof-replay.tcl` after source pin verification. Upstream incorporation or merge not established.
