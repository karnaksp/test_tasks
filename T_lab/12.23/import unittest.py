def diff(price_list, amount_of_credit):
    for price in price_list:
        if amount_of_credit >= price:
            amount_of_credit -= price
    return amount_of_credit


def enumerable(price_list, amount_of_credit):
    max_value = 0
    n = amount_of_credit
    while n != 0:
        dif = diff(price_list, n)
        if dif > max_value:
            max_value = dif
        n -= 1
    return max_value


if __name__ == "__main__":
    count_present, amount_of_credit = map(int, input().split())
    presents = list(map(int, input().split()))

    result = enumerable(presents, amount_of_credit)

    print(result)
