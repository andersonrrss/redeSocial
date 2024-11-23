# Rede Social - Lily

Uma rede social não muito sofisticada, com apenas o "essencial", como seguir pessoas, postar publicações e conversar.
## Como rodar?
1. Compile os arquivos de TS para JS, usando o comando ```tsc``` dentro da pasta raiz do projeto
2. Compile o css do tailwind com o comando `npx tailwindcss -i static/css/src/input.css -o static/css/output.css` dentro da pasta `api`, e se por um acaso for desenvolver alguma interface use o comando `npx tailwindcss -i static/css/src/input.css -o static/css/output.css --watch` para que o tailwind compile de maneira automática.
3. Faça o download das bibliotecas pelo `requirements.txt` usando o comando ```pip install -r requirements.txt```
4. Rode o ```app.py``` dentro da pasta `api` por exemplo, usando o comando ```python api/app.py ``` na raiz do projeto

## A fazer:
- Implementar os comentários
- Excluir mensagens
- Refazer campo de envio de mensagens para que obedeça a formatação que o usuário desejar
- Terminar as funções de edição de perfil
- Refazer a interface de edição de perfil

## Como está organizado o projeto?

### Arquivos Python
1. `app.py` é o principal arquivo do servidor do projeto armazenando todas as transferências de dados e as rotas da rede social
- o arquivo `app.py` configura a rede social usando o `config.py`
2. `models.py` é o arquivo de modelo para o banco de dados
3. `helpers.py` contém algumas funções úteis que são usadas no `app.py` _eu preciso usar mais esse arquivo_
4. `requirements.txt` é o arquivo que armazena todas as dependências dos códigos em Python, use-o para instalar as bibliotecas necessárias usando o comando `pip install -r requirements.txt`
### Arquivos `.html`
*TODOS* os arquivos `.html` estão dentro da pasta `template`. O código `macros.html` é quase um `helpers.py` guardando alguns códigos jinja tanto para melhorar a legibilidade do código quanto para evitar que eu copie o mesmo código várias vezes(como o macro `render_post`).

### Pasta `static`
Dentro da pasta `static` estão todos os arquivos `.css`, `.js` e todos os arquivos de fotos da rede social como as fotos de perfil e as fotos dos posts

### Arquivos `.ts`
Os arquivos `.ts` estão TODOS localizados dentro da pasta `api/src`. O arquivo `tsconfig.json` está configurado para compilar os arquivos `.ts` em arquivos `.js` na pasta `api/static/js`.