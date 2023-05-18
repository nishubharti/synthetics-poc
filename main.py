#!/usr/bin/env python3

import urllib.parse
from git import Repo
import sys

git_repo=sys.argv[1]
git_token=sys.argv[2]

def clone_git_repo(git_url,git_token):
    local_path_of_git_repo = r'temprepo'
    parsed_url = urllib.parse.urlparse(git_url)
    hostname = parsed_url.netloc
        
    modified_git_url = git_url.replace(hostname, f'{git_token}@{hostname}')
    Repo.clone_from(modified_git_url, local_path_of_git_repo)
    print("clone done!!!")
    
def main():
    clone_git_repo(git_repo,git_token)
    
if __name__ == '__main__':
    main()
    
