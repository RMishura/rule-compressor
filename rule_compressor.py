import argparse

import pandas as pd

class Rule:
    def __init__(self, description: str):
        lhs, rhs = description.split("=>")
        lhs = lhs.strip()
        conditions = [cond.strip() for cond in lhs.split("AND")]
        self.predicates = []
        for cond in conditions:
            if cond.startswith("NOT "):
                var_name = cond[4:].strip()
                positive = False
            else:
                var_name = cond
                positive = True
            self.predicates.append((var_name, positive))

    def apply(self, person_id) -> bool:
        is_old = True
        for var_name, positive in self.predicates:
            val = data[var_name][person_id]

            if pd.isna(val):
                return False

            if positive:
                is_old = is_old and (val == True)
            else:
                is_old = is_old and (val == False)
        return is_old

    def usefulness(self):
        young = 0
        old = 0
        for person_id in range(len(data)):
            if self.apply(person_id):
                if data["donor_is_old"][person_id]:
                    old += 1
                else:
                    young += 1
        return (old - young)/(old + young)**0.5

    def __repr__(self):
        return f"Rule({self.predicates})"

def load(path: str) -> list[Rule]:
    rules = []
    with open(path, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                rule = Rule(line)
            rules.append(rule)
    return rules


def apply(rules: list[Rule], person_id: int) -> int:
    cnt = 0
    for rule in rules:
        cnt += (rule.apply(person_id) == True)
    return cnt

def save(rules: list[Rule], path: str):
    with open(path, "w") as file:
        for rule in rules:
            lhs = " AND ".join(
                (f"NOT {var}" if not positive else var)
            for var, positive in rule.predicates
            )
            file.write(f"{lhs} => donor_is_old\n")

def similarity(r1: Rule, r2: Rule) -> float:
    intersection = 0
    union = 0
    for person_id in range(len(data)):
        if r1.apply(person_id) and r2.apply(person_id):
            intersection += 1
        if r1.apply(person_id) or r2.apply(person_id):
            union += 1
    return intersection/union

def compression(rules: list[Rule], limit=None, threshold = 0.8) -> list[Rule]:

    if limit is None:
        limit = len(rules) // 3

    sorted_rules = sorted(rules, key=lambda rule: rule.usefulness(), reverse=True)
    chosen_rules = []

    for r1 in sorted_rules:
        if all(similarity(r1, r2) <= threshold for r2 in chosen_rules) and len(chosen_rules) < limit:
            chosen_rules.append(r1)

    return chosen_rules


def main():
    global data
    parser = argparse.ArgumentParser()
    parser.add_argument("data", type=str)
    parser.add_argument("in_rules", type=str)
    parser.add_argument("out_rules", type=str)
    parser.add_argument("--limit", type=int, default=None)

    args = parser.parse_args()

    data = pd.read_csv(args.data, sep="\t")

    rules = load(args.in_rules)

    compressed_rules = compression(rules, limit=args.limit)

    save(compressed_rules, args.out_rules)

    print(f"Compressed {len(rules)} rules into {len(compressed_rules)} rules.")


if __name__ == "__main__":
    main()
