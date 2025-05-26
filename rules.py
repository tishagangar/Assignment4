# rules.py
from production import IF, AND, THEN, OR, NOT, match, populate, simplify
from data import poker_data, abc_data, minecraft_data, simpsons_data, black_data, zookeeper_rules

# Problem 4
def transitive_rule():
    return IF(
        AND('(?x) beats (?z)', '(?z) beats (?y)'),
        THEN('(?x) beats (?y)')
    )

# Problem 5
def family_rules():
    rules = []
    rules.append(IF('parent (?x) (?y)', THEN('child (?y) (?x)')))
    rules.append(IF(AND('parent (?x) (?z)', 'parent (?z) (?y)'), THEN('grandparent (?x) (?y)')))
    rules.append(IF('grandparent (?x) (?y)', THEN('grandchild (?y) (?x)')))
    rules.append(IF(AND('parent (?p) (?x)', 'parent (?p) (?y)', NOT('(?x) = (?y)')), THEN('sibling (?x) (?y)')))
    rules.append(IF(AND('parent (?px) (?x)', 'parent (?py) (?y)', 'sibling (?px) (?py)', NOT('sibling (?x) (?y)')), THEN('cousin (?x) (?y)')))
    return rules

# Problem 6
def backchain_to_goal_tree(rules, hypothesis):
    goal = OR(hypothesis)
    for rule in rules:
        binding = match(rule.consequent(), hypothesis)
        if binding:
            inst = populate(rule.antecedent(), binding)
            if isinstance(inst, AND):
                goal.conds.append(AND(*[backchain_to_goal_tree(rules, c) for c in inst]))
            elif isinstance(inst, OR):
                goal.conds.append(OR(*[backchain_to_goal_tree(rules, c) for c in inst]))
            else:
                goal.conds.append(backchain_to_goal_tree(rules, inst))
    return simplify(goal)

