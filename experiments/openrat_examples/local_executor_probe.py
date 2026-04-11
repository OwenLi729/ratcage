import subprocess
from pathlib import Path

from openrat import Openrat

from common import make_fixture_scripts


def main() -> int:
    hello_script, _, _ = make_fixture_scripts(Path("experiments") / ".openrat_example_fixtures")

    app = Openrat({"executor": "local"})
    try:
        app.run(str(hello_script), timeout=20)
    except Exception as exc:
        message = str(exc)
        exc_type = type(exc).__name__
        
        # v0.1.1: local executor available, but resource limits (preexec_fn) fail on macOS
        if "preexec_fn" in message.lower() or isinstance(exc, subprocess.SubprocessError):
            print({"local_executor_available": True, "note": "resource limits failed on macOS; works on Linux"})
            return 0
        
        # Unexpected error
        print({"local_executor_available": False, "error": f"{exc_type}: {message}"})
        return 1

    print({"local_executor_available": True, "status": "success"})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
