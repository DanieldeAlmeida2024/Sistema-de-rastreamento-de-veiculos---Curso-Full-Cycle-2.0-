# Histórico — Orquestrador de Rastreamento

## TRACK-COMPOSE 1.1.0 — 14/11/2026

- Corrigida divergência `golang-simulator` → `golang-simulador` nos caminhos.
- Eliminada inclusão duplicada das pilhas Mongo/Kafka em múltiplos subcomposes.
- Adicionados comandos de inicialização Go/Nest/Next no Compose raiz.
- Limitadas portas locais de Nest/Next/Mongo a 127.0.0.1.
- Adicionados `.env.example`, `.gitignore`, verificação CI Docker Compose.
- Atualizados gitlinks para commits de main já revisados de Go, NestJS, Next e Kafka.
- Kafka atualizado para `059c9095bdb0`: broker externo 9094 e Control Center 9021 apenas em loopback, listener interno 9092 somente na rede Docker.
- CI estendida para verificar comandos reais e binds de host ao renderizar o Compose JSON.
- Documentados riscos: Mongo root/root, Kafka PLAINTEXT, ausência de E2E real.

## TRACK-COMPOSE 1.0.0 — baseline

- Orquestração original por includes de submódulos, sem CI Compose real.
- Documentos iniciais descreviam apenas arquitetura conceitual.

**Sem deploy:** esta revisão não levanta os serviços nem altera volumes/bancos reais.

## TRACK-COMPOSE 1.2.0 — contrato de eventos e pins (14/11/2026)

- Gitlink `nestjs-api/` atualizado para `d65bff1ad1578321346015fc4d07a2ce47b051b5` (validação Google Maps antes de persistir/publicar).
- Gitlink `golang-simulador/` atualizado para `0cb1073df2d477e8d5796728e7b1c831325c9ee3` (limites de eventos/pontos e rejeição pré-publicação).
- Mantidos pins Next.js e Kafka, volumes e configuração Compose anterior.
- Adicionada regressão automática dos limites cruzados em `tests/test_kafka_route_contract.py`.
- Nenhuma modificação da infraestrutura ou execução de E2E, nenhum deploy. Falha Kafka depois de uma persistência ainda requer outbox/idempotência.

## TRACK-COMPOSE 1.3.0 — Next.js/NestJS com chave privada (14/11/2026)

- Atualizado gitlink `next-frontend/` para `89b66a567aca07570bfa247baf245b4d1723a766`, após CI aprovado no projeto filho.
- A mesma `ROUTES_API_KEY` agora é passada para os servidores Nest e Next, sem exposição `NEXT_PUBLIC_`.
- O modo de demonstração de rotas sem login é habilitado deliberadamente **somente nesta stack local**, cuja exposição ao host permanece em loopback.
- Workflow Compose verifica alinhamento do segredo entre os dois serviços e o flag local, além de portas e contratos Kafka anteriores.
- Continuam pendentes autenticação por operador, Socket.IO autorizado e testes E2E reais.

## TRACK-COMPOSE 1.4.0 — gitlink Kafka nativo (14/11/2026)

- Gitlink `kafka/` atualizado para `a4b1cc83f7baf72734e7786af2fa9b5a56dfffdb` com publicador `RouteCreated`/`DeliveryStarted` nativo.
- Incluídas regressões de contrato `TRACK-C10` a `TRACK-C14` sobre o código efetivamente pinado, sem Kafka real.
- Mantidos os pins NestJS, Go e Next.js da revisão anterior e todas as portas em loopback.
- Não são alterados tópicos, segurança de rede, volumes, fluxos de entrega ou serviços já em execução.
