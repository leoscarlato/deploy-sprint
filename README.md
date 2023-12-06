## Quadro Kanban Atualizado:

https://trello.com/invite/b/R4U47rtK/ATTId11d9405613afc78d801a59690aca25d4B992717/sprint-4

## Links Importantes (Entregas estão disponibilizadas no repositório e no link abaixo) :

https://docs.google.com/document/d/1AtBtWD_XQZTQGxew3lpobhV40u84v632ZA4rfMDdJX4/edit

# Descrição dos Diretórios

- ### **/notebooks**: Contém os notebooks da aplicação.
  - **modelos_regressao**: Notebook onde é feito os testes dos modelos de regressão.
  - **modelos_classificacao**: Notebook onde é feito os testes dos modelos de classificação.
  - **primeiras_analises**: Notebook onde foi desenvolvida nossa análise exploratória.
  - **analises_visuais**: Notebook composto majoritariamente de gráficos que nos auxiliaram no entendimento dos dados.
 
- ### **/modelos**: Contém os modelos da aplicação.
  - **classification_model**: Nosso melhor modelo de classificação.
  - **regression_model**: Nosso melhor modelo de regressão.

- ### **/data**: Possui os dados mensais disponibilizados pela empresa parceira divididos em pastas por mês.
  - **df_total**: Dados mensais concatenados após passarem pelo script "script_data_basico".

- ### **/scripts**: Contém os scripts que permitem a replicação do tratamento de dados.
  - **script_data_basico**: Script que possui o tratamento que deve ser aplicado nos dados independente do modelo escolhido de ML.
  - **script_data_classificacao**: Script que possui o tratamento que deve ser aplicado nos dados que serão utilizados em modelos de classificação (o script_data_basico deve ser aplicado antes).
  - **script_data_regressao**: Script que possui o tratamento que deve ser aplicado nos dados que serão utilizados em modelos de regressão (o script_data_basico deve ser aplicado antes).

- ### **/entregas**: Pasta com os documentos das entregas intermediárias.

- ### **/api**: Pasta da nossa Api.
  - **app.py**: 

- ### **/dash**:

- ### **/analise-colunas-iguais**: Pasta de analise de colunas
  - **dataCondensing**: Notebook que demonstra que parte das colunas possuem valores identicos independente do mês de retirada dos dados.

- ### **requirements.txt**: Arquivo com as dependências do nosso projeto






