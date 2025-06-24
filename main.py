import pandas as pd
import os
import time
import random
from algorithms import (
    solve_portfolio_DP,
    solve_portfolio_greedy,
    solve_portfolio_bruteforce
)


def load_properties_data(filename: str) -> pd.DataFrame:
    """
    Load property data from a CSV file with index in the first column.
    """
    dataset_path = os.path.abspath(os.path.join(filename))
    return pd.read_csv(dataset_path, index_col=0)


def compare_algorithms(properties_df: pd.DataFrame, total_budget_rp: int) -> pd.DataFrame:
    """
    Compare multiple portfolio selection algorithms (DP, Greedy, Brute Force)
    and return a summary DataFrame with performance metrics.
    """
    algorithms = {
        'Dynamic Programming': solve_portfolio_DP,
        'Greedy': solve_portfolio_greedy,
        'Brute Force': solve_portfolio_bruteforce
    }
    results = []

    for name, func in algorithms.items():
        start_time = time.time()
        try:
            npv, selected_idxs, cost = func(properties_df, total_budget_rp)
            error = None
        except Exception as e:
            npv, selected_idxs, cost = None, [], None
            error = str(e)
        elapsed = time.time() - start_time

        results.append({
            'Algorithm': name,
            'Total NPV': npv,
            'Total Cost': cost,
            'Num Items': len(selected_idxs),
            'Time (s)': round(elapsed, 4),
            'Error': error
        })

    return pd.DataFrame(results)


def test_greedy_accuracy(properties_df: pd.DataFrame, total_budget_rp: int,
                         num_tests: int = 100, sample_size: int = 20) -> None:
    """
    Run multiple trials sampling random subsets and compare Greedy vs DP.
    Prints the number and rate of times Greedy yields suboptimal NPV.
    """
    failures = 0
    for i in range(num_tests):
        random_seed = random.randint(0, 1_000_000)
        sample = properties_df.sample(n=sample_size, random_state=random_seed)
        dp_npv, _, _ = solve_portfolio_DP(sample, total_budget_rp)
        greedy_npv, _, _ = solve_portfolio_greedy(sample, total_budget_rp)
        if greedy_npv < dp_npv:
            failures += 1

    print(f"\nGreedy vs DP Accuracy over {num_tests} trials:")
    print(f" suboptimal {failures} times ({failures/num_tests:.2%} failure rate)")
    print(f"Greedy matched DP {num_tests - failures} times ({(num_tests-failures)/num_tests:.2%} success rate)")


def main():
    # Configuration
    budget = 10_000_000_000  # Total budget in Rp
    data_file = 'rumah123_2025_sale_modelled.csv'
    num_trials = 1000
    sample_size = 20

    # Load and preprocess
    df = load_properties_data(data_file)
    df.query('NPV > 0', inplace=True)
    properties = df[['price_in_rp', 'NPV']]

    # Display basic info
    print(f"Total Properties Available: {len(properties)}")
    print(f"Total Budget: Rp {budget:,.0f}")
    print("=" * 60)

    # Perform comparative analysis once on full sample
    properties_sample = properties.sample(n=sample_size, random_state=42)
    summary_df = compare_algorithms(properties_sample, budget)
    print("\nComparison of Algorithms on 20-sample:")
    print(summary_df.to_string(index=False))

    # Test greedy accuracy over multiple random trials
    test_greedy_accuracy(properties, budget, num_trials, sample_size)

    # Identify best by highest NPV (ignoring errors in the sample test)
    valid = summary_df.dropna(subset=['Total NPV'])
    if not valid.empty:
        best_idx = valid['Total NPV'].idxmax()
        best = valid.loc[best_idx]
        algo_name = str(best['Algorithm'])
        best_npv = best['Total NPV']
        print(f"\nBest Algorithm on 20-sample: {algo_name} (NPV = Rp {best_npv:,.0f})")

        # Show details of selected properties by best
        print("\nDetails of Selected Properties by Best Algorithm on 20-sample:")
        algorithm_map = {
            'Dynamic Programming': solve_portfolio_DP,
            'Greedy': solve_portfolio_greedy,
            'Brute Force': solve_portfolio_bruteforce
        }
        best_func = algorithm_map.get(algo_name)
        if best_func:
            _, best_idxs, _ = best_func(properties_sample, budget)
            print(properties_sample.loc[best_idxs].to_string())
        else:
            print(f"Error: Unknown algorithm '{algo_name}'")
    else:
        print("\nNo valid results to compare on 20-sample.")


if __name__ == "__main__":
    main()