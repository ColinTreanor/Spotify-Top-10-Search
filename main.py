from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import streamlit as st


# -- STREAMLIT PAGE SETUP -- 
st.set_page_config(page_title="Spotify Search", page_icon="🎵", layout="wide")
st.markdown("<h1 style='text-align: center; color: #F0F8FF;'>🎵 Spotify Top 10 Search 🎵</h1>", unsafe_allow_html=True)
left_column, middle_column, right_column = st.columns(3)


#st.title(":green[:musical_note:]")
with middle_column:
    st.write("##")
    st.subheader("Enter your favorite Spotify artist here ⬇ to see their top 10 songs!")
    artist = st.text_input("Enter an artist")
    


# -- SPOTIFY API PROGRAM -- 
load_dotenv()

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")

# -- function that return the user token required for the api -- 
def get_token():
    # -- concat the id and secret -- 
    auth_string = client_id + ":" + client_secret 

    # -- encode the above string using utf-8 -- 
    auth_bytes = auth_string.encode("utf-8")

    # -- create a base64 string to be passed into the headers when request is sent to the spotofy accounts service api -- 
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")

    url = "https://accounts.spotify.com/api/token"

    headers = {
        # -- authorization header that will verify that everything is correct and then send back the token -- 
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    #-- spotify requires the parameter "grant_type" to be passed through as the name "client_credentials" -- 
    data = {"grant_type": "client_credentials"}

    # -- return json data in the content field -- 
    result = post(url, headers=headers, data=data)

    # -- convert the json string to a python dictionary and then parse the token -- 
    json_result = json.loads(result.content)
    token = json_result["access_token"]

    return token

# -- returns the authentication header to add simplicity in the code-- 
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# -- returns the json data of the specified artist -- 
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)   
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]

    if len(json_result)==0:
        print("No artists with this name")
        return None
    
    return json_result[0]

# -- returns the json data that contains the top 10 songs from the artist -- 
def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)   
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

if len(artist) != 0:
    token = get_token() 
    result = search_for_artist(token, artist)
    artist_id = result["id"]
    songs = get_songs_by_artist(token, artist_id)

# -- print songs -- 
if len(artist) != 0:
    with middle_column:
        st.write("Here are " + artist + " 's top 10 songs!")
        for idx, song in enumerate(songs):
            st.write(f"{idx + 1}. {song['name']}")


