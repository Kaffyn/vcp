# VCP - Vector Context Protocol

[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Alpha](https://img.shields.io/badge/Status-Alpha-orange)](https://github.com/vectora/vcp)

**VCP** é um protocolo aberto e agnóstico para recuperação de contexto semântico. Desacopla agentes de AI das implementações específicas de vector databases, permitindo uma padronização de mercado semelhante ao **LSP** (Language Server Protocol) ou **MCP** (Model Context Protocol).

## 🎯 Filosofia

VCP foi criado com três princípios fundamentais:

### 1. **Agnóstico a Frameworks**

Não importa se você está usando LangChain, LangGraph, ou construindo seu próprio agente em Rust/Go — VCP funciona. O core do protocolo tem **zero dependências** de frameworks específicos.

### 2. **Agnóstico a Vector Stores**

Suporte nativo para LanceDB, Qdrant, PostgreSQL, SQLite com embeddings, Redis/Valkey. Novos adapters podem ser adicionados sem modificar o core.

### 3. **Product-as-SDK**

Inspire-se em como o Node.js, Python, e LangChain funcionam. VCP é instalado como um SDK via `pip` ou `npm`, com **extras opcionais** que você escolhe:

```bash
uv add vcp[lancedb, langchain, valkey]
# vs
npm install @vcp/core @vcp/lancedb @vcp/langchain
```

---

## 📦 Arquitetura

```
VCP = Protocol (Schema) + SDKs (Python/TS) + Adapters (DB drivers) + Integrations (LangChain, etc.)
```

### **Core Protocol** (`core/schema/`)

Define o contrato — as 4 operações fundamentais que todo vector store deve implementar:

```python
# core/schema/operations.py
class Document:
    id: str                           # Identificador único
    text: str                         # Conteúdo do documento
    metadata: dict[str, Any] | None   # Metadados customizados

class SearchQuery:
    query: str                        # Texto ou embedding da busca
    limit: int = 10                   # Quantidade de resultados
    metadata_filters: dict | None     # Filtros opcionais

class SearchResult:
    id: str                           # Documento encontrado
    text: str                         # Conteúdo
    score: float                      # Score de relevância (0-1)
    metadata: dict | None             # Metadados
```

### **SDKs** (`sdks/python/`, `sdks/typescript/`)

Biblioteca agnóstica que você instala no seu projeto:

```python
from vcp import VCPClient
from vcp.adapters.lancedb import LanceDBAdapter

# Setup
adapter = LanceDBAdapter(db_path="./data")
client = VCPClient(adapter)

# Uso
await client.ingest([
    {"id": "1", "text": "Hello World", "metadata": {"source": "docs"}}
])

results = await client.search("greeting", limit=5)
ranked = await client.rerank("greeting", results)
await client.forget(["1"])  # Remove documento
```

### **Adapters** (`adapters/lancedb/`, `adapters/qdrant/`, etc.)

Implementações do protocolo para cada vector store. Cada adapter:

- Herda de `BaseAdapter`
- Implementa as 4 operações (ingest, search, rerank, forget)
- Pode ter dependências específicas (ex: `lancedb`, `qdrant-client`)

```python
from vcp.adapters.base import BaseAdapter

class LanceDBAdapter(BaseAdapter):
    async def ingest(self, documents: list[dict]) -> dict: ...
    async def search(self, query: str, limit: int = 10) -> list[dict]: ...
    async def rerank(self, query: str, candidates: list[dict]) -> list[dict]: ...
    async def forget(self, doc_ids: list[str]) -> dict: ...
```

### **Integrations** (`integrations/langchain/`)

Camada de consumo — como o VCP se conecta a frameworks populares. **Separada do core** para manter neutralidade:

```python
from vcp.integrations.langchain import VCPRetriever

# LangChain passa a usar VCP como fonte de contexto
retriever = VCPRetriever(vcp_client=client, search_type="similarity")
result = retriever.invoke("query")
```

---

## 🚀 Instalação

### Requisitos

- Python 3.11+ (para SDK Python)
- `uv` (recomendado) ou `pip`

### Opção 1: Instalação Rápida (Recomendado)

```bash
# Clone ou esteja no diretório do VCP
cd vcp

# Instale dependências
uv sync

# Configure adapters detectados automaticamente
uv run vcp init
```

**Saída esperada:**

```
🔍 VCP Init - Discovery Mode
==================================================
✓ Detectados: lancedb, valkey
✓ Config gerado em .vcp/config.json
```

### Opção 2: Instalação com Extras Customizados

```bash
# Instale apenas o que precisa
uv add vcp[lancedb]           # Apenas LanceDB
uv add vcp[langchain]          # Integração LangChain
uv add vcp[full]               # Todos os adapters + integrações
uv add vcp[dev]                # Ferramentas de desenvolvimento
```

### Opção 3: TypeScript/Node.js

```bash
# Core do protocolo
npm install @vcp/core

# Adapters específicos (à medida que desenvolver)
npm install @vcp/lancedb
npm install @vcp/qdrant

# Integração LangChain (future)
npm install @vcp/langchain
```

---

## 📚 Uso Básico

### Exemplo Python Completo

```python
import asyncio
from vcp import VCPClient
from vcp.adapters.lancedb import LanceDBAdapter

async def main():
    # 1. Inicialize o adapter (automaticamente detectado por vcp init)
    adapter = LanceDBAdapter(db_path="./vector_store")
    client = VCPClient(adapter)

    # 2. Ingest - Adicione documentos
    documents = [
        {
            "id": "doc-1",
            "text": "The future of AI is open and collaborative",
            "metadata": {"source": "blog", "date": "2024-05-13"}
        },
        {
            "id": "doc-2",
            "text": "Protocols enable interoperability across systems",
            "metadata": {"source": "whitepaper", "date": "2024-05-10"}
        }
    ]

    ingest_result = await client.ingest(documents)
    print(f"✓ {ingest_result['count']} documentos ingeridos")

    # 3. Search - Busque semelhantes
    results = await client.search("open source AI", limit=5)
    for result in results:
        print(f"  - {result['id']}: {result['score']:.2%}")

    # 4. Rerank - Reordene por relevância custom
    ranked = await client.rerank("AI open", results)
    print(f"✓ {len(ranked)} documentos rerankeados")

    # 5. Forget - Remova documento
    removed = await client.forget(["doc-1"])
    print(f"✓ {removed['count']} documentos removidos")

asyncio.run(main())
```

### Exemplo com LangChain

```python
from vcp import VCPClient
from vcp.adapters.lancedb import LanceDBAdapter
from vcp.integrations.langchain import VCPRetriever
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

# Setup VCP como retriever do LangChain
adapter = LanceDBAdapter(db_path="./data")
vcp_client = VCPClient(adapter)
retriever = VCPRetriever(vcp_client=vcp_client)

# Use em uma chain
llm = ChatOpenAI(model="gpt-4")
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever
)

result = qa.invoke("What is VCP?")
print(result)
```

---

## 🛠️ Adapters Suportados

| Adapter          | Status       | Instalação               | Descrição                                           |
| ---------------- | ------------ | ------------------------ | --------------------------------------------------- |
| **LanceDB**      | ✅ Alpha     | `uv add vcp[lancedb]`    | Banco de vetores embutido, rápido, ideal para MVP   |
| **Qdrant**       | ✅ Alpha     | `uv add vcp[qdrant]`     | Servidor vector database robusto e escalável        |
| **SQLite**       | ✅ Alpha     | `uv add vcp[sqlite]`     | Leve, zero dependências, perfeito para prototipagem |
| **PostgreSQL**   | 🔄 Planejado | `uv add vcp[postgresql]` | pgvector para produção com SQL completo             |
| **Valkey/Redis** | ✅ Alpha     | `uv add vcp[valkey]`     | Cache de alto desempenho e retrieval rápido         |
| **Pinecone**     | 🔄 Planejado | `uv add vcp[pinecone]`   | Managed vector database na cloud                    |
| **Milvus**       | 🔄 Planejado | `uv add vcp[milvus]`     | Open-source, escalável para bilhões de vetores      |

Criar um novo adapter é simples — implemente `BaseAdapter` e contribua!

---

## 🔌 Integrações

VCP é **first-class** em frameworks de AI:

### LangChain / LangGraph

```python
from vcp.integrations.langchain import VCPRetriever, VCPTool

# Como retriever em chains
retriever = VCPRetriever(vcp_client)

# Como tool em LangGraph
tools = [VCPTool(vcp_client)]
```

### FastAPI / REST APIs

```python
from fastapi import FastAPI
from vcp import VCPClient

app = FastAPI()
vcp_client = VCPClient(adapter)

@app.post("/search")
async def search(query: str):
    results = await vcp_client.search(query)
    return {"results": results}
```

### CLI

```bash
# Auto-discovery de adapters instalados
uv run vcp init

# (Future) Busca via CLI
uv run vcp search "my query"
```

---

## 🏗️ Estrutura do Projeto

```
vcp/
├── core/
│   └── schema/                    # Protocolo puro (agnóstico)
│       ├── operations.py          # Document, SearchQuery, SearchResult
│       └── types.py               # (future) Tipos Pydantic completos
│
├── sdks/
│   ├── python/
│   │   ├── src/vcp/
│   │   │   ├── __init__.py
│   │   │   ├── client.py          # VCPClient
│   │   │   ├── adapters/
│   │   │   │   ├── base.py        # BaseAdapter (interface)
│   │   │   │   ├── lancedb.py
│   │   │   │   ├── qdrant.py
│   │   │   │   └── sqlite.py
│   │   │   └── cli/
│   │   │       └── init.py        # Discovery + auto-config
│   │   └── pyproject.toml         # Extras: [lancedb, qdrant, ...]
│   │
│   └── typescript/                # (future)
│       └── packages/
│           ├── core/              # @vcp/core
│           ├── lancedb/           # @vcp/lancedb
│           └── langchain/         # @vcp/langchain
│
├── integrations/
│   └── langchain/
│       ├── retriever.py           # VCPRetriever
│       └── tools.py               # VCPTool para LangGraph
│
├── tests/
│   ├── test_schema.py
│   ├── test_adapters.py
│   └── test_cli.py
│
├── pyproject.toml                 # Config root
├── README.md                       # Este arquivo
└── LICENSE
```

---

## 🧪 Desenvolvimento

### Rodando Testes

```bash
# Instale devtools
uv sync --extra dev

# Rode os testes
uv run pytest

# Com coverage
uv run pytest --cov=vcp
```

### Code Quality

```bash
# Linting
uv run ruff check .

# Formatting
uv run ruff format .

# Type checking
uv run mypy src/vcp
```

---

## 🤝 Como Contribuir

### Criar um Novo Adapter

1. **Crie a classe** em `sdks/python/src/vcp/adapters/seu_adapter.py`:

   ```python
   from vcp.adapters.base import BaseAdapter

   class SeuAdapter(BaseAdapter):
       async def ingest(self, documents: list[dict]) -> dict: ...
       async def search(self, query: str, limit: int = 10) -> list[dict]: ...
       async def rerank(self, query: str, candidates: list[dict]) -> list[dict]: ...
       async def forget(self, doc_ids: list[str]) -> dict: ...
   ```

2. **Adicione a dependência** em `pyproject.toml`:

   ```toml
   [project.optional-dependencies]
   seu_adapter = ["sua-lib-favorita>=1.0.0"]
   ```

3. **Teste** com `uv run pytest`

4. **Abra um PR**

---

## 🌍 Comunidade

- 💬 **Discussões:** [GitHub Discussions](https://github.com/vectora/vcp/discussions)
- 🐛 **Issues:** [GitHub Issues](https://github.com/vectora/vcp/issues)
- 📝 **Roadmap:** [Projects](https://github.com/vectora/vcp/projects)

---

## 📖 Recursos Adicionais

- [Especificação do Protocolo](./core/schema/operations.py)
- [Guia de Implementação de Adapters](./CONTRIBUTING.md) (future)
- [Exemplos](./examples/) (future)

---

## 📄 Licença

MIT © 2026 Vectora. Veja [LICENSE](./LICENSE) para detalhes.

---

## 🙏 Agradecimentos

Inspirado por:

- **LSP** (Language Server Protocol) — padrão para editores
- **MCP** (Model Context Protocol) — padrão para agentes AI
- **LangChain** — abstração de modelos de linguagem
- **AsyncIO** — design agnóstico de transporte

VCP traz esses conceitos para o mundo de **vector databases e retrieval semântico**.

---

Made with ❤️ by Vectora | [Website](https://vectora.ai) | [Twitter](https://twitter.com/vectora_ai)
