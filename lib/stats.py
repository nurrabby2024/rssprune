"""Statistics helpers for RSSPrune."""

import math
from collections import Counter


def mean(values):
 if not values:
 return 0.0
 return sum(values) / len(values)


def median(values):
 if not values:
 return 0.0
 ordered = sorted(values)
 n = len(ordered)
 mid = n // 2
 if n % 2 == 1:
 return float(ordered[mid])
 return (ordered[mid - 1] + ordered[mid]) / 2.0


def stdev(values):
 if len(values) < 2:
 return 0.0
 m = mean(values)
 return math.sqrt(sum((x - m) ** 2 for x in values) / (len(values) - 1))


def percentiles(values):
 if not values:
 return {}
 ordered = sorted(values)
 n = len(ordered)
 out = {}
 for p in (10, 25, 50, 75, 90):
 idx = min(n - 1, max(0, round(n * p / 100)))
 out[p] = ordered[idx]
 return out


def top_counter(values, limit=10):
 return Counter(values).most_common(limit)


def summarize(values):
 return {
 "count": len(values),
 "mean": round(mean(values), 3),
 "median": round(median(values), 3),
 "stdev": round(stdev(values), 3),
 "min": min(values) if values else None,
 "max": max(values) if values else None,
 "percentiles": percentiles(values),
 }