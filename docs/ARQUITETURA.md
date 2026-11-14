# Arquitetura — sistema Full Cycle de rastreamento

Versão TRACK-COMPOSE 1.1.0 · 14/11/2026.

## Estrutura realmente versionada

O repositório pai é um **orquestrador de quatro submódulos Git**, mais MongoDB local. A pasta Go chama-se **`golang-simulador/`**, não `golang-simulator/` — o antigo include usava caminho inexistente.

| Diretório | Responsabilidade | Pin desta revisão |
| --- | --- | --- |
| `nestjs-api/` | API REST, Google Maps, eventos e Socket.IO | `a6c9f69c54f7` |
| `golang-simulador/` | Eventos de frete/posição e consumidor Kafka | `a33d35f12651` |
| `next-frontend/` | Páginas de rotas e mapas Next.js/React | `3093a5a2e884` |
| `kafka/` | Kafka + ZooKeeper + ferramentas de desenvolvimento | `059c9095bdb0` |
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
