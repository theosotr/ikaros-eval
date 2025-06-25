import argparse
import csv
import os

import numpy as np
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


def get_stats_data(data_dir):
    data_types = []
    data_constructors = []
    data_gadts = []
    data_params = []
    data_generics = []
    data_cases = []
    for file in os.listdir(data_dir):
        if not file.endswith(".stats"):
            continue
        segs = file.split(".stats")
        compiler, oracle = tuple(segs[0].split("_"))
        oracle = oracle.capitalize()
        file_path = os.path.join(data_dir, file)
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)
            for row in csv_reader:
                nu_types = int(row[0])
                nu_constructors = int(row[1])
                nu_gadts = int(row[3])
                nu_params = int(round(float(row[4])))
                nu_generics = int(row[5])
                nu_patterns = int(row[7])
                data_types.append(nu_types)
                data_constructors.append(nu_constructors)
                data_gadts.append(nu_gadts)
                data_params.append(nu_params)
                data_generics.append(nu_generics)
                data_cases.append(nu_patterns)
    return [
        {
            "samples": data_types,
            "use_log": False,
            "figname": "types.pdf",
            "description": "Type declarations",
        },
        {
            "samples": data_constructors,
            "use_log": False,
            "figname": "constructors.pdf",
            "description": "Constructors"
        },
        {
            "samples": data_gadts,
            "use_log": False,
            "figname": "gadts.pdf",
            "description": "GADTs"
        },
        {
            "samples": data_params,
            "use_log": False,
            "figname": "params.pdf",
            "description": "Constructor params",
        },
        {
            "samples": data_generics,
            "use_log": False,
            "figname": "generics.pdf",
            "description": "Polymorphic types",
        },
        {
            "samples": data_cases,
            "use_log": True,
            "figname": "patterns.pdf",
            "description": "Patterns",
        },
    ]


def generate_histogram(samples, use_log, histogram_filename):
    """Generate histogram and save it as a PDF without white space."""
    plt.figure(figsize=(4, 1))  # Fixed height (1 inch)

    nu_bins = len(set(samples))
    if use_log:
        new_samples = []
        for s in samples:
            if s < 1:
                new_samples.append(s + 1)
            else:
                new_samples.append(s)
        samples = new_samples
        plt.xscale('log')
        bins = np.logspace(np.log10(min(samples)), np.log10(max(samples)), 20)
    else:
        if nu_bins > 12:
            nu_bins = 12
        bins = np.linspace(min(samples), max(samples), nu_bins + 1)

    # Create histogram
    # bins = optimal_bins(samples)

    plt.hist(samples, bins=bins, color='red', edgecolor='white', linewidth=0.8)

    # Remove all axis labels and ticks
    plt.xticks([])  # Remove xticks
    plt.yticks([])  # Remove yticks
    plt.gca().spines['top'].set_visible(False)  # Remove top spine
    plt.gca().spines['right'].set_visible(False)  # Remove right spine
    plt.gca().spines['left'].set_visible(False)  # Remove left spine
    plt.gca().spines['bottom'].set_visible(False)  # Remove bottom spine

    plt.gca().tick_params(axis='x', which='both', bottom=False, top=False)  # Hides all x ticks
    plt.gca().tick_params(axis='y', which='both', left=False, right=False)  # Hides all y ticks
    # Set the limits to be tight around the bars, no padding
    plt.xlim(min(samples), max(samples))  # Limit x-axis to the range of the samples
    plt.ylim(0, np.max(np.histogram(samples, bins=bins)[0]))  # Limit y-axis to the maximum frequency

    # Use tight_layout to remove extra space around the plot
    plt.tight_layout(pad=0)  # Ensure no padding around the plot

    # Save histogram as PDF with tight bounding box to remove white space around it
    plt.savefig(histogram_filename, dpi=300, bbox_inches='tight', transparent=True)
    plt.close()


def print_statistics_table(title, sample_data, output_dir):

    def print_line(columns, values):
        row_format = "{:<20}" + "{:<10}" * (len(columns) - 2) + "{:<30}"
        print(row_format.format(*values))

    header = ("Description", "5%", "Mean", "Median", "95%", "Histogram")
    row_format = "{:<20}" + "{:<10}" * (len(header) - 2) + "{:<30}"
    lenght = 10 * (len(header) - 2) + 50
    print(title.center(lenght))
    print(lenght * "=")
    print(row_format.format(*header))
    print(lenght * "-")

    for i, data in enumerate(sample_data):
        samples, figname, use_log, description = data["samples"], \
            data["figname"], data["use_log"], data['description']

        # Calculate statistics
        percentile_5 = np.percentile(samples, 5)
        mean = round(np.mean(samples))
        median = np.median(samples)
        percentile_95 = np.percentile(samples, 95)

        # Generate histogram file name
        histogram_filename = figname
        histogram_dir = f"{output_dir}/histograms"

        # Ensure the directory exists to save the histograms
        if not os.path.exists(histogram_dir):
            os.makedirs(histogram_dir)

        # Generate histogram and save it in the 'histograms' directory
        histogram_path = os.path.join(histogram_dir, histogram_filename)
        generate_histogram(samples, use_log, histogram_path)

        row = description, percentile_5, mean, median, percentile_95, histogram_path
        print_line(header, row)


def main():
    args = get_args()
    df = load_data(args.data)
    plot_pattern_diagram(df, args.output)

    stats = get_stats_data(args.data)
    print_statistics_table("Table 2b", stats, args.output)


if __name__ == "__main__":
    main()
