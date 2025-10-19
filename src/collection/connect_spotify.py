import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
from pprint import pprint
import sys

def main():
    # Carregar as variáveis de ambiente do arquivo .env
    load_dotenv()

    CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

    if not CLIENT_ID or not CLIENT_SECRET:
        print("Erro: Credenciais 'SPOTIPY_CLIENT_ID' ou 'SPOTIPY_CLIENT_SECRET' não encontradas.")
        print("Por favor, crie um arquivo .env na raiz do projeto e adicione suas credenciais.")
        sys.exit(1)

    print("Credenciais carregadas com sucesso.")

    try:
        auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

        # Instância do cliente Spotify
        sp = spotipy.Spotify(auth_manager=auth_manager)
        print("Autenticação com a API do Spotify realizada com sucesso!")

        '''
            FAZER A BUSCA DE UM ARTISTA AQUI
            pelo que eu entendi, basta pegar a URI do artista no spotify
            e usar o método artist() da biblioteca spotipy para buscar os dados e printar no terminal

            Exemplo abaixo:
        '''

        artist_uri = 'spotify:artist:2yNNYQBChuox9A5Ka93BIn'
        print(f"\nBuscando dados para o artista URI: {artist_uri} ...")

        artist_data = sp.artist(artist_uri)

        print("\n--- DADOS DO ARTISTA OBTIDOS ---")
        pprint(artist_data)
        print("----------------------------------")

        print(f"\nNome: {artist_data['name']}")
        print(f"Gêneros: {artist_data['genres']}")
        print(f"Seguidores: {artist_data['followers']['total']}")

        print("\nTarefa da Semana 1 (Script de Autenticação e Coleta) concluída com sucesso.")

    except spotipy.SpotifyException as e:
        print(f"Erro durante a chamada da API do Spotify: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main()