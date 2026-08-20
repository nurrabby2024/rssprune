"""Output exporters for RSSPrune."""

import csv
import json
from pathlib import Path


class Exporter:
 def __init__(self, rows):
 self.rows = rows

 def to_json(self, path):
 Path(path).parent.mkdir(parents=True, exist_ok=True)
 with open(path, "w", encoding="utf-8") as fh:
 json.dump(self.rows, fh, indent=2, default=str)
 return path

 def to_csv(self, path):
 Path(path).parent.mkdir(parents=True, exist_ok=True)
 if not self.rows:
 Path(path).write_text("", encoding="utf-8")
 return path
 keys = list(self.rows[0].keys())
 with open(path, "w", encoding="utf-8", newline="") as fh:
 writer = csv.DictWriter(fh, fieldnames=keys)
 writer.writeheader()
 writer.writerows(self.rows)
 return path

 def to_markdown(self, path):
 Path(path).parent.mkdir(parents=True, exist_ok=True)
 if not self.rows:
 Path(path).write_text("", encoding="utf-8")
 return path
 keys = list(self.rows[0].keys())
 lines = ["| " + " | ".join(keys) + " |", "| " + " | ".join("---" for _ in keys) + " |"]
 for row in self.rows:
 lines.append("| " + " | ".join(str(row.get(k, "")) for k in keys) + " |")
 Path(path).write_text("\n".join(lines), encoding="utf-8")
 return path

 def to_text(self, path):
 Path(path).parent.mkdir(parents=True, exist_ok=True)
 lines = [json.dumps(r, default=str) for r in self.rows]
 Path(path).write_text("\n".join(lines), encoding="utf-8")
 return path