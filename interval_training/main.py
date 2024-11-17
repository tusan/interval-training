import random

import click

CIRCLE_OF_FIFTH_MAJOR_SCALES = {
    "C": ["C", "D", "E", "F", "G", "A", "B"],
    "G": ["G", "A", "B", "C", "D", "E", "F#"],
    "D": ["D", "E", "F#", "G", "A", "B", "C#"],
    "A": ["A", "B", "C#", "D", "E", "F#", "G#"],
    "E": ["E", "F#", "G#", "A", "B", "C#", "D#"],
    "B": ["B", "C#", "D#", "E", "F#", "G#", "A#"],
    "Cb": ["Cb", "Db", "Eb", "Fb", "Gb", "Ab", "Bb"],
    "F#": ["F#", "G#", "A#", "B", "C#", "D#", "E#"],
    "Gb": ["Gb", "Ab", "Bb", "Cb", "Db", "Eb", "F"],
    "Db": ["Db", "Eb", "F", "Gb", "Ab", "Bb", "C"],
    "C#": ["C#", "D#", "E#", "F#", "G#", "A#", "B#"],
    "Ab": ["Ab", "Bb", "C", "Db", "Eb", "F", "G"],
    "Eb": ["Eb", "F", "G", "Ab", "Bb", "C", "D"],
    "Bb": ["Bb", "C", "D", "Eb", "F", "G", "A"],
    "F": ["F", "G", "A", "Bb", "C", "D", "E"],
}

INTERVALS = [*range(1, 10), 11, 13]

ALTERATIONS = ["", "b", "#", "bb", "x"]
ALTERATIONS_WEIGHT = [100, 20, 20, 10, 10]


def get_interval(tune: str, interval: int, alteration: str) -> str:
    if tune not in CIRCLE_OF_FIFTH_MAJOR_SCALES:
        raise ValueError(
            f"Provide only tunes from circle of fifth: {CIRCLE_OF_FIFTH_MAJOR_SCALES.keys()}"
        )
    if interval not in INTERVALS:
        raise ValueError(f"Accepted intervals: {INTERVALS}")

    correct_interval = CIRCLE_OF_FIFTH_MAJOR_SCALES[tune][(interval - 1) % 7]

    return (
        (
            f"{correct_interval}{alteration}".replace("##", "x")
            .replace("#b", "")
            .replace("b#", "")
            .replace("#x", "x#")
        )
        if alteration
        else correct_interval
    )


def format_row(row: dict[str, str]) -> list[str]:
    return [f"{interval}{alteration}" for interval, alteration in row.items()]


def build_questions(include_alterations: bool) -> tuple[int, str]:
    return (
        random.choices(INTERVALS)[0],
        (
            random.choices(ALTERATIONS, weights=ALTERATIONS_WEIGHT)[0]
            if include_alterations
            else ""
        ),
    )


@click.command()
@click.option(
    "--tune",
    prompt="Tune from circle of fifth to practice",
    default=lambda: random.choice(list(CIRCLE_OF_FIFTH_MAJOR_SCALES)),
)
@click.option("--count", prompt="How many questions", default=20)
@click.option(
    "--include-alterations", prompt="Include interval outside major scale", is_flag=True, default=True
)
def main(tune: str, count: int, include_alterations: bool):
    if tune not in CIRCLE_OF_FIFTH_MAJOR_SCALES:
        raise ValueError(
            f"Provide only tunes from circle of fifth: {CIRCLE_OF_FIFTH_MAJOR_SCALES.keys()}"
        )

    interval_training(count, tune, include_alterations)


class QuestionTracker:
    def __init__(self):
        self.__correct_count = 0
        self.__wrong_answers = []

    def correct(self):
        self.__correct_count += 1

    def wrong(self, question: str, answer: str, correct_answer: str):
        self.__wrong_answers.append((question, answer, correct_answer))

    def print_stats(self):
        print("RESULT:")
        print(f"{self.__correct_count} correct answers")
        print("wrong answer:")

        for question, answer, correct_answer in self.__wrong_answers:
            print(f"question {question}, answer {answer} but was {correct_answer}")


def interval_training(count: int, tune: str, include_alterations: bool) -> None:
    question_tracker = QuestionTracker()

    try:
        for i in range(1, count + 1):
            interval, alteration = build_questions(include_alterations)
            answer = click.prompt(f"{interval}{alteration}")
            correct_answer = get_interval(tune, interval, alteration)

            if answer == correct_answer:
                question_tracker.correct()
            else:
                question_tracker.wrong(f"{interval}{alteration}", answer, correct_answer)
    finally:
        question_tracker.print_stats()


if __name__ == "__main__":
    main()
