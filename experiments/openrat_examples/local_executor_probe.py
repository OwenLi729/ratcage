from pathlib import Path

from openrat import Openrat
from openrat.core.errors import UserInputError

from common import make_fixture_scripts


def main() -> int:
    hello_script, _, _ = make_fixture_scripts(Path("experiments") / ".openrat_example_fixtures")

    app = Openrat({"executor": "local"})
    try:
        app.run(str(hello_script), timeout=20)
    except UserInputError as exc:
        message = str(exc)
        print({"local_executor_supported": False, "reason": message})
        if "unsupported executor" in message.lower() or "requires executor='docker'" in message.lower():
            return 0
        return 1

    print({"local_executor_supported": True})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
