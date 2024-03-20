import base64
from requests import post, get
import json

def get_token():
    # Spotify API token, registered in https://developer.spotify.com/dashboard creat a app and there are the Client_ID and Client_Secret in the settings
    auth_string = "Client_ID" + ":" + "Client_Secret" 
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {"Authorization": "Basic " + auth_base64,
               "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, data=data, headers=headers)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = 'http://api.spotify.com/v1/search'
    header = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=1"

    query_url = url + '?' + query
    result = get(query_url, headers=header)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist found")
        return None
    return json_result[0]

def get_song_artist(token, artist_id):
    url = f"http://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=DE"# DE = Germany
    header = get_auth_header(token)
    result = get(url, headers=header)
    json_result = json.loads(result.content)["tracks"]
    return json_result

token = get_token()
artist_info = search_for_artist(token, "ACDC") # Artist name for search

if artist_info:
    artist_id = artist_info["id"]
    songs = get_song_artist(token, artist_id)
    print("Top-Songs von AC/DC:")
    for song in songs:
        print("- " + song["name"])