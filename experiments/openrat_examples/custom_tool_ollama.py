from openrat import Message, Openrat

from common import ensure_ollama_running, ensure_qwen_model


def read_metrics(arguments: dict) -> dict:
    metric = arguments.get("metric", "accuracy")
    store = {"accuracy": 0.94, "loss": 0.12, "f1": 0.91}
    value = store.get(metric)
    if value is None:
        return {"error": f"unknown metric '{metric}'", "available": list(store.keys())}
    return {"metric": metric, "value": value}


def main() -> int:
    ensure_ollama_running()
    ensure_qwen_model("qwen3:4b")

    app = Openrat(
        {
            "executor": "docker",
            "docker_image": "python:3.11",
            "provider": "openai_compatible",
            "base_url": "http://localhost:11434/v1",
            "api_key": "ollama",
            "model_name": "qwen3:4b",
            "autonomy": 3,
            "user_approvals": {"host.exec"},
        }
    )

    app.tool_registry.register("read_metrics", read_metrics, capability="host.exec")
    tool_result = app.tool_registry.execute("read_metrics", {"metric": "f1"})

    messages = [
        Message(role="system", content="You are concise."),
        Message(role="user", content="Reply with exactly: custom tool setup complete."),
    ]
    response = app.chat(messages, max_turns=4)

    print({"tool_result": tool_result, "chat_response": response.content})

    ok = tool_result.get("metric") == "f1" and abs(float(tool_result.get("value", 0.0)) - 0.91) < 1e-9
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
