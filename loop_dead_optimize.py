from collections import defaultdict

def dead_optimize(lines):
    table = dict()
    for i in range(len(lines)):
        line = lines[i]
        if "=" in line and "goto" not in line:
            if line[0] not in table.keys():
                if line[0][0] != "t":
                    table[line[0]] = [-1]
                else:
                    table[line[0]] = []
            for rhs in line[2:]:
                if rhs in table.keys():
                    table[rhs].append(i)
        elif line[0] == "param":
            try:
                int(line[1])
            except:
                table[line[1]].append(i)

        else:
            if "if" in line and "goto" in line:
                if line[1] in table.keys():
                    table[line[1]].append(i)
                if line[2] in table.keys():
                    table[line[3]].append(i)
    # print(table)

    optimizedTac = []
    prevLHS = ""
    line2remove = []
    for i in range(len(lines)):
        line = lines[i]
        if "=" in line and "goto" not in line:
            if len(table[line[0]]) > 0:
                optimizedTac.append(line)
            # else:
            #     print(line)
        else:
            optimizedTac.append(line)

    for i in line2remove:
        optimizedTac.pop(i)

    junk_dict = {}
    for i in reversed(range(len(lines))):
        line = lines[i]
        if "=" in line and "goto" not in line:
            if line[0] not in junk_dict.keys():
                junk_dict[line[0]] = []
            else:
                if (line[0] not in line[2:]):
                    junk_dict[line[0]].append(i)

    vals = []
    [vals.extend(l) for l in junk_dict.values()]
    print(vals)
    print(len(optimizedTac))
    optimizedTac = [l for i,l in enumerate(optimizedTac) if i not in vals]
    print(len(optimizedTac))
    return optimizedTac

def loop_invariance(lines):
    table = dict()
    start = 0
    for i in range(len(lines)):
        line = lines[i]
        if line[0] == "if":
            start = 0
        if line[0][0] != "L" and start == 0:
            if "=" in line and "goto" not in line:
                if line[0] not in table.keys():
                        table[line[0]] = line[2]
        else:
            start = 1
            for k,rhs in enumerate(line[2:]):
                if rhs in table.keys():
                    lines[i][2+k] = table[rhs]
    return lines

def loop_unroll(lines):
    newLines = []
    newL = []
    start = 0
    for i in reversed(range(len(lines))):
        line = lines[i]
        if line[0][0] == "L":
            start = 0
            for ll in newLines:
                newL.insert(0, ll)
            newLines = []

        if start == 1:
            newLines.append(line)

        if line[0] == "if" and "goto" in line and start == 0:
            if int(line[3]) > 20 and int(line[3])%2 == 0:
                start = 1
                lines[i][3] = str(int(line[3])//2)
                newL.insert(0, line)
                continue
        else:
            newL.insert(0, line)
    return newL


if __name__ == "__main__":
    lines = open("optimizedTac.s", "r").readlines()
    for l in range(len(lines)):
        lines[l] = lines[l].strip().split()

    optimizedTac = dead_optimize(lines)
    optimizedTac2 = loop_unroll(optimizedTac)
    optimizedTac = [" ".join(line)+"\n" for line in optimizedTac]
    fp = open("deadCodeEliminated", "w")
    fp.writelines(optimizedTac)
    fp.close()


    optimizedTac2 = [" ".join(line)+"\n" for line in optimizedTac2]
    fp = open("loopInvariance", "w")
    fp.writelines(optimizedTac2)
    fp.close()
