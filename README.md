# VCP — Vector Context Protocol

O **Vector Context Protocol (VCP)** é um padrão aberto para a comunicação entre agentes de IA e sistemas de armazenamento vetorial. Ele estabelece um contrato universal para ingestão, recuperação semântica e gestão de contexto, permitindo que agentes se tornem agnósticos à implementação do banco de vetores (Qdrant, LanceDB, Pinecone, etc).

## 🚀 Por que o VCP?

Hoje, agentes de IA estão presos ao SDK do banco de vetores que utilizam. O VCP desacopla essa dependência:

- **Padronização:** Um único contrato para Ingestão, Busca, Reranking e Gestão de TTL.
- **Agnóstico a Backend:** Troque de Qdrant para LanceDB sem alterar uma linha de código do seu Agente.
- **Compatível com Agentes:** Projetado para rodar via `stdio` (como o padrão MCP), permitindo que agentes executem servidores VCP como processos filhos isolados.
- **Alta Performance:** Desenvolvido para lidar com fluxos de dados de embedding de forma eficiente.

## ⚙️ Operações Primitivas

O protocolo é definido por 4 operações fundamentais:

1. `ingest`: Normaliza o pipeline de entrada (chunking, embedding, metadata schema).
2. `search`: Busca agnóstica por similaridade (query textual ou vetorial).
3. `rerank`: Refinamento semântico de candidatos com modelos plugáveis.
4. `forget`: Gestão de contexto _stale_ e compliance (LGPD/GDPR) via IDs ou TTL.

## 🏗 Arquitetura do Ecossistema

- **Core Schema:** Contrato definido em JSON Schema/Protobuf.
- **SDKs:** Implementações cliente/servidor em Python e TypeScript.
- **Adapters:** Implementações específicas para backends (e.g., `vcp-adapter-lancedb`, `vcp-adapter-qdrant`).
