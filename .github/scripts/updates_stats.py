from github import Github
import os
import datetime

def update_readme(stats):
    with open('README.md', 'r') as file:
        content = file.read()
        
    # Update stats section
    stats_section = f"""## 📊 Repository Stats
- ⭐ Stars: {stats['stars']}
- 🍴 Forks: {stats['forks']}
- 📬 Open Issues: {stats['issues']}
- 👀 Watchers: {stats['watchers']}
"""
    # Update content with new stats
    # Add logic to update other sections

def main():
    g = Github(os.environ['GITHUB_TOKEN'])
    repo = g.get_repo("AasishPokhrel/shit")
    
    stats = {
        'stars': repo.stargazers_count,
        'forks': repo.forks_count,
        'issues': repo.open_issues_count,
        'watchers': repo.watchers_count
    }
    
    update_readme(stats)

if __name__ == "__main__":
    main()
