
import streamlit as st
from justwatch import JustWatch

# Platform map to JustWatch internal provider names
PLATFORMS = {
    'Netflix': 'nfx',
    'Amazon Prime Video': 'prime_video',
    'Disney+': 'disney',
    'Apple TV+': 'atp',
    'Paramount+': 'prmt',
    'BBC iPlayer': 'bbciplayer',
    'All 4': 'all4',
    'ITVX': 'itvx',
}

# Genres from JustWatch
GENRES = [
    'action', 'adventure', 'animation', 'comedy', 'crime', 'documentary',
    'drama', 'fantasy', 'history', 'horror', 'kids', 'music',
    'mystery', 'romance', 'sci-fi', 'sport', 'thriller', 'war', 'western'
]

# UI
st.set_page_config(page_title="Movie & TV Finder", layout="wide")
st.title("🎬 Movie & TV Finder Agent")

country = st.selectbox("🌍 Select your country", ['GB', 'US', 'IT', 'DE', 'FR', 'ES'], index=0)
genre = st.selectbox("🎭 Genre", GENRES, index=GENRES.index('horror'))
platforms = st.multiselect("📺 Streaming platforms", list(PLATFORMS.keys()), default=['Amazon Prime Video'])
min_rating = st.slider("⭐ Minimum TMDB rating (0–100)", 0, 100, 80)
content_type = st.radio("🎞️ Content type", ['movie', 'show'], index=0)

# Button
if st.button("🔍 Find Titles"):
    st.info("Searching JustWatch…")
    justwatch = JustWatch(country=country)

    provider_ids = [PLATFORMS[p] for p in platforms]
    content = 'show' if content_type == 'show' else 'movie'

    results = justwatch.search_for_item(
        content_types=[content],
        genres=[genre],
        providers=provider_ids,
        monetization_types=['flatrate'],
        scoring_filter={'tmdb:score': min_rating / 10}
    )

    items = results.get('items', [])

    if not items:
        st.warning("No matching titles found.")
    else:
        for item in items[:10]:
            title = item.get('title')
            year = item.get('original_release_year', '')
            url = f"https://www.justwatch.com{item['full_path']}"
            score = item.get('scoring', [{}])[0].get('value', '?')
            img_url = f"https://images.justwatch.com{item['poster'].get('url')}.sxs" if item.get('poster') else None

            st.markdown(f"### [{title} ({year})]({url})")
            if img_url:
                st.image(img_url, width=150)
            st.markdown(f"⭐ **TMDB**: {round(score * 10, 1)}/100")
            st.markdown("---")
