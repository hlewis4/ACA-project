from defClass import instructionClass as instClass
import copy

with open(r"C:\Users\hashi\Desktop\ACA\ACA project\reg.txt") as reg:
    reg_lines = reg.read().splitlines()
print("reg_lines",reg_lines)

with open(r"C:\Users\hashi\Desktop\ACA\ACA project\data.txt") as data_v:
    data_lines = data_v.read().splitlines()
print("data lines", data_lines)

with open(r"C:\Users\hashi\Desktop\ACA\ACA project\inst.txt") as f:
    lines = f.read().splitlines()

print("Instructions")
print(lines)

for i in range(len(lines)):
    lines[i] = lines[i].lstrip()
    print(lines[i])


inst = []
for x in range(len(lines)):
    inst.append(lines[x].split(' '))

for i in range(len(inst)):
    inst[i] = [item.replace(",", "") for item in inst[i]]


for i in range(len(inst)):
    inst[i] = [item.replace(":", "") for item in inst[i]]
print("inst  ",inst)

for i in range(len(inst)):
    while '' in inst[i]:
        inst[i].remove('')
print("inst", inst)

#UNROLLING INFO
elements = []
elements = ["BNE","BEQ","J"]
unrolling_info = []
for elem in elements:
    for items in inst:
        if items[0] == elem:
            unrolling_info.append(items[0])
            unrolling_info.append(items[1])
            unrolling_info.append(items[2])
            unrolling_info.append(items[3])
print("res", unrolling_info)


for i in range(len(inst)):
    if inst[i][0] == unrolling_info[3]:
        unrolling_info.append(int(i))
        inst[i].remove(unrolling_info[3])

print("res", unrolling_info)

#integer values of register data in list
register_data = []
for item in reg_lines:
    register_data.append(int(item,2))
print("register data",register_data)

#integer values for data.txt
data_values = []
for item in data_lines:
    data_values.append(int(item,2))
print("data values",data_values)

#INSTRUCTIONS
instruction = []
for i in range(len(inst)):  # create a list with nested lists
    instruction.append([])
    for j in range(len(inst[i])):
            if j == 2 and len(inst[i][j]) >= 5:
                v = inst[i][j].split("(")[0]
                w = inst[i][j].split("(")[1]
                w = w.replace(")","")
                print("w ", w)
                instruction[i].append(v)
                instruction[i].append(w)
            else:
                instruction[i].append(inst[i][j])

print("instructions:")
print(instruction)

# assign to objects
instruction_ob = []
dest = 0
s1 = 0
s2 = 0

# length = len(instruction)

for i in instruction:
    length = len(i)
    if length == 4:
        dest = i[1]
        if len(i[2]) == 1:
            s1 = int(i[2])
        else:
            s1 = i[2]
        if len(i[3]) == 1:
            s2 = int(i[3])
        else:
            s2 = i[3]

    elif length == 1:
        dest = 0
        s1 = 0
        s2 = 0

    instruction_ob.append(instClass(i[0], dest, s1, s2))
inc = 0
for u in instruction_ob:
    u.word_address = inc
    inc+=1
for i in instruction_ob:
    print(i.name,i.dest,i.s1,i.s2)
#INSTRUCTION OBJECTS COPY
instruction_ob_copy = []
instruction_ob_copy = copy.deepcopy(instruction_ob)



#READ CONFIG FILE
with open(r"C:\Users\hashi\Desktop\ACA\ACA project\config.txt") as f:
    config = f.read().splitlines()
print("Config file")
print(config)

cycles = []
for x in range(len(config)):
    cycles.append(config[x].split(' '))

for i in range(len(cycles)):
    cycles[i] = [item.replace(",", "") for item in cycles[i]]
print(cycles)

fp_add = 0
fp_mul = 0
fp_divide = 0
add_pipeline = False
mul_pipeline = False
div_pipeline = False
mem = 0
icache = 0
dcache = 0

for i in cycles:
    if "adder:" in i:
        fp_add = int(i[2])
        if "yes" in i:
            add_pipeline = True
        else:
            add_pipeline = False

    if "Multiplier:" in i:
        fp_mul = int(i[2])
        if "yes" in i:
            mul_pipeline = True
        else:
            mul_pipeline = False

    if "divider:" in i:
        fp_divide = int(i[2])
        if "yes" in i:
            div_pipeline = True
        else:
            div_pipeline = False

    if "memory:" in i:
        mem = int(i[2])
    if "I-Cache:" in i:
        icache = int(i[1])
    if "D-Cache:" in i:
        dcache = int(i[1])
# PIPELINE LOGIC STARTS

#operands = [IF, ID , IU, MEM , ADD, MUL, DIV, WB]
operands = [False, False, False, False, False, False, False, False]
exe_in_ld = 10000
exe_in_add = 1000
exe_in_mul = 1000
exe_in_div = 10000
count = 1
flag_if = 0
flag_ld = 0
flag_id = 0
flag_iu = 0
flag_add = 0
flag_mul = 0
flag_div = 0
ld_pass = [0] * len(instruction_ob)
add_pass = [fp_add] * len(instruction_ob)
mul_pass = [fp_mul] * len(instruction_ob)
div_pass = [fp_divide] * len(instruction_ob)


registers = [0] * 32
fp_registers = [0] * 32


def hazard(instruction_ob):
    x = 0
    y = 0
    z = 0
    if instruction_ob.name in ["L.D","LW","S.D","SW"]:
        x = int(instruction_ob.dest[1:])
        z = int(instruction_ob.s2[1:])

        if instruction_ob.dest[0] == "F" and instruction_ob.s2[0] == "R":
            if fp_registers[x] == 0:
                if registers[z] == 0:
                    return 0
                else:
                    return 1
            else:
                return 1
        if instruction_ob.dest[0] == "F" and instruction_ob.s2[0] == "F":
            if fp_registers[x] == 0:
                if fp_registers[z] == 0:
                    return 0
                else:
                    return 1
            else:
                return 1

        if instruction_ob.dest[0] == "R" and instruction_ob.s2[0] == "R":
            if registers[x] == 0:
                if registers[z] == 0:
                    return 0
                else:
                    return 1
            else:
                return 1

        if instruction_ob.dest[0] == "R" and instruction_ob.s2[0] == "R":
            if registers[x] == 0:
                if fp_registers[z] == 0:
                    return 0
                else:
                    return 1
            else:
                return 1

    if instruction_ob.name in ["DADDI", "BE", "BNE","DSUBI", "ANDI","ORI"]:
        x = int(instruction_ob.dest[1:])
        y = int(instruction_ob.s1[1:])

        if instruction_ob.dest[0] == "F":
            if fp_registers[x] == 0:
                if fp_registers[y] == 0:
                    return 0
                else:
                    return 1
            else:
                return 1

        if instruction_ob.dest[0] == "R":
            if registers[x] == 0:
                if registers[y] == 0:
                    return 0
                else:
                    return 1
            else:
                return 1

    if instruction_ob.name in ["ADD.D", "SUB.D", "MUL.D", "DIV.D", "DSUB","DADD","AND","OR"]:
        x = int(instruction_ob.dest[1:])
        y = int(instruction_ob.s1[1:])
        z = int(instruction_ob.s2[1:])
        if instruction_ob.dest[0] == "F":
            if fp_registers[x] == 0:
                if fp_registers[y] == 0:
                    if fp_registers[z] == 0:
                        return 0
                    else:
                        return 1
                else:
                    return 1
            else:
                return 1

        if instruction_ob.dest[0] == "R":
            if registers[x] == 0:
                if registers[y] == 0:
                    if registers[z] == 0:
                        return 0
                    else:
                        return 1
                else:
                    return 1
            else:
                return 1

    if instruction_ob.name == "HLT":
        return 0


def make_busy(instruction_ob):
    x = 0
    y = 0
    z = 0
    if instruction_ob.name in ["L.D","S.D","LW","SW"]:
        x = int(instruction_ob.dest[1:])
        z = int(instruction_ob.s2[1:])
        if instruction_ob.dest[0] == "F":
            fp_registers[x] = 1
        if instruction_ob.dest[0] == "R":
            registers[x] = 1
        if instruction_ob.s2[0] == "F":
            fp_registers[z] = 1
        if instruction_ob.s2[0] == "R":
            registers[z] = 1

    if instruction_ob.name in ["DADDI", "BE", "BNE","DSUBI","ANDI","ORI"]:
        x = int(instruction_ob.dest[1:])
        y = int(instruction_ob.s1[1:])
        if instruction_ob.dest[0] == "F":
            fp_registers[x] = 1
        if instruction_ob.dest[0] == "R":
            registers[x] = 1
        if instruction_ob.s1[0] == "F":
            fp_registers[y] = 1
        if instruction_ob.s1[0] == "R":
            registers[y] = 1

    if instruction_ob.name in ["ADD.D", "MUL.D", "SUB.D", "DIV.D", "DSUB","DADD","AND","OR"]:
        x = int(instruction_ob.dest[1:])
        y = int(instruction_ob.s1[1:])
        z = int(instruction_ob.s2[1:])
        if instruction_ob.dest[0] == "F":
            fp_registers[x] = 1
        if instruction_ob.dest[0] == "R":
            registers[x] = 1
        if instruction_ob.s1[0] == "F":
            fp_registers[y] = 1
        if instruction_ob.s1[0] == "R":
            registers[y] = 1
        if instruction_ob.s2[0] == "F":
            fp_registers[z] = 1
        if instruction_ob.s2[0] == "R":
            registers[z] = 1


def make_free(instruction_ob):
    x = 0
    y = 0
    z = 0
    if instruction_ob.name in ["L.D","S.D","LW","SW"]:
        x = int(instruction_ob.dest[1:])
        z = int(instruction_ob.s2[1:])
        if instruction_ob.dest[0] == "F":
            fp_registers[x] = 0
        if instruction_ob.dest[0] == "R":
            registers[x] = 0
        if instruction_ob.s2[0] == "F":
            fp_registers[z] = 0
        if instruction_ob.s2[0] == "R":
            registers[z] = 0

    if instruction_ob.name in ["DADDI", "BE", "BNE","DSUBI","ANDI","ORI"]:
        x = int(instruction_ob.dest[1:])
        y = int(instruction_ob.s1[1:])
        if instruction_ob.dest[0] == "F":
            fp_registers[x] = 0
        if instruction_ob.dest[0] == "R":
            registers[x] = 0
        if instruction_ob.s1[0] == "F":
            fp_registers[y] = 0
        if instruction_ob.s1[0] == "R":
            registers[y] = 0

    if instruction_ob.name in ["ADD.D", "MUL.D", "SUB.D", "DIV.D", "DSUB","DADD","AND","OR"]:
        x = int(instruction_ob.dest[1:])
        y = int(instruction_ob.s1[1:])
        z = int(instruction_ob.s2[1:])
        if instruction_ob.dest[0] == "F":
            fp_registers[x] = 0
        if instruction_ob.dest[0] == "R":
            registers[x] = 0
        if instruction_ob.s1[0] == "F":
            fp_registers[y] = 0
        if instruction_ob.s1[0] == "R":
            registers[y] = 0
        if instruction_ob.s2[0] == "F":
            fp_registers[z] = 0
        if instruction_ob.s2[0] == "R":
            registers[z] = 0

def calculate_destination(instruction_ob):
    if instruction_ob.name == "DADDI":
        x = int(instruction_ob.dest[1:])
        y = int(instruction_ob.s1[1:])
        register_data[x] = register_data[y] + int(instruction_ob.s2)
        instruction_ob.dest_data = register_data[x]
        print("register data y and s2", register_data[y], int(instruction_ob.s2))
        print("DADDI ",instruction_ob.dest_data)

    if instruction_ob.name == "DSUBI":
        x = int(instruction_ob.dest[1:])
        y = int(instruction_ob.s1[1:])
        register_data[x] = register_data[y] - int(instruction_ob.s2)
        instruction_ob.dest_data = register_data[x]

    if instruction_ob.name == "DSUB":
        x = int(instruction_ob.dest[1:])
        y = int(instruction_ob.s1[1:])
        z = int(instruction_ob.s2[1:])
        register_data[x] = register_data[y] - register_data[z]
        instruction_ob.dest_data = register_data[x]

    if instruction_ob.name == "DADD":
        x = int(instruction_ob.dest[1:])
        y = int(instruction_ob.s1[1:])
        z = int(instruction_ob.s2[1:])
        register_data[x] = register_data[y] + register_data[z]
        instruction_ob.dest_data = register_data[x]


#I-CACHE
block_address = 0
i_hit = 0
d_hit = 0
i_miss = 0
d_miss = 0
i_access_number = 0
d_access_number = 0
if_pass = [0] * len(instruction_ob)
if_cycles = 1000
d_block_0 = {d_value_0: [] for d_value_0 in range(2)}
lru_0 = 0
lru_1 = 0
d_block_1 = {d_value_1: [] for d_value_1 in range(2)}

print("register data",register_data)

def data_cache(instruction_ob):
    set_address = 0
    v = 0
    next =0
    block_start_number = 0
    global d_hit
    global d_access_number
    global d_miss
    global lru_0, lru_1


    if instruction_ob.name in ["LW","SW"]:
        z = int(instruction_ob.s2[1:])
        instruction_ob.dest_data = int(instruction_ob.s1) + register_data[z]
        set_address = int(instruction_ob.dest_data/16) % 2
        if set_address == 0:
            for ff in len(d_block_0):
                if instruction_ob.dest_data in d_block_0[ff]:
                    next = 1
                    v = ff
                    d_hit += 1
                    d_access_number +=1
                    lru_0 = int(not(v))
            if next == 1:
                return dcache
            if next == 0:
                d_miss += 1
                d_access_number += 1
                block_start_number = int(instruction_ob.dest_data/16) * 16
                d_block_0.update({lru_0: []})
                d_block_0[lru_0].append(block_start_number)
                d_block_0[lru_0].append(block_start_number+4)
                d_block_0[lru_0].append(block_start_number+8)
                d_block_0[lru_0].append(block_start_number+12)
                lru_0 = int(not(lru_0))
                return 2 * (mem + dcache)

        if set_address == 1:
            for ff in len(d_block_1):
                if instruction_ob.dest_data in d_block_1[ff]:
                    next = 1
                    v = ff
                    d_hit += 1
                    d_access_number +=1
                    lru_1 = int(not(v))
            if next == 1:
                return dcache
            if next == 0:
                d_miss +=1
                d_access_number +=1
                block_start_number = int(instruction_ob.dest_data/16) * 16
                d_block_1.update({lru_1: []})
                d_block_1[lru_1].append(block_start_number)
                d_block_1[lru_1].append(block_start_number+4)
                d_block_1[lru_1].append(block_start_number+8)
                d_block_1[lru_1].append(block_start_number+12)
                lru_1 = int(not(lru_1))
                return 2*(mem+dcache)
    if instruction_ob.name in ["L.D","S.D"]:
        double_list = []
        cycles_for_execution = 0
        z = int(instruction_ob.s2[1:])
        instruction_ob.dest_data = int(instruction_ob.s1) + register_data[z]
        double_list.append(instruction_ob.dest_data)
        double_list.append(instruction_ob.dest_data+4)
        print("double list",double_list)
        for item in double_list:
            set_address = 0
            v = 0
            next = 0
            set_address = int(item/ 16) % 2
            if set_address == 0:
                for ff in range(len(d_block_0)):
                    if item in d_block_0[ff]:
                        next = 1
                        v = ff
                        d_hit += 1
                        d_access_number += 1
                        lru_0 = int(not(v))
                if next == 1:
                    cycles_for_execution = cycles_for_execution + dcache
                if next == 0:
                    d_miss += 1
                    d_access_number += 1
                    block_start_number = int(item/ 16) * 16
                    d_block_0.update({lru_0: []})
                    d_block_0[lru_0].append(block_start_number)
                    d_block_0[lru_0].append(block_start_number + 4)
                    d_block_0[lru_0].append(block_start_number + 8)
                    d_block_0[lru_0].append(block_start_number + 12)
                    lru_0 = int(not(lru_0))
                    cycles_for_execution = cycles_for_execution + (2 * (mem + dcache))

            if set_address == 1:
                for gg in range(len(d_block_1)):
                    if item in d_block_1[gg]:
                        next = 1
                        v = gg
                        d_hit += 1
                        d_access_number += 1
                        lru_1 = int(not(v))
                if next == 1:
                    cycles_for_execution = cycles_for_execution + dcache
                if next == 0:
                    d_miss += 1
                    d_access_number += 1
                    block_start_number = int(item / 16) * 16
                    d_block_1.update({lru_1: []})
                    d_block_1[lru_1].append(block_start_number)
                    d_block_1[lru_1].append(block_start_number + 4)
                    d_block_1[lru_1].append(block_start_number + 8)
                    d_block_1[lru_1].append(block_start_number + 12)
                    lru_1 = int(not(lru_1))
                    cycles_for_execution = cycles_for_execution + (2 * (mem + dcache))

        return cycles_for_execution


block = {value: [] for value in range(4)}


for e in range(len(instruction_ob)):
    if instruction_ob[e].name == unrolling_info[0]:
        value_1 = int(instruction_ob[e].dest[1:])
        value_2 = int(instruction_ob[e].s1[1:])
        compare_value1 = int(reg_lines[value_1],2)
        compare_value2 = int(reg_lines[value_2],2)

print("v1 ",compare_value1)
print("v2 ",compare_value2)

cycles_for_dcache = 0
for i in range(1000):
    for j in range(len(instruction_ob)):

        # IF stage
        if (j == 0 and (operands[0] is False) and (instruction_ob[j].IF_complete is False)) or (j == 0 and (operands[0] is True) and if_pass[j] == 1):

            #icache
            block_address = int((instruction_ob[j].word_address/4) % 4)
            if (instruction_ob[j].word_address in block[block_address] and if_pass[j] == 0):
                    i_hit += 1
                    i_access_number += 1
                    flag_if = 1
                    instruction_ob[j].IF = count
                    operands[0] = True
                    instruction_ob[j].IF_complete = True
                    instruction_ob[j].IF = count

            else:
                if if_pass[j] == 0:
                    i_miss +=1
                    i_access_number +=1
                    block.update({block_address: []})
                    t_list = []
                    t_list.clear()
                    for kk in range(j, j + 4):
                        if kk < len(instruction_ob):
                           t_list.append(instruction_ob[kk].word_address)
                    block.update({block_address: t_list})
                if if_cycles > 2*(mem + icache):
                    if_cycles = 2 * (mem + icache)
                if if_cycles > 1:
                    instruction_ob[j].IF = count
                    operands[0] = True
                    if_pass[j] = 1

                if if_cycles == 1:
                    instruction_ob[j].IF_complete = True
                    instruction_ob[j].IF = count
                    if_pass[j] = 0
                    flag = 1
                    if_cycles = 1000
            continue
        else:
            if (instruction_ob[j].IF_complete is False and (operands[0] is False)) or((instruction_ob[j].IF_complete is False) and (operands[0] is True) and if_pass[j] ==1 ):
                if instruction_ob[j - 1].ID > 0:
                    #icache
                    block_address = int((instruction_ob[j].word_address / 4) % 4)
                    if (instruction_ob[j].word_address in block[block_address] and if_pass[j] == 0):
                        i_hit += 1
                        i_access_number += 1
                        flag_if = 1
                        operands[0] = True
                        instruction_ob[j].IF_complete = True
                        instruction_ob[j].IF = count
                    else:
                        if if_pass[j] == 0:
                            i_miss += 1
                            i_access_number += 1
                            block.update({block_address: []})
                            t_list = []
                            t_list.clear()
                            for kk in range(j, j + 4):
                                if kk < len(instruction_ob):
                                    t_list.append(instruction_ob[kk].word_address)
                            block.update({block_address: t_list})
                        if if_cycles > 2 * (mem + icache):
                            if_cycles = 2 * (mem + icache)
                        if if_cycles > 1:
                            instruction_ob[j].IF = count
                            operands[0] = True
                            if_pass[j] = 1

                        if if_cycles == 1:
                            instruction_ob[j].IF_complete = True
                            instruction_ob[j].IF = count
                            if_pass[j] = 0
                            flag = 1
                            if_cycles = 1000

                    continue

        # ID stage
        if instruction_ob[j].ID_complete == False and instruction_ob[j].IF > 0:
            x = hazard(instruction_ob[j])
            if x == 0:
                if instruction_ob[j].IF > 0 and (operands[1] is False) and (instruction_ob[j].ID_complete is False):
                    operands[1] = True
                    flag_id = 1
                    instruction_ob[j].ID = count
                    instruction_ob[j].ID_complete = True
                    make_busy(instruction_ob[j])
                    flag = 1
                    operands[0] = False
                    if instruction_ob[j].name == "HLT" and instruction_ob[j - 1].name == "HLT":
                        instruction_ob[j].ID = 0
                    if instruction_ob[j].name == "BNE":
                        print(compare_value1, compare_value2)
                        if compare_value1 != compare_value2:
                            dd = unrolling_info[4]
                            num = 0
                            instruction_ob = instruction_ob[:-1]
                            add_pass = add_pass[:-1]
                            ld_pass = ld_pass[:-1]
                            mul_pass = mul_pass[:-1]
                            div_pass = div_pass[:-1]
                            if_pass = if_pass[:-1]

                            for dd in instruction_ob_copy:
                                instruction_ob.append(dd)
                                num += 1
                            for ww in range(num):
                                add_pass.append(fp_add)
                                mul_pass.append(fp_mul)
                                div_pass.append(fp_divide)
                                ld_pass.append(0)
                                if_pass.append(0)
                                make_free(instruction_ob[j])
                    continue
            if x == 1:
                operands[0] = True
                instruction_ob[j].ID = count
                if instruction_ob[j].dest != 0:
                    for k in range(j):
                        if not instruction_ob[j].name in ["L.D","LW","S.D","SW","J"]:
                            g1 = int(instruction_ob[j].s1[1:])
                            o1 = instruction_ob[j].s1[0]
                            if o1 == "R":
                                if registers[g1] == 1 and instruction_ob[k].dest == instruction_ob[j].s1:
                                    instruction_ob[j].RAW = "Y"
                            if o1 == "F":
                                if fp_registers[g1] == 1 and instruction_ob[k].dest == instruction_ob[j].s1:
                                    instruction_ob[j].RAW = "Y"
                        if not instruction_ob[j].name in ["DADDI", "BE", "BNE", "HLT","DSUBI","ANDI","OR","J"]:
                            g2 = int(instruction_ob[j].s2[1:])
                            o2 = instruction_ob[j].s2[0]
                            if o2 == "R":
                                if registers[g2] == 1 and instruction_ob[k].dest == instruction_ob[j].s2:
                                    instruction_ob[j].RAW = "Y"
                            if o2 == "F":
                                if fp_registers[g2] == 1 and instruction_ob[k].dest == instruction_ob[j].s2:
                                    instruction_ob[j].RAW = "Y"


                    if not instruction_ob[k].name in ["HLT","BNE","BE","J"]:
                        for k in range(j):
                            g3 = int(instruction_ob[j].dest[1:])
                            o3 = instruction_ob[j].dest[0]
                            if o3 == "R":
                                if registers[g3] == 1 and instruction_ob[k].dest == instruction_ob[j].dest:
                                    instruction_ob[j].WAW = "Y"
                            if o3 == "F":
                                if fp_registers[g3] == 1 and instruction_ob[k].dest == instruction_ob[j].dest:
                                    instruction_ob[j].WAW = "Y"
                    if instruction_ob[j].name in ["BNE","BE"]:
                        for k in range(j):
                            g3 = int(instruction_ob[j].dest[1:])
                            o3 = instruction_ob[j].dest[0]
                            if o3 == "R":
                                if registers[g3] == 1 and instruction_ob[k].dest == instruction_ob[j].dest:
                                    instruction_ob[j].RAW = "Y"
                            if o3 == "F":
                                if fp_registers[g3] == 1 and instruction_ob[k].dest == instruction_ob[j].dest:
                                    instruction_ob[j].RAW = "Y"

                continue


        # EXE stage
        # IU cycle.
        if instruction_ob[j].name in ["L.D", "DADDI", "DSUB","DADD","DSUBI","S.D","LW","SW"]:
            if instruction_ob[j].ID > 0 and (operands[2] is False) and (instruction_ob[j].IU_complete is False):
                operands[2] = True
                flag_iu = 1
                instruction_ob[j].IU = count
                instruction_ob[j].EXE = count
                instruction_ob[j].IU_complete = True
                calculate_destination(instruction_ob[j])
                if instruction_ob[j].name == "DSUB":
                    compare_value1 = compare_value1 - compare_value2
                    print("compare1 ",compare_value1)
                    print("compare2 ",compare_value2)
                if instruction_ob[j].name == "DSUBI":
                    compare_value1 = compare_value1 - 1
                    print("compare1 ",compare_value1)
                    print("compare2 ",compare_value2)
                continue

        # MEM stage
        if instruction_ob[j].name in ["L.D","LW","S.D","SW"]:
            if (instruction_ob[j].IU > 0 and (operands[3] is False) and (instruction_ob[j].EXE_complete is False)) or (
                    instruction_ob[j].IU > 0 and ld_pass[j] == 1 and (instruction_ob[j].MEM_complete is False)):
                if exe_in_ld > cycles_for_dcache:
                    cycles_for_dcache = data_cache(instruction_ob[j])
                    exe_in_ld = cycles_for_dcache
                if exe_in_ld > 1:
                    operands[3] = True
                    ld_pass[j] = 1
                    continue
                else:
                    flag_ld = 1
                    flag_iu = 1
                    instruction_ob[j].EXE = count
                    instruction_ob[j].EXE_complete = True
                    instruction_ob[j].MEM_complete = True
                    exe_in_ld = 10000
                    ld_pass[j] = 0
                    continue
            else:
                if (instruction_ob[j].MEM_complete is False) and (instruction_ob[j].IU_complete is True) and (
                        operands[3] is True):
                    instruction_ob[j].STRUCT = "Y"
                    operands[2] = True
                    flag_iu = 0
                    instruction_ob[j].IU = count

        if instruction_ob[j].name in ["DSUB", "DADDI","DSUBI","DADD"]:
            if instruction_ob[j].IU > 0 and (operands[3] is False) and (instruction_ob[j].EXE_complete is False):
                operands[3] = True
                instruction_ob[j].EXE = count
                instruction_ob[j].EXE_complete = True
                instruction_ob[j].MEM_complete = True
                flag_ld = 1
                flag_iu = 1
                continue
            else:
                if instruction_ob[j].IU > 0 and (operands[3] is True) and (instruction_ob[j].MEM_complete is False):
                    operands[2] = True
                    flag_iu = 0
                    instruction_ob[j].IU = count
                    continue

        # ADD
        if instruction_ob[j].name in ["ADD.D","SUB.D"]:
            if add_pipeline is False:
                if instruction_ob[j].ID > 0 and (operands[4] is False) and (
                        instruction_ob[j].EXE_complete is False) or (
                        instruction_ob[j].ID > 0 and (add_pass[j] == 1) and (instruction_ob[j].EXE_complete is False)):
                    if exe_in_add > fp_add:
                        exe_in_add = fp_add
                    if exe_in_add > 1:
                        operands[4] = True
                        add_pass[j] = 1
                        continue
                    else:
                        flag_add = 1
                        instruction_ob[j].EXE = count
                        instruction_ob[j].EXE_complete = True
                        exe_in_add = 1000
                        continue
                else:
                    if (instruction_ob[j].EXE_complete is False) and (instruction_ob[j].ID_complete is True) and operands[4] is True:
                        operands[2] = True
                        flag_iu = 0
                        instruction_ob[j].ID = count
                        continue

            if add_pipeline is True:
                if (instruction_ob[j].ID > 0 and (operands[4] is False) and (
                        instruction_ob[j].EXE_complete is False)) or (
                        instruction_ob[j].ID > 0 and (add_pass[j] <= fp_add) and (
                        instruction_ob[j].EXE_complete is False)):
                    if add_pass[j] > 1:
                        operands[4] = True
                        instruction_ob[j].EXE = count
                        add_pass[j] -= 1
                        continue
                    else:
                        instruction_ob[j].EXE_complete = True
                        instruction_ob[j].EXE = count
                        continue

        # MUL
        if instruction_ob[j].name == "MUL.D":
            if mul_pipeline is False:
                if instruction_ob[j].ID > 0 and (operands[5] is False) and (
                        instruction_ob[j].EXE_complete is False) or (
                        instruction_ob[j].ID > 0 and (mul_pass[j] == 1) and (instruction_ob[j].EXE_complete is False)):
                    if exe_in_mul > fp_mul:
                        exe_in_mul = fp_mul
                    if exe_in_mul > 1:
                        operands[5] = True
                        mul_pass[j] = 1
                        continue
                    else:
                        flag_mul = 1
                        instruction_ob[j].EXE = count
                        instruction_ob[j].EXE_complete = True
                        exe_in_mul = 1000
                        continue
                else:
                    if (instruction_ob[j].EXE_complete is False) and (instruction_ob[j].ID_complete is True) and \
                            operands[5] is True:
                        operands[2] = True
                        flag_iu = 0
                        instruction_ob[j].ID = count
                        continue

            if mul_pipeline is True:
                if (instruction_ob[j].ID > 0 and (operands[5] is False) and (
                        instruction_ob[j].EXE_complete is False)) or (
                        instruction_ob[j].ID > 0 and (mul_pass[j] <= fp_mul) and (
                        instruction_ob[j].EXE_complete is False)):
                    if mul_pass[j] > 1:
                        operands[5] = True
                        instruction_ob[j].EXE = count
                        mul_pass[j] -= 1
                        continue
                    else:
                        instruction_ob[j].EXE_complete = True
                        instruction_ob[j].EXE = count
                        continue

        # DIV
        if instruction_ob[j].name == "DIV.D":
            if div_pipeline is False:
                if instruction_ob[j].ID > 0 and (operands[6] is False) and (instruction_ob[j].EXE_complete is False) or \
                        instruction_ob[j].ID > 0 and (div_pass[j] == 1) and (instruction_ob[j].EXE_complete is False):
                    if exe_in_div > fp_divide:
                        exe_in_div = fp_divide
                    if exe_in_div > 1:
                        operands[6] = True
                        div_pass[j] = 1
                        continue
                    else:
                        flag_div = 1
                        instruction_ob[j].EXE = count
                        instruction_ob[j].EXE_complete = True
                        exe_in_div = 1000
                        continue
            if div_pipeline is True:
                if (instruction_ob[j].ID > 0 and (operands[6] is False) and (
                        instruction_ob[j].EXE_complete is False)) or (
                        instruction_ob[j].ID > 0 and (div_pass[j] <= fp_divide) and (
                        instruction_ob[j].EXE_complete is False)):
                    if div_pass[j] > 1:
                        operands[6] = True
                        instruction_ob[j].EXE = count
                        div_pass[j] -= 1
                        continue
                    else:
                        instruction_ob[j].EXE_complete = True
                        instruction_ob[j].EXE = count
                        continue

        # WriteBack
        if (instruction_ob[j].EXE_complete is True) and (operands[7] is False) and (
                instruction_ob[j].WB_complete is False):
            operands[7] = True
            instruction_ob[j].WB = count
            instruction_ob[j].WB_complete = True
            make_free(instruction_ob[j])
            for d in instruction_ob:
                if d.EXE_complete is True and d.WB_complete is False:
                    d.EXE = count
                    instruction_ob[j].STRUCT = "Y"
            continue


    count += 1
    if mul_pipeline is False:
        if exe_in_mul > 0:
            exe_in_mul -= 1
    if add_pipeline is False:
        if exe_in_add > 0:
            exe_in_add -= 1
    if exe_in_ld > 0:
        exe_in_ld -= 1
    if if_cycles > 0:
        if_cycles -= 1
    if flag_if == 1:
        operands[0] = False
        flag_if = 0
    if flag_id == 1:
        operands[1] = False
        flag_id = 0
    operands[2] = False
    if flag_ld == 1:
        operands[3] = False
        flag_ld = 0
    if add_pipeline is False:
        if flag_add == 1:
            operands[4] = False
            flag_add = 0
    if add_pipeline is True:
        operands[4] = False

    if mul_pipeline is False:
        if flag_mul == 1:
            operands[5] = False
            flag_mul = 0
    if mul_pipeline is True:
        operands[5] = False

    if div_pipeline is False:
        if flag_div == 1:
            operands[6] = False
            flag_div = 0
    if div_pipeline is True:
        operands[6] = False

    operands[7] = False
    if i==54:
        print("before last LD",register_data)
    if i == 47:
        print("DADDI R5",instruction_ob[8].dest_data)
print("IF    ID     EXE     MEM    RAW    WAW     STRUCT")
temp_list = []
for instruction_obj in instruction_ob:
    temp_list.clear()
    temp_list.append(instruction_obj.IF)
    temp_list.append(instruction_obj.ID)
    temp_list.append(instruction_obj.EXE)
    temp_list.append(instruction_obj.WB)
    temp_list.append(instruction_obj.RAW)
    temp_list.append(instruction_obj.WAW)
    temp_list.append(instruction_obj.STRUCT)
    print(temp_list)

print("i access numbers ", i_access_number)
print("i misses", i_miss)
print("i hits ", i_hit)

print("d access numbers ", d_access_number)
print("d misses", d_miss)
print("d hits ", d_hit)
print("d block 0",d_block_0)
print("d block 1 ",d_block_1)
