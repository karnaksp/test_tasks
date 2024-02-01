from typing import List


def can_establish_contact(n: int, relationships: List[int]) -> str:
    if n % 2 == 0:
        # Если количество разработчиков четное, то каждое число должно быть не 0
        if all(contact != 0 for contact in relationships):
            return "Yes"
        else:
            return "No"
    else:
        # Если количество разработчиков нечетное
        # и каждый разработчик может контактировать хотя бы с одним
        # и хотя бы один разработчик может контактировать хотя бы с двумя
        if all(contact != 0 for contact in relationships) and any(
            contact >= 2 for contact in relationships
        ):
            return "Yes"
        else:
            return "No"


def main():
    t = int(input())

    results = []
    for _ in range(t):
        n = int(input())
        contacts = list(map(int, input().split()))
        result = can_establish_contact(n, contacts)
        results.append(result)

    for res in results:
        print(res)


if __name__ == "__main__":
    main()
