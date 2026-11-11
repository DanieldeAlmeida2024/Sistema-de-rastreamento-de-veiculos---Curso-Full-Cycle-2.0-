# Plano de testes — Workspace orquestrador de rastreamento — submódulos e Compose

Versão **1.0.0**, 11/11/2026; código base `c41f00bb2a1e7adcaaf44176125dfd23ae87314f`; critérios não executados neste PR.

| ID | Cenário | Aceitação | Situação |
|---|---|---|---|
| SYS-01 | git submodule update --init --recursive | Submódulos resolvem para SHAs registrados | Pendente de execução |
| SYS-02 | docker compose config | Todos os paths include existem; detectar conflito simulador | Pendente de execução |
| SYS-03 | docker compose up (ambiente limpo) | Serviços Mongo/Kafka/Node/Go/Next resolvem DNS | Pendente de execução |
| SYS-04 | Criar rota na API | RouteCreated recebido pelo simulador | Pendente de execução |
| SYS-05 | Calcular frete | FreightCalculated entregue sem duplicata inesperada | Pendente de execução |
| SYS-06 | Iniciar rota | DeliveryStarted resulta em DriverMoved | Pendente de execução |
| SYS-07 | WebSocket no frontend | Atualização de posições aparece na tela | Pendente de execução |
| SYS-08 | Falha em broker/mongo | Nenhum serviço oculta falha de infraestrutura | Pendente de execução |
| SYS-09 | Restart da stack | Volumes preservam dados conforme política | Pendente de execução |
| SYS-10 | Inspecionar secrets | Nenhuma credencial real está no git | Pendente de execução |

A matriz separa observações do código de hipóteses de aceite. Execute primeiro testes isolados com fixtures sintéticas, depois integração em ambiente efêmero e, por último, E2E autorizado. Registrar SHA, versões de serviços, logs sanitizados, data e estado PASS/FAIL/BLOCKED. Não usar um teste estrutural Python como evidência de uma integração de rede.
