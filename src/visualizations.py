import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from pathlib import Path
import json

def create_language_trend_viz():
    """Create visualization for programming language trends"""
    stats_dir = Path('.github/stats')
    dfs = []
    
    for stats_file in sorted(stats_dir.glob('stats_*.json')):
        with open(stats_file, 'r') as f:
            data = json.load(f)
            lang_data = data['languages']
            df = pd.DataFrame.from_dict(lang_data, orient='index')
            df['date'] = data['timestamp']
            dfs.append(df)
    
    if dfs:
        df_combined = pd.concat(dfs)
        fig = px.line(df_combined, 
                     x='date', 
                     y='stars', 
                     color=df_combined.index,
                     title='Programming Language Popularity Trends')
        fig.write_html('docs/visualizations/language_trends.html')

def create_topic_popularity_viz(latest_stats_file):
    """Create visualization for topic popularity"""
    with open(latest_stats_file, 'r') as f:
        data = json.load(f)
    
    topics = data['topics']
    topic_names = list(topics.keys())
    repo_counts = [topic['total_count'] for topic in topics.values()]
    
    fig = go.Figure(data=[
        go.Bar(x=topic_names, y=repo_counts)
    ])
    fig.update_layout(
        title='Popular Topics on GitHub',
        xaxis_title='Topics',
        yaxis_title='Number of Repositories'
    )
    fig.write_html('docs/visualizations/topic_popularity.html')

def main():
    # Create visualizations directory if it doesn't exist
    Path('docs/visualizations').mkdir(parents=True, exist_ok=True)
    
    # Generate visualizations
    create_language_trend_viz()
    
    # Get latest stats file
    latest_stats = sorted(Path('.github/stats').glob('stats_*.json'))[-1]
    create_topic_popularity_viz(latest_stats)

if __name__ == "__main__":
    main()
