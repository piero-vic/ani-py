import typer
from cli import main


app = typer.Typer(add_completion=False)


if __name__ == '__main__':
    app.command()(main)
    app()
