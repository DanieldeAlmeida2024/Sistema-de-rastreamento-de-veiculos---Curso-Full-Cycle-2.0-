# Requisitos — orquestração de rastreamento Full Cycle

Versão TRACK-COMPOSE 1.1.0 · 14/11/2026.

## Funcionais

- **RF01:** permitir clonagem dos quatro submódulos nas pastas efetivamente existentes.
- **RF02:** gerar configuração Docker Compose incluindo uma vez Mongo e Kafka.
- **RF03:** iniciar processos de servidor Nest, Next e simulador Go, não contêineres ociosos com `tail -f /dev/null`.
- **RF04:** configurar `DATABASE_URL`/ `MONGO_URI`, Kafka e os endereços HTTP internos/externos necessários.
- **RF05:** indicar `ROUTES_API_KEY` obrigatória e chave Google Maps opcional para testar boot sem mapas.
- **RF06:** preservar links fixos para SHAs testáveis dos submódulos.

## Não funcionais

- **RNF01:** restringir as portas Mongo, Nest, Next, Kafka externo e Control Center ao loopback do host no ambiente padrão.
- **RNF02:** ignorar `.env` e demais configurações sensíveis no Git.
- **RNF03:** validar `docker compose config` no GitHub Actions, sem iniciar serviços nem volumes.
- **RNF04:** documentação de risco de Mongo root/root e Kafka PLAINTEXT.
- **RNF05:** não afirmar deploy, homologação E2E ou desempenho sem execução real.

**Fora do escopo:** bootstrap de credenciais reais, migração de dados, publicação de serviços, autenticação de console Kafka, tuning, roteamento externo e E2E com Google Maps.
