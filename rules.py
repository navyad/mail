import json


def load_rules():
    with open('rules.json', 'r') as file:
        rules_data = json.load(file)
        return rules_data


def find_rule_by_description(description):
    for rule in load_rules():
        if rule['description'] == description:
            return rule
    raise Exception(f"Rule not found: {description}")
