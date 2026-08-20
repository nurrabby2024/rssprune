"""Output formatters for RSSPrune."""

import json


class Formatter:
 def format(self, data):
 raise NotImplementedError

 def file_suffix(self):
 raise NotImplementedError


class JsonFormatter(Formatter):
 def format(self, data):
 return json.dumps(data, indent=2, default=str)

 def file_suffix(self):
 return ".json"


class CompactJsonFormatter(Formatter):
 def format(self, data):
 return json.dumps(data, separators=(",", ":"), default=str)

 def file_suffix(self):
 return ".json"


class LineFormatter(Formatter):
 def format(self, data):
 if isinstance(data, (list, tuple)):
 return "\n".join(str(item) for item in data)
 return str(data)

 def file_suffix(self):
 return ".txt"


class KeyValueFormatter(Formatter):
 def format(self, data):
 if isinstance(data, dict):
 return "\n".join(f"{k}={v}" for k, v in data.items())
 return str(data)

 def file_suffix(self):
 return ".env"


FORMATTERS = {
 "json": JsonFormatter(),
 "json-compact": CompactJsonFormatter(),
 "lines": LineFormatter(),
 "keyvalue": KeyValueFormatter(),
}


def get_formatter(name):
 try:
 return FORMATTERS[name]
 except KeyError:
 raise ValueError(f"unknown formatter: {name}")