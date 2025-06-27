import argparse
import csv
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


plt.style.use('default')
sns.set(style="whitegrid")
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
        description='Study the performance of the generated programs')
    parser.add_argument("data",
                        help="Directory with statistics")
    return parser.parse_args()


def load_data(data_dir):
    data = {
        "scalac_construction": {},
        "scalac_z3": {},
        "javac_construction": {},
        "javac_z3": {},
        "ghc_construction": {},
        "ghc_z3": {},
    }
    for file in os.listdir(data_dir):
        if not file.endswith(".stats"):
            continue
        segs = file.split(".stats")
        compiler, oracle = tuple(segs[0].split("_"))
        oracle = oracle.lower()
        file_path = os.path.join(data_dir, file)
        df = pd.read_csv(file_path)[:10000]
        key = f"{compiler}_{oracle}"
        data[key]["compilation"] = df["processing_time"]
        data[key]["generation"] = df["program_gen_time"]
        if oracle == "z3":
            data[key]["SMT solving"] = df["solver_time"]
    return data


def print_performance_table(title, data, unit):

    def print_line(columns, values):
        row_format = "{:<20}" * len(columns)
        print(row_format.format(*values))

    def convert_metric(val):
        if unit == "ms":
            val = round(val / 1000, 1)
        return str(val) + unit

    if title != "SMT solving":
        header = ("", "RefPG", "RPG")
    else:
        header = ("", "w/ timeout", "w/o timeout")
    row_format = "{:<20}" * len(header)
    lenght = 20 * len(header)
    key = title
    title = f"{title.capitalize()} time (Table 3)"
    print(title.center(lenght))
    print(lenght * "=")
    print(row_format.format(*header))
    print(lenght * "-")

    for compiler in ["javac", "scalac", "ghc"]:
        if key != "SMT solving":
            metric1 = convert_metric(
                round(data[f"{compiler}_construction"][key].mean())
            )
        else:
            df = data[f"{compiler}_z3"][key]
            filtered_df = df[df < 50000]
            metric1 = convert_metric(
                round(filtered_df.mean())
            )

        metric2 = convert_metric(
            round(data[f"{compiler}_z3"][key].mean())
        )
        row = (compiler, metric1, metric2)
        print_line(header, row)


def main():
    args = get_args()
    data = load_data(args.data)
    print_performance_table("generation", data, "μs")
    print()
    print_performance_table("compilation", data, "ms")
    print()
    print_performance_table("SMT solving", data, "ms")


if __name__ == "__main__":
    main()
