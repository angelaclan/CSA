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

f = target_module.get_function("func")
cfg = binding.get_function_cfg(f)
graph = Graph(f)
file = open("cfg.dot", "w")
file.write(cfg)
file.close()

for bb in graph.bbs:
    print("Basic block:", bb)
    for i in graph.bbs[bb].instructions:
        print("  Instruction: ", i)
        print("    Cible: ", i.name)
        print("    Opcode: ", i.opcode)
        for o in i.operands:
            if o.name is "":
                #type + valeur immediate
                print("      Operand[valeur]: ", o)
            else:
                #variable
                print("      Operand[variable]: ", o.name)
    print("")

