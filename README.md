# TICO.GG

![TICOGG1](https://i.imgur.com/i12rUYb.png)

------------

##   Vamos começar respondendo algumas perguntas que você possa ter em mente

#### P: Quem é você e por que você resolveu publicar esse protótipo de api baseada em estatística de lol open source?
#### R: Meu nome é Marcelo, tenho 20 anos e adoro programar :) . Resolvi fazer este projeto por conta de um insight que tive com um amigo após de descobrir que a api da Riot era aberta para quem quisesse explorar e criar projetos de grande porte ou apenas para uso pessoal, ambos chegamos a conclusão que seria muito diferenciado ter um projeto envolvendo data analysis de lol =D (Descobri pouco tempo depois que iria me custar algumas horas de sono e um pouquinho de cabelo hehehe...)
#### P: Você é um programador senior?
#### R: Não, sendo sincero fiz este protótipo inteiro a base de café, documentações e stackoverflow (e alguns outros sites de artigos de programação).  Você poderá ver ao longo desse repositório que os códigos não são de um programador senior e que podem ser otimizados, erros que podem ser corrigidos , etc...
#### P: Quem é tico?
#### R: Meu doguinho <3

#### P: Por que django?
#### R: Porque é uma boa tecnologia que eu pretendo masterizar e trabalhar , então preciso de bastante prática e experiências diversas.

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


#### Bom por enquanto é isto pessoal, irei continuar atualizando esse repositório conforme avanços no projeto e novos contribuidores :)

![TICOGG2](https://i.imgur.com/LUwuQUq.png)
