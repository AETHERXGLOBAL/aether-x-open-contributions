# Original reproducible test candidates

The original OpenTelemetry and Redis candidates are retained byte-for-byte from their source-pinned internal native test evidence, not PRs incorporated by upstream. Additional experiments below are separately scoped and must not be interpreted as upstream-qualified or merged tests.

| Candidate | Source and documented limits | SHA-256 |
|---|---|---|
| [OpenTelemetry #15966](opentelemetry/README.md) | Go Graph.Build warning integration, one controlled mutation, not full Collector startup | `45221c859ecc9da6b190fcef009d66cde64fc1020020d6ddf5813d85bc81685b` |
| [Redis #15930](redis/15930/README.md) | Native Tcl baseline RED vs candidate GREEN; uses DEBUG LOADAOF, non-production only | `bbe6b2ef4970a954f9fb095e818fafdb0f6ffdeb8a6cf482eadafc56c6687f62` |
| [Pydantic #14230](pydantic/14230/README.md) | Local 2.13.5 reproduction plus exact upstream main RED→GREEN qualification on Python 3.10–3.14; 1,381 native cases per runtime, 9 before/6 after (3 new native regressions fixed; 6 existing source failures retained; 0 new); unassigned, internal Draft only | `e4cb62ecd0ad086600202845998568f8ccb92cdf68431ff51ddbd25d45745ade` |

See [historical SHA256SUMS](SHA256SUMS.txt) for the original frozen candidates and each source-specific README for later dated experiments. The Pydantic candidate's SHA-256 is recorded above without modifying the historical checksum snapshot. Independently auditing archive bytes is not the same as independently executing a second runtime.
