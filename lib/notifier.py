"""Notification helpers for RSSPrune."""

import os
import subprocess
import sys


class Notifier:
 def __init__(self, enabled=True):
 self.enabled = enabled

 def send(self, title, message, level="info"):
 if not self.enabled:
 return False
 if sys.platform == "win32":
 return self._toast(title, message)
 return self._console(title, message, level)

 def _toast(self, title, message):
 try:
 subprocess.Popen(
 [
 "powershell",
 "-NoProfile",
 "-Command",
 f"Add-Type -AssemblyName System.Windows.Forms; "
 f"[System.Windows.Forms.MessageBox]::Show('{message}','{title}')",
 ],
 stdout=subprocess.DEVNULL,
 stderr=subprocess.DEVNULL,
 )
 return True
 except Exception:
 return False

 def _console(self, title, message, level):
 sys.stderr.write(f"[{level.upper()}] {title}: {message}\n")
 return True

 @classmethod
 def from_env(cls):
 return cls(enabled=os.getenv("NOTIFICATIONS", "1") == "1")