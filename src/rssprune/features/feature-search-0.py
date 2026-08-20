"""Search handling for RSSPrune."""

import threading
import time


class SearchHandler:
 """Processes search requests with retries and timeouts."""

 def __init__(self, timeout=15, retries=2):
 self.timeout = timeout
 self.retries = retries
 self._lock = threading.Lock()
 self._processed = 0
 self._errors = 0

 def run(self, payload, **options):
 """Run a single search operation."""
 started = time.time()
 attempts = 0
 last_error = None
 while attempts <= self.retries:
 attempts += 1
 try:
 result = self._execute(payload, options)
 with self._lock:
 self._processed += 1
 return {"ok": True, "value": result, "duration_ms": round((time.time() - started) * 1000, 2)}
 except Exception as err:
 last_error = err
 time.sleep(min(1, 0.2 * attempts))
 with self._lock:
 self._errors += 1
 return {"ok": False, "error": str(last_error), "attempts": attempts}

 def _execute(self, payload, options):
 if not payload:
 raise ValueError("empty search payload")
 return {"search": str(payload)[:200], "attempts": 0}

 def stats(self):
 with self._lock:
 return {"processed": self._processed, "errors": self._errors}


def run_search(payload, **options):
 """Module-level convenience entry point."""
 return SearchHandler().run(payload, **options)