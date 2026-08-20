"""Simple state migrations for RSSPrune."""

import json
from pathlib import Path


class Migration:
 version = 0

 def up(self, data):
 return data


class MigrationRunner:
 def __init__(self, state_path, migrations):
 self.state_path = Path(state_path)
 self.migrations = sorted(migrations, key=lambda m: m.version)

 def current(self):
 if not self.state_path.exists():
 return 0
 try:
 meta = json.loads(self.state_path.read_text(encoding="utf-8")).get("__meta__", {})
 return int(meta.get("version", 0))
 except (ValueError, OSError):
 return 0

 def run(self):
 version = self.current()
 if not self.state_path.exists():
 data = {}
 else:
 data = json.loads(self.state_path.read_text(encoding="utf-8"))
 applied = []
 for migration in self.migrations:
 if migration.version <= version:
 continue
 data = migration.up(data)
 applied.append(migration.version)
 version = migration.version
 if applied:
 data["__meta__"] = {"version": version}
 self.state_path.parent.mkdir(parents=True, exist_ok=True)
 self.state_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
 return applied