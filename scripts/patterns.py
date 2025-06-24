import argparse
import os

import pandas as pd
import matplotlib.pyplot as plt
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
        description='Study the characteristics of the generated programs')
    parser.add_argument("data", help="Directory with statistics")
    parser.add_argument("output", help="Directory to store the figure.")
    return parser.parse_args()


def load_data(data_dir):
    data = {}
    stat = 'num_patterns'
    for file in os.listdir(data_dir):
        if not file.endswith(".stats"):
            continue
        segs = file.split(".stats")
        compiler, oracle = tuple(segs[0].split("_"))
        oracle = oracle.capitalize()
        file_path = os.path.join(data_dir, file)
        df = pd.read_csv(file_path)[:10000]
        if oracle not in data:
            data[oracle] = df[stat]
        else:
            data[oracle] = pd.concat([data[oracle], df[stat]],
                                     ignore_index=True)
    return pd.DataFrame(data=data)


def plot_pattern_diagram(df, output_dir):
    fig, ax = plt.subplots()

    method_mapping = {"Z3": "RPG", "Construction": "RefPG"}
    bins = [0, 5, 10, 20, 50, 100, float('inf')]
    labels = ["[1, 5]", "[6, 10]", "[11, 20]", "[21, 50]", "[51, 100]", "> 100"]

    df_melted = df.melt(var_name="Method", value_name="Patterns")
    df_melted["Method"] = df_melted["Method"].map(method_mapping)
    df_melted["Category"] = pd.cut(df_melted["Patterns"], bins=bins, labels=labels, right=True)
    category_counts = df_melted.groupby(["Method", "Category"]).size().reset_index(name="Count")

    sns.barplot(data=category_counts, x="Category", y="Count", hue="Method", palette="gray")

    plt.legend()
    plt.xlabel("Number of cases")
    plt.ylabel('Frequency')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/patterns.pdf', bbox_inches='tight',
                pad_inches=0)


def main():
    args = get_args()
    df = load_data(args.data)
    plot_pattern_diagram(df, args.output)


if __name__ == "__main__":
    main()
