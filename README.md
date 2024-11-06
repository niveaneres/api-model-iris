# API Model Iris

Esse projeto consiste em um aplicação em Python que realiza inferência de um modelo pré-treinado, que é capaz de realizar classificações utilizando características como comprimento e largura de pétalas e sépalas, retornando uma das três espécies de íris: Iris-setosa, Iris-versicolor e Iris-virginica. 

## Instalação
#### Clone o repositório
```bash
git clone https://github.com/niveanfj/api-model-iris.git
```

#### Acesse o diretório do repositório
```bash
cd api-model-iris
```  

#### Crie um ambiente virtual (recomendado)
Sinta-se a vontade para usar outro gerenciador de pacotes, neste exemplo usaremos anaconda.
```bash
conda create -n env-api-model-iris python=3.11
```
Ativando o ambiente:
```bash
conda activate env-api-model-iris
```


#### Realize a instalação das bibliotecas necessárias
```bash
pip install -r requirements.txt
```
#### Execute a aplicação
```bash
flask --app app run
```

## Endpoints
A API possui os seguintes endpoints:
#### status
* Método: GET <br>
* URL: http://127.0.0.1:5000/status <br>
* Descrição: Retorna o status da API

#### inference
* Método: POST <br>
* URL: http://localhost:5000/inference/ <br>
* Descrição: 
Recebe um JSON com as features para inferência e retorna a classe correspondente. 

## Exemplo de uso da API:
```python
import requests
url = 'http://localhost:5000/inference/'

data = {
    "SepalLengthCm": 0.0, 
    "SepalWidthCm": 1.5799999999999, 
    "PetalLengthCm": 5, 
    "PetalWidthCm": -1.0
}

response = requests.post(url, json=data)
print("Resposta:", response.json())
```
Resposta:
```python   
Resposta: {'category': 'Iris-versicolor'}
```
## Docker

A aplicação também pode ser utilizada com docker, através da porta 9002.<br><br>
http://localhost:9002/status  <br>
http://localhost:9002/inference/

Para facilitar a usabilidade, utilize os comandos com Make. Assim, para construir a imagem e executar o container, basta executar:   
```makefile
make run
```
Para parar:
```makefile
make stop
```
Para parar, apagar o container e a imagem:
```makefile 
make clean
```
 
## Estrutura do código
#### Estrutura de pastas
```
.
└── api-model-iris/
    ├── lmodel/
    │   ├── artifacts
    │   │   └──iris.pkl
    │   └── __init__.py
    │   ├── model.py
    │   └── services.py
    ├── tests/
    │   └── __init__.py
    │   ├── test_app.py
    │   └── test_model.py
    ├── app.py
    ├── Dockerfile
    ├── Makefile
    ├── requirements.txt
    └── README.md
```

#### Principais funções/arquivos
* __lmodel/model.py__: 
  * Contém a classe "ModelHandler" para manipulação do modelo, responsável pelo carregamento, inferência e atribuição do nome da classe detectada quando receber o atributo de label (class_name).
* __lmodel/services.py__: 
  * Contém as funções para validar se o JSON de entrada é valido e corresponde as features esperadas pelo modelo. <br> 
  * Possui também a função "run_inferece", responsável por transformar o JSON em um dataframe pandas e rodar a inferência no modelo.<br><br> Obs: A transformação em dataframe garante que os valores estejam atrelados a cada feature, evitando que caso os dados estejam desordenados no JSON sejam interpretados de maneira errônea pelo modelo.
* __app.py__: 
  * Configuração do log, para exibir o estado/progresso dos processos realizados dentro da aplicação;
  * Instanciando o modelo, essa etapa é realizada aqui e o modelo passado como parâmetro para as demais funções, para que no caso de múltiplas inferências o processo não torne a API lenta ao carregar o modelo a cada predição.
  * Definição das rotas necessárias (status, inference) e implementação da logica necessária para realizar as inferências.
* __tests__: 
  * Testes unitários, para garantir que as funções principais do modelo continuem funcionando após modificações no código. Eles validam que, caso haja alterações, o comportamento da aplicação permaneça o mesmo. 

## Ferramentas utilizadas
* __Flask__: Utilizado para criar a API que serve o modelo de machine learning, permitindo que o modelo seja acessado via requisições HTTP de forma simples e escalável.

* __Sklearn__: Usado para desenvolver e treinar o modelo de machine learning, fornecendo uma vasta gama de algoritmos e ferramentas de pré-processamento eficientes e fáceis de integrar.

* __Pandas__: Ferramenta essencial para manipulação e análise de dados, permitindo o carregamento, limpeza e transformação eficiente dos dados antes do treinamento e da previsão do modelo.

* __Docker__: Utilizado para criar containers que encapsulam a aplicação e o modelo, garantindo que o ambiente de execução seja reproduzível e independente da infraestrutura.

* __Pytest__: Framework de testes usado para garantir a qualidade do código, permitindo a automação dos testes unitários e a verificação contínua da funcionalidade da aplicação.



## Melhorias

  * __Monitoramento__:<br> Implementaria uma ferramenta de monitoramento, como o MLflow, para registrar as versões do modelo, além de acompanhar as métricas de desempenho. Faria a rastreabilidade do modelo, verificando o desempenho ao longo do tempo e integrando com validação de data drift, para garantir que caso tenha desvio nos dados de entrada seja identificado e integraria testes A/B para avaliar a performance do modelo.

  * __Pipeline CI/CD__: <br> Criaria um pipeline de integração contínua (CI) e entrega contínua (CD) para garantir que o código seja automaticamente testado, validado e implantado em produção. Esse pipeline realizaria a execução de testes unitários, validação do modelo e verificação de métricas de desempenho antes de subir o código. 
   
  * __Escalabilidade__: <br> Utilizaria o Kubernetes para gerenciar a infraestrutura e garantir a escalabilidade do modelo conforme a demanda. Orquestrando os containers e distribuindo a carga de trabalho entre diferentes nós e, quando necessário, subir novos nós automaticamente para lidar com picos de tráfego.



