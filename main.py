#!/usr/bin/env python3
"""RSSPrune - Fetches feeds, filters unread items and exports a clean digest to a file.

A standalone script that does one thing and does it well.
"""

import argparse
import json
import sys
import time
from pathlib import Path

from lib.logger import build_logger

log = build_logger("rssprune")


def collect_inputs(path=None):
 if path:
 with open(path, "r", encoding="utf-8") as fh:
 return json.load(fh)
 return {"items": ["alpha", "beta", "gamma"]}


def transform(items):
 """Apply the core rssprune transformation."""
 out = []
 for item in items:
 out.append({
 "value": item,
 "length": len(str(item)),
 "processed_at": int(time.time()),
 })
 return out


def render(results):
 lines = []
 for r in results:
 lines.append(f"{r['value']:>12} len={r['length']} at={r['processed_at']}")
 return "\n".join(lines)


def main(argv=None):
 parser = argparse.ArgumentParser(description="RSSPrune")
 parser.add_argument("input", nargs="?", help="input JSON file")
 parser.add_argument("-o", "--output", help="write output to a file")
 parser.add_argument("-v", "--verbose", action="store_true")
 args = parser.parse_args(argv)

 data = collect_inputs(args.input)
 results = transform(data["items"])
 text = render(results)

 if args.output:
 Path(args.output).write_text(text, encoding="utf-8")
 else:
 print(text)

 if args.verbose:
 print(f"\n{len(results)} items processed", file=sys.stderr)
 log.info(f"processed {len(results)} items")
 return 0


if __name__ == "__main__":
 sys.exit(main())