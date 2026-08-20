"""File watcher for RSSPrune."""

import hashlib
import os
import threading
import time
from pathlib import Path


def file_hash(path):
 digest = hashlib.sha256()
 with open(path, "rb") as fh:
 for block in iter(lambda: fh.read(65536), b""):
 digest.update(block)
 return digest.hexdigest()


class FileWatcher:
 def __init__(self, paths, interval=1.0, recursive=True):
 self.paths = [Path(p) for p in paths]
 self.interval = interval
 self.recursive = recursive
 self._handlers = []
 self._snap = {}
 self._stop = threading.Event()
 self._thread = threading.Thread(target=self._loop, daemon=True)

 def on_change(self, fn):
 self._handlers.append(fn)
 return self

 def start(self):
 self._snap = self._scan()
 self._thread.start()
 return self

 def stop(self):
 self._stop.set()
 self._thread.join(timeout=5)

 def _walk(self):
 for base in self.paths:
 if base.is_file():
 yield base
 elif base.is_dir():
 files = base.rglob("*") if self.recursive else base.glob("*")
 for p in files:
 if p.is_file():
 yield p

 def _scan(self):
 snapshot = {}
 for p in self._walk():
 try:
 snapshot[str(p)] = (p.stat().st_size, p.stat().st_mtime)
 except OSError:
 continue
 return snapshot

 def _loop(self):
 while not self._stop.is_set():
 time.sleep(self.interval)
 current = self._scan()
 changed = [Path(k) for k, v in current.items() if self._snap.get(k) != v]
 removed = [Path(k) for k in self._snap if k not in current]
 for p in changed + removed:
 for fn in self._handlers:
 try:
 fn(p)
 except Exception:
 continue
 self._snap = current