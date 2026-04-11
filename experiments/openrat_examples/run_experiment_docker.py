from pathlib import Path

from openrat import Openrat

from common import ensure_docker_running, make_fixture_scripts


def main() -> int:
    ensure_docker_running()
    hello_script, _, _ = make_fixture_scripts(Path("experiments") / ".openrat_example_fixtures")

    app = Openrat({"executor": "docker", "docker_image": "python:3.11"})
    result = app.run(str(hello_script), timeout=30, isolate=True, memory="256m", cpus="0.5")

    ok = result.get("status") == "completed" and result.get("return_code") == 0
    print(result)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
