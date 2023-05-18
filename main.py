import urllib.parse
from git import Repo
import os
os.environ["GIT_PYTHON_REFRESH"] = "quiet"

GIT_REPO=os.environ['GIT_REPO']
GIT_TOKEN=os.environ['GIT_TOKEN']

def clone_git_repo(git_url,git_token):
    local_path_of_git_repo = r'temprepo'
    parsed_url = urllib.parse.urlparse(git_url)
    hostname = parsed_url.netloc
        
    modified_git_url = git_url.replace(hostname, f'{git_token}@{hostname}')
    Repo.clone_from(modified_git_url, local_path_of_git_repo)
    print("clone done!!!")
    
def main():
    clone_git_repo(GIT_REPO,GIT_TOKEN)
    
if __name__ == '__main__':
    main()
    
