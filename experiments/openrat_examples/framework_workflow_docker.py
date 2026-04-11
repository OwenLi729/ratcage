from pathlib import Path

from openrat import AutonomyLevel, ExperimentSpec, Openrat, Session

from common import ensure_docker_running, make_fixture_scripts


def main() -> int:
    ensure_docker_running()
    _, train_script, evaluate_script = make_fixture_scripts(Path("experiments") / ".openrat_example_fixtures")

    session = Session(
        autonomy=AutonomyLevel.OBSERVE,
        patch_policy="disabled",
    )

    spec = ExperimentSpec(
        goals=("Train model", "Evaluate on test set"),
        metrics={"accuracy": None, "loss": None},
        tasks={
            "train": {
                "name": "Training task",
                "tool": "executor",
                "payload": {"command": ["python", str(train_script)], "timeout": 120},
            },
            "evaluate": {
                "name": "Evaluation task",
                "tool": "executor",
                "payload": {"command": ["python", str(evaluate_script)], "timeout": 60},
            },
        },
        dependencies={"evaluate": ("train",)},
    )

    app = Openrat({"executor": "docker", "docker_image": "python:3.11"})
    plan = app.build_plan(spec, session)
    artifact = app.execute_plan(plan, session, tools={})

    summary = artifact.summarize()
    print(summary)
    return 0 if summary.get("status") == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
