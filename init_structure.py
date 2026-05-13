from pathlib import Path


def create_vcp_monorepo():
    # Estrutura modular
    # core: O contrato (schema/types)
    # sdk: As libs cliente (py/ts)
    # adapters: Os servidores que falam o protocolo
    # integrations: LangChain/LangGraph wrappers

    structure = [
        "core/schema",
        "sdks/python/src/vcp",
        "sdks/typescript/src",
        "adapters/lancedb",
        "adapters/qdrant",
        "adapters/sqlite",
        "adapters/postgresql",
        "adapters/valkey",
        "integrations/langchain",
        "integrations/langgraph",
        "tests/protocol",
        "tests/adapters",
    ]

    for folder in structure:
        path = Path(folder)
        path.mkdir(parents=True, exist_ok=True)
        (path / ".gitkeep").touch()
        print(f"✅ Criado: {folder}/.gitkeep")


if __name__ == "__main__":
    create_vcp_monorepo()
