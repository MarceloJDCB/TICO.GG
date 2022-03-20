# TICO.GG

![TICOGG1](https://i.imgur.com/i12rUYb.png)

------------

##   Vamos começar respondendo algumas perguntas que você possa ter em mente

#### 1. P: Quem é você e por que você resolveu publicar esse protótipo de api baseada em estatística de lol open source?
#### R: Meu nome é Marcelo, tenho 20 anos e adoro programar :) . Resolvi fazer este projeto por conta de um insight que tive com um amigo após de descobrir que a api da Riot era aberta para quem quisesse explorar e criar projetos de grande porte ou apenas para uso pessoal, ambos chegamos a conclusão que seria muito diferenciado ter um projeto envolvendo data analysis de lol =D (Descobri pouco tempo depois que iria me custar algumas horas de sono e um pouquinho de cabelo hehehe...)
#### 2. P: Você é um programador experiente?
#### R: Profissionalmente tenho poucos meses de experiência porém eu já tenho ciência do que é programação desde os 11 anos de idade (fazia códigos bobinhos em vb.net) e estudo de uma maneira séria desde 2017. Sendo sincero fiz este protótipo inteiro a base de café, documentações (Django, Celery, Python e RIOT API) e stackoverflow (e alguns outros sites de artigos de programação).  Você poderá ver ao longo desse repositório que os códigos não são de um programador senior e que podem ser otimizados, erros que podem ser corrigidos , etc...
#### 3. P: Quem é tico?
#### R: Meu doguinho <3
#### 4. P: Por que django?
#### R: Porque é uma boa tecnologia que eu pretendo masterizar , trabalhar e além de tudo é um framework feito em python (Uma linguagem muito querida por mim) , então preciso de bastante prática e experiências diversas.
#### 5. P: Por que você escolheu a biblioteca celery para executar requests?
#### R: Porque é uma excelente biblioteca que nos habilita de um jeito simples a fazer multiplas tarefas ao mesmo tempo. Por exemplo quando pegamos uma lista de 10 partidas em um codigo inline ele executaria cada uma linha por linha esperando uma terminar para começar a outra, com celery conseguimos distribuir essa lista para vários childs de workers disponíveis e executar várias partidas ao mesmo tempo fazendo com que o tempo de espera seja dividido pelos childs e caía drásticamente. A sua implementação não está 100% completa mas no futuro pretendo adicionar alguns comandos interessantes a mais como: Tratamento de erros nas consultas, reiniciar uma tarefa específica quando algo da errado , etc...

------------
## Como faço para ter acesso a API na minha máquina?
### 1. Instale e configure o RabbitMQ no seu computador (Mensageiro que será usado pelo celery)
### [Rabbit MQ](https://www.rabbitmq.com/download.html "Rabbit MQ")
### 2. Abra o CMD (Win + R / CMD /  ENTER)
### 3. Vá até o diretório da pasta aonde você extraiu a api usando o comando 
`cd ...TICO.GG\TICOBackend` 
### 4. Rode os próximos comandos: 

`python -m venv venv`

`venv\Scripts\activate.bat`

`python manage.py create superuser`  

`python manage.py runserver`

### 5. Caso não rode de primeira execute os comandos no mesmo diretório:

`venv\Scripts\activate.bat`

`pip install -r requirements.txt`

`python manage.py migrate` 

`python manage.py makemigrations`

## Rodando o Celery ~alguns comandos importantes
### Iniciando o celery (Nota: você precisa iniciar o celery para que o algoritmo que busca o jogador funcione):
`celery -A core worker -l INFO -P gevent --loglevel=info`
### Iniciando o celery beat (Esta parte é para quem decida ir a fundo e queira fazer modificações no código para adicionar funções agendadas duranteo  tempo)
`celery -A core beat -l info`


------------
## Endpoints e seu uso correto:

- ### requestPlayer

#### input name
#### output: player info
#### exemplo de input:
`{
"name":"player"
}`

- ### getMatch

#### input matchid
#### output: match info
#### exemplo de input:
`{
"matchid":"match_id"
}`
#### input matchid e puuid
#### output: match info do player
#### exemplo de input:
`{
"matchid":"matchid",
"player":"puuid"
}`

- ### getTimeLine

#### input matchid
#### output: match time line info
#### exemplo de input:
`{
"matchid":"match_id"
}`
#### input matchid e name
#### output: time line do player
#### exemplo de input:
`{
"matchid":"matchid",
"name":"player_name"
}`

- ### getRune

#### input id
#### output: rune info
#### exemplo de input:
`{
"id":"rune_id"
}`
#### input rune list id
#### output: runes info
#### exemplo de input:
`{
"runes":[
{"id":"rune_id1"},
{"id":"rune_id2"}
]
}`
- ### getItem

#### input id
#### output: item info
#### exemplo de input:
`{
"id":"item_id"
}`
#### input item list id
#### output: items info
#### exemplo de input:
`{
"items":[
{"id":"item_id1"},
{"id":"item_id2"}
]
}`

#### Bom por enquanto é isto pessoal, irei continuar atualizando esse repositório conforme avanços no projeto e novos contribuidores :)

![TICOGG2](https://i.imgur.com/LUwuQUq.png)
