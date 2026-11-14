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
