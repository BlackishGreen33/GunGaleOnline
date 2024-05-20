"""Count a file """

import logging
from collections.abc import Generator
from pathlib import Path

# Config root logger
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def count(source_file: str, dest_file: str):
    """
    Count source
    :param source_file:
    :param dest_file:
    :return:
    """
    words = read_from_file(Path(source_file))

    total = 0

    for _ in words:
        total += 1

    write_to_file(Path(dest_file), total)


def read_from_file(source_file: Path) -> Generator[str, None, None]:
    """

    :param source_file:
    :return:
    """
    # Read source_file
    logging.debug("Read file: %s", source_file)
    with open(source_file, "r", encoding="utf-8") as source_obj:
        for line in source_obj:
            for word in line.split(" "):
                yield word


def write_to_file(dest_file: Path, total_words: int) -> None:
    """
    Write result to file
    :param dest_file:
    :param total_words:
    :return:
    """
    logging.debug("Count %s words, write to %d", dest_file, total_words)
    with open(dest_file, "w", encoding="utf-8") as dest_obj:
        dest_obj.write(f"Total count: {total_words}")
