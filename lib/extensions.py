"""Public extension points for RSSPrune.

Third-party code can register behavior without touching the core. This keeps the
project stable while the ecosystem around it grows.
"""


class Extension:
 name = "base-extension"
 priority = 100

 def before_run(self, context):
 pass

 def after_run(self, context):
 pass


class ExtensionManager:
 def __init__(self):
 self._extensions = []

 def add(self, extension):
 if not isinstance(extension, Extension):
 raise TypeError("expected an Extension")
 self._extensions.append(extension)
 self._extensions.sort(key=lambda e: e.priority)
 return self

 def before_run(self, context):
 for ext in self._extensions:
 ext.before_run(context)

 def after_run(self, context):
 for ext in reversed(self._extensions):
 ext.after_run(context)

 def names(self):
 return [ext.name for ext in self._extensions]