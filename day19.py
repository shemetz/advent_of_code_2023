import re
from typing import NamedTuple, List, Dict

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

XMAS = str  # x, m, a, or s
Rule = NamedTuple("Rule", field=XMAS, less_vs_more=bool, value=int, target=str)
Workflow = NamedTuple("Workflow", name=str, default=str, rules=List[Rule])
Part = NamedTuple("Part", x=int, m=int, a=int, s=int)
INPUT_WORKFLOW_NAME = "in"

rule_lines = input_lines[:input_lines.index('')]
part_lines = input_lines[input_lines.index('') + 1:]
workflows: Dict[str, Workflow] = {}
for line in rule_lines:
    # e.g. px{a<2006:qkq,m>2090:A,rfg}
    name, stuff = line.strip("}").split("{")
    s_rules = stuff.split(",")
    s_rules_2 = s_rules[:-1]
    default = s_rules[-1]
    rules = []
    for s_rule in s_rules_2:
        field, value, target = re.split("[><:]", s_rule)
        less_vs_more = "<" in s_rule
        rules.append(Rule(field=field, less_vs_more=less_vs_more, value=int(value), target=target))
    workflow = Workflow(name=name, default=default, rules=rules)
    workflows[workflow.name] = workflow
parts = []
for line in part_lines:
    # e.g. {x=787,m=2655,a=1222,s=2876}
    s_equals = line.strip("{}").split(",")
    equals = [s_equal.split("=") for s_equal in s_equals]
    values = {left: int(right) for left, right in equals}
    part = Part(*values.values())
    parts.append(part)


def put_through_workflow(part: Part, workflow_name: str):
    if workflow_name in "AR":
        return workflow_name
    workflow = workflows[workflow_name]
    rules = workflow.rules
    for rule in rules:
        if rule.less_vs_more:
            if part.__getattribute__(rule.field) < rule.value:
                return put_through_workflow(part, rule.target)
        else:
            if part.__getattribute__(rule.field) > rule.value:
                return put_through_workflow(part, rule.target)
    return put_through_workflow(part, workflow.default)


total_sum = 0
for part in parts:
    outcome = put_through_workflow(part, INPUT_WORKFLOW_NAME)
    if outcome == "A":
        total_sum += part.x + part.m + part.a + part.s
print(total_sum)  # 352052

# part 2... oh fuck this is a tough one

count = 0

# PLAN A: brute force.  totally fails, too slow.

# PLAN B: only try relevant range combinations.  works for example but STILL TOO SLOW for real input (ETA: 5 hours)
# import itertools
# def calc_relevant_ranges(field_name: str):
#     relevant_ones = [n for n in range(2, 4000) if
#                      any(r.field == field_name and r.value == (n if r.less_vs_more else n - 1)
#                          for wf in workflows.values() for r in wf.rules)]
#     return [1] + relevant_ones + [4001]
# relevant_x_ranges = calc_relevant_ranges("x")
# relevant_m_ranges = calc_relevant_ranges("m")
# relevant_a_ranges = calc_relevant_ranges("a")
# relevant_s_ranges = calc_relevant_ranges("s")
# for from_x, to_x in itertools.pairwise(relevant_x_ranges):
#     print("... from x:", from_x)
#     for from_m, to_m in itertools.pairwise(relevant_m_ranges):
#         for from_a, to_a in itertools.pairwise(relevant_a_ranges):
#             for from_s, to_s in itertools.pairwise(relevant_s_ranges):
#                 pseudopart = Part(from_x, from_m, from_a, from_s)
#                 outcome = put_through_workflow(pseudopart, INPUT_WORKFLOW_NAME)
#                 if outcome == "A":
#                     count += (to_x - from_x) * (to_m - from_m) * (to_a - from_a) * (to_s - from_s)





# PLAN C:  funnel

Constraint = NamedTuple("Constraint", field=XMAS, bottom=int, top=int)   # [bottom, top) - exclusive top
Constraints = Dict[XMAS, Constraint]


def recursive_partial_solve(starting_workflow_name: str, constraints: Constraints):
    if starting_workflow_name == "A":
        multisum = 1
        for constraint in constraints.values():
            multisum *= constraint.top - constraint.bottom
        return multisum
    if starting_workflow_name == "R":
        return 0
    workflow = workflows[starting_workflow_name]
    sub_count = 0
    remaining_constraints = constraints.copy()
    for rule in workflow.rules:
        c_field, c_bot, c_top = constraints[rule.field]
        ch_bot, ch_top = c_bot, c_top
        cl_bot, cl_top = c_bot, c_top
        if rule.less_vs_more:
            ch_top = min(rule.value, remaining_constraints[c_field].top)
            cl_bot = max(c_bot, ch_top)
        else:
            ch_bot = max(rule.value + 1, remaining_constraints[c_field].bottom)
            cl_top = min(ch_bot, c_top)
        harder_constraints = remaining_constraints.copy()
        harder_constraints[c_field] = Constraint(c_field, ch_bot, ch_top)
        if harder_constraints[c_field].bottom < harder_constraints[c_field].top:  # if even possible
            sub_count += recursive_partial_solve(rule.target, harder_constraints)
        leftover_constraints = remaining_constraints.copy()
        leftover_constraints[c_field] = Constraint(c_field, cl_bot, cl_top)
        remaining_constraints = leftover_constraints
    sub_count += recursive_partial_solve(workflow.default, remaining_constraints)
    return sub_count


starting_constraints = {field: Constraint(field, 1, 4001) for field in "xmas"}
print(recursive_partial_solve(INPUT_WORKFLOW_NAME, starting_constraints))  # 287106896578654 is TOO HIGH
