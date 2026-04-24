import matplotlib.pyplot as plt
from statistics import mean, stdev
from binary_function import genetic_algorithm
from arithmetic_function import evolutionary_algorithm
from random import randint,random

# Tworzenie danych do testów
def gen_pop_bin(number_of_indv, number_of_genes):
    return [[randint(0,1) for _ in range(number_of_genes)] for _ in range(0,number_of_indv) ]

def gen_pop_real(number_of_indv, number_of_genes):
    return [[random()*10-5 for _ in range(number_of_genes)] for _ in range(0,number_of_indv) ]

# Wielokrotne uruchomienie
def run_multiple(algorithm, pop_generator, runs, pop_size, genes, params):
    results = []

    for _ in range(runs):
        population = pop_generator(pop_size, genes)
        _, score = algorithm(population, **params)
        results.append(score)

    return results


# Statystyki
def compute_stats(results):
    return {
        "mean": mean(results),
        "std": stdev(results),
        "min": min(results),
        "max": max(results)
    }


def print_stats(name, stats):
    print(f"\n=== {name} ===")
    print(f"Średnia: {stats['mean']:.4f}")
    print(f"Odch.std: {stats['std']:.4f}")
    print(f"Min: {stats['min']:.4f}")
    print(f"Max: {stats['max']:.4f}")

# Test jednego ustawienia
def test_config(name, algorithm, pop_generator, runs, pop_size, genes, params):
    results = run_multiple(algorithm, pop_generator, runs, pop_size, genes, params)
    stats = compute_stats(results)
    print_stats(name, stats)
    return results


# Zmiana parametrów
def parameter_sweep(param_name, values, algorithm, pop_generator, runs, pop_size, genes, base_params):
    means = []
    stds = []

    for val in values:
        params = base_params.copy()
        params[param_name] = val

        results = run_multiple(algorithm, pop_generator, runs, pop_size, genes, params)
        stats = compute_stats(results)

        means.append(stats["mean"])
        stds.append(stats["std"])

        print(f"{param_name}={val} -> mean={stats['mean']:.4f}")

    return values, means, stds


# Wykresy
def plot_line(x, means, stds, title, xlabel):
    plt.figure()
    plt.errorbar(x, means, yerr=stds, marker='o')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Wartość funkcji celu")
    plt.grid()
    plt.show()


def plot_box(results_list, labels, title):
    plt.figure()
    plt.boxplot(results_list, labels=labels)
    plt.title(title)
    plt.ylabel("Wartość funkcji celu")
    plt.grid()
    plt.show()




if __name__ == "__main__":

    RUNS = 25

    # Ga
    ga_params = {
        "Fes": 9000,
        "k": 4,
        "n": 2,
        "pc": 0.9
    }

    ga_results = test_config(
        "GA - baseline",
        genetic_algorithm,
        gen_pop_bin,
        RUNS,
        pop_size=100,
        genes=80,
        params=ga_params
    )

    # Test parametru k
    k_values = [2, 4, 6, 8]
    x, means, stds = parameter_sweep(
        "k",
        k_values,
        genetic_algorithm,
        gen_pop_bin,
        RUNS,
        100,
        80,
        ga_params
    )

    plot_line(x, means, stds, "GA: wpływ k", "k")

    # Ea
    ea_params = {
        "fes": 9000,
        "mu": 20,
        "sigma": 0.5,
        "lambda_": 100,
        "pc": 0.9
    }

    ea_results = test_config(
        "EA - baseline",
        evolutionary_algorithm,
        gen_pop_real,
        RUNS,
        pop_size=100,
        genes=10,
        params=ea_params
    )

    # Test parametru sigma
    sigma_values = [0.1, 0.3, 0.5, 1.0]
    x, means, stds = parameter_sweep(
        "sigma",
        sigma_values,
        evolutionary_algorithm,
        gen_pop_real,
        RUNS,
        100,
        10,
        ea_params
    )

    plot_line(x, means, stds, "EA: wpływ sigma", "sigma")

    # Porównanie algorytmów
    plot_box(
        [ga_results, ea_results],
        ["GA (binarny)", "EA (rzeczywisty)"],
        "Porównanie algorytmów"
    )