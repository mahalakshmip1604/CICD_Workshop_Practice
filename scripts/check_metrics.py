"""Quality gate: exit 1 if the model is not good enough.

Usage: python scripts/check_metrics.py metrics.json --min-auc 0.70
"""

from __future__ import annotations

import argparse
import json
import sys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("metrics_file")
    parser.add_argument("--min-auc", type=float, default=0.70)
    args = parser.parse_args()

    with open(args.metrics_file) as f:
        metrics = json.load(f)

    auc = metrics["roc_auc"]
    if auc < args.min_auc:
        print(f"FAIL: roc_auc {auc} < required {args.min_auc}")
        return 1
    print(f"PASS: roc_auc {auc} >= required {args.min_auc}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
