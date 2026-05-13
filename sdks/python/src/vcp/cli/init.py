"""VCP Init - Discovery e Autoconfiguração"""

import asyncio
import json
import sys
from pathlib import Path


async def discover_adapters() -> dict:
    """Detecta adapters instalados via importação"""
    adapters = {}
    candidates = {
        "lancedb": "lancedb",
        "qdrant": "qdrant_client",
        "sqlite": "aiosqlite",
        "valkey": "redis",
    }
    for adapter_name, import_name in candidates.items():
        try:
            __import__(import_name)
            adapters[adapter_name] = True
        except ImportError:
            pass
    return adapters


def generate_config(adapters: dict) -> dict:
    """Gera .vcp/config.json baseado nos adapters detectados"""
    config = {
        "version": "0.1.0",
        "adapters": list(adapters.keys()),
        "default_adapter": list(adapters.keys())[0] if adapters else "lancedb",
    }
    return config


async def main():
    """Executa o setup wizard"""
    print("🔍 VCP Init - Discovery Mode")
    print("=" * 50)
    adapters = await discover_adapters()
    if adapters:
        print(f"✓ Detectados: {', '.join(adapters.keys())}")
    else:
        print("⚠ Nenhum adapter detectado. Instale com: uv add vcp[lancedb]")
        sys.exit(1)
    config = generate_config(adapters)
    config_path = Path(".vcp/config.json")
    config_path.parent.mkdir(exist_ok=True)
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    print(f"✓ Config gerado em {config_path}")


if __name__ == "__main__":
    asyncio.run(main())
