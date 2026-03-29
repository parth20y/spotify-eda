# 🎵 Spotify Tracks — EDA & Storytelling

![Python](https://img.shields.io/badge/Python-3.12-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red) ![DuckDB](https://img.shields.io/badge/DuckDB-SQL-yellow) ![Kaggle](https://img.shields.io/badge/Dataset-Kaggle-20BEFF)

An end-to-end exploratory data analysis of **114,000+ Spotify tracks**, uncovering what makes a song popular across genres using audio features like danceability, energy, valence, and tempo.

---

## Key Questions Explored

- Which genres are the most popular on Spotify?
- What audio features correlate most with popularity?
- Which genres are the happiest vs saddest based on valence?
- How do danceability and energy vary across genres?
- What do the most popular tracks have in common?

---

## Dashboard Preview

> Interactive filters by genre and popularity range, live-updating charts, and a top tracks table.

| Chart | Description |
|---|---|
| Top Genres by Popularity | Horizontal bar chart ranked by avg popularity |
| Danceability vs Energy | Scatter plot colored by genre |
| Mood by Genre | Valence-based happy/neutral/sad classification |
| Audio Feature Radar | Multi-axis genre comparison across 6 features |
| Top 20 Tracks | SQL-powered table of most popular tracks |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| `pandas` | Data cleaning & feature engineering |
| `matplotlib` / `seaborn` | Static EDA plots in notebook |
| `plotly` | Interactive dashboard charts |
| `DuckDB` | SQL queries on the dataframe |
| `Streamlit` | Interactive web dashboard |
| `Jupyter` | EDA notebook |

---

## How to Run

### 1. Clone the repo
```bash
git clone https://github.com/parth20y/spotify-eda.git
cd spotify-eda
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Download the dataset
```bash
kaggle datasets download -d maharshipandya/-spotify-tracks-dataset -p data/ --unzip
```

### 5. Run the Jupyter notebook
```bash
cd notebooks
jupyter notebook eda.ipynb
```

### 6. Launch the Streamlit dashboard
```bash
cd app
streamlit run dashboard.py
```

---

## 📁 Project Structure
```
spotify-eda/
├── data/                  # Raw dataset (downloaded via Kaggle)
├── notebooks/
│   └── eda.ipynb          # Full EDA notebook
├── app/
│   └── dashboard.py       # Streamlit dashboard
├── sql/                   # DuckDB query files
├── requirements.txt
└── README.md
```

---

## Dataset

- **Source:** [Spotify Tracks Dataset](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset) on Kaggle
- **Size:** 114,000+ tracks across 114 genres
- **Features:** danceability, energy, loudness, speechiness, acousticness, instrumentalness, liveness, valence, tempo, popularity and more
---

## Key Findings

- **Anime and pop** genres top the popularity charts
- **Energy and loudness** are positively correlated with popularity
- **Acoustic and classical** genres score lowest on energy but highest on acousticness
- **Latin and dance** genres are the happiest (highest valence)
- **Black metal and sad** genres score lowest on valence

---

*Built as part of a data science portfolio. See my other projects on [GitHub](https://github.com/parth20y).*