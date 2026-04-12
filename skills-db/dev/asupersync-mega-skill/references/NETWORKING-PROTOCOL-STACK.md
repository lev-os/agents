# Networking and Protocol Stack

Asupersync ships a cancel-safe networking stack from raw sockets through application protocols. Every layer participates in structured concurrency.

## Reactor and I/O

### Reactor Backends

Source: `src/runtime/reactor/`

| Backend | Platform | Source |
|---------|----------|--------|
| epoll | Linux | `src/runtime/reactor/epoll.rs` |
| kqueue | macOS/BSD | `src/runtime/reactor/kqueue.rs` |
| Windows | Windows | `src/runtime/reactor/windows.rs` |
| io_uring | Linux 5.1+ | `src/runtime/reactor/io_uring.rs` (feature: `io-uring`) |
| Lab | Testing | `src/runtime/reactor/lab.rs` |

### I/O Driver

Source: `src/runtime/io_driver.rs`

- Registrations are RAII-backed; deregistration treats `NotFound` as already-cleaned
- Token slabs are generation-tagged (blocks stale-token wakeups after reuse)
- Unknown tokens logged instead of panic (diagnostics under fault conditions)
- Oneshot waker semantics: reactor disarms interest after each readiness event, stream re-arms explicitly

### epoll Specifics

- Edge-triggered and edge-oneshot modes
- Explicit PRIORITY/HUP/ERROR propagation
- Stale fd/token cleanup on `ENOENT` and closed-fd conditions (including fd-reuse edge cases)

### io_uring Specifics

- Timeout expiry (`ETIME`) handled as timeout, not failure
- Stale completions for deregistered tokens ignored

## TCP

Source: `src/net/tcp/`

- `TcpStream`, `TcpListener`, split reader/writer halves
- Registered with I/O reactor, oneshot waker semantics
- `VirtualTcp` (`src/net/tcp/virtual_tcp.rs`): fully in-memory TCP for lab tests, same API, deterministic

## UDP

Source: `src/net/udp.rs`

Async UDP with send/receive and cancellation safety.

## Unix Sockets

Source: `src/net/unix/`

Unix domain sockets with stream and datagram support.

## DNS

Source: `src/net/dns/`

Async DNS resolution with address-family selection.

## WebSocket

Source: `src/net/websocket/`

RFC 6455: handshake, binary/text frames, ping/pong, close frames with status codes. Split reader/writer for concurrent send/receive within same region.

## HTTP/1.1

Source: `src/http/h1/`

- Chunked transfer encoding
- Connection keep-alive
- Streaming request/response bodies
- Integration with connection pool

## HTTP/2

Source: `src/http/h2/`

- Frame parsing
- HPACK header compression
- Flow control
- Stream multiplexing over single connection
- Integration with connection pool

## Connection Pooling

Source: `src/http/pool.rs`

Shared connection pool for HTTP/1.1 and HTTP/2 with keep-alive management.

## Response Compression

Source: `src/http/compress.rs`

Optional response compression middleware.

## TLS

Source: `src/tls/`

Wraps `rustls` for TLS 1.2/1.3:

| Feature Flag | Root Certs |
|-------------|------------|
| `tls` | Bring your own |
| `tls-native-roots` | OS trust store |
| `tls-webpki-roots` | Mozilla WebPKI bundle |

## QUIC and HTTP/3

Source: `src/net/quic_core/`, `src/net/quic_native/`, `src/http/h3_native.rs`

In progress. Native feature surfaces exposed via `quic`/`http3` features.

## Transport Layer

Source: `src/transport/`

Low-level delivery behavior above raw sockets and below protocol clients:

| Module | Purpose |
|--------|---------|
| `router.rs` | Endpoint health, routing state, atomics, RAII connection guards |
| `aggregator.rs` | Multipath symbol intake, dedup windows, reorder handling |
| `sink.rs` | Queued waiters with atomic flags, `Waker::will_wake` dedup |
| `stream.rs` | Queued waiters with explicit wakeup bookkeeping |

Shared channel close paths wake both send and receive waiters (no stranded operations).

## Bytes

Source: `src/bytes/`

Zero-copy buffer types: `Bytes`, `BytesMut`, `Buf`, `BufMut`. Compatible API surface for buffer management across the stack.

## Codec

Source: `src/codec/`

Encoding/decoding primitives and framing layer. Used by HTTP, WebSocket, gRPC, and database wire protocols.

## gRPC

Source: `src/grpc/`

Native gRPC client/server with health checks. `CallContext::with_cx(...)` for capability-scoped handlers.

## Web Framework

Source: `src/web/`

Router, extractors, middleware, request-region isolation. Request-as-region pattern for structured concurrency per request.

## Service Layer

Source: `src/service/`

`ServiceBuilder` with middleware: timeout, load_shed, concurrency_limit, rate_limit, retry. Optional Tower adapter via `tower` feature.

## Cancel Safety Across the Stack

All networking layers respect:
- Region budgets for reads/writes
- Cancellation drains connections cleanly
- Lab runtime substitutes virtual TCP for deterministic network testing
- Two-phase semantics where applicable (send permits on channels)
