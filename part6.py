from production import AND, OR, match, populate, simplify, pretty_goal_tree
from data import zookeeper_rules

def backchain_to_goal_tree(rules, hypothesis):
    goal = OR(hypothesis)
    for rule in rules:
        binding = match(rule.consequent(), hypothesis)
        if binding:
            inst = populate(rule.antecedent(), binding)
            if isinstance(inst, AND):
                goal.append(AND(*[
                    backchain_to_goal_tree(rules, c)
                    for c in inst
                ]))
            elif isinstance(inst, OR):
                goal.append(OR(*[
                    backchain_to_goal_tree(rules, c)
                    for c in inst
                ]))
            else:
                goal.append(backchain_to_goal_tree(rules, inst))
    return simplify(goal)

# Example outputs
print("Penguin tree:")
pretty_goal_tree(backchain_to_goal_tree(zookeeper_rules, 'opus is a penguin'))

print("\nCheetah tree:")
pretty_goal_tree(backchain_to_goal_tree(zookeeper_rules, 'mark is a cheetah'))

