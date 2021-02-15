file = open("./todo.asm")
file1 = open("./done.asm","a+")
line = file.readline()

while line!="":  
        line1 = line[21:]
        file1.write(line1)
        line = file.readline()
file1.close()
file.close()