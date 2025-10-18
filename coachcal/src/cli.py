import typer

app = typer.Typer()


@app.command()
def hello():
    print("CoachCal CLI bootstrap ok")


if __name__ == "__main__":
    app()
