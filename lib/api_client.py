"""HTTP client wrapper for RSSPrune."""

import json
import time
import urllib.error
import urllib.parse
import urllib.request


class ApiClient:
 def __init__(self, base_url, token=None, timeout=30, retries=3):
 self.base_url = base_url.rstrip("/")
 self.token = token
 self.timeout = timeout
 self.retries = retries

 def request(self, method, path, data=None, params=None):
 url = self.base_url + path
 if params:
 url += "?" + urllib.parse.urlencode(params)
 body = json.dumps(data).encode() if data is not None else None
 headers = {"Content-Type": "application/json", "User-Agent": "rssprune"}
 if self.token:
 headers["Authorization"] = "Bearer " + self.token

 for attempt in range(self.retries):
 req = urllib.request.Request(url, data=body, headers=headers, method=method)
 try:
 with urllib.request.urlopen(req, timeout=self.timeout) as resp:
 raw = resp.read()
 return json.loads(raw) if raw else {}
 except urllib.error.HTTPError as err:
 if err.code in (429, 500, 502, 503, 504) and attempt < self.retries - 1:
 time.sleep(0.5 * (2 ** attempt))
 continue
 raise
 except urllib.error.URLError:
 if attempt < self.retries - 1:
 time.sleep(0.5 * (2 ** attempt))
 continue
 raise

 def get(self, path, params=None):
 return self.request("GET", path, params=params)

 def post(self, path, data=None):
 return self.request("POST", path, data=data)

 def put(self, path, data=None):
 return self.request("PUT", path, data=data)

 def delete(self, path):
 return self.request("DELETE", path)