import numpy as np
import itertools

def solve_portfolio_DP(properties_df, total_budget_rp):
    BASE_UNIT = 1_000_000 # Base unit for discretization (e.g., 1 million Rp)

    # round weights to nearest unit
    weights = (properties_df['price_in_rp'] / BASE_UNIT).astype(int)
    values = properties_df['NPV'].values
    budget_d = int(round(total_budget_rp / BASE_UNIT))
    n_items = len(properties_df)

    # USE 1D DP Array + 'keep' mask for backtracking.
    dp = np.zeros(budget_d + 1)
    keep = np.zeros((n_items, budget_d + 1), dtype=bool)

    for i in range(n_items):
        w_i = weights.iloc[i]
        v_i = values[i]
        for w in range(budget_d, w_i - 1, -1):
            if dp[w - w_i] + v_i > dp[w]:
                dp[w] = dp[w - w_i] + v_i
                keep[i, w] = True
    
    max_npv = dp[budget_d]

    # backtrack via 'keep' mask
    selected_indices = []
    w = budget_d
    for i in range(n_items - 1, -1, -1):
        if keep[i, w]:
            selected_indices.append(properties_df.index[i])
            w -= weights.iloc[i]

    selected_indices.reverse()  
    selected_df = properties_df.loc[selected_indices]
    total_cost = selected_df['price_in_rp'].sum()

    return max_npv, selected_indices, total_cost

def solve_portfolio_greedy(properties_df, total_budget_rp):
    df = properties_df.copy()
    df['ratio'] = df['NPV'] / df['price_in_rp']
    df_sorted = df.sort_values(by='ratio', ascending=False)

    selected = []
    total_cost = 0
    total_npv = 0

    for idx, row in df_sorted.iterrows():
        price = row['price_in_rp']
        if total_cost + price <= total_budget_rp:
            selected.append(idx)
            total_cost += price
            total_npv += row['NPV']
    
    selected_df = properties_df.loc[selected]
    return total_npv, selected, total_cost

def solve_portfolio_bruteforce(properties_df, total_budget_rp, max_items=50):
    n = len(properties_df)
    if n > max_items:
        raise ValueError(f"Too many items ({n}) for brute-force (default limit: {max_items}). "
        "Please sample fewer items")
    
    best_npv = 0
    best_subset = []

    items = list(properties_df.index)
    prices = properties_df['price_in_rp'].to_dict()
    npvs = properties_df['NPV'].to_dict()

    for r in range(1, n + 1):
        for combo in itertools.combinations(items, r):
            cost = sum(prices[i] for i in combo)
            if cost <= total_budget_rp:
                npv_sum = sum(npvs[i] for i in combo)
                if npv_sum > best_npv:
                    best_npv = npv_sum
                    best_subset = list(combo)
    
    total_cost = sum(prices[i] for i in best_subset)
    return best_npv, best_subset, total_cost