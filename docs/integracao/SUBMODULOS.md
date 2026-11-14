# Rastreabilidade de submódulos — Full Cycle

**Revisão:** 14/11/2026. O repositório orquestrador versiona SHAs exatos de NestJS, Next.js, Kafka e Go, evitando instalação de componentes flutuantes.

| Componente | Commit fixado |
| --- | --- |
| nestjs-api | `d65bff1ad1578321346015fc4d07a2ce47b051b5` |
| next-frontend | `4fd5fa77dc622d49b668809bc40e1f02effb5bc9` |
| golang-simulator | `0cb1073df2d477e8d5796728e7b1c831325c9ee3` |
| kafka | `4fcea5cf784e4118799fdfdf30ff286640827c34` |

O Next.js avançou **2 commits de documentação** sobre `89b66a567aca07570bfa247baf245b4d1723a766`, sem modificações em código de produção nessa comparação. A sincronização restaura a correspondência entre o README do componente, os diagramas e a revisão que o checkout recursivo realmente entrega.

## Verificação
```bash
git submodule update --init --recursive
git submodule status
docker compose -f docker-compose.yaml config --quiet
```

O CI testa coerência das referências e configuração do Compose; **não garante que todos os contêineres sobem ou trocam mensagens de ponta a ponta**. A integração Google Maps requer credencial externa; não utilizar secrets reais em fixtures ou imagens.


## Kafka — isolamento de contratos (14/11/2026)

O submódulo Kafka passa a fornecer o tópico exclusivo `laboratorio` para eventos didáticos. Os tópicos `route`, `freight` e `simulation` são reservados a contratos nativos. Os testes do componente rejeitam envelopes genéricos nesses tópicos antes de conectar e mantêm o evento `RouteCreated` nativo no Go. Checkout do pai atualizado para `4fcea5cf784e4118799fdfdf30ff286640827c34`; a validação declarativa do Compose e o contrato de eventos não substituem E2E com broker real.
