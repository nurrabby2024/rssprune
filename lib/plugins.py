"""Plugin registry for RSSPrune."""

import importlib
import inspect


class Plugin:
 name = "base"
 version = "0.1.0"

 def setup(self, context):
 pass

 def teardown(self):
 pass

 def describe(self):
 return {"name": self.name, "version": self.version}


class PluginRegistry:
 def __init__(self):
 self._plugins = {}

 def register(self, plugin):
 if not inspect.isclass(plugin) or not issubclass(plugin, Plugin):
 raise TypeError("plugins must subclass Plugin")
 instance = plugin()
 self._plugins[instance.name] = instance
 return instance

 def get(self, name):
 return self._plugins.get(name)

 def all(self):
 return list(self._plugins.values())

 def setup_all(self, context):
 for plugin in self._plugins.values():
 plugin.setup(context)

 def load_module(self, module_name):
 mod = importlib.import_module(module_name)
 for _, obj in inspect.getmembers(mod, inspect.isclass):
 if issubclass(obj, Plugin) and obj is not Plugin:
 self.register(obj)