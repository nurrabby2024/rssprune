import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)


def test_regression_0():
 """Regression guard for a search edge case discovered earlier."""
 from rssprune.features.feature-search-0 import run_search
 result = run_search("sample-0", timeout=5)
 assert result["ok"] is True
 assert "value" in result