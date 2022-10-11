import re
import sys

class Assembler:

    def main(self):
        file_name = sys.argv[1]
        myfile = open(file_name)

        self.var_table = {}
        self.set_default_vars_to_table()
        self.read1(myfile)
        myfile.close()

        print(self.var_table)

        myfile = open(file_name)
        self.read2(myfile, file_name)
        myfile.close()

    def set_default_vars_to_table(self):
        self.var_table = {
            "R0" : 0,
            "R1" : 1,
            "R2" : 2,
            "R3" : 3,
            "R4" : 4,
            "R5" : 5,
            "R6" : 6,
            "R7" : 7,
            "R8" : 8,
            "R9" : 9,
            "R10" : 10,
            "R11" : 11,
            "R12" : 12,
            "R13" : 13,
            "R14" : 14,
            "R15" : 15,
            "SCREEN" : 16384,
            "KBD"  : 24576,
            "SP"   : 0,
            "LCL"  : 1,
            "ARG"  : 2,
            "THIS" : 3,
            "THAT" : 4,
        }
        
    def read1(self, myfile):
        line_num = 0
        line     = myfile.readline()
        while line:
            line = line.strip()
            if line.startswith("(") and line[-1] == ")":
                self.var_table[line[1:-1]] = line_num # take parenthes and insert value
            elif line != "" and (line.startswith("//") == False):
                line_num += 1
            line      = myfile.readline()

    def read2(self, myfile, file_name): #test
        var_index = 16
        line     = myfile.readline()

        dot_idx = file_name.find(".")
        file_name = file_name[:dot_idx]
        f = open(file_name + ".hack", "a")
        
        while line:
            line = line.strip()
            if re.search("//", line):
                comment_idx = line.find("/")
                line = line[:comment_idx]
                
                line = line.strip()


            if line.startswith("@"):
                if re.search("@[0-9]", line):
                    f.write('{0:016b}'.format(int(line[1:]))+"\n")
                else: # @i and shit
                    if line[1:] in self.var_table:
                        f.write('{0:016b}'.format(self.var_table[line[1:]])+"\n")
                    else:
                        self.var_table[line[1:]] = var_index
                        f.write('{0:016b}'.format(var_index)+"\n")
                        var_index += 1
            
            # elif line.startswith("(") and line[-1] == ")":

            elif re.search("=", line): # assign values
                equal_idx = line.find("=")

                left_side = line[:equal_idx]
                dest_inst_table = {
                    ""   : "000",
                    "M"  : "001",
                    "D"  : "010",
                    "MD" : "011",
                    "A"  : "100",
                    "AM" : "101",
                    "AD" : "110",
                    "AMD": "111",
                }

                right_side = line[equal_idx+1:]
                comp_inst_table = {
                    "0"   : "1110101010",
                    "1"   : "1110111111",
                    "-1"  : "1110111010",
                    "D"   : "1110001100",
                    "A"   : "1110110000",
                    "!D"  : "1110001101",
                    "!A"  : "1110110001",
                    "-D"  : "1110001111",
                    "-A"  : "1110110011",
                    "D+1" : "1110011111",
                    "A+1" : "1110110111",
                    "D-1" : "1110001110",
                    "A-1" : "1110110010",
                    "D+A" : "1110000010",
                    "D-A" : "1110010011",
                    "A-D" : "1110000111",
                    "D&A" : "1110000000",
                    "D|A" : "1110010101",

                    "M"   : "1111110000",
                    "!M"  : "1111110001",
                    "-M"  : "1111110011",
                    "M+1" : "1111110111",
                    "M-1" : "1111110010",
                    "D+M" : "1111000010",
                    "D-M" : "1111010011",
                    "M-D" : "1111000111",
                    "D&M" : "1111000000",
                    "D|M" : "1111010101",
                }

                f.write(comp_inst_table[right_side] + dest_inst_table[left_side] + "000"+"\n")

            elif re.search(";", line): # jmp
                colonge_idx = line.find(";")

                # destination value
                dest_inst_table = {
                    "0"  : "000",
                    "M"  : "001",
                    "D"  : "010",
                    "MD" : "011",
                    "A"  : "100",
                    "AM" : "101",
                    "AD" : "110",
                    "AMD": "111",
                }

                # computation value
                comp_inst_table = {
                    "0"   : "1110101010",
                    "1"   : "1110111111",
                    "-1"  : "1110111010",
                    "D"   : "1110001100",
                    "A"   : "1110110000",
                    "!D"  : "1110001101",
                    "!A"  : "1110110001",
                    "-D"  : "1110001111",
                    "-A"  : "1110110011",
                    "D+1" : "1110011111",
                    "A+1" : "1110110111",
                    "D-1" : "1110001110",
                    "A-1" : "1110110010",
                    "D+A" : "1110000010",
                    "D-A" : "1110010011",
                    "A-D" : "1110000111",
                    "D&A" : "1110000000",
                    "D|A" : "1110010101",

                    "M"   : "1111110000",
                    "!M"  : "1111110001",
                    "-M"  : "1111110011",
                    "M+1" : "1111110111",
                    "M-1" : "1111110010",
                    "D+M" : "1111000010",
                    "D-M" : "1111010011",
                    "M-D" : "1111000111",
                    "D&M" : "1111000000",
                    "D|M" : "1111010101",
                }

                left_side = line[:colonge_idx]
                if re.search("=", left_side):
                    equal_idx = left_side.find("=")
                    dest_side = left_side[:equal_idx]
                    comp_side = left_side[equal_idx:]

                    left_side_binary = comp_inst_table[comp_side] + dest_inst_table[dest_side]
                else:
                    dest_side_binary = "000"
                    comp_side = left_side

                    left_side_binary = comp_inst_table[comp_side] + dest_side_binary
                    
                    
                right_side = line[colonge_idx+1:]
                jmp_inst_table = {
                    "null" : "000",
                    "JGT"  : "001",
                    "JEQ"  : "010",
                    "JGE"  : "011",
                    "JLT"  : "100",
                    "JNE"  : "101",
                    "JLE"  : "110",
                    "JMP"  : "111",
                }

                f.write(left_side_binary + jmp_inst_table[right_side]+"\n")

            line = myfile.readline()

        f.close()

    
asm = Assembler()
asm.main()