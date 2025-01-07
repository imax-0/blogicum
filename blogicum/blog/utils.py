import blogicum.constans as const


def get_first_words(line: str) -> str:
    return ' '.join(
        line.split()[:const.COUNT_WORDS_DISPLAYED_IN_TITLE]
    )
