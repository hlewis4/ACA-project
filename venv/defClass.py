class instructionClass:
    def __init__(self, name, dest, s1, s2):
        self.name=name
        self.dest=dest
        self.s1=s1
        self.s2=s2
        self.IF = 0
        self.ID = 0
        self.EXE = 0
        self.MEM = 0
        self.WB = 0
        self.IU = 0
        self.IF_complete = False
        self.ID_complete = False
        self.ID_busy = False
        self.EXE_complete = False
        self.WB_complete = False
        self.IU_complete = False
        self.MEM_complete =False
        self.ADD_complete =False
        self.MUl_complete=False
        self.DIV_complete=False
        self.RAW = "N"
        self.WAW = "N"
        self.STRUCT = "N"
        self.word_address = 0
        self.dest_data = 0
        self.ICACHE_complete = False
        self.raw_instructions = ""
        