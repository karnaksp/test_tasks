from typing import Dict


def can_form_tinkoff(word: str) -> str:
    """
    Check if a word can be formed using the letters in "TINKOFF".

    Args:
        word (str): The word to be checked.

    Returns:
        str: "yes" if the word can be formed, "no" otherwise.
    """
    target_word: str = "TINKOFF"
    word_count: Dict[str, int] = {letter: word.count(letter) for letter in set(word)}
    target_count: Dict[str, int] = {
        letter: target_word.count(letter) for letter in set(target_word)
    }

    for letter, count in target_count.items():
        if (
            letter not in word_count
            or word_count[letter] < count
            or word_count[letter] > count
        ):
            return "no"
    return "yes"


def main():
    n = int(input())

    results = []
    for _ in range(n):
        input_str = input().strip()
        result = can_form_tinkoff(input_str)
        results.append(result)

    for res in results:
        print(res)


if __name__ == "__main__":
    main()
