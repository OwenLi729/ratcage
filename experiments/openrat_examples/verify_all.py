import subprocess
import sys
from pathlib import Path

SCRIPTS = [
    "run_experiment_docker.py",
    "framework_workflow_docker.py",
    "custom_tool_ollama.py",
    "local_executor_probe.py",
]


def main() -> int:
    base = Path(__file__).resolve().parent
    all_ok = True

    print("=== Openrat examples verification (excluding chat_agent.py) ===")
    for script in SCRIPTS:
        script_path = base / script
        completed = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
        ok = completed.returncode == 0
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {script}")
        if completed.stdout.strip():
            print(f"  stdout: {completed.stdout.strip()}")
        if completed.stderr.strip():
            print(f"  stderr: {completed.stderr.strip()}")
        if not ok:
            all_ok = False

    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
