from sys import argv
from os import system

fname = argv[1]
tmpfname = "temporary_file.c"
system("python sanitize.py %s > temporary_file.c"%fname)
system("gcc -Wall -O3 %s -lm -o %s bdwgc/gc.a"%(tmpfname, fname[:-3]))
system("rm temporary_file.c")


