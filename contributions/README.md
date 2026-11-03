# Public contributions by upstream project

Each link identifies a real public GitHub discussion or author-submitted pull request. **A comment is not evidence of a merged patch.**

## aws/aws-cdk (1)

- [NAT setup shell false-success report](https://github.com/aws/aws-cdk/pull/39581#issuecomment-6543247473) — Discussion

## aws/aws-cli (1)

- [S3 transfer failures must not be reported as success](https://github.com/aws/aws-cli/issues/10743#issuecomment-6518880900) — Discussion

## aws/aws-lc (1)

- [ChaCha20-Poly1305 cumulative counter-wrap guard: proposed reject-without-state-change regression across encrypt/decrypt streaming updates, output sentinel, AAD-only path and authentication tag equivalence.](https://github.com/aws/aws-lc/pull/3722#issuecomment-6543610074) — Discussion

## aws/aws-sdk-go-v2 (1)

- [DynamoDB nil set union serialization edge cases](https://github.com/aws/aws-sdk-go-v2/issues/3612#issuecomment-6519020447) — Discussion

## cloudflare/agents (1)

- [Stale orphan recovery replay-order invariant: a reprocessed older continuation S1 must not overwrite newer persisted S2 parts on the same assistant leaf; suggests monotonic recovery/generation-watermark regression.](https://github.com/cloudflare/agents/pull/2781#issuecomment-6543532180) — Discussion

## cloudflare/workers-sdk (3)

- [Ambiguous container deploy retry and idempotency](https://github.com/cloudflare/workers-sdk/issues/16596#issuecomment-6518556026) — Discussion
- [Cloudflare Workers Access Managed OAuth: guarded 401 resource-metadata detection, 302 redirect hostname spoofing boundaries and eight-case isolated RED/GREEN predicate contract](https://github.com/cloudflare/workers-sdk/issues/16604#issuecomment-6552006588) — Discussion
- [Chrome child process inherits all Miniflare/Wrangler environment variables, including potential credentials; request limited environmental propagation and synthetic-secret isolation regression.](https://github.com/cloudflare/workers-sdk/pull/16612#issuecomment-6543096080) — Discussion

## elastic/elasticsearch (1)

- [ES|QL serialized local plan data request breaker reservation cleanup across distributed cancellation and remote transport failure.](https://github.com/elastic/elasticsearch/pull/164141#issuecomment-6542529325) — Discussion

## google/adk-python (1)

- [Google ADK Redis streaming partial events: proposed cross-backend conformance regression verifying last_update_time, list_sessions ordering, complete/partial interleaving and non-persistence of state deltas.](https://github.com/google/adk-python/pull/7902#issuecomment-6543727326) — Discussion

## google/gvisor (6)

- [SO_PEERCRED provenance on AF_UNIX SOCK_SEQPACKET](https://github.com/google/gvisor/issues/16694#issuecomment-6518805372) — Discussion
- [CUDA GPU-active task discovery completeness](https://github.com/google/gvisor/issues/16723#issuecomment-6519314174) — Discussion
- [Existing ICMP broadcast/multicast test expectation conflict](https://github.com/google/gvisor/pull/16721#issuecomment-6519482798) — Discussion
- [StateFile SaveLocked crash consistency: file/directory sync, power-loss semantics and inode identity](https://github.com/google/gvisor/issues/16786#issuecomment-6551510566) — Discussion
- [IPv6 multicast interface regression test currently conflates pre-existing address-bound NIC checks with new SO_BINDTODEVICE guard; propose wildcard/unbound differential syscall test.](https://github.com/google/gvisor/pull/16774#issuecomment-6542642860) — Discussion
- [TCP wildcard port reservation identity across checkpoint/restore and dual-stack IPv4-mapped connection; proposed regression for release-once and old snapshot compatibility boundary.](https://github.com/google/gvisor/pull/16775#issuecomment-6543159987) — Discussion

## grafana/grafana (1)

- [Grafana GitHub App JWT clock drift: proposed verifier-side RS256 signature and skew acceptance matrix test, expiration precision, documented +60 second tolerance limits.](https://github.com/grafana/grafana/pull/136699#issuecomment-6543813718) — Discussion

## GuillaumeFalourd/useful-actions (2)

- [ExecSurface GitHub Action directory entry and runnable example](https://github.com/GuillaumeFalourd/useful-actions/pull/1534) — AETHER-authored PR · merged
- [ExecSurface Action version update](https://github.com/GuillaumeFalourd/useful-actions/pull/1536) — AETHER-authored PR · merged

## microsoft/TypeScript (2)

- [Differential semantic-equivalence API-surface tests](https://github.com/microsoft/TypeScript/issues/65051#issuecomment-6518847399) — Discussion
- [dirty.SyncMap tombstone resurrection: stale-reference lifecycle safety and targeted regression probe](https://github.com/microsoft/TypeScript/pull/65072#issuecomment-6551598550) — Discussion

## microsoft/vscode (5)

- [Partial-clone capability cache invalidation](https://github.com/microsoft/vscode/pull/345133#issuecomment-6519188199) — Discussion
- [TreeView visual and internal selection synchronization](https://github.com/microsoft/vscode/issues/345141#issuecomment-6519405462) — Discussion
- [Decoupling local decoration request cancellation from outstanding RPC reply retention for a non-cooperative extension provider.](https://github.com/microsoft/vscode/pull/345347#issuecomment-6542473235) — Discussion
- [VS Code agent path-token OOM: proposed bounded cache retention across customization-index rebuilds for oversized unresolved tokens, with positive-control path resolution and negative-cache invalidation.](https://github.com/microsoft/vscode/issues/345353#issuecomment-6543635730) — Discussion
- [Public technical correction of earlier hypothesis](https://github.com/microsoft/vscode/issues/345353#issuecomment-6603460715) — Discussion

## NVIDIA/aicr (1)

- [End-to-end binary attestation read-verify-bundle byte identity under source-path replacement and read/cancellation failure; separate FIFO and cancelled-context behavioral regression.](https://github.com/NVIDIA/aicr/pull/3539#issuecomment-6543586434) — Discussion

## NVIDIA/TensorRT-LLM (2)

- [Streaming n>1: decoded text vs token IDs](https://github.com/NVIDIA/TensorRT-LLM/issues/21309#issuecomment-6518466734) — Discussion
- [Unified-memory budget vs container cgroup limits](https://github.com/NVIDIA/TensorRT-LLM/issues/21317#issuecomment-6519238035) — Discussion

## open-telemetry/opentelemetry-collector (3)

- [Batching isolation: negative integration-test boundaries](https://github.com/open-telemetry/opentelemetry-collector/pull/15966#issuecomment-6518083853) — Discussion
- [CA reload TLS policy preservation: tls.Config.Clone and security regression coverage](https://github.com/open-telemetry/opentelemetry-collector/issues/16273#issuecomment-6551564143) — Discussion
- [Source-pinned Graph.Build native PASS and mutation test](https://github.com/open-telemetry/opentelemetry-collector/pull/15966#issuecomment-6607382404) — Discussion

## openai/openai-python (1)

- [Python SDK WebSocket sync/async entry guards: failure-path regression for clear_connection callback raising while handling original exception, preserving primary error and ensuring close attempted.](https://github.com/openai/openai-python/pull/4219#issuecomment-6543667481) — Discussion

## ossf/scorecard (1)

- [Trusted base-source pull_request_target negative control](https://github.com/ossf/scorecard/issues/5379#issuecomment-6518696955) — Discussion

## pytorch/pytorch (3)

- [Reentrant autocast per-invocation state restoration](https://github.com/pytorch/pytorch/issues/202706#issuecomment-6519082840) — Discussion
- [AOTAutograd detached nonzero-offset partial-slice mutation: missing base version bump causes silently wrong gradient; executed CPU regression with positive/negative controls](https://github.com/pytorch/pytorch/issues/202806#issuecomment-6551875732) — Discussion
- [Deterministic Python GIL progress during THPStorage_dealloc: test-owned native DataPtr deleter with handshake and bounded timeout, exactly-once release, shared-memory cleanup, and callback GIL re-acquisition safety.](https://github.com/pytorch/pytorch/pull/202881#issuecomment-6543691954) — Discussion

## redis/node-redis (2)

- [Node-Redis read-only Lua scripts: live Redis ACL integration proposal covering NOSCRIPT cold-cache EVAL_RO fallback, cached EVALSHA_RO, MULTI/EXEC command selection, write prohibition and correctly authorized writable control.](https://github.com/redis/node-redis/pull/3564#issuecomment-6543755329) — Discussion
- [Redis ACL key-pattern isolation proposal](https://github.com/redis/node-redis/pull/3567#issuecomment-6550671199) — Discussion

## redis/redis (3)

- [Expiry progress with BGSAVE and delayed rehashing](https://github.com/redis/redis/pull/16112#issuecomment-6518953883) — Discussion
- [Atomic Slot Migration write acknowledgment safety: post-grant cancellation fence and protocol test boundaries](https://github.com/redis/redis/issues/16130#issuecomment-6551625949) — Discussion
- [Streams AOF source-pinned RED to GREEN evidence](https://github.com/redis/redis/pull/15930#issuecomment-6605978538) — Discussion

## sbilly/awesome-security (1)

- [ExecSurface directory listing proposal, not merged](https://github.com/sbilly/awesome-security/pull/747) — AETHER-authored PR · closed without merge

[Back to portfolio](../README.md)
