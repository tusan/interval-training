import random
from collections import deque

import click

CIRCLE_OF_FIFTH_MAJOR_SCALES = {
    "C": ["C", "D", "E", "F", "G", "A", "B"],
    "G": ["G", "A", "B", "C", "D", "E", "F#"],
    "F": ["F", "G", "A", "Bb", "C", "D", "E"],
    "D": ["D", "E", "F#", "G", "A", "B", "C#"],
    "Bb": ["Bb", "C", "D", "Eb", "F", "G", "A"],
    "A": ["A", "B", "C#", "D", "E", "F#", "G#"],
    "Eb": ["Eb", "F", "G", "Ab", "Bb", "C", "D"],
    "E": ["E", "F#", "G#", "A", "B", "C#", "D#"],
    "Ab": ["Ab", "Bb", "C", "Db", "Eb", "F", "G"],
    "B": ["B", "C#", "D#", "E", "F#", "G#", "A#"],
    "Db": ["Db", "Eb", "F", "Gb", "Ab", "Bb", "C"],
    "F#": ["F#", "G#", "A#", "B", "C#", "D#", "E#"],
    "Gb": ["Gb", "Ab", "Bb", "Cb", "Db", "Eb", "F"],
    "Cb": ["Cb", "Db", "Eb", "Fb", "Gb", "Ab", "Bb"],
    "C#": ["C#", "D#", "E#", "F#", "G#", "A#", "B#"],
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


class QuestionTracker:
    def __init__(self):
        self.__correct_count = 0
        self.__wrong_answers = []

    def right(self):
        self.__correct_count += 1

    def wrong(self, question: str, answer: str, correct_answer: str):
        self.__wrong_answers.append((question, answer, correct_answer))

    def stats(self) -> str:
        result = f"\nRESULT:\n{self.__correct_count} correct answers\n\n"
        return f"{result}Wrong answers:\n{'\n'.join([
            f"question {question}th, answer {answer} but was {correct_answer}"
            for question, answer, correct_answer in self.__wrong_answers
        ])}" if self.__wrong_answers else result


class QuestionBuilder:
    def __init__(self, tune: str, include_alterations: bool):
        self.__include_alterations = include_alterations
        self.__tune = tune

        self.__question_tracker = QuestionTracker()
        self.__already_seen = deque(maxlen=7)

    def build_question(self) -> tuple[int, str]:
        for i in range(0, 100):
            interval, alteration = self.__build_question()
            k = f"{interval}{alteration}"
            if k not in self.__already_seen:
                self.__already_seen.append(k)
                return interval, alteration
        raise ValueError("Seems you already checked all the possibility")

    def __build_question(self) -> tuple[int, str]:
        return (
            random.choices(INTERVALS)[0],
            (
                random.choices(ALTERATIONS, weights=ALTERATIONS_WEIGHT)[0]
                if self.__include_alterations
                else ""
            ),
        )


    def register_answer(self, interval: int, alteration: str, answer: str) -> None:
        correct_answer = get_interval(self.__tune, interval, alteration)

        if answer == correct_answer:
            self.__question_tracker.right()
        else:
            self.__question_tracker.wrong(
                f"{interval}{alteration}", answer, correct_answer
            )

    def finalize(self) -> str:
        return self.__question_tracker.stats()


def interval_training(count: int, tune: str, include_alterations: bool) -> None:
    question_builder = QuestionBuilder(tune, include_alterations)

    print(f"Tune: {tune}")
    try:
        for i in range(1, count + 1):
            interval, alteration = question_builder.build_question()
            answer = click.prompt(f"{interval}{alteration}th")
            question_builder.register_answer(interval, alteration, answer)
    finally:
        print(question_builder.finalize())


@click.command()
@click.option(
    "--tune",
    prompt="Tune from circle of fifth to practice",
    default=lambda: random.choice(list(CIRCLE_OF_FIFTH_MAJOR_SCALES)),
)
@click.option("--count", prompt="How many questions", default=20)
@click.option(
    "--include-alterations",
    prompt="Include interval outside major scale",
    is_flag=True,
    default=True,
)
def main(tune: str, count: int, include_alterations: bool):
    if tune not in CIRCLE_OF_FIFTH_MAJOR_SCALES:
        raise ValueError(
            f"Provide only tunes from circle of fifth: {CIRCLE_OF_FIFTH_MAJOR_SCALES.keys()}"
        )

    interval_training(count, tune, include_alterations)


if __name__ == "__main__":
    main()
