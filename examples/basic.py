"""Minimal example for RSSPrune."""

from rssprune import rssprune


def main():
 runner = rssprune({"name": "RSSPrune", "dry_run": False})
 result = runner.execute()
 print(result)


if __name__ == "__main__":
 main()