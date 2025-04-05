# Worst Movie API
API RESTful para leitura da lista de indicados e vencedores da categoria Pior Filme do Golden Raspberry Awards.

# Preparação Ambiente
Esta aplicação foi desenvolvida para ser containerizada, então é necessário ter o **docker** e o **docker compose** instalados na sua máquina.

Após clonar este repositório para a sua máquina local e antes de colocar a aplicação no ar, você precisa seguir dois passos:
 1. Salvar o arquivo `.csv` que será utilizado no diretório `./data`, respeitando o formato de colunas: 
     - `year;title;studios;producers;winner`
 2. Criar um arquivo `.env` dentro do diretório `./backend`, com o conteúdo abaixo variáveis:
    ```
    DJANGO_SUPERUSER_USERNAME=<username do superuser>
    DJANGO_SUPERUSER_EMAIL=<email do superuser>
    DJANGO_SUPERUSER_PASSWORD=<senha do superuser>
    SECRET_KEY=<chave secreta da aplicação, pode ser uma que você gerar>
    DADOS=<Nome do arquivo `.csv` salvo no passo anterior>
    ```

# Deploy
Com o ambiente preparado, dentro do diretório raiz do projeto execute os dois comandos abaixo em sequência:

```bash
docker compose build
docker compose up
```

A aplicação estará disponível no url http://0.0.0.0:8000/ ou http://localhost:8000/, dispondo também dos end-points abaixo:
 - `/api/movies/`: Retorna todos os filmes que concorreram ou foram premiados
 - `/api/studios/`: Retorna todos os estúdios cujos filmes concorreram ou foram premiados
 - `/api/producers/`: Retorna todos os produtores cujos filmes concorreram ou foram premiados
 - `/api/producers/minmaxpyai/`: Retorna o produtor com maior intervalo entre dois prêmios consecutivos, e o que obteve dois prêmios mais rápido
 - `/api/awards/`: Retorna todos as premiações realizadoas, com concorrentes e premiados.

# Testes
Para executar os testes entre no container que está rodando com o comando:
```bash
docker exec -it <CONTAINER ID> bash
```
Caso não saiba o `<CONTAINER ID>`, execute o comando abaixo para descobrir
```bash
docker ps
```
Já dentro do terminal do container execute o comando abaixo para rodar os testes:
```python
python manage.py test
```
