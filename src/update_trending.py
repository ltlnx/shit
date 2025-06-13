import os
import requests
from datetime import datetime, timedelta
import pytz

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
HEADERS = {'Authorization': f'token {GITHUB_TOKEN}'} if GITHUB_TOKEN else {}

def get_trending_repos():
    # Calculate date for repos created in the last week
    week_ago = (datetime.now(pytz.UTC) - timedelta(days=7)).strftime('%Y-%m-%d')
    
    # GitHub Search API query
    query = f'created:>{week_ago} sort:stars-desc'
    url = f'https://api.github.com/search/repositories?q={query}&per_page=10'
    
    response = requests.get(url, headers=HEADERS)
    return response.json()['items']

def format_repo_entry(repo):
    stars = repo['stargazers_count']
    description = repo['description'] or 'No description provided'
    return f"- [{repo['full_name']}]({repo['html_url']}): {description} ⭐{stars}"

def update_public_repos_file():
    trending = get_trending_repos()
    
    # Read current content
    with open('PUBLIC_REPOS.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the Trending section and update it
    trending_section = '## Trending\n'
    trending_entries = '\n'.join(format_repo_entry(repo) for repo in trending)
    
    # Split content at Trending section
    parts = content.split('## Trending')
    if len(parts) >= 2:
        # Find the next section
        next_section = parts[1].split('\n## ')[0]
        # Replace old trending content
        new_content = parts[0] + trending_section + trending_entries + '\n\n## ' + '## '.join(parts[1].split('\n## ')[1:])
    else:
        new_content = content + '\n' + trending_section + trending_entries + '\n'
    
    # Write updated content
    with open('PUBLIC_REPOS.md', 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == '__main__':
    update_public_repos_file()
