import click


def green_or_red_string(boolean, correct_string, incorrect_string=None):
    if incorrect_string is None:
        incorrect_string = correct_string

    color = "bright_green" if boolean else "red"
    message = correct_string if boolean else incorrect_string
    return click.style(message, fg=color)
