import argparse
import pickle
import os

import matplotlib.pyplot as plt

import numpy as np

import seaborn as sns

plt.style.use('default')
sns.set(style="whitegrid")
plt.rcParams['font.family'] = 'Ubuntu'
plt.rcParams['font.serif'] = 'Ubuntu'
plt.rcParams['font.monospace'] = 'Inconsolata Medium'
plt.rcParams['font.size'] = 19
plt.rcParams['axes.labelsize'] = 22
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 19
plt.rcParams['ytick.labelsize'] = 18
plt.rcParams['legend.fontsize'] = 22
plt.rcParams['figure.titlesize'] = 24
plt.rcParams['figure.figsize'] = (9, 5)
plt.rcParams['pdf.fonttype'] = 42


def get_args():
    parser = argparse.ArgumentParser(
        description='Study the evolution of bug detection')
    parser.add_argument("data", help="Directory with pickled data.")
    parser.add_argument("output", help="Directory to store the figure.")
    parser.add_argument("--avoid-log-scale",
                        default=False,
                        action="store_true",
                        help="Avoid using log scale in the y axis.")
    return parser.parse_args()


def load_data(data_dir):
    oracles = ["z3", "construction"]
    compilers = ["scalac", "javac", "ghc"]
    data = {}
    for compiler in compilers:
        for oracle in oracles:
            file_path = os.path.join(data_dir, f"{compiler}_{oracle}.pkl")
            if not os.path.exists(file_path):
                continue
            with open(file_path, "rb") as f:
                data[f"{compiler}_{oracle}"] = pickle.load(f)
    return data


def print_table(title, data):
    map_oracles = {
        "z3": "RPG",
        "construction": "RefPG",
    }
    new_data = {
        "RPG": {
            "scalac": 0,
            "javac": 0,
            "ghc": 0
        },
        "RefPG": {
            "scalac": 0,
            "javac": 0,
            "ghc": 0,
        }
    }
    for key, times in data.items():
        if not times:
            continue
        compiler, oracle = tuple(key.split("_"))
        oracle = map_oracles.get(oracle)
        new_data[oracle][compiler] = len(list(times.values())[0])

    # res should be a dict of dict in the following format:
    # {"row name": {"column name": value, ...}, ...}
    def print_line(columns, values):
        row_format = "{:<10}" * len(columns)
        print(row_format.format(*values))

    header = ("Pat Gen", "scalac", "javac", "ghc", "Total")

    row_format = "{:<10}" * len(header)
    lenght = 10 * len(header)
    print(title.center(lenght))
    print(lenght * "=")
    print(row_format.format(*header))
    print(lenght * "-")

    for pat_gen, values in new_data.items():
        total = sum(val for val in values.values())
        row = [pat_gen] + [values["scalac"], values["javac"], values["ghc"],
                           total]
        print_line(header, row)


def plot_evolution_diagram(data, output_dir, log_scale):
    map_oracles = {
        "Z3": "RPG",
        "Construction": "RefPG",
    }

    plot_data = {}
    for label, bug_dict in data.items():
        for (compiler, oracle), times in bug_dict.items():
            key = f"{compiler} - {map_oracles[oracle]}"
            if key not in plot_data:
                plot_data[key] = []
            plot_data[key].extend(times)

    all_times = []
    for times in plot_data.values():
        all_times.extend(times)

    all_times = sorted(all_times)

    standardized_data = {}

    for key, times in plot_data.items():
        print("Size of data: ", len(times))
        times = np.array(times)  # Convert to numpy array for easy processing
        times.sort()
        cumulative_counts = np.arange(1, len(times) + 1)

        interpolated_counts = []
        current_count = 0
        index = 0

        for t in all_times:
            if index < len(times) and times[index] == t:
                current_count = cumulative_counts[index]
                index += 1
            interpolated_counts.append(current_count)

        standardized_data[key] = (all_times, interpolated_counts)

    fig, ax = plt.subplots(figsize=(10, 6))

    color_palette = sns.color_palette("colorblind")

    for i, (key, (times, counts)) in enumerate(standardized_data.items()):
        times = np.array(times)
        color = color_palette[i % len(color_palette)]
        ax.plot(times, counts, label=key, linestyle='-', linewidth=3,
                color=color)

    if log_scale:
        ax.set_yscale("log")

    ax.set_xlabel("Time (hours)")
    ax.set_ylabel("Cumulative bug count")
    ax.legend()

    plt.tight_layout()
    plt.savefig(f"{output_dir}/evolution.pdf", bbox_inches='tight',
                pad_inches=0)


def main():
    args = get_args()
    data = load_data(args.data)
    plot_evolution_diagram(data, args.output,
                           log_scale=not args.avoid_log_scale)
    print_table("Table 1c", data)


if __name__ == "__main__":
    main()
