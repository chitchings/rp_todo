# this module provides the RP To-Do CLI

from pathlib import Path
from typing import Optional, List

import typer as t

from rptodo import __app_name__, __version__, ERRORS, config, database, rptodo

app = t.Typer()


@app.command()
def init(
    db_path: str = t.Option(
        str(database.DEFAULT_DB_FILE_PATH),
        "--db-path",
        "-db",
        prompt="to-do database location?",
    ),
) -> None:
    app_init_error = config.init_app(db_path)
    if app_init_error:
        t.secho(
            f"Createing config file failed with {ERRORS[app_init_error]}",
            fg=t.colors.RED,
        )
        raise t.Exit(1)
    else:
        t.secho(f"The to-do database is {db_path}", fg=t.colors.GREEN)


def get_todoer() -> rptodo.Todoer:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        t.secho('Config file not found. please, run "rptodo init"', fg=t.colors.RED)
        raise t.Exit(1)
    if db_path.exists():
        return rptodo.Todoer(db_path)
    else:
        t.secho('database not found. please run "rptodo init"', fg=t.colors.RED)
        raise t.Exit(1)


@app.command()
def add(
    description: List[str] = t.Argument(...),
    priority: int = t.Option(2, "--priority", "-p", min=1, max=3),
) -> None:
    """Add a new to-do with a DESCRIPTION"""
    todoer = get_todoer()
    todo, error = todoer.add(description, priority)
    if error:
        t.secho(f'Adding a to-do failed with "{ERRORS[error]}" ', fg=t.colors.RED)
        raise t.Exit(1)
    else:
        t.secho(
            f"""todo: "{todo['Description']}" was added """
            f"""with priority: {priority}""",
            fg=t.colors.GREEN,
        )


def _version_callback(value: bool) -> None:
    if value:
        t.echo(f"{__app_name__} v{__version__}")
        raise t.Exit()


@app.callback()
def main(
    version: Optional[bool] = t.Option(
        None,
        "--version",
        "-v",
        help="Show the applications version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
