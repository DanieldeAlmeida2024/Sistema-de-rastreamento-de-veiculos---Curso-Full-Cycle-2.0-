# Rastreamento de veículos — orquestrador Full Cycle

Projeto de laboratório com **Go, NestJS, Next.js, Kafka e MongoDB**. O repositório raiz organiza os submódulos Git do frontend, backend, simulador e Kafka, além de fornecer o MongoDB local.

## Clonar e preparar

```bash
git clone --recurse-submodules https://github.com/DanieldeAlmeida2024/Sistema-de-rastreamento-de-veiculos---Curso-Full-Cycle-2.0-.git
cd Sistema-de-rastreamento-de-veiculos---Curso-Full-Cycle-2.0-
git submodule update --init --recursive
cp .env.example .env
```

No PowerShell, substitua `cp` por `Copy-Item .env.example .env`. Edite o `.env`: defina `ROUTES_API_KEY` com no mínimo 32 caracteres aleatórios e `GOOGLE_MAPS_API_KEY` se for usar mapas. **Não envie o .env ao Git.**

## Validar Compose sem ligar serviços

```bash
docker compose -f docker-compose.yaml config --quiet
docker compose -f docker-compose.yaml config --services
```

O workflow de CI `validar-compose.yml` executa essa verificação com uma chave **fictícia** de teste, sem ligar Docker, criar banco ou publicar nada.

## Executar ambiente didático (somente local)

```bash
docker compose -f docker-compose.yaml up --build -d
docker compose -f docker-compose.yaml ps
docker compose -f docker-compose.yaml logs --tail=100 nest next simulator
```

O frontend é acessível em `http://localhost:3001` e o NestJS em `http://localhost:3000`. As portas desses serviços e Mongo estão limitadas ao `127.0.0.1`.

O Compose principal **corrige a pasta Go para `golang-simulador/`** e define comandos reais dos serviços. Antes, os Dockerfiles dos subprojetos ficavam apenas em `tail -f /dev/null`; isso não inicia a aplicação. A raiz importa Mongo e Kafka uma vez para evitar conflitos.

## Segurança e limitações

**Ambiente exclusivamente de desenvolvimento.** O exemplo MongoDB usa `root/root`; o Kafka tem listeners PLAINTEXT e portas expostas pelo submódulo. Não abra portas no roteador/firewall e não use essas credenciais/dados em produção. Os pins dos submódulos são commits específicos — `git submodule update --remote` pode alterar os códigos e requer nova validação.

O GitHub Actions verifica configuração e checkout, **não** executa integração real de containers, Google Maps, Socket.IO ou eventos GPS. As dependências externas podem precisar de configuração e APIs válidas para funcionar.

[Arquitetura](docs/ARQUITETURA.md) · [Requisitos](docs/REQUISITOS.md) · [UML](docs/UML.puml) · [Plano de testes](docs/PLANO_TESTES.md).

---

## Documentação original preservada

# Imersão Fullcycle 20 - Sistema de rastreamento de veículos

![Imersão Full Stack && Full Cycle](https://events-fullcycle.s3.amazonaws.com/events-fullcycle/static/site/img/grupo_4417.png)

Participe gratuitamente: https://imersao.fullcycle.com.br/

## Requerimentos

Cada projeto tem seus próprios requerimentos, mas uma ferramenta é comum a todos: o Docker.

### Docker

Dependendo do seu sistema operacional, você tem 2 opções para instalar o Docker:

- [Docker Desktop] - Interface gráfica para gerenciar e usar o Docker.
- [Docker Engine] - Apenas a engine do Docker, sem interface gráfica, chamado de Docker Nativo.

Se você tem 8GB ou menos de memória RAM, recomendamos o uso do Docker Engine, pois a interface gráfica do Docker Desktop + a execução dos containers pode consumir praticamente a memória da máquina, caso contrário usar o Docker Desktop é mais prático.

Se você quiser saber mais detalhes sobre isto, veja nosso vídeo [https://www.youtube.com/watch?v=99dCerRKO6s](https://www.youtube.com/watch?v=99dCerRKO6s).

Se você estiver no Windows, use o WSL 2. Veja nosso tutorial [https://github.com/codeedu/wsl2-docker-quickstart](https://github.com/codeedu/wsl2-docker-quickstart).

## Rodar a aplicação

Rode todas as aplicações com o comando:

```bash
docker-compose up -d
```

Este comando irá subir todos os containers necessários para rodar todo o projeto

Acesse as pastas `golang-simulator`, `nestjs-api` e `next-frontend` e siga as instruções.

Como você já vai ter rodado todos os containers com o comando acima, mas instruções pule o passo de *levantar os containers*


## Arquitetura do projeto

![alt text](./arquitetura_projeto.png)
