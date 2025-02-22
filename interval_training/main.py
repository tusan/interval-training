from __future__ import annotations

import sys

import click

from interval_training.triad import TriadTrainingApp
from interval_training.interval import IntervalTrainingApp
from interval_training.lib import (
    MAJOR_SCALES,
    random_scale,
)


@click.group()
def cli():
    pass


@cli.command()
@click.option("--count", prompt="Question count", default=20)
def triad(count: int) -> None:
    click.echo(TriadTrainingApp(count).run())


@cli.command()
@click.option("--count", prompt="Question count", default=20)
@click.option(
    "--tune",
    prompt="Tune to practice",
    default=random_scale,
    type=click.Choice(MAJOR_SCALES),
)
@click.option(
    "--exclude-alterations",
    prompt="Use only diatonic intervals",
    is_flag=True,
    default=False,
)
def interval(count: int, tune: str, exclude_alterations: bool) -> None:
    click.echo(IntervalTrainingApp(count, tune, exclude_alterations).run())


def main():
    try:
        cli()
    except Exception as e:
        click.echo(e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
