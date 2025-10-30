import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
from pprint import pprint
from pymongo import MongoClient

# --- DADOS DO TERMO DE ABERTURA ---
ARTIST_URIs_TO_FETCH = {
    "Taylor Swift": "spotify:artist:06HL4z0CvFAxyc27GXpf02",
    "Dua Lipa": "spotify:artist:6M2wZ9GZgrQXHCFfjv46we",
    "Imagine Dragons": "spotify:artist:53XhwfbYqKCa1cC15pYq2q",
    "Arctic Monkeys": "spotify:artist:7Ln80lUS6He07XvHI8qqHH",
    "Kendrick Lamar": "spotify:artist:2YZyLoL8N0Wb9xBt1NhZWg",
    "Drake": "spotify:artist:3TVXtAsR1Inumwj472S9r4",
    "Anitta": "spotify:artist:7FNnA9vBm6EKceENgCGRMb",
    "Jão": "spotify:artist:59FrDXDVJz0EKqYg39dnT2",
    "Calvin Harris": "spotify:artist:7CajNmpbOovFoOoasH2HaY",
    "David Guetta": "spotify:artist:1Cs0zKBU1kc0i8ypK3B9ai"
}
# -----------------------------------

def get_spotify_client():
    load_dotenv()
    CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

    auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    token = auth_manager.get_access_token(as_dict=False)
    print(f"Token obtido com sucesso: {token[:20]}...")

    sp = spotipy.Spotify(auth=token)
    return sp

def collect_artist_data(sp, artist_uri):
    try:
        print(f"   Buscando dados do artista... (URI: {artist_uri})")
        artist_info = sp.artist(artist_uri)

        print("   Buscando top faixas...")
        top_tracks = sp.artist_top_tracks(artist_uri, country="BR")
        track_ids = [track['id'] for track in top_tracks['tracks']]

        # print("   Buscando 'audio features' das top faixas...")
        # audio_features = []
        # if track_ids:
        #     audio_features = sp.audio_features(tracks=track_ids)

        print("   Buscando álbuns...")
        albums_response = sp.artist_albums(artist_uri, album_type='album', country="BR", limit=2)

        # print("   Buscando artistas relacionados...")
        # related_artists = sp.artist_related_artists(artist_uri)

        artist_full_data = {
            "artist_info": artist_info,
            "top_tracks": top_tracks,
            "audio_features": None,
            "albums": albums_response,
            "related_artists": None
        }

        print(f"   Coleta para {artist_info['name']} concluída.")
        return artist_full_data

    except spotipy.SpotifyException as e:
        print(f"Erro durante a chamada da API do Spotify: {e}")
        return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado na coleta: {e}")
        return None

def get_mongo_collection():
    load_dotenv() # Carregas as credenciais do mongo
    # Atribui as credenciais a variáveis
    MONGO_URI = os.getenv("MONGODB_URI")
    MONGO_DB = os.getenv("MONGODB_DB")
    MONGO_COLLECTION = os.getenv("MONGODB_COLLECTION")

    # Cria o cliente, seleciona o banco e coleção
    client = MongoClient(MONGO_URI) 
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    print(f"Conectado ao MongoDB: {MONGO_DB}.{MONGO_COLLECTION}")
    return collection # Retorna a coleção, onde os dados serão gravados

def main():
    sp = get_spotify_client()
    all_collected_data = []
    collection = get_mongo_collection() # Chama a função get_mongo_collection

    print("\n--- INICIANDO COLETA EM LARGA ESCALA (SEMANA 2) ---")
    for artist_name, artist_uri in ARTIST_URIs_TO_FETCH.items():
        print(f"\nColetando dados para: {artist_name}...")
        
        data = collect_artist_data(sp, artist_uri)
        
        if data:
            all_collected_data.append(data)

            print(f"\n--- JSON BRUTO COLETADO PARA: {artist_name} ---")
            # Manda JSON para o MongoDB 
            collection.insert_one(data)
            print(f"   → Dados de {artist_name} inseridos com sucesso no MongoDB.")

            pprint(data)
            print("--------------------------------------------------")

    print("\n--- COLETA EM LARGA ESCALA CONCLUÍDA ---")
    print(f"Total de {len(all_collected_data)} artistas processados com sucesso.")

if __name__ == "__main__":
    main()