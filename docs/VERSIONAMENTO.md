# Histórico — Orquestrador de Rastreamento

## TRACK-COMPOSE 1.1.0 — 14/11/2026

- Corrigida divergência `golang-simulator` → `golang-simulador` nos caminhos.
- Eliminada inclusão duplicada das pilhas Mongo/Kafka em múltiplos subcomposes.
- Adicionados comandos de inicialização Go/Nest/Next no Compose raiz.
- Limitadas portas locais de Nest/Next/Mongo a 127.0.0.1.
- Adicionados `.env.example`, `.gitignore`, verificação CI Docker Compose.
- Atualizados gitlinks para commits de main já revisados de Go, NestJS, Next e Kafka.
- Documentados riscos: Mongo root/root, Kafka PLAINTEXT, ausência de E2E real.

## TRACK-COMPOSE 1.0.0 — baseline

- Orquestração original por includes de submódulos, sem CI Compose real.
- Documentos iniciais descreviam apenas arquitetura conceitual.

**Sem deploy:** esta revisão não levanta os serviços nem altera volumes/bancos reais.
