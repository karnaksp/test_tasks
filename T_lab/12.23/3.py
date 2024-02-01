from collections import defaultdict


def dfs(node, target_companies, company_count, graph, prices):
    # Рекурсивная функция DFS для обхода дерева
    current_cost = prices[node][1]  # Учитываем стоимость текущей вершины

    if prices[node][0] in target_companies:
        company_count[prices[node][0]] = 1

    for child in graph[node]:
        child_cost, child_company_count = dfs(
            child, target_companies, company_count, graph, prices
        )
        current_cost += child_cost
        for company in target_companies:
            company_count[company] += child_company_count[company]

    return current_cost, company_count


def min_cost_to_buy_stock(n, k, target_companies, tree_info):
    graph = defaultdict(list)
    prices = {}

    for i in range(1, n + 1):
        parent, cost, company = tree_info[i - 1]
        graph[parent].append(i)
        prices[i] = (company, cost)

    min_total_cost = float("inf")

    for i in range(1, n + 1):
        company_count = {company: 0 for company in target_companies}
        total_cost, company_count = dfs(
            i, target_companies, company_count, graph, prices
        )

        if all(company_count[company] > 0 for company in target_companies):
            min_total_cost = min(min_total_cost, total_cost)

    return min_total_cost if min_total_cost != float("inf") else 1


# Пример использования:
# if __name__ == "__main__":
#     n, k = map(int, input().split())
#     company_shares = [input().strip() for _ in range(k)]
#     tree_info = [input().split() for _ in range(n)]

#     result = min_cost_to_buy_shares(n, k, company_shares, tree_info)
#     print(result)

if __name__ == "__main__":
    n, k = map(int, input().split())
    target_companies = [input().strip() for _ in range(k)]

    tree_info = [list(input().split()) for _ in range(n)]
    tree_info = [(int(x[0]), int(x[1]), x[2]) for x in tree_info]

    result = min_cost_to_buy_stock(n, k, target_companies, tree_info)
    print(result)
