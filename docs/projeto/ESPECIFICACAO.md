# Workspace orquestrador de rastreamento — submódulos e Compose

Versão **1.0.0**, 11/11/2026; código base `c41f00bb2a1e7adcaaf44176125dfd23ae87314f`; critérios não executados neste PR.

## Inventário, contratos e operação
Este repositório é **orquestrador de workspace**, não uma segunda implementação de API. O arquivo `.gitmodules` aponta para quatro repositórios: `nestjs-api`, `next-frontend`, `golang-simulador` (path local do submódulo associado a `golang-simulator` no GitHub) e `kafka`. O `docker-compose.yaml` raiz usa `include` para `./golang-simulator/compose.yaml`, `./nestjs-api/docker-compose.yaml` e `./next-frontend/docker-compose.yaml`.

**Inconsistência observada:** o submódulo tem path `golang-simulador` enquanto o Compose inclui `golang-simulator`. Um clone com submódulos pode falhar no `docker compose config` mesmo quando os repositórios isolados compilam. Corrigir a relação de caminhos mediante PR específico, não editar às cegas. O banco MongoDB mantém Compose em `mongodb/docker-compose.yaml` e Dockerfile local. Dependências e credenciais devem permanecer fora de versões publicadas.

Os contratos de rota/frete/simulação são propriedade de `nestjs-api` e `golang-simulator`, respectivamente; não duplicar fontes ou fingir testes desta pasta como testes E2E. Deixar claro quais componentes possuem próprio CI, como os submódulos são fixados por SHA e como o runner resolve o workspace completo.

## Verificações locais
```bash
git submodule update --init --recursive && docker compose config
```

Links cruzados: [diagramas](../uml/README.md) · [riscos e testes](../testes/PLANO_DE_TESTES.md) · [versões](../controle/VERSIONAMENTO.md).
