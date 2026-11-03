# Original reproducible test candidates

These are original AETHER test sources retained byte-for-byte from their source-pinned internal native test evidence, not PRs incorporated by upstream.

| Candidate | Source and documented limits | SHA-256 |
|---|---|---|
| [OpenTelemetry #15966](opentelemetry/README.md) | Go Graph.Build warning integration, one controlled mutation, not full Collector startup | `45221c859ecc9da6b190fcef009d66cde64fc1020020d6ddf5813d85bc81685b` |
| [Redis #15930](redis/15930/README.md) | Native Tcl baseline RED vs candidate GREEN; uses DEBUG LOADAOF, non-production only | `bbe6b2ef4970a954f9fb095e818fafdb0f6ffdeb8a6cf482eadafc56c6687f62` |

See [SHA256SUMS](SHA256SUMS.txt) and source-specific README files. Independently auditing archive bytes is not the same as independently executing a second runtime.
