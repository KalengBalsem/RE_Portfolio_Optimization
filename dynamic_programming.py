import pandas as pd
import numpy as np
import os
import random

def load_properties_data(filename):
    dataset_path = os.path.abspath(os.path.join(filename))
    return pd.read_csv(dataset_path, index_col=0)

def solve_portfolio_knapsack(properties_df, total_budget_rp):
    BASE_UNIT = 1_000_000 # Base unit for discretization (e.g., 1 million Rp)

    weights = (properties_df['price_in_rp'] / BASE_UNIT).astype(int)
    values = properties_df['NPV']
    budget_d = int(total_budget_rp / BASE_UNIT)
    n_items = len(properties_df)

    dp = np.zeros((n_items + 1, budget_d + 1))

    for i in range(1, n_items + 1):
        item_index = i - 1
        weight = weights.iloc[item_index]
        value = values.iloc[item_index]
        for w in range(budget_d + 1):
            dp[i][w] = dp[i - 1][w]

            if weight <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - weight] + value)

    max_npv = dp[n_items][budget_d]

    selected_indices = []
    w = budget_d
    for i in range(n_items, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            item_index = i - 1
            selected_indices.append(properties_df.index[item_index])
            weight = weights.iloc[item_index]
            w -= weight
    selected_indices.reverse()

    selected_properties_df = properties_df.loc[selected_indices]
    total_cost = selected_properties_df['price_in_rp'].sum()

    return max_npv, selected_indices, total_cost

# Example usage
budget = 5_000_000_000

df_sale_2025 = load_properties_data('rumah123_2025_sale_modelled.csv')

df_sale_2025.query('NPV > 0', inplace=True)

properties = df_sale_2025[['price_in_rp', 'NPV']].sample(n=30, random_state=42)

print("Available Properties:")
print(properties)
print("\nTotal Budget: Rp {:,.0f}".format(budget))
print("-" * 40)


# Solve the problem
max_npv, selected_items, total_cost = solve_portfolio_knapsack(properties, budget)

print("\n--- Optimal Portfolio Found ---")
print("Maximum NPV Achievable: Rp {:,.0f}".format(max_npv))
print("Total Cost of Portfolio: Rp {:,.0f}".format(total_cost))
print("Selected Properties:", selected_items)
print("\nDetails of Selected Properties:")
print(properties.loc[selected_items])

print("\n", properties)