import os
import re
from github import Github
import markdown
from datetime import datetime

def validate_message(content):
    # Check for basic markdown formatting
    if not content.strip().startswith('-'):
        return False
    
    # Check for proper attribution format
    if not re.search(r'@[\w-]+', content):
        return False
    
    return True

def validate_story(content):
    # Check for minimum length
    if len(content.strip()) < 50:
        return False
    
    # Check for basic markdown formatting
    if not re.search(r'#{1,6}\s+.*', content):
        return False
    
    # Check for author attribution
    if not re.search(r'@[\w-]+', content):
        return False
    
    return True

def process_messages():
    with open('MESSAGES.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ensure proper structure
    if '# Community Messages for the One Billionth Repo' not in content:
        content = '# Community Messages for the One Billionth Repo\n\n' + content
    
    if 'Add your message below!' not in content:
        content = content.replace('# Community Messages for the One Billionth Repo\n',
                                '# Community Messages for the One Billionth Repo\n\n'
                                'Add your message below!  \n'
                                '_You can add a PR or comment with your congratulations, jokes, or hopes for the future._\n\n---\n\n')
    
    # Sort messages
    messages = content.split('---\n\n')[1].strip().split('\n')
    messages = [m for m in messages if m.strip() and validate_message(m)]
    messages.sort()
    
    # Rebuild file
    header = content.split('---\n\n')[0] + '---\n\n'
    return header + '\n'.join(messages)

def process_stories():
    try:
        with open('STORIES.md', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        content = '''# GitHub Stories

Share your GitHub journey and experiences here! Add your story with a pull request.

## Guidelines
- Add a meaningful title for your story
- Include your GitHub handle
- Share something unique about your experience
- Keep it friendly and constructive

---

'''
    
    # Split into sections and validate
    sections = re.split(r'(?=##\s+)', content)
    header = sections[0]
    stories = sections[1:]
    
    # Sort stories by title
    stories = [s for s in stories if validate_story(s)]
    stories.sort(key=lambda x: re.search(r'##\s+(.*)', x).group(1).lower())
    
    return header + '\n'.join(stories)

def main():
    token = os.getenv('GITHUB_TOKEN')
    pr_number = int(os.getenv('PR_NUMBER'))
    
    g = Github(token)
    repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))
    pr = repo.get_pull(pr_number)
    
    files_changed = [f.filename for f in pr.get_files()]
    
    if 'MESSAGES.md' in files_changed:
        processed_content = process_messages()
        with open('MESSAGES.md', 'w', encoding='utf-8') as f:
            f.write(processed_content)
    
    if 'STORIES.md' in files_changed:
        processed_content = process_stories()
        with open('STORIES.md', 'w', encoding='utf-8') as f:
            f.write(processed_content)

if __name__ == '__main__':
    main()
