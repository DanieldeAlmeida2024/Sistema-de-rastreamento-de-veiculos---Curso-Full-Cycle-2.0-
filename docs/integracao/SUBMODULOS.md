# Rastreabilidade de submódulos — Full Cycle

**Revisão:** 14/11/2026. O repositório orquestrador versiona SHAs exatos de NestJS, Next.js, Kafka e Go, evitando instalação de componentes flutuantes.

| Componente | Commit fixado |
| --- | --- |
| nestjs-api | `d65bff1ad1578321346015fc4d07a2ce47b051b5` |
| next-frontend | `c423edcc4f817c86470c71c85e13dfc66d01b4ed` |
| golang-simulator | `0cb1073df2d477e8d5796728e7b1c831325c9ee3` |
| kafka | `4fcea5cf784e4118799fdfdf30ff286640827c34` |

A versão inicialmente sincronizada alterava apenas documentação. A revisão atual incorpora também correções do painel de GPS e do ciclo de vida de listeners, validadas pelo workflow do Next.js.

## Verificação
```bash
git submodule update --init --recursive
git submodule status
docker compose -f docker-compose.yaml config --quiet
```

O CI testa coerência das referências e configuração do Compose; **não garante que todos os contêineres sobem ou trocam mensagens de ponta a ponta**. A integração Google Maps requer credencial externa; não utilizar secrets reais em fixtures ou imagens.


## Kafka — isolamento de contratos (14/11/2026)

O submódulo Kafka passa a fornecer o tópico exclusivo `laboratorio` para eventos didáticos. Os tópicos `route`, `freight` e `simulation` são reservados a contratos nativos. Os testes do componente rejeitam envelopes genéricos nesses tópicos antes de conectar e mantêm o evento `RouteCreated` nativo no Go. Checkout do pai atualizado para `4fcea5cf784e4118799fdfdf30ff286640827c34`; a validação declarativa do Compose e o contrato de eventos não substituem E2E com broker real.

## Next.js — controle de painel e listeners GPS (14/11/2026)

O checkout de `next-frontend` passa a conter o [PR #20](https://github.com/DanieldeAlmeida2024/next-frontend/pull/20): a página `/admin` só monta o cliente de GPS quando a demonstração local foi expressamente habilitada; `MapDriver` isola inscrições por rota, cancela respostas tardias e valida latitude/longitude. Build Next.js, testes Node e gate npm audit de severidade alta passaram no PR. **Isto não habilita identidade individual nem emissor HMAC do NestJS**; o PR `nestjs-api#11` permanece não integrado até que o cliente e o emissor sejam homologados. A atualização de gitlink não inicia containers nem publica serviço.
