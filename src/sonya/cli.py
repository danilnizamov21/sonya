import typer

from sonya.orchestrator import collect_tgstat, inspect_telegram, pars_messages

app = typer.Typer(
    name="sonya",
    help="CLI для сбора и обработки Telegram-каналов.",
    no_args_is_help=True,
)


@app.command()
def tgstat(
    topic: str = typer.Argument(
        ...,
        help="Раздел TGStat, например gambling.",
    ),
):
    """Собрать Telegram-каналы из TGStat."""
    collect_tgstat(topic)


@app.command()
def telegram(
    limit: int = typer.Option(
        20,
        "--limit",
        "-l",
        min=1,
        help="Количество каналов для проверки.",
    ),
    batch_size: int = typer.Option(
        10,
        "--batch-size",
        "-b",
        min=1,
        help="Количество каналов в одной транзакции.",
    ),
):
    """Проверить Telegram-каналы и сохранить их HTML."""
    inspect_telegram(
        limit=limit,
        batch_size=batch_size,
    )


@app.command()
def pars():
    """Париснг html в Json"""
    pars_messages()


if __name__ == "__main__":
    app()
