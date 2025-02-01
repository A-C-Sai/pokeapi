import requests
import streamlit as st

base_url = "https://pokeapi.co/api/v2"

def get_pokemon_data(name):
    url = "{}/pokemon/{}/".format(base_url, name)

    try:
        response = requests.get(url)
        response.raise_for_status()
        pokemon_data = response.json()
        return pokemon_data
    except requests.exceptions.HTTPError as http_err:
        st.error(f"Invalid Pokémon name. Please check your input. (HTTP {http_err})")
    except requests.exceptions.RequestException as req_err:
        st.error("Failed to retrieve data. Please check your internet connection.")
    
    return None

st.set_page_config(page_title="Pokemon", layout="wide", initial_sidebar_state="expanded")
pokemon = st.sidebar.text_input("Enter a Pokémon name:")
btn = st.sidebar.button("Search Stats")

if btn:
    if pokemon:
        pokemon_data = get_pokemon_data(pokemon.strip().lower())

        if pokemon_data:
            name = pokemon_data["name"]
            abilities = [ability["ability"]["name"] for ability in pokemon_data["abilities"]]
            base_stats = [(stat["stat"]["name"],stat["base_stat"]) for stat in pokemon_data["stats"]]
            img = pokemon_data["sprites"]["other"]["official-artwork"]["front_default"]
            audio = pokemon_data["cries"]["latest"]

            st.title(name.strip().capitalize())
            st.image(img)

            st.divider()

            st.subheader("Stats")
            cols= st.columns(len(base_stats))
            for col,(stat,val) in zip(cols,base_stats):
                col.metric(stat.upper(),value=val,border=True)
            
            st.divider()

            st.subheader("Abilities")
            for ability in abilities:
                st.write(f"- {ability.capitalize()}")

            st.divider()

            st.subheader("Cry")
            col1,_,_ = st.columns(3)
            col1.audio(audio)

    else: 
        st.warning("Please enter a Pokémon name.")