#!/usr/bin/env python3
"""Read lev.now feedback answers from the user's browser storage on disk.

The feedback component saves answers to localStorage under
`lev-now-feedback-<pageId>`. Chromium-family browsers persist localStorage in a
per-profile LevelDB, so the answers can be collected without a server, a
debugging port, or the user pasting JSON back into a terminal.

Usage:
  feedback-answers.py SPEC.json [--wait] [--settle 20] [--interval 5] [--timeout 3600]
  feedback-answers.py --page-id PAGE_ID

With --wait, exits 0 once every feedback item in the spec has a choice or note
and the stored answers have not changed for --settle seconds; exits 2 on
timeout after printing the partial answers. Chromium commits localStorage to
disk a few seconds after a change, so a fresh click can take ~5 s to appear.
"""

import argparse
import glob
import json
import os
import struct
import sys
import time

BROWSER_ROOTS = [
    "~/Library/Application Support/BraveSoftware/Brave-Browser",
    "~/Library/Application Support/Google/Chrome",
    "~/Library/Application Support/Chromium",
    "~/.config/BraveSoftware/Brave-Browser",
    "~/.config/google-chrome",
    "~/.config/chromium",
]
KEY_PREFIX = "lev-now-feedback-"


def varint(buf, i):
    result = shift = 0
    while True:
        byte = buf[i]
        i += 1
        result |= (byte & 0x7F) << shift
        shift += 7
        if byte < 0x80:
            return result, i


def snappy_decompress(buf):
    length, i = varint(buf, 0)
    out = bytearray()
    while i < len(buf):
        tag = buf[i]
        i += 1
        kind = tag & 3
        if kind == 0:
            n = tag >> 2
            if n >= 60:
                extra = n - 59
                n = int.from_bytes(buf[i:i + extra], "little")
                i += extra
            n += 1
            out += buf[i:i + n]
            i += n
            continue
        if kind == 1:
            n = ((tag >> 2) & 7) + 4
            offset = ((tag >> 5) << 8) | buf[i]
            i += 1
        elif kind == 2:
            n = (tag >> 2) + 1
            offset = int.from_bytes(buf[i:i + 2], "little")
            i += 2
        else:
            n = (tag >> 2) + 1
            offset = int.from_bytes(buf[i:i + 4], "little")
            i += 4
        start = len(out) - offset
        if offset >= n:
            out += out[start:start + n]
        else:  # overlapping copy repeats the bytes it is producing
            for j in range(n):
                out.append(out[start + j])
    if len(out) != length:
        raise ValueError("snappy length mismatch")
    return bytes(out)


def log_entries(data):
    """Yield (sequence, key, value-or-None) from a LevelDB write-ahead log."""
    records, pending, pos, block = [], b"", 0, 32768
    while pos + 7 <= len(data):
        left = block - pos % block
        if left < 7:
            pos += left
            continue
        length, kind = struct.unpack_from("<HB", data, pos + 4)
        chunk = data[pos + 7:pos + 7 + length]
        pos += 7 + length
        if kind == 1:
            records.append(chunk)
        elif kind == 2:
            pending = chunk
        elif kind == 3:
            pending += chunk
        elif kind == 4:
            records.append(pending + chunk)
            pending = b""
    for record in records:
        try:
            seq = struct.unpack_from("<Q", record, 0)[0]
            i = 12
            while i < len(record):
                tag = record[i]
                i += 1
                klen, i = varint(record, i)
                key = record[i:i + klen]
                i += klen
                value = None
                if tag == 1:
                    vlen, i = varint(record, i)
                    value = record[i:i + vlen]
                    i += vlen
                yield seq, key, value
                seq += 1
        except (IndexError, struct.error):
            continue  # torn tail record while the browser is writing


def block_at(data, handle_buf, i):
    offset, i = varint(handle_buf, i)
    size, i = varint(handle_buf, i)
    raw = data[offset:offset + size]
    return (snappy_decompress(raw) if data[offset + size] == 1 else raw), i


def block_entries(block):
    restarts = struct.unpack_from("<I", block, len(block) - 4)[0]
    end = len(block) - 4 - 4 * restarts
    i, key = 0, b""
    while i < end:
        shared, i = varint(block, i)
        unshared, i = varint(block, i)
        vlen, i = varint(block, i)
        key = key[:shared] + block[i:i + unshared]
        i += unshared
        yield key, block[i:i + vlen]
        i += vlen


def table_entries(data):
    """Yield (sequence, key, value-or-None) from a LevelDB .ldb table."""
    footer = data[-48:]
    _, i = varint(footer, varint(footer, 0)[1])  # skip metaindex handle
    index, _ = block_at(data, footer, i)
    for _, handle in block_entries(index):
        block, _ = block_at(data, handle, 0)
        for internal_key, value in block_entries(block):
            trailer = struct.unpack_from("<Q", internal_key, len(internal_key) - 8)[0]
            yield trailer >> 8, internal_key[:-8], (value if trailer & 0xFF == 1 else None)


def storage_key_matches(key, name):
    return key.endswith(b"\x00\x01" + name.encode("latin-1")) or key.endswith(
        b"\x00\x00" + name.encode("utf-16-le"))


def decode_value(value):
    if value is None:
        return None
    return value[1:].decode("latin-1") if value[0] == 1 else value[1:].decode("utf-16-le")


_TABLES = {}  # .ldb files never change once written: (path, size, mtime) -> feedback entries


def feedback_entries(path):
    stat = os.stat(path)
    ident = (path, stat.st_size, stat.st_mtime)
    if ident in _TABLES:
        return _TABLES[ident]
    data = open(path, "rb").read()
    markers = (KEY_PREFIX.encode("latin-1"), KEY_PREFIX.encode("utf-16-le"))
    entries = [entry for entry in (table_entries(data) if path.endswith(".ldb") else log_entries(data))
               if any(marker in entry[1] for marker in markers)]
    if path.endswith(".ldb"):
        _TABLES[ident] = entries
    return entries


def read_stored(page_id):
    """Return the newest stored answers for page_id across browser profiles."""
    name = KEY_PREFIX + page_id
    best = None  # (mtime, seq, origin, raw, db)
    for root in BROWSER_ROOTS:
        for db in glob.glob(os.path.join(os.path.expanduser(root), "*", "Local Storage", "leveldb")):
            found = None
            for path in glob.glob(os.path.join(db, "*.ldb")) + glob.glob(os.path.join(db, "*.log")):
                try:
                    for seq, key, value in feedback_entries(path):
                        if storage_key_matches(key, name) and (found is None or seq > found[1]):
                            found = (os.path.getmtime(path), seq, key.split(b"\x00")[0][1:].decode("latin-1"), value, db)
                except (OSError, ValueError, IndexError, struct.error):
                    continue
            if found and (best is None or found[0] > best[0]):
                best = found
    if best is None or best[3] is None:
        return None
    raw = decode_value(best[3])
    profile = os.path.relpath(best[4], os.path.expanduser("~"))
    return {"origin": best[2], "profile": profile, "stored": json.loads(raw or "{}")}


def feedback_elements(spec):
    return [e for e in spec.get("elements", {}).values() if e.get("type") == "feedback"]


def collect(spec):
    pages, decided, total = [], 0, 0
    for element in feedback_elements(spec):
        props = element["props"]
        found = read_stored(props["pageId"])
        stored = found["stored"] if found else {}
        answers = []
        for item in props["items"]:
            entry = stored.get(item["id"], {})
            note = entry.get("note") or "\n".join(filter(None, [entry.get("other"), entry.get("notes")])) or None
            choice = entry.get("choice")
            option = item["options"][choice] if isinstance(choice, int) and choice < len(item["options"]) else None
            answer = {"id": item["id"], "title": item["title"], "choice": option["label"] if option else None,
                      "recommended": bool(option and option.get("recommended")) if option else None, "note": note}
            answers.append(answer)
            total += 1
            decided += bool(option or note)
        pages.append({"pageId": props["pageId"], "source": found and {k: found[k] for k in ("origin", "profile")},
                      "answers": answers})
    return {"decided": decided, "total": total, "complete": total > 0 and decided == total, "pages": pages}


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("spec", nargs="?", help="RenderSpec JSON containing feedback elements")
    parser.add_argument("--page-id", help="print the raw stored answers for one pageId")
    parser.add_argument("--wait", action="store_true", help="poll until every item is answered and settled")
    parser.add_argument("--settle", type=float, default=20, help="seconds answers must stay unchanged (default 20)")
    parser.add_argument("--interval", type=float, default=5, help="poll interval in seconds (default 5)")
    parser.add_argument("--timeout", type=float, default=3600, help="give up after this many seconds (default 3600)")
    args = parser.parse_args()
    if args.page_id:
        print(json.dumps(read_stored(args.page_id), indent=2, ensure_ascii=False))
        return 0
    if not args.spec:
        parser.error("SPEC.json or --page-id is required")
    spec = json.load(open(args.spec))
    if not feedback_elements(spec):
        parser.error(f"{args.spec} has no feedback element")
    result = collect(spec)
    if args.wait:
        deadline, last, stable_since = time.monotonic() + args.timeout, None, time.monotonic()
        while True:
            snapshot = json.dumps(result["pages"], sort_keys=True)
            if snapshot != last:
                last, stable_since = snapshot, time.monotonic()
            if result["complete"] and time.monotonic() - stable_since >= args.settle:
                break
            if time.monotonic() >= deadline:
                print(json.dumps(result, indent=2, ensure_ascii=False))
                return 2
            time.sleep(args.interval)
            result = collect(spec)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
