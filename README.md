### Repo Destroyer - Python CLI

Feature List:

1. User must add/store their authentication token
2. User can get a list of all repos and save them
2. Allows user to delete a single github repository
3. Allows user to delete a list of repositories
5. Allows uer to delete all repos in a loop

Commands:

`repo_destroyer authenticate`

- Add / edit Github API Credentials

`repo_destroyer fetch`

- Fetches list of repo names and saves to `db/repos.txt`

`repo_destroyer destroy --all {looks in repos.txt}`

- Looks for `db/repos.txt`, asks user for confirmation then deletes all repos in the list.

`repo_destroyer destroy --repo {repo_name}`

- Destroys a single repository