from __future__ import annotations

import random
import click
from interval_training.lib import QuestionBuilder, MAJOR_SCALES, Answer


def interval_training(count: int, tune: str, exclude_alterations: bool) -> None:
    question_builder = QuestionBuilder(tune, exclude_alterations)

    print(f"Tune: {tune}")
    try:
        for _ in range(1, count + 1):
            interval = question_builder.build_question()
            answer = click.prompt(f"{interval.interval}{interval.alteration} th")
            question_builder.register_answer(Answer(interval, answer))
    finally:
        print(question_builder.stats())


@click.command()
@click.option(
    "--tune",
    prompt="Tune to practice",
    default=lambda: random.choice(list(MAJOR_SCALES)),
    type=click.Choice(MAJOR_SCALES)
)
@click.option("--count", prompt="Question count", default=20)
@click.option(
    "--exclude-alterations",
    prompt="Use only diatonic intervals",
    is_flag=True,
    default=False,
)
def main(tune: str, count: int, exclude_alterations: bool):
    interval_training(count, tune, exclude_alterations)


if __name__ == "__main__":
    main()
