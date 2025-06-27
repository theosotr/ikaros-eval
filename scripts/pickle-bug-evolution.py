import argparse
from collections import defaultdict
import pickle
from datetime import datetime, timezone
import os


def get_args():
    parser = argparse.ArgumentParser(
        description=("Extract the time when each method discovered bugs and"
                     " stored them in picked data"))
    parser.add_argument("--ikaros-run",
                        required=True,
                        help=("Path to the directory that stores the"
                              " results of an Ikaros run"))
    parser.add_argument("--time-dir",
                        required=True,
                        help=("Directory that indicates the time"
                              " when each Ikaros run terminated"))
    parser.add_argument("--duration", type=int,
                        required=True,
                        help=("The duration of each Ikaros run in seconds"))
    parser.add_argument("--output-dir",
                        required=True,
                        help=("Directory to store the pickled data"))
    return parser.parse_args()


def extract_end_date(compiler, oracle, timedir):
    file_path = os.path.join(timedir, f"{compiler}_{oracle.lower()}")
    if not os.path.exists(file_path):
        return None

    return os.path.getmtime(file_path)


def extract_data(args, compiler, oracle, end_date):
    dirs = [
        os.path.join(args.ikaros_run, oracle, compiler,
                     "exhaustiveness", "false_positive"),
        os.path.join(args.ikaros_run, oracle, compiler,
                     "exhaustiveness", "false_negative"),
    ]
    suffixes = {
        "scalac": ".scala",
        "javac": ".java",
        "ghc": ".hs"
    }
    suffix = suffixes[compiler]
    data = defaultdict(list)
    total_seconds = args.duration
    for d in dirs:
        if not os.path.exists(d):
            continue
        for f in os.listdir(d):
            if not f.endswith(suffix):
                continue

            path = os.path.join(d, f)
            modtimestamp = os.path.getctime(path)
            offset = datetime.now().astimezone().utcoffset()
            tz_offset = timezone(offset)
            mod_time = \
                datetime.fromtimestamp(modtimestamp).replace(tzinfo=tz_offset)

            end_time = \
                datetime.fromtimestamp(end_date).replace(tzinfo=tz_offset)
            diff = total_seconds - (end_time - mod_time).total_seconds()

            data[(compiler, oracle)].append(diff)
    return data


def pickle_data(compiler, oracle, data, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{compiler}_{oracle.lower()}.pkl")
    with open(file_path, "wb") as file:
        pickle.dump(data, file)


def main():
    args = get_args()
    compilers = ["javac", "scalac", "ghc"]
    oracles = ["Construction", "Z3"]
    for compiler in compilers:
        for oracle in oracles:
            end_date = extract_end_date(compiler, oracle, args.time_dir)
            if end_date is None:
                continue
            data = extract_data(args, compiler, oracle, end_date)
            pickle_data(compiler, oracle, data, args.output_dir)


if __name__ == "__main__":
    main()
