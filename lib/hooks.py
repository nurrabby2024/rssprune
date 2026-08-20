"""Event hooks for RSSPrune.

Hooks let callers run custom code around core operations without modifying the
package. This keeps the core small while remaining fully customizable.
"""


class HookManager:
 def __init__(self):
 self._hooks = {}

 def on(self, event, fn):
 self._hooks.setdefault(event, []).append(fn)
 return self

 def off(self, event, fn):
 self._hooks.setdefault(event, []).remove(fn)

 def fire(self, event, *args, **kwargs):
 for fn in self._hooks.get(event, []):
 fn(*args, **kwargs)

 def fire_until(self, event, *args, **kwargs):
 """Fire hooks until one returns a truthy value."""
 for fn in self._hooks.get(event, []):
 result = fn(*args, **kwargs)
 if result:
 return result
 return None

 def events(self):
 return list(self._hooks.keys())


hooks = HookManager()