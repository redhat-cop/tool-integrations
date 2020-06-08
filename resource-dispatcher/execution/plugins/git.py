import os
from repositories import generate_ssh_command
from git import Repo


def process(context, params):
    if "action" not in params:
        raise Exception("Git plugin requires `action` to be set as a parameter.")
    run_action(params)


def run_action(params):
    repo_directory = params["directory"] if "directory" in params else "."
    branch = params["branch"] if "branch" in params else "master"
    message = params["message"] if "message" in params else "Commit message"
    author_name = params["author_name"] if "author_name" in params else "Automated Tool"
    author_email = params["author_email"] if "author_email" in params else "email@email.com"
    url = params["url"] if "url" in params else None

    if "secret" in params and url and not url.startswith("http"):
        env = {
            "GIT_SSH_COMMAND": generate_ssh_command(params)
        }
    else:
        env = {}

    if params["action"] == "clone" or params["action"] == "pull":
        repo = fetch(url, repo_directory, branch, env)
    elif params["action"] == "add-all-changes":
        repo = add_all(repo_directory)
    elif params["action"] == "commit":
        commit(repo_directory, message, author_name, author_email)
    elif params["action"] == "push":
        push(url, repo_directory, env)


def fetch(url, repo_directory, branch, env={}):
    if not os.path.exists(repo_directory):
        os.makedirs(repo_directory)
        print(f"Cloning {url}...")
        repo = Repo.clone_from(url, repo_directory, branch=branch, env=env)
        print(f"Cloned {url}")
    else:
        repo = Repo.init(repo_directory)
        repo.remotes.origin.pull(env=env)
    return repo


def add_all(repo_directory):
    repo = Repo.init(repo_directory)
    repo.git.add(all=True)
    print("All files added")
    return repo


def commit(repo_directory, message, author_name, author_email):
    repo = Repo.init(repo_directory)
    repo.config_writer().set_value("user", "name", author_name).release()
    repo.config_writer().set_value("user", "email", author_email).release()
    try:
        repo.git.commit('-m', message, author=f"{author_name} <{author_email}>")
        print("Committed to repository")
    except Exception as e:
        if "nothing to commit, working tree clean" in str(e):
            print("Nothing to commit")
        else:
            raise e


def push(url, repo_directory, env={}):
    repo = Repo.init(repo_directory)
    repo.remotes.origin.push(env=env)
    print("Pushed repository")
