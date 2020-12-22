Repo Destroyer allows you to quickly delete large numbers of GitHub repositories.

Installation:

```
$ pip install --editable .
$ repo_destroyer
```

Usage:

```
Commands:
  authenticate  Add or update GitHub credentials
  destroy       Destroy repositories in db/repositories
  fetch         Fetch a list of a repos from Github
```

#### Authenticate

Before authenticating, visit https://github.com/settings/tokens and create a token with 'delete_repo' scope.

`repo_destroyer authenticate` will prompt the user for their username and a personal access token. Credentials are saved
in `db/credentials.csv`.

#### Fetch (Repos)

`repo_destroyer fetch` will fetch a full list of all of your repos and save them in `db/repositories.txt`. Repo
Destroyer will iterate through this list when you run `repo_destroyer destroy`. Feel free to edit this file manually to
avoid deleting important repositories.

#### Destroy

`repo_destroyer destroy` will look for `db/repositories.txt` and proceed to iterate through the list of repositories in
that file. For each repo, the user will be asked if they want to delete that repository.