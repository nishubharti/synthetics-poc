#!/usr/bin/env python3
from github import Github
import os
import urllib.parse

GIT_REPO=os.environ['GIT_REPO']
GIT_TOKEN=os.environ['GIT_TOKEN']


def get_git_repo(git_url,git_token):
   
    parsed_url = urllib.parse.urlparse(git_url)
    hostname=parsed_url.netloc
    folder_path = "synthetics/ping"
    g = Github(base_url=f'https://{hostname}/api/v3', login_or_token=git_token)
    gitRepo=git_url.split(hostname+'/')[1]
    repo = g.get_repo(gitRepo)

    contents = repo.get_contents(folder_path)

    for content_file in contents:
  
        if content_file.type == "file":
            file_content = content_file.decoded_content.decode("utf-8")
            print(f"Content of '{content_file.path}':")
            print(file_content)
            print("=" * 50)
    
def main():
    get_git_repo(GIT_REPO,GIT_TOKEN)
    
if __name__ == '__main__':
    main()