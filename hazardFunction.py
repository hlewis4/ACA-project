
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