import argparse
import json
from collections import defaultdict


lang_lookup = {
    'scala': 'scalac',
    'java': 'javac',
    'haskell': 'ghc',
    'total': 'Total'
}

status_lookup = {
    "fixed": "Fixed",
    "confirmed": "Confirmed",
    "unconfirmed": "Unconfirmed",
    "won't fix": "Wont fix"
}

symptom_lookup = {
    "fn-exhaustiveness": "Exhaustiveness FN",
    "fp-exhaustiveness": "Exhaustiveness FP",
    "fp-redundancy": "Redundancy FP",
    "performance": "Performance",
}


def get_args():
    parser = argparse.ArgumentParser(
        description='Process bugs.json to answer RQs')
    parser.add_argument("input", help="JSON File with bugs.")
    parser.add_argument("rq", choices=['rq1', 'rq2'], help="Select RQ.")
    return parser.parse_args()


def process(bug, res, chars, categories):
    lang = bug['language']
    status = bug['status']
    symptom = bug['symptom']
    lang = lang_lookup.get(lang)
    status = status_lookup.get(status)
    symptom = symptom_lookup.get(symptom)
    res[lang]['status'][status] += 1
    res[lang]['symptom'][symptom] += 1
    res['total']['status'][status] += 1
    res['total']['symptom'][symptom] += 1

    bcategories = set()
    for char in bug['characteristics']:
        bcategories.add(char)
        chars[char] += 1
    for c in bcategories:
        categories[c] += 1


def print_table(title, column_name, res, extra_line=True, first_col=20):
    # res should be a dict of dict in the following format:
    # {"row name": {"column name": value, ...}, ...}
    def print_line(title, columns, values):
        row_format = f"{{:<{first_col}}}" + "{:<10}" * len(columns)
        print(row_format.format(
            title,
            *(values[column] for column in columns)
        ))
    if len(res.values()) == 0:
        return

    header = [column_name] + list(list(res.values())[0].keys())
    row_format = f"{{:<{first_col}}}" + "{:<10}" * (len(header) - 1)
    lenght = first_col + 10 * (len(header) - 1)
    print(title.center(lenght))
    print(lenght * "=")
    pretty_header = [lang_lookup.get(h, h) for h in header]
    print(row_format.format(*pretty_header))
    print(lenght * "-")
    for counter, item in enumerate(res.items()):
        row_name, values = item
        if extra_line and counter == len(res)-1:
            print(lenght * "-")
        print_line(row_name, header[1:], values)
    print()


def print_chars(title, column_name, res, extra_line=True, first_col=20):
    # res should be a dict of dict in the following format:
    # {"row name": {"column name": value, ...}, ...}
    def print_line(title, columns, values):
        row_format = "{:<10}" * len(columns)
        print(row_format.format(*values))

    if len(res.values()) == 0:
        return

    header = ("ID", "Language", "ADT", "GADT", "Poly. ADT", "constant", "null")

    row_format = "{:<10}" * len(header)
    lenght = 10 * len(header)
    print(title.center(lenght))
    print(lenght * "=")
    print(row_format.format(*header))
    print(lenght * "-")

    indexes = {
        "ADT": 2,
        "GADT": 3,
        "Poly. ADT": 4,
        "constant": 5,
        "null": 6
    }

    for i, bug in enumerate(res.values()):
        row = [i + 1, bug["language"]] + ["No"] * (len(header) - 2)
        chars = bug["characteristics"]
        for char in chars:
            row[indexes[char]] = "Yes"

        print_line("", header, row)


def main():
    args = get_args()
    with open(args.input, 'r') as f:
        data = json.load(f)
    chars = defaultdict(lambda: 0)
    res = defaultdict(lambda: {
        'status': {
            'Unconfirmed': 0,
            'Confirmed': 0,
            'Fixed': 0,
            'Wont fix': 0,
        },
        'symptom': {
            'Exhaustiveness FP': 0,
            'Exhaustiveness FN': 0,
            'Redundancy FP': 0,
            'Performance': 0
        },
        "chars": {
            "ADT": 0,
            "GADT": 0,
            "Poly. ADT": 0,
            "constant": 0,
            "null": 0
        }
    })
    categories = defaultdict(lambda: 0)
    for bug in data.values():
        process(bug, res, chars, categories)

    langs = ['scalac', 'javac', 'ghc', 'total']

    def per_attribute(attrs, attr, total=True):
        r = {
            s: {lang: res[lang][attr][s]
                for lang in langs}
            for s in attrs
        }
        if total:
            r['Total'] = {lang: sum(res[lang][attr][s] for s in r)
                          for lang in langs}
        return r

    if args.rq == 'rq1':
        status_cat = res['total']['status'].keys()
        status = per_attribute(status_cat, 'status', total=True)
        print_table('Table 1a', 'Status', status)

    if args.rq == 'rq2':
        symtoms_cat = res['total']['symptom'].keys()
        symptoms = per_attribute(symtoms_cat, 'symptom', total=False)
        print_table('Table 1b', 'Symptoms', symptoms, extra_line=False)

        print()
        print_chars('Table 2a', 'Characteristics', data,
                    extra_line=False)


if __name__ == "__main__":
    main()
