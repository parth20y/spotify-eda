import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import duckdb
import os

# Page config
st.set_page_config(
    page_title="Spotify EDA Dashboard",
    page_icon="🎵",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    base = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base, '..', 'data', 'dataset.csv')
    df = pd.read_csv(data_path)
    df = df.drop_duplicates()
    df = df.dropna()
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
    df['duration_s'] = (df['duration_ms'] / 1000).round(1)
    return df

df = load_data()
con = duckdb.connect()
con.register('spotify', df)

# Sidebar filters
st.sidebar.title("🎵 Filters")
all_genres = sorted(df['track_genre'].unique().tolist())
selected_genres = st.sidebar.multiselect(
    "Select Genres",
    options=all_genres,
    default=all_genres[:8]
)

min_pop, max_pop = st.sidebar.slider(
    "Popularity Range",
    min_value=0, max_value=100,
    value=(0, 100)
)

# Filter data
filtered = df[
    (df['track_genre'].isin(selected_genres)) &
    (df['popularity'].between(min_pop, max_pop))
]

# Header
st.title("🎵 Spotify Tracks — EDA Dashboard")
st.markdown(f"Exploring **{len(filtered):,}** tracks across **{filtered['track_genre'].nunique()}** genres")

# KPI row
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Tracks", f"{len(filtered):,}")
col2.metric("Avg Popularity", f"{filtered['popularity'].mean():.1f}")
col3.metric("Avg Danceability", f"{filtered['danceability'].mean():.2f}")
col4.metric("Avg Energy", f"{filtered['energy'].mean():.2f}")
col5.metric("Avg Valence", f"{filtered['valence'].mean():.2f}")

st.divider()

# Row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Genres by Popularity")
    genre_pop = filtered.groupby('track_genre')['popularity'].mean().sort_values(ascending=False).reset_index()
    fig = px.bar(genre_pop, x='popularity', y='track_genre',
                 orientation='h', color='popularity',
                 color_continuous_scale='Greens',
                 labels={'popularity': 'Avg Popularity', 'track_genre': 'Genre'})
    fig.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Danceability vs Energy")
    fig2 = px.scatter(filtered.sample(min(3000, len(filtered))),
                      x='danceability', y='energy',
                      color='track_genre', opacity=0.5,
                      labels={'danceability': 'Danceability', 'energy': 'Energy'})
    fig2.update_traces(marker=dict(size=5))
    fig2.update_layout(legend=dict(font=dict(size=9)))
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Row 2
col1, col2 = st.columns(2)

with col1:
    st.subheader("Mood by Genre (Valence)")
    mood = filtered.groupby('track_genre')['valence'].mean().sort_values(ascending=False).reset_index()
    mood['mood'] = mood['valence'].apply(
        lambda x: 'Happy 😊' if x > 0.6 else ('Neutral 😐' if x > 0.4 else 'Sad 😢')
    )
    color_map = {'Happy 😊': '#1DB954', 'Neutral 😐': '#FFA500', 'Sad 😢': '#E74C3C'}
    fig3 = px.bar(mood, x='valence', y='track_genre',
                  orientation='h', color='mood',
                  color_discrete_map=color_map,
                  labels={'valence': 'Avg Valence', 'track_genre': 'Genre'})
    fig3.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("Audio Feature Radar by Genre")
    features = ['danceability', 'energy', 'speechiness',
                'acousticness', 'valence', 'liveness']
    radar_data = filtered.groupby('track_genre')[features].mean()
    fig4 = go.Figure()
    for genre in radar_data.index[:6]:
        fig4.add_trace(go.Scatterpolar(
            r=radar_data.loc[genre].values,
            theta=features,
            fill='toself',
            name=genre,
            opacity=0.6
        ))
    fig4.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True
    )
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# Top tracks table
st.subheader("🏆 Top 20 Most Popular Tracks")
top_tracks = con.execute("""
    SELECT track_name, artists, track_genre, popularity,
           ROUND(danceability, 2) AS danceability,
           ROUND(energy, 2) AS energy,
           ROUND(valence, 2) AS valence
    FROM spotify
    ORDER BY popularity DESC
    LIMIT 20
""").df()
st.dataframe(top_tracks, use_container_width=True, hide_index=True)