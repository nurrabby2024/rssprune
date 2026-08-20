"""Lightweight runtime monitoring for RSSPrune."""

import threading
import time
from collections import deque


class Monitor:
 def __init__(self, window=300):
 self.window = window
 self._events = deque(maxlen=10000)
 self._started = time.time()
 self._lock = threading.Lock()

 def record(self, name, duration_ms=None, ok=True):
 with self._lock:
 self._events.append({
 "name": name,
 "at": time.time(),
 "duration_ms": duration_ms,
 "ok": ok,
 })

 def uptime(self):
 return round(time.time() - self._started, 2)

 def snapshot(self):
 with self._lock:
 cutoff = time.time() - self.window
 recent = [e for e in self._events if e["at"] >= cutoff]
 counts = {}
 durations = {}
 for e in recent:
 key = e["name"]
 counts[key] = counts.get(key, 0) + 1
 if e["duration_ms"] is not None:
 durations.setdefault(key, []).append(e["duration_ms"])
 return {
 "uptime_s": self.uptime(),
 "window_s": self.window,
 "calls": len(recent),
 "by_name": {
 name: {
 "count": count,
 "avg_ms": round(sum(durations[name]) / len(durations[name]), 2)
 if name in durations and durations[name] else None,
 }
 for name, count in counts.items()
 },
 }