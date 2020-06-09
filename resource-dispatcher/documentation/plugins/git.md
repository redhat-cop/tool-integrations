# Git Plugin

The Git plugin interacts with Git repositories

## Parameters

| Parameter | Description | Required | Default |
|---|---|---|---|
| `directory` | Directory of an existory repository, or directory to clone to | False | `.` |
| `branch` | Git branch to work with | False | `master` |
| `url` | Git url to use, either SSH or HTTPS | False (for local actions) | N/A |
| `action` | Either `clone`, `pull`, `add-all-changes`, `commit`, or `push` | True |
| `secret.ssh_private_key` | Path to a private key to use for cloning, pushing, pulling | False | N/A |
| `message` | Message to use for committing | False | "Commit message" |
| `author_name` | Author name to use for committing | False | "Automated Tool" |
| `author_email` | Author email to use for committing | False | "email@email.com" |

## How Context Is Used

Context is not used by this plugin.

## Example Usages

```yaml
tasks:
  - name: git-stuff
    description: Git plugin example
    triggers:
      - type: webhook
        route: /do_stuff
    steps:
      - plugin: git
        params:
          action: clone
          url: git@github.com:org/repo.git
          secret:
            ssh_private_key: /my/path/to/an/ssh/key
      - plugin: script
        params:
          script: |
            # Update some files and stuff in here
      - plugin: git
        params:
          action: add-all-changes
      - plugin: git
        params:
          action: commit
          message: Auto-update generated files
      - plugin: git
        params:
          action: push
          secret:
            ssh_private_key: /my/path/to/an/ssh/key
```
