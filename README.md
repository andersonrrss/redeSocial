# Rede Social - Lily

Uma rede social não muito sofisticada, com apenas o "essencial", como seguir pessoas, postar publicações e conversar.
## Como rodar?
1. Faça o download das bibliotecas pelo `requirements.txt` usando o comando ```pip install -r requirements.txt```
2. Faça o download das dependências do Frontend usando ```npm install```
3. Rode o aplicativo usando o comando ```python -m app.run```, o código vai compilar automaticamente o typescript e o tailwind, se algum erro ocorrer, você pode tentar resolver ou compilá-los manualmente usando os comandos abaixo
4. Em caso de erro compile o css do tailwind com o comando `npx tailwindcss -i app/static/css/src/input.css -o app/static/css/output.css` e adicione `--watch` ao final do comando se quiser que o código compile enquanto você o muda
5. Em caso de erro compile o Typescript apenas usando o comando `tsc`

## A fazer:
- Implementar os comentários
- Excluir mensagens
- Refazer campo de envio de mensagens para que obedeça a formatação que o usuário desejar
- Terminar as funções de edição de perfil
- Refazer a interface de edição de perfil
