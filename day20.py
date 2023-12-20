import math
from collections import deque
from dataclasses import dataclass
from types import SimpleNamespace
from typing import Dict, Tuple, Optional

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

ModuleName = str
ModuleType = SimpleNamespace()
ModuleType.BROADCASTER = "broadcaster"
ModuleType.FLIP_FLOP = "%"
ModuleType.CONJUNCTION = "&"
ModuleType.FAKE = "FAKE"
PulseLevel = bool
HIGH_PULSE = True
LOW_PULSE = False
PRINTED_PULSES = {HIGH_PULSE: "█", LOW_PULSE: "░", None: ""}


@dataclass
class Module:
    name: ModuleName
    type: ModuleType
    outputs: Tuple[ModuleName, ...]
    state: Optional[PulseLevel]  # for flip flop
    inputs_memory: Dict[ModuleName, PulseLevel]  # for conjunction

    def reset(self):
        match self.type:
            case ModuleType.FLIP_FLOP:
                self.state = LOW_PULSE  # "off"
            case ModuleType.CONJUNCTION:
                self.inputs_memory = {k: LOW_PULSE for k in self.inputs_memory}

    def __str__(self):
        return f"{self.type}{self.name}    {PRINTED_PULSES[self.state]}"

    def to_char(self) -> str:
        match self.type:
            case ModuleType.FLIP_FLOP:
                return PRINTED_PULSES[self.state]
            case ModuleType.CONJUNCTION:
                the_sum = sum([0, 1][v] for v in self.inputs_memory.values())
                hexed = hex(the_sum)[2:]
                return str(hexed)
            case ModuleType.BROADCASTER:
                return "+"
            case ModuleType.FAKE:
                return "*"
        return "??? this should not happen"


modules: Dict[ModuleName, Module] = {}
for line in input_lines:
    # e.g. "broadcaster -> a", "%a -> inv, con"
    left, right = line.split(" -> ")
    match (left[0], left[1:]):
        case "b", "roadcaster":
            name = ModuleType.BROADCASTER
            m_type = ModuleType.BROADCASTER
        case "%", name:
            m_type = ModuleType.FLIP_FLOP
        case "&", name:
            m_type = ModuleType.CONJUNCTION
        case _:
            raise ValueError(f"Unknown module type: {left[0]}")
    outputs = right.split(", ")
    module = Module(name=name, type=m_type, outputs=outputs, state=None, inputs_memory={})
    modules[name] = module
    for output_name in outputs:
        if output_name not in modules:
            modules[output_name] = Module(name=output_name, type=ModuleType.FAKE, outputs=(), state=None,
                                          inputs_memory={})
for module in modules.values():
    for output_name in module.outputs:
        module2 = modules[output_name]
        if module2.type == ModuleType.CONJUNCTION:
            module2.inputs_memory[module.name] = LOW_PULSE


def press():
    low_pulse_count = 0
    high_pulse_count = 0
    # 1. press button, sending low pulse to broadcast
    pulses: deque[Tuple[ModuleName, ModuleName, PulseLevel]] = deque()
    pulses.append(("PRESS", ModuleType.BROADCASTER, LOW_PULSE))
    # 2. go through pulses
    while pulses:
        source_module_name, target_module_name, pulse_level = pulses.popleft()
        # print(f"{source_module_name} -{'high' if pulse_level else 'low'}-> {target_module_name}")
        if pulse_level == HIGH_PULSE:
            high_pulse_count += 1
        else:
            low_pulse_count += 1
        module: Module = modules[target_module_name]
        match module.type:
            case ModuleType.BROADCASTER:
                for output_name in module.outputs:
                    pulses.append((module.name, output_name, pulse_level))
            case ModuleType.FLIP_FLOP:
                if pulse_level == LOW_PULSE:
                    module.state = not module.state
                    for output_name in module.outputs:
                        pulses.append((module.name, output_name, module.state))
            case ModuleType.CONJUNCTION:
                module.inputs_memory[source_module_name] = pulse_level
                if all(module.inputs_memory.values()):  # if all are HIGH_PULSE
                    for output_name in module.outputs:
                        pulses.append((module.name, output_name, LOW_PULSE))
                else:
                    for output_name in module.outputs:
                        pulses.append((module.name, output_name, HIGH_PULSE))
            case ModuleType.FAKE:
                pass
            case _:
                raise ValueError(f"Unknown module type: {module.type}")
    return low_pulse_count, high_pulse_count


total_low_pulse_count = 0
total_high_pulse_count = 0
for button_presses in range(1, 1001):
    lpc, hpc = press()
    total_low_pulse_count += lpc
    total_high_pulse_count += hpc
multiplied = total_low_pulse_count * total_high_pulse_count
print("Part 1:", multiplied)  # 731517480


# Part 2... oh boy

def visualize():
    return "".join([module.to_char() for module in modules.values()])


for module in modules.values():
    module.reset()

for bp in range(0, 8):
    print(f"{bp:06} {visualize()}")
    press()
print(f"{8:06} {visualize()}")
print("...")
for bp in range(8, 2046):
    press()
print(f"{2046:06} {visualize()}")
press()
print(f"{2047:06} {visualize()}")
# print("non-high flip flops:", end="    ")
# for m in modules.values():
#     if m.state == LOW_PULSE:
#         print(f"{m.name}{m.to_char()}", end="    ")
# print()
press()
print(f"{2048:06} {visualize()}")
# print(f" they became:           {'    '.join(xx + modules[xx].to_char() for xx in ['sz', 'pm', 'gz', 'zq'])}")
press()
print(f"{2049:06} {visualize()}")
print("...")
for bp in range(2050, 4096):
    press()
print(f"{4096:06} {visualize()}")
press()
print(f"{4097:06} {visualize()}")


"""
000000 ░░0░░░0░░░0░░░░░░░0░░░░░+░░░0░░░░░░░░0░░0░░░░0░░░*░░░░░0░░░
000001 ░░1░░░1░░░1░░░█░░░1░░░░░+███0░░░░░░░░1░░1░░░░1░░░*░░░░░1░░░
000002 █░1░░░1░░░0░░░░░░█1░░░░░+░░░0░░░█░░░░0░░1░░░░1░░░*█░░░░1░░░
000003 █░2░░░2░░░1░░░█░░█1░░░░░+███0░░░█░░░░1░░1░░░░1░░░*█░░░░1░░░
000004 ░█1░░░0░░░0░░█░░░░1░░░░░+░░░0░░░░██░░0░░1░░░░1░░░*░░░░░1░░░
000005 ░█2░░░1░░░1░░██░░░1░░░░░+███0░░░░██░░1░░1░░░░1░░░*░░░░░1░░░
000006 ██2░░░1░░░0░░█░░░█1░░░░░+░░░0░░░███░░0░░1░░░░1░░░*█░░░░1░░░
000007 ██3░░░2░░░1░░██░░█1░░░░░+███0░░░███░░1░░1░░░░1░░░*█░░░░1░░░
000008 ░░1░░░1░░░0░░░░█░░1█░░░░+░░░0░░░░░░░░0░░1░░█░1░░░*░█░░░1░░░
...
002046 ██9███7░█░6███░███1█████+░░░0████████5░█1████1███*█████1░██
002047 ██a███8░█░7███████1█████+███0████████6░█1████1███*█████1░██  <- non-high flip flops:    sz░    pm░    gz░    zq░    
002048 ░░1░░░1█░█1░░░░░░░1░░░░░+░░░0░░░░░░░░1█░1░░░░1░░░*░░░░░1█░░  <- they became:            sz█    pm█    gz█    zq█
002049 ░░2░░░2█░█2░░░█░░░1░░░░░+███0░░░░░░░░2█░1░░░░1░░░*░░░░░1█░░
...
004096 ░░0░░░0░░░0█░█░███1█░░█░+░░░0░░░░██░░0░█1░█░░1░█░*█░░░░1░░░  --  no, I skipped too far, it's no longer convenient
004097 ░░1░░░1░░░1█░█████1█░░█░+███0░░░░██░░1░█1░█░░1░█░*█░░░░1░░░
"""

# THINGS I LEARNED:
# 1. the first conj module (index 2) counts the log-1 of the button presses, up to 10 (it never reaches 11)
# 2. after 2047 presses, that conj is at 10, and every single thing is lit(high) except:  sz, pm, gz, zq

