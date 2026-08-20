"""Persistent state store for RSSPrune."""

import json
import os
import tempfile
from pathlib import Path


class StateStore:
 def __init__(self, path=None):
 self.path = Path(path or os.path.join(tempfile.gettempdir(), "rssprune-state.json"))
 self._data = {}
 self._load()

 def _load(self):
 if self.path.exists():
 try:
 self._data = json.loads(self.path.read_text(encoding="utf-8"))
 except (ValueError, OSError):
 self._data = {}

 def get(self, key, default=None):
 return self._data.get(key, default)

 def set(self, key, value):
 self._data[key] = value
 self._save()

 def update(self, mapping):
 self._data.update(mapping)
 self._save()

 def delete(self, key):
 self._data.pop(key, None)
 self._save()

 def all(self):
 return dict(self._data)

 def _save(self):
 self.path.parent.mkdir(parents=True, exist_ok=True)
 tmp = self.path.with_suffix(".tmp")
 tmp.write_text(json.dumps(self._data, indent=2), encoding="utf-8")
 os.replace(tmp, self.path)