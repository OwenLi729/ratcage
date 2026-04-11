import subprocess
import sys
"""Entry point for split Openrat example verification scripts.

Runs all example checks in experiments/openrat_examples/, including local executor probe.
"""


def main() -> None:
    completed = subprocess.run(
        [sys.executable, "experiments/openrat_examples/verify_all.py"],
        check=False,
    )
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


if __name__ == "__main__":
    main()
