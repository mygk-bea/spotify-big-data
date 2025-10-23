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

        # exemplo demonstrando a captura de dados de um artista
        taylor_uri = 'spotify:artist:06HL4z0CvFAxyc27GXpf02'
        taylor_data = sp.artist(taylor_uri)

        # exemplo demonstrando a captura de dados de albuns
        red_uri = 'spotify:album:6kZ42qRrzov54LcAk4onW9'
        # simplificando para pegar somente do market do Brasil
        red_data = sp.album(red_uri, market="BR")

        print("\n--- DADOS BRUTOS DA TAYLOR SWIFT ---")
        print(taylor_data)
        print("----------------------------------")

        print("--- DADOS SELECIONADOS DA TAYLOR SWIFT ---")
        # dados importantes requisitados pelo Termo de Abertura
        print(f"ID: {taylor_data['id']}")
        print(f"Nome: {taylor_data['name']}")
        print(f"Seguidores: {taylor_data['followers']['total']}")
        print(f"Popularidade: {taylor_data['popularity']}")
        # o campo de gêneros da Taylor é vazio mesmo, foi verificado
        print(f"Gêneros: {taylor_data['genres']}")
        print("----------------------------------")

        print("--- DADOS SELECIONADOS DO ALBUM RED ---")

        # verificação do recebimento de dados
        # print(red_data)

        # dados importantes requisitados pelo Termo de Abertura
        print(f"ID: {red_data['id']}")
        print(f"Título: {red_data['name']}")
        print(f"Tipo de álbum: {red_data['album_type']}")
        print(f"Data de lançamento: {red_data['release_date']}")

        print("\nTarefa da Semana 1 (Script de Autenticação e Coleta) concluída com sucesso.")

    except spotipy.SpotifyException as e:
        print(f"Erro durante a chamada da API do Spotify: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main()