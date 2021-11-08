#!/usr/bin/env python3.7
import sys
sys.path.append("../llvmlite/lib/python3.7/site-packages")
from ctypes import CFUNCTYPE, c_double, c_int, c_char_p, POINTER, c_char, cast
from llvmlite import ir, binding
from cfg_helper import Graph

binding.initialize()
binding.initialize_native_target()
binding.initialize_native_asmprinter()  # yes, even this one


f = open(sys.argv[1], "rb")
b = f.read()
target = binding.Target.from_default_triple()
target_machine = target.create_target_machine()

    
target_module  = binding.parse_bitcode(b)
engine = binding.create_mcjit_compiler(target_module, target_machine)

addr = engine.get_function_address("func")

engine.finalize_object()
engine.run_static_constructors()

print("func addr: ", hex(addr))
print(dir(engine))
sys.exit(0)


f = target_module.get_function("func")
cfg = binding.get_function_cfg(f)
graph = Graph(f)
file = open("cfg.dot", "w")
file.write(cfg)
file.close()

state = {}
worklist = [graph.entry]

def bottom_state():
    s = set()
    for bb in graph.bbs:
        s.add(bb)
    return s
    
def entry_state():
    return set()

def update(s, bb):
    r = s.copy()
    r.add(bb.name)
    return r

def join(s1, s2):
    return s1.intersection(s2)
    

def process_bb(bb):
    s = state[bb.name]
    successors = set()
    s = update(s, bb)
    for successor in graph.succ[bb.name]:
        if state[successor] != s:
            state[successor] = join(state[successor], s)
            worklist.append(graph.bbs[successor])

def run():
    for k in graph.bbs:
        state[k] = bottom_state()

    state[graph.entry.name] = entry_state()
                    
    while worklist != []:
        bb = worklist.pop()
        successors = process_bb(bb)

    for s in state:
        print(s, "dominates: ", state[s])

run()
