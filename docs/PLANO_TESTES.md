# Plano de testes — orquestração Docker

Versão TRACK-COMPOSE 1.2.0 · 14/11/2026.

## CI estrutural (executado)

Em checkout com submódulos recursivos e variável de teste `ROUTES_API_KEY`:

```bash
git submodule update --init --recursive
docker compose -f docker-compose.yaml config --quiet
docker compose -f docker-compose.yaml config --services
```

| ID | Cenário | Esperado |
| --- | --- | --- |
| GIT-01 | `git submodule update --init --recursive` | Pastas Go, Nest, Next, Kafka presentes |
| GIT-02 | Nome de pasta Go | `golang-simulador/compose.yaml` encontrado |
| GIT-03 | Pins de submódulos | Cada gitlink aponta a commit verificável |
| COMPOSE-01 | `docker compose config --quiet` | Código de saída 0; sintaxe e paths válidos |
| COMPOSE-02 | Lista de serviços | `simulator`, `nest`, `next`, `mongo`, `kafka` presentes |
| COMPOSE-03 | Startup | Comandos definidos para processos reais, sem `tail` |
| COMPOSE-04 | Exposição local | Nest, Next, Mongo, Kafka externo e Control Center escutam somente em `127.0.0.1` |

O workflow inspeciona o JSON gerado pelo Docker Compose, verifica portas dos cinco serviços expostos ao host e comandos de execução Go/Nest/Next. Isso ainda não envolve rede real.

## Testes de integração necessários antes de anunciar sistema funcional

- **E2E-01:** subir ambiente isolado, verificar saúde de Kafka, Mongo, Nest e Next.
- **E2E-02:** criar rota no Next, salvar via Nest/Mongo e gerar eventos Kafka.
- **E2E-03:** iniciar simulação Go e observar posições atualizadas via Socket.IO.
- **E2E-04:** confirmar permissões/segredos necessários e limite da API do Google Maps.
- **SEC-01:** inspecionar portas 9092, 9094 e 9021 (Kafka/control center) e configurar acesso restrito.
- **OPS-01:** medir tempo de bootstrap, estado de volumes, shutdown e recuperação após falha.

Nenhum destes testes E2E/SEC/OPS foi executado pela CI de configuração. **Docker Compose válido não significa serviço funcional.**

## TRACK-COMPAT-01 — acordo de mensagens entre submódulos

| Caso | Critério |
| --- | --- |
| TRACK-C01 | Gitlink NestJS usa o código com limite de 600 pontos |
| TRACK-C02 | Gitlink Go usa o mesmo limite de 600 pontos |
| TRACK-C03 | O produtor valida o número de etapas antes de criar rota no Mongo |
| TRACK-C04 | O simulador recusa mensagens acima de 256 KiB antes do parse JSON |
| TRACK-C05 | O simulador valida rotas persistidas antes de publicar movimentos |

O workflow invoca `python -m unittest discover -s tests -p 'test_kafka_route_contract.py' -v` depois de baixar os submódulos recursivamente. Esses testes conferem o código **dos SHAs fixados**, e não a ponta a ponta de uma entrega Kafka.
