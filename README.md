# Projeto Spotify Big Data
Projeto acadêmico desenvolvido para a disciplina de BI e Big Data. O objetivo é construir um pipeline de engenharia de dados completo, desde a coleta até a modelagem, utilizando dados públicos da API do Spotify.

Este pipeline coleta dados de artistas, álbuns e músicas (incluindo *audio features*), armazena os dados brutos (JSON) em um ambiente NoSQL e, em seguida, utiliza o Spark para processar e transformar esses dados em um modelo dimensional (Fato e Dimensões) otimizado para análises.

## 🛠️ Tecnologias Utilizadas

* **Fonte de Dados:** Spotify Web API
* **Coleta & Autenticação:** Python (com a biblioteca `Spotipy`)
* **Armazenamento (Data Lake):** MongoDB Atlas
* **Processamento (ETL):** Apache Spark (via Databricks)
* **Armazenamento (Data Warehouse):** Formato Parquet

## 🚀 Como Executar o Projeto

```bash
git clone [https://github.com/mygk-bea/spotify-big-data.git]
cd spotify-big-data

# Crie o ambiente virtual (uma pasta chamada 'venv')
python -m venv venv
.\venv\Scripts\activate

# Instala todas as bibliotecas listadas no requirements.txt
pip install -r requirements.txt

# Cria um .env baseado no molde
copy .env.example .env

python src/collection/connect_spotify.py
```