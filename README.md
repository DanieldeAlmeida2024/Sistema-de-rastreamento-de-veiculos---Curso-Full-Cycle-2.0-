# Sistema de Rastreamento de Veículos — Full Cycle

Laboratório de arquitetura distribuída para cadastro e acompanhamento de rotas, simulação de deslocamentos e comunicação por eventos. Os componentes são mantidos em repositórios separados e reunidos aqui por **Git submodules** e Docker Compose.

## Componentes

| Repositório | Responsabilidade |
| --- | --- |
| [nestjs-api](https://github.com/DanieldeAlmeida2024/nestjs-api) | API de rotas, mapas, persistência e atualizações |
| [next-frontend](https://github.com/DanieldeAlmeida2024/next-frontend) | Interface para rotas, motoristas e mapas |
| [golang-simulator](https://github.com/DanieldeAlmeida2024/golang-simulator) | Simulação de deslocamento e geração de eventos |
| [kafka](https://github.com/DanieldeAlmeida2024/kafka) | Mensageria e configuração de broker |
| Este repositório | Orquestração com Docker Compose e integração do ambiente |

A pasta do simulador Go neste repositório se chama `golang-simulador/`, conforme `.gitmodules`.

## Preparar o ambiente

Requer Docker, Docker Compose e Git.

```bash
git clone --recurse-submodules https://github.com/DanieldeAlmeida2024/Sistema-de-rastreamento-de-veiculos---Curso-Full-Cycle-2.0-.git
cd Sistema-de-rastreamento-de-veiculos---Curso-Full-Cycle-2.0-
git submodule update --init --recursive
cp .env.example .env
```

No PowerShell, `Copy-Item .env.example .env` substitui `cp`.

Configure `ROUTES_API_KEY` com valor aleatório de pelo menos 32 caracteres. Para funcionalidades com mapas, configure também a chave apropriada do Google Maps. O arquivo `.env` não deve ser versionado.

## Verificação e execução

```bash
docker compose -f docker-compose.yaml config --quiet
docker compose -f docker-compose.yaml config --services
docker compose -f docker-compose.yaml up --build -d
docker compose -f docker-compose.yaml ps
docker compose -f docker-compose.yaml logs --tail=100 nest next simulator
```

Os acessos de desenvolvimento descritos no Compose incluem frontend em `http://localhost:3001` e NestJS em `http://localhost:3000`. Verifique os mapeamentos de portas efetivos no ambiente local.

O workflow `validar-compose.yml` valida o arquivo de orquestração e o checkout dos submódulos, não substituindo teste de integração com todos os serviços ativos.

## Segurança do laboratório

MongoDB utiliza credenciais de demonstração e Kafka opera com listeners sem TLS no ambiente didático. As portas externas previstas são vinculadas a loopback. Não exponha essas configurações na internet nem reutilize dados e segredos de laboratório em produção.

Os submódulos apontam para commits específicos. Atualizações de cada dependência devem ser revisadas e validadas no Compose antes de alterar seus pins.

## Documentação e curso

[Arquitetura](docs/ARQUITETURA.md) · [Requisitos](docs/REQUISITOS.md) · [UML](docs/UML.puml) · [Plano de testes](docs/PLANO_TESTES.md).

Projeto desenvolvido a partir da [Imersão Full Cycle](https://imersao.fullcycle.com.br/). Diagrama de referência: [arquitetura_projeto.png](arquitetura_projeto.png).

## Compatibilidade dos componentes fixados

Esta revisão reúne o produtor NestJS e o simulador Go com o mesmo limite de **600 coordenadas** por rota (até 300 etapas do Google Maps). O produtor rejeita direções inválidas antes de gravar; o simulador recusa mensagens Kafka acima de **256 KiB** e direções excessivamente extensas. O workflow do repositório verifica automaticamente que o código dos submódulos fixados mantém esses contratos alinhados.

Como os componentes são Git submodules, use `git submodule update --init --recursive` após atualizar o repositório pai; executar `git pull` dentro de um submódulo pode colocá-lo em outro commit, diferente da revisão testada. Não há homologação E2E nem deploy nesta atualização.

## Next.js com chave privada do NestJS — integração de laboratório

O Next.js agora compartilha a **mesma** `ROUTES_API_KEY` do NestJS como variável de ambiente **somente no contêiner servidor Next** (sem prefixo `NEXT_PUBLIC_`). Isso permite que consultas, criação e início de rotas cheguem aos endpoints protegidos do NestJS.

Como não há login/autorização por usuário neste laboratório, o Compose define `ALLOW_UNAUTHENTICATED_ROUTE_DEMO=true` explicitamente **apenas para o ambiente local**. A porta do Next permanece vinculada a `127.0.0.1:3001` e a do Nest a `127.0.0.1:3000`. Nunca reutilize esse sinalizador num deploy público; substitua por autenticação e permissões por recurso.

O submódulo `next-frontend/` foi atualizado para a versão com validação de IDs, tratamento de erros upstream, ausência de cache compartilhado e testes de contrato. Use `git submodule update --init --recursive` para obter o commit pinado.

## Publicação de eventos compatíveis com o simulador

O submódulo `kafka/` agora inclui `publicar-rastreamento`, um comando Python que gera `RouteCreated` e `DeliveryStarted` **no contrato nativo que o Go Simulator consome**. O publicador genérico anterior continua disponível apenas para estudo independente: seu envelope `tipo/dados` não deve ser enviado ao tópico `route` do simulador em execução.

O teste do repositório pai verifica os limites de **600 pontos** em NestJS, Kafka Python e Go, e o teto de **256 KiB** no parser. Confira a sintaxe e exemplos em [kafka/README.md](kafka/README.md) após sincronizar os submódulos. Não execute eventos experimentais em sistemas de terceiros nem associe os exemplos a operações reais de entrega.
