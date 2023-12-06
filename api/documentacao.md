# api.py

## Como rodar a API

### Instalar as dependências

Para baixar as dependências do projeto, basta executar o comando:

``` pip install -r requirements.txt ```

### Rodar a API

Para rodar a API, basta executar o comando:

``` python api.py ```

## Como utilizar a API


## Rotas :

- ### /classification/predict (POST) :

    - Rota utilizada para prever se o cliente vai ou não continuar com o plano no próximo mês.
    - Recebe um json com os dados do cliente, trata os dados e retorna a previsão em formato json na chave "prediction".

- ### /regression/predict (POST) :

    - Rota utilizada para prever o tempo em dias que o cliente vai continuar com o plano.
    - Recebe um json com os dados do cliente, trata os dados e retorna a previsão em formato json na chave "prediction".



## Exemplo de uso da API

### Json exemplo para requisição para ambas as rotas :

```
{"features" : {"birthdate":42.0,"id_gender":"64.0","id_marrital_status":82.0,"id_health_plan":"Outros","notes_count":0,"done_activities_count":5,"start_of_service":61.0,"Qde Todos Atendimentos":2,"Faltas Todos Atendimento":2,"F\u00edsico":3.0,"Psicol\u00f3gico":2.0,"Social":2.0,"Ambiental":3.0,"Mensagens Inbound":50.0,"Mensagens Outbound":45.0,"Liga\u00e7\u00f5es Inbound":0.0,"Liga\u00e7\u00f5es Outbound":0.0,"Qde Total de Tentativas de Cobran\u00e7a":1.0,"M\u00e9todo de Pagamento":"Cart\u00e3o de cr\u00e9dito","Qde Total de Faturas Inadimpletes":false,"Valor Total Inadimpl\u00eancia":0.0,"Tem Problema em Aberto":1,"Tempo \u00daltima Mensagem Inbound":39.0,"Tempo \u00daltima Mensagem Outbound":39.0,"Quem Enviou \u00daltima Mensagem":"Empresa"}}


```

### Exemplo de resposta da rota /classification/predict :

```
{
    "prediction": "False"
}

```


### Exemplo de resposta da rota /regression/predict :

```
{
    "prediction": 20.3577048604311
}

```



    
