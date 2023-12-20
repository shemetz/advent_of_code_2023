import math
from collections import deque
from dataclasses import dataclass
from types import SimpleNamespace
from typing import Dict, Tuple, Optional, List

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


class GlobalContext:
    press_count: int
    big_four_conj_activation_times: List[int]

    def __init__(self):
        self.press_count = 0
        self.big_four_conj_activation_times = []


global_context = GlobalContext()


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

    def on_full_conjunction(self):
        if len(self.inputs_memory) > 4:
            print(f"conj activated!  {self.name}, at press {global_context.press_count}")
            global_context.big_four_conj_activation_times.append(global_context.press_count)

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


def reset_all():
    global_context.press_count = 0
    global_context.big_four_conj_activation_times = []
    for module in modules.values():
        module.reset()


def press():
    low_pulse_count = 0
    high_pulse_count = 0
    # 1. press button, sending low pulse to broadcast
    pulses: deque[Tuple[ModuleName, ModuleName, PulseLevel]] = deque()
    pulses.append(("PRESS", ModuleType.BROADCASTER, LOW_PULSE))
    global_context.press_count += 1
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
                    module.on_full_conjunction()
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
    print(f"{global_context.press_count:06}", "".join([module.to_char() for module in modules.values()]))


reset_all()
for idx in range(0, 4):
    print("|||||| " + idx * " " + "".join(
        m.name[:3].ljust(4, " ") if i2 % 4 == idx else "" for i2, m in enumerate(modules.values())))

for bp in range(0, 8):
    visualize()
    press()
for bp in range(8, 2046):
    if math.log2(bp).is_integer():
        visualize()
        print("...")
    press()
visualize()
press()
visualize()
# print("non-high flip flops:", end="    ")
# for m in modules.values():
#     if m.state == LOW_PULSE:
#         print(f"{m.name}{m.to_char()}", end="    ")
# print()
press()
visualize()
# print(f" they became:           {'    '.join(xx + modules[xx].to_char() for xx in ['sz', 'pm', 'gz', 'zq'])}")
press()
visualize()

"""
|||||| dt  jk  kj  rt  qq  bb  bro kh  gs  bh  qh  gb  nk  mb  zq  
||||||  fm  vx  pm  sx  sk  jm  hp  gf  pd  fl  lb  xm  rx  xh  lj  
||||||   hd  kc  tb  qn  pv  sl  zb  pb  tx  gz  zm  mv  zc  cd  lg  
||||||    tl  sz  fc  vj  df  vz  xv  gr  db  xp  lq  js  mp  hz  
000000 ░░0░░░0░░░0░░░░░░░0░░░░░+░░░0░░░░░░░░0░░0░░░░0░░░*░░░░░0░░░
000001 ░░1░░░1░░░1░░░█░░░1░░░░░+███0░░░░░░░░1░░1░░░░1░░░*░░░░░1░░░  <- 1 = qn, hp, zb, xv
000002 █░1░░░1░░░0░░░░░░█1░░░░░+░░░0░░░█░░░░0░░1░░░░1░░░*█░░░░1░░░  <- 2 = dt, sk, gs, zc
000003 █░2░░░2░░░1░░░█░░█1░░░░░+███0░░░█░░░░1░░1░░░░1░░░*█░░░░1░░░
000004 ░█1░░░0░░░0░░█░░░░1░░░░░+░░░0░░░░██░░0░░1░░░░1░░░*░░░░░1░░░  <- 4 = fm, sx, pd, tx
000005 ░█2░░░1░░░1░░██░░░1░░░░░+███0░░░░██░░1░░1░░░░1░░░*░░░░░1░░░
000006 ██2░░░1░░░0░░█░░░█1░░░░░+░░░0░░░███░░0░░1░░░░1░░░*█░░░░1░░░
000007 ██3░░░2░░░1░░██░░█1░░░░░+███0░░░███░░1░░1░░░░1░░░*█░░░░1░░░
000008 ░░1░░░1░░░0░░░░█░░1█░░░░+░░░0░░░░░░░░0░░1░░█░1░░░*░█░░░1░░░  <- 8 = vj, df, lq, mp
...
000016 ░░0░░░1░░░1░░░░░░░1░█░░░+░░░0░░░░░░░░1░░1░░░█1░█░*░░░░░1░█░  <- 16 = bb, gb, js, lf
...
000032 ░░1░░░0░░░0█░░░░█░1░░░░░+░░░0░░░░░░░░1░░1█░░░1█░░*░░░░░1░░░  <- 32 = fc, sk, lb, mv
...
000064 ░░1░░░1░░░1░█░░░░░1░░█░░+░░░0░░█░░░░░0░░1░█░░1░░░*░░░░░1░░░  <- etc
...
000128 ░░1░░░0░░░1░░░░░░░1░░░░░+░░░0░█░░░░█░1░█1░░░░1░░░*░░█░░1░░░
...
000256 ░░1░░░1░█░1░░░░░░░1░░░█░+░░░0░░░░░░░░0░░1░░░░1░░░*░░░█░1░░█
...
000512 ░░1█░░1░░░1░░░░░░░1░░░░█+░░░0░░░░░░░░1░░1░░░░1░░█*░░░░█1░░░
...
001024 ░░1░██1░░░1░░░░░░░1░░░░░+░░░0█░░░░░░█1░░1░░░░1░░░*░░░░░1░░░
...
002046 ██9███7░█░6███░███1█████+░░░0████████5░█1████1███*█████1░██
002047 ██a███8░█░7███████1█████+███0████████6░█1████1███*█████1░██  <- non-high flip flops:    sz░    pm░    gz░    zq░    
002048 ░░1░░░1█░█1░░░░░░░1░░░░░+░░░0░░░░░░░░1█░1░░░░1░░░*░░░░░1█░░  <- they became:            sz█    pm█    gz█    zq█
002049 ░░2░░░2█░█2░░░█░░░1░░░░░+███0░░░░░░░░2█░1░░░░1░░░*░░░░░1█░░
...
004096 ░░0░░░0░░░0█░█░███1█░░█░+░░░0░░░░██░░0░█1░█░░1░█░*█░░░░1░░░  --  no, I skipped too far, it's no longer convenient
004097 ░░1░░░1░░░1█░█████1█░░█░+███0░░░░██░░1░█1░█░░1░█░*█░░░░1░░░

||||||                                                  rx        
||||||                                                  !        
||||||                             kh-------------------^
||||||                             !
||||||                   +---------^-----------+----+---------+    
||||||                   pv                    qh   xm        hz   
||||||                   !                     !    !         ! 
||||||           +-------^                     |    |         |
||||||          [tb]                           |    |         |
||||||                                         |    |         |
||||||                                      +--^    |         |   
||||||                                     [fl]     |         |
||||||                                              |         |
||||||       +--------------------------------------^         |
||||||      [kc]                                              |
||||||                                                        |
||||||   +----------------------------------------------------^
||||||  [hd]
"""

"""
 THINGS I LEARNED:
  1. the first conj module (index 2) counts the log-1 of the button presses, up to 10 (it never reaches 11)
  2. after 2047 presses, that conj is at 10, and every single thing is lit(high) except:  sz, pm, gz, zq
 99. to get rx a low pulse, we need kh to send a low pulse
 98. to activate &kh, we need to get all of the following to send high pulse:  &pv, &qh, &xm, &hz
 97. each of those is a simple inverted, the output of another conj
 96. &pv is inverted &tb;    &qh is inverted &fl;    &xm is inverted &kc;    &hz is inverted &hd
 95. so we need to get &tb, &fl, &kc, &hd to send low pulse
 94. which means we need every single one of their inputs to be high
 - for tb we need all of the following: ['pm', 'qn', 'jm', 'gf', 'db', 'gb', 'xh', 'cd']
 - for fl we need all of the following: ['bb', 'vz', 'xv', 'bh', 'gz', 'lb', 'mb']
 - for kc we need all of the following: ['vx', 'sz', 'rt', 'zb', 'gs', 'lq', 'nk', 'lj', 'lg']
 - for hd we need all of the following: ['dt', 'fm', 'tl', 'jk', 'kj', 'hp', 'pb', 'gr', 'mv', 'mp', 'zq']
 93. I'm PRETTY SURE that it's every single flip flop
 92. these are also all conjunctors, none remain, nice!
  3. after 2047 presses, every single flip flop is indeed activated, except:  sz, pm, gz, zq
  4. those are each one of the flip flops needed for the big four (tb, fl, kc, hd)
  5. on step 2048, these four flip flops are activated but all other flip flops are deactivated
  6. okay... but that causes changes later, making some of those big four conjs active earlier, which messes stuff up.
 - tb sends pulses to these:  sx, qn, vj, qq, sk, (pv)
 - fl sends pulses to these:  xv, tx, sl, df, (qh), zc, zm
 - kc sends pulses to these:  zb, xp, pd, fc, (xm)
 - hd sends pulses to these:  hp, js, (hz)
 ... I don't know how that helps me
  7. I want to try simplifying some subsets of modules, to see if I can get a better understanding of what's going on
  8. starting from the bottom up this time, showing one click at a time
  9. broadcaster activates:  qn, hp, zb, xv, which all get flipped up
 10. second button press causes all of them to flip down, which triggers a flip-up of new ones:
 11. -qn leads to +sk, (+tb)
 12. -hp leads to +dt, (+hd)
 13. actually let's focus on qn's "chain".
 one button click activates qn, and two clicks activate sk, and four clicks activate sx.
 so:  1 = qn,  2 = sk,  4 = sx, 8 = vj, 16 = gb
 gb leads to qq and another +tb
 so put another way:
 qn = 1 and +tb
 sk = 2
 sx = 4
 vj = 8
 gb = 16 and +tb
 qq = 32
 jm = 64 and +tb
 db = 128 and +tb
 xh = 256 and +tb
 cd = 512 and +tb 
 gf = 1024 and +tb
 pm = 2048 and +tb and that's it
 
 14. so for tb to be activated we need to count exactly to 2048, and then press the button again (which flips all of
 these flip flops off, which makes all of them transmit a high pulse to tb at once)
 15. once tb activates, what happens?
 &tb -> sx, qn, vj, qq, sk, pv
 16. it reactivates the following...
 sx (4), qn (1), vj (8), qq (32), sk (2), and pv which is the target conj for later
 17. in other words, after this counter reaches 2048, the next click resets it to... 1 + 2 + 4 + 8 + 32 = 47
 18. and based on the things missing a +tb, we should expect another activation of tb at...
 4096 - 32 - 8 - 4 - 2 = 4096 - 46 = 4050
 19. wait... 46 and 47..?  hmmmm
 
 (enabling logs when the conjs activate)
"""

print("...")
for bp in range(2050, 4049):
    press()
visualize()
press()
visualize()
press()
for bp in range(4051, 4097):
    press()

"""
yup!  oh wow it's simpler than I thought, I can just directly get those activation times...
okay, I have a plan forming now...
"""

print("...resetting everything...")
reset_all()
for bp in range(0, 4096):
    press()
multi_sum = 1
for bp in global_context.big_four_conj_activation_times:
    multi_sum *= bp
print(multi_sum)  # 244178746156661

# omg it was that easy
