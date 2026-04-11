from pathlib import Path
import subprocess
import time


def ensure_ollama_running() -> None:
    check = subprocess.run(["ollama", "ps"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if check.returncode == 0:
        return
    subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)


def ensure_qwen_model(tag: str = "qwen3:4b") -> None:
    has_model = subprocess.run(
        ["ollama", "show", tag],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if has_model.returncode != 0:
        subprocess.run(["ollama", "pull", tag], check=True)


def ensure_docker_running() -> None:
    ready = subprocess.run(["docker", "info"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if ready.returncode == 0:
        return
    subprocess.run(["open", "-a", "Docker"], check=False)
    for _ in range(45):
        ready = subprocess.run(["docker", "info"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if ready.returncode == 0:
            return
        time.sleep(2)
    raise RuntimeError("Docker is not ready. Start Docker Desktop and rerun.")


def make_fixture_scripts(base: Path) -> tuple[Path, Path, Path]:
    base.mkdir(parents=True, exist_ok=True)
    hello = base / "example_hello.py"
    train = base / "example_train.py"
    evaluate = base / "example_evaluate.py"

    hello.write_text("print('hello from run_experiment example')\n", encoding="utf-8")
    train.write_text("print('train step complete')\n", encoding="utf-8")
    evaluate.write_text("print('evaluate step complete')\n", encoding="utf-8")
    return hello, train, evaluate
