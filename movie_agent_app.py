
import streamlit as st
import requests

API_KEY = "250ec77960426ade4b83d7086b2d41fa"
BASE_URL = "https://api.themoviedb.org/3"

# Supported platforms and their TMDB provider IDs
PLATFORMS = {
    'Netflix': 8,
    'Amazon Prime Video': 9,
    'Disney+': 337,
    'Apple TV+': 350,
    'Paramount+': 531,
}

# Get genre list from TMDB
@st.cache_data
def get_genres():
    url = f"{BASE_URL}/genre/movie/list?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    genres = response.json().get('genres', [])
    return {genre['name'].lower(): genre['id'] for genre in genres}

GENRES = get_genres()

# Streamlit UI
st.set_page_config(page_title="TMDB Movie & TV Finder", layout="wide")
st.title("🎬 TMDB Movie & TV Finder")

country = st.selectbox("🌍 Select your country", ['GB', 'US', 'IT', 'DE', 'FR', 'ES'], index=0)
media_type = st.radio("🎞️ Content type", ['movie', 'tv'], index=0)
genre = st.selectbox("🎭 Genre", list(GENRES.keys()), index=list(GENRES.keys()).index('horror'))
platforms = st.multiselect("📺 Streaming platforms", list(PLATFORMS.keys()), default=['Amazon Prime Video'])
min_rating = st.slider("⭐ Minimum TMDB average vote (0–10)", 0.0, 10.0, 7.0, 0.1)

if st.button("🔍 Search"):
    with st.spinner("Searching TMDB..."):
        results = []

        for platform in platforms:
            provider_id = PLATFORMS[platform]
            url = f"{BASE_URL}/discover/{media_type}"
            params = {
                'api_key': API_KEY,
                'language': 'en-US',
                'sort_by': 'popularity.desc',
                'with_watch_providers': provider_id,
                'watch_region': country,
                'with_genres': GENRES[genre],
                'vote_average.gte': min_rating,
                'page': 1
            }
            r = requests.get(url, params=params)
            if r.status_code == 200:
                results.extend(r.json().get('results', []))
            else:
                st.error(f"TMDB request failed: {r.status_code}")
                st.stop()

        if not results:
            st.warning("No matching titles found.")
        else:
            for item in results[:10]:
                title = item.get('title') or item.get('name')
                year = (item.get('release_date') or item.get('first_air_date') or '')[:4]
                vote = item.get('vote_average', '?')
                overview = item.get('overview', '')
                poster_path = item.get('poster_path')
                poster_url = f"https://image.tmdb.org/t/p/w300{poster_path}" if poster_path else None
                tmdb_url = f"https://www.themoviedb.org/{media_type}/{item['id']}"

                st.markdown(f"### [{title} ({year})]({tmdb_url})")
                if poster_url:
                    st.image(poster_url, width=150)
                st.markdown(f"⭐ **TMDB rating**: {vote}/10")
                st.markdown(f"📝 {overview}")
                st.markdown("---")
