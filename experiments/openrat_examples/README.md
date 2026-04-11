# Openrat Examples Verification (excluding `chat_agent.py`)

This folder contains split, runnable versions of the Openrat `examples/` flows:

- `run_experiment_docker.py`
- `framework_workflow_docker.py`
- `custom_tool_ollama.py`
- `local_executor_probe.py`
- `verify_all.py` (runs all of the above)

## Prerequisites

From the repo root:

```bash
source .venv/bin/activate
```

Make sure these are available:

- Docker Desktop installed (script will try to start it if needed)
- Ollama installed
- `qwen3:4b` model available (`custom_tool_ollama.py` auto-pulls if missing)

## Run all at once

```bash
python experiments/standard.py
```

or directly:

```bash
python experiments/openrat_examples/verify_all.py
```

Success means all scripts print `[PASS]` and command exit code is `0`.

## Run individually

```bash
python experiments/openrat_examples/run_experiment_docker.py
python experiments/openrat_examples/framework_workflow_docker.py
python experiments/openrat_examples/custom_tool_ollama.py
python experiments/openrat_examples/local_executor_probe.py
```

## Local executor (v0.1.1)

The `LocalExecutor` is available:
- On **Linux**: local executor works with resource limits
- On **macOS**: local executor available but resource limit preexec_fn fails

`local_executor_probe.py` detects and reports this correctly.
