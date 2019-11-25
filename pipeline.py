from defClass import instructionClass as instClass

with open(r"C:\Users\hashi\Desktop\ACA\ACA project\inst.txt") as f:
    lines = f.read().splitlines()
print("Instructions")
print(lines)

inst = []
for x in range(len(lines)):
    inst.append(lines[x].split(' '))

for i in range(len(inst)):
    inst[i] = [item.replace(",", "") for item in inst[i]]

instruction = []
for i in range(len(inst)): # create a list with nested lists
    instruction.append([])
    for j in range(len(inst[i])):
        if j==2 and len(inst[i][j])==5:
            instruction[i].append(inst[i][j][0])
            instruction[i].append(inst[i][j][2:4])
        else:
            instruction[i].append(inst[i][j])




instruction_ob = []
dest = 0
s1 = 0
s2 = 0

length = len(instruction)

for i in instruction:
    if length == 4:
        dest = i[1][:-1]
        if len(i[2][-1]) == 1:
            s1 = int(i[2][:-1])
        else:
            s1 = i[2][:-1]
        if len(i[3]) == 1:
            s2 = len(i[3])
        else:
            s2 = i[3]

    elif length == 1:
        dest = 0
        s1 = 0
        s2 = 0

    instruction_ob.append(instClass(i[0], dest, s1, s2))
print("Instructions after parsing")
print(instruction)

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

fp_add=0
fp_mul=0
fp_divide=0
add_pipeline = False
mul_pipeline = False
div_pipeline =False
mem=0


for i in cycles:
        if "adder:" in i:
            fp_add=int(i[2])
            if "yes" in i:
                add_pipeline=True
            else:
                add_pipeline=False


        if "Multiplier:" in i:
            fp_mul=int(i[2])
            if "yes" in i:
                mul_pipeline = True
            else:
                mul_pipeline = False

        if "divider:" in i:
            fp_divide=int(i[2])
            if "yes" in i:
                div_pipeline=True
            else:
                div_pipeline = False

        if "memory:" in i:
             mem=int(i[2])

print(fp_add)
print(mul_pipeline)
print(mem)

operands=[False,False,False,False,False,False,False,False]
exe_in_ld=10000
exe_in_add=1000
exe_in_mul=1000
exe_in_div=10000
count = 1
flag_ld=0
flag_add=0
flag_mul=0
flag_div=0
ld_pass=[0]*len(instruction_ob)
add_pass=[0]*len(instruction_ob)
mul_pass=[0]*len(instruction_ob)
div_pass=[0]*len(instruction_ob)
print(len(instruction_ob))

counter = [0]*len(instruction_ob)

for i in range(40):
    for j in range(len(instruction_ob)):

        #IF stage
        if i == 0 and not operands[0]:
            instruction_ob[j].IF = count
            operands[0] = True
            instruction_ob[j].IF_complete = True
            continue
        else:
            if instruction_ob[j].IF_complete is False and (operands[0] is False):
                if instruction_ob[j-1].ID > 0:
                    operands[0]=True
                    instruction_ob[j].IF = count
                    instruction_ob[j].IF_complete=True
                    continue

        #ID stage
        if instruction_ob[j].IF > 0 and (operands[1] is False) and (instruction_ob[j].ID_complete is False):
            operands[1] = True
            instruction_ob[j].ID = count
            instruction_ob[j].ID_complete = True
            continue


        #EXE stage

        #IU cycle
        if instruction_ob[j].name in ["L.D", "DADDI", "DSUB"]:
            if instruction_ob[j].ID > 0 and (operands[2] is False) and (instruction_ob[j].IU_complete is False):
                operands[2] = True
                instruction_ob[j].IU = count
                instruction_ob[j].EXE = count
                instruction_ob[j].IU_complete = True
                continue

         #MEM stage
        if instruction_ob[j].name in ["L.D","DADDI","DSUB"]:
            if (instruction_ob[j].IU > 0 and (operands[3] is False) and (instruction_ob[j].EXE_complete is False)) or (instruction_ob[j].IU > 0 and ld_pass[j] ==1 and (instruction_ob[j].EXE_complete is False)):
                if exe_in_ld > mem:
                    exe_in_ld = mem
                if exe_in_ld > 1:
                    operands[3] = True
                    ld_pass[j] = 1
                    continue
                else:
                    flag_ld = 1
                    instruction_ob[j].EXE = count
                    instruction_ob[j].EXE_complete = True
                    continue
        #ADD
        if instruction_ob[j].name == "ADD.D" or instruction_ob[j].name == "SUB.D":
            if instruction_ob[j].ID > 0 and (operands[4] is False) and (instruction_ob[j].EXE_complete is False) or (instruction_ob[j].ID > 0 and (add_pass[j] == 1) and (instruction_ob[j].EXE_complete is False)):
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
                    continue

        #MUL
        if instruction_ob[j].name == "MUL.D":
            if instruction_ob[j].ID > 0 and (operands[5] is False) and (instruction_ob[j].EXE_complete is False) or (instruction_ob[j].ID > 0 and (mul_pass[j] == 1) and (instruction_ob[j].EXE_complete is False)):
                if exe_in_mul>fp_mul:
                    exe_in_mul = fp_mul
                if exe_in_mul > 1:
                    operands[5] = True
                    mul_pass[j] = 1
                    continue
                else:
                    flag_mul = 1
                    instruction_ob[j].EXE = count
                    instruction_ob[j].EXE_complete = True
                    continue

        #DIV
        if instruction_ob[j].name == "DIV.D":
            if instruction_ob[j].ID > 0 and (operands[6] is False) and (instruction_ob[j].EXE_complete is False) or instruction_ob[j].ID > 0 and (div_pass[j] == 1) and (instruction_ob[j].EXE_complete is False):
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
                    continue

        #WriteBack
        if (instruction_ob[j].EXE_complete is True) and (operands[7] is False) and (instruction_ob[j].WB_complete is False):
            operands[7] = True
            instruction_ob[j].WB = count
            instruction_ob[j].WB_complete = True
            continue


    count += 1
    if(exe_in_mul>0):
        exe_in_mul -= 1
    if exe_in_add>0:
        exe_in_add -= 1
    if exe_in_ld > 0:
        exe_in_ld-=1

    operands[0]=False
    operands[1]=False
    operands[2]=False
    if flag_ld==1:
        operands[3]=False
    if flag_add==1:
        operands[4] =False
    if flag_mul==1:
        operands[5] =False
    if flag_div==1:
        operands[6] =False
    operands[7]=False


temp_list = []
for instruction_obj in instruction_ob:
    temp_list.clear()
    temp_list.append(instruction_obj.IF)
    temp_list.append(instruction_obj.ID)
    temp_list.append(instruction_obj.EXE)
    temp_list.append(instruction_obj.WB)
    print(temp_list)

