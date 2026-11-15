# Rastreabilidade de submódulos — Full Cycle

**Revisão:** 14/11/2026. O repositório orquestrador versiona SHAs exatos de NestJS, Next.js, Kafka e Go, evitando instalação de componentes flutuantes.

| Componente | Commit fixado |
| --- | --- |
| nestjs-api | `d65bff1ad1578321346015fc4d07a2ce47b051b5` |
| next-frontend | `c423edcc4f817c86470c71c85e13dfc66d01b4ed` |
| golang-simulator | `e6d00387ca6974226a7f885d6d01f0e879e2d1cb` |
| kafka | `0d7336c7d0e461814ad61885cdeb70594d3ca6a8` |

A versão inicialmente sincronizada alterava apenas documentação. A revisão atual incorpora também correções do painel de GPS e do ciclo de vida de listeners, validadas pelo workflow do Next.js.

## Verificação
```bash
git submodule update --init --recursive
git submodule status
docker compose -f docker-compose.yaml config --quiet
```

O CI testa coerência das referências e configuração do Compose; **não garante que todos os contêineres sobem ou trocam mensagens de ponta a ponta**. A integração Google Maps requer credencial externa; não utilizar secrets reais em fixtures ou imagens.


## Kafka — isolamento de contratos (14/11/2026)

O submódulo Kafka passa a fornecer o tópico exclusivo `laboratorio` para eventos didáticos. Os tópicos `route`, `freight` e `simulation` são reservados a contratos nativos. Os testes do componente rejeitam envelopes genéricos nesses tópicos antes de conectar e mantêm o evento `RouteCreated` nativo no Go. Checkout do pai atualizado para `0d7336c7d0e461814ad61885cdeb70594d3ca6a8`; a validação declarativa do Compose e o contrato de eventos não substituem E2E com broker real.

## Next.js — controle de painel e listeners GPS (14/11/2026)

O checkout de `next-frontend` passa a conter o [PR #20](https://github.com/DanieldeAlmeida2024/next-frontend/pull/20): a página `/admin` só monta o cliente de GPS quando a demonstração local foi expressamente habilitada; `MapDriver` isola inscrições por rota, cancela respostas tardias e valida latitude/longitude. Build Next.js, testes Node e gate npm audit de severidade alta passaram no PR. **Isto não habilita identidade individual nem emissor HMAC do NestJS**; o PR `nestjs-api#11` permanece não integrado até que o cliente e o emissor sejam homologados. A atualização de gitlink não inicia containers nem publica serviço.

## Kafka + Go — quarentena de eventos permanentemente inválidos

A versão atual do `kafka` cria o tópico local `route-dlq` (PR #8). O `golang-simulator` (PR #7) classifica erros permanentes de contrato sem confundi-los com falhas de Mongo, publicação ou cancelamento; publica o payload bruto e os metadados de origem na DLQ, e só depois confirma o offset `route`. Em erro de escrita na DLQ o offset permanece não confirmado. Os testes Go verificam ordem e falhas por injeção de callbacks e o Compose Kafka é validado estaticamente; não foi executado E2E com Kafka/Mongo, nem configuradas ACL/TLS/retenção em produção. Um crash depois do publish e antes do commit pode duplicar a DLQ.
