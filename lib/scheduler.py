"""In-process job scheduler for RSSPrune."""

import heapq
import threading
import time
from dataclasses import dataclass


@dataclass(order=True)
class Job:
 run_at: float
 seq: int
 fn: object
 name: str = ""

 def __hash__(self):
 return hash((self.run_at, self.seq))


class Scheduler:
 def __init__(self):
 self._heap = []
 self._seq = 0
 self._lock = threading.Lock()
 self._cond = threading.Condition(self._lock)
 self._stop = threading.Event()
 self._thread = threading.Thread(target=self._run, daemon=True, name="scheduler")

 def start(self):
 self._thread.start()
 return self

 def stop(self):
 self._stop.set()
 with self._cond:
 self._cond.notify_all()
 self._thread.join(timeout=5)

 def at(self, when, fn, name=""):
 with self._lock:
 self._seq += 1
 heapq.heappush(self._heap, Job(when, self._seq, fn, name))
 with self._cond:
 self._cond.notify()

 def every(self, seconds, fn, name=""):
 def loop():
 self.at(time.time() + seconds, loop, name)
 fn()
 self.at(time.time() + seconds, loop, name)
 return self

 def _run(self):
 while not self._stop.is_set():
 with self._cond:
 while self._heap and self._heap[0].run_at > time.time():
 wait = self._heap[0].run_at - time.time()
 self._cond.wait(timeout=min(wait, 60))
 if self._stop.is_set():
 return
 if self._heap:
 job = heapq.heappop(self._heap)
 else:
 self._cond.wait(timeout=60)
 continue
 try:
 job.fn()
 except Exception:
 continue

 def pending(self):
 with self._lock:
 return len(self._heap)