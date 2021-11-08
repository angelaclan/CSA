class Graph(object):
    def __init__(self, f):
        j = 0
        k = 0
        self.entry = None

        for bb in f.blocks:
            bb.name = "bb" + str(k)
            if k == 0:
                self.entry = bb
            for i in bb.instructions:
                if str(i.type) != "void":
                    i.name="val" + str(j)
                    j = j + 1
            k = k + 1

        j = 0
        for arg in f.arguments:
            arg.name ="arg" + str(j)
            j = j + 1

        self.bbs = {}
        self.succ = {}

        for bb in f.blocks:
            self.bbs[bb.name] = bb
            self.succ[bb.name] = set()
            for instr in bb.instructions:
                if instr.opcode == "br":
                    for op in instr.operands:
                        if str(op.type) == "label":
                            self.succ[bb.name].add(op.name)
                            
