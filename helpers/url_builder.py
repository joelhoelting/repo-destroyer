root_url = 'https://api.github.com'


def build_url(key, username="microsoft", repository='invalid'):
    url_dict = {
        'validate_token': root_url,
        'validate_user': f"{root_url}/users/{username}",
        'list_repos': f"{root_url}/users/{username}/repos?per_page=100",
        'delete_repos': f"{root_url}/repos/{username}/{repository}"
    }
    return url_dict[key]
