"""Tiny string templating for RSSPrune."""

import re


TOKEN_RE = re.compile(r"\{\{[ \t]*(\w+)[ \t]*\}\}")


class Template:
 def __init__(self, source):
 self.source = source

 def render(self, context):
 def _replace(match):
 key = match.group(1)
 if key not in context:
 return match.group(0)
 value = context[key]
 if isinstance(value, (dict, list)):
 import json
 return json.dumps(value, default=str)
 return str(value)

 return TOKEN_RE.sub(_replace, self.source)

 @classmethod
 def from_file(cls, path):
 return cls(Path(path).read_text(encoding="utf-8"))


def render_string(source, context):
 return Template(source).render(context)


def render_file(path, context):
 from pathlib import Path
 return render_string(Path(path).read_text(encoding="utf-8"), context)