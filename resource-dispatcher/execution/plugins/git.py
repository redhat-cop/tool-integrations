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
    author_email = (
        params["author_email"] if "author_email" in params else "email@email.com"
    )
    url = params["url"] if "url" in params else None

    if "secret" in params and url and not url.startswith("http"):
        env = {"GIT_SSH_COMMAND": generate_ssh_command(params)}
    else:
        env = {}

    if params["action"] == "clone" or params["action"] == "pull":
        fetch(url, repo_directory, branch, env)
    elif params["action"] == "add-all-changes":
        add_all(url, repo_directory)
    elif params["action"] == "commit":
        commit(url, repo_directory, message, author_name, author_email)
    elif params["action"] == "push":
        push(url, repo_directory, env)


def fetch(url, repo_directory, branch, env={}):
    if not os.path.exists(repo_directory):
        os.makedirs(repo_directory)
        print(f"Cloning {url}...")
        try:
            repo = Repo.clone_from(url, repo_directory, branch=branch, env=env)
            print(f"Cloned {url}")
        except Exception as e:
            if "not found in upstream origin" in str(e):
                print(f"Branch {branch} not found: {url}")
            elif "The project you were looking for could not be found" in str(e):
                print(f"Project not found: {url}")
            else:
                raise e
    else:
        repo = Repo.init(repo_directory)
        repo.remotes.origin.pull(env=env)


def add_all(url, repo_directory):
    repo = Repo.init(repo_directory)
    repo.git.add(all=True)
    print(f"All files added: {url}")


def commit(url, repo_directory, message, author_name, author_email):
    repo = Repo.init(repo_directory)
    repo.config_writer().set_value("user", "name", author_name).release()
    repo.config_writer().set_value("user", "email", author_email).release()
    try:
        repo.git.commit("-m", message, author=f"{author_name} <{author_email}>")
        print(f"Committed to repository: {url}")
    except Exception as e:
        if "nothing to commit" in str(e):
            print(f"Nothing to commit: {url}")
        else:
            raise e


def push(url, repo_directory, env={}):
    try:
        repo = Repo.init(repo_directory)
        repo.remotes.origin.push(env=env)
        print(f"Pushed repository: {url}")
    except Exception as e:
        if "object has no attribute 'origin'" in str(e):
            print(f"Remote origin does not exist: {url}")
        else:
            raise e
