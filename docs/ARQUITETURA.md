# Arquitetura — sistema Full Cycle de rastreamento

Versão TRACK-COMPOSE 1.2.0 · 14/11/2026.

## Estrutura realmente versionada

O repositório pai é um **orquestrador de quatro submódulos Git**, mais MongoDB local. A pasta Go chama-se **`golang-simulador/`**, não `golang-simulator/` — o antigo include usava caminho inexistente.

| Diretório | Responsabilidade | Pin desta revisão |
| --- | --- | --- |
| `nestjs-api/` | API REST, Google Maps, eventos e Socket.IO | `d65bff1ad157` |
| `golang-simulador/` | Eventos de frete/posição e consumidor Kafka | `0cb1073df2d4` |
| `next-frontend/` | Páginas de rotas e mapas Next.js/React | `89b66a567aca` |
| `kafka/` | Kafka + ZooKeeper + ferramentas de desenvolvimento | `a4b1cc83f7ba` |
| `mongodb/` | MongoDB local com replica set de nó único | Arquivos neste repo |

Gitlinks fixam SHAs: `git pull` do pai não atualiza automaticamente os submódulos para `main`. Use `git submodule update --init --recursive` para reproduzir a revisão do repositório pai.

## Docker Compose raiz

O Compose inclui **uma única vez** `mongodb/docker-compose.yaml` e `kafka/docker-compose.yaml`, depois define `simulator`, `nest` e `next` diretamente, evitando includes repetidos de Mongo/Kafka.

- `simulator`: `go run ./cmd/simulator`, Mongo `mongo:27017`, Kafka `kafka:9092`.
- `nest`: `npm ci && npx prisma generate && npm run start:dev`, porta host `127.0.0.1:3000`.
- `next`: `npm ci && npm run dev -- --hostname 0.0.0.0`, porta host `127.0.0.1:3001`.
- `mongo`: host `127.0.0.1:27017`, sem exposição direta a outras interfaces.
- `kafka`: serviços de desenvolvimento do submódulo, com listeners PLAINTEXT: `kafka:9092` interno e `localhost:9094` externo somente em loopback; Control Center em `localhost:9021`.

O endereço da API **interno** à rede Docker é `http://nest:3000`. O endereço acessado pelo **navegador** é `http://localhost:3000`. O proxy de rotas no Next fica em `http://localhost:3001/api`.

## Limites e segurança

O MongoDB do laboratório usa credenciais **root/root** do material didático. O Kafka usa listeners PLAINTEXT e uma console sem autenticação, agora com portas externas limitadas a 127.0.0.1; esta topologia **não é segura para produção nem para rede compartilhada**. Bloqueie as portas no firewall e use redes internas dedicadas. A chave `ROUTES_API_KEY` é exigida no `.env` local e não é versionada; chave Google Maps precisa de restrição por domínio/referrer.

A CI valida a estrutura de submódulos e a **configuração declarativa** do Compose. Ela **não sobe contêineres nem executa GPS/Google Maps/Kafka/Mongo E2E**. Os subprojetos incluem comandos de desenvolvimento; possíveis mudanças de API/versões devem ser homologadas com a infraestrutura ligada.

## Orçamento Kafka compartilhado pelo produtor e consumidor

Nesta revisão, os gitlinks de **NestJS** e **Go Simulator** apontam aos commits já integrados nas respectivas branches `main`:

- NestJS: `d65bff1ad1578321346015fc4d07a2ce47b051b5`.
- Go Simulator: `0cb1073df2d477e8d5796728e7b1c831325c9ee3`.

O produtor `RoutesService.create` valida o retorno de Google Directions antes de gravar dados e publica no máximo 600 coordenadas (300 etapas). O simulador recusa eventos JSON acima de 256 KiB e rotas acima de 600 pontos. Rotas inválidas ou excessivamente extensas precisam ser rejeitadas, corrigidas ou futuramente segmentadas. A verificação `tests/test_kafka_route_contract.py` impede divergência silenciosa desses limites nos submódulos fixados.

Essa checagem é estática; **não** executa Kafka/Mongo reais nem prova a entrega de eventos entre os processos.

## TRACK-COMPOSE 1.3.0 — NestJS e Next.js com credencial servidor-servidor

O gitlink `next-frontend/` foi atualizado para `89b66a567aca07570bfa247baf245b4d1723a766`. O backend exige `x-routes-api-key` para ações e consultas em `/routes`; o servidor Next fornece a credencial `ROUTES_API_KEY` recebida do mesmo `.env` local do orquestrador.

O navegador não recebe a chave em variáveis públicas. No entanto, a demonstração local ainda permite operações sem login quando `ALLOW_UNAUTHENTICATED_ROUTE_DEMO=true`, portanto **não é um controle de autorização real**. A CI verifica o mapeamento da chave nos dois contêineres e os binds de porta em loopback.

**Pendente:** identidade de operador, autorização por rota, segurança do Socket.IO, limitação de consultas Google Maps, E2E e isolamento por ambiente antes de exposição pública.

## TRACK-COMPOSE 1.4.0 — sincronização de eventos nativos no Kafka Python

- `kafka/`: novo pin `a4b1cc83f7baf72734e7786af2fa9b5a56dfffdb`.
- A CLI genérica segue produzindo envelopes com `tipo/dados`; a nova CLI `publicar-rastreamento` produz no tópico `route` os eventos planos `RouteCreated` e `DeliveryStarted`, como NestJS e Go.
- A verificação do repositório pai executa o serializer Kafka real do gitlink por `runpy`, valida o JSON e compara os limites de pontos com os contratos Nest/Go.
- O broker continua uma pilha didática com PLAINTEXT sem SASL; a compatibilidade estática não comprova entrega no Kafka ou processamento em MongoDB.
