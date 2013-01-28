#!/usr/bin/python

import random
import subprocess
import os
import sys
import threading

target = "convert"
fuzz_factor = 500

def create_test_file(test_num):
    global fuzz_factor
    global good_data
    data = list(good_data)

    mutations = random.randrange(1,fuzz_factor);

    for mnum in range(mutations):
        mut = random.randrange(256)
        pos = random.randrange(len(data))
        data[pos] = "%c" % mut

    bad_file = open("%d.png" % test_num,"w")
    bad_file.write("".join(data))
    bad_file.close()

def save_test_file(test_num):
    try:
        os.rename("%d.png" % test_num, "saved%d.png" % test_num)
    except:
        pass

def remove_test_file(test_num):
    try:
        os.unlink("%d.png" % test_num)
    except:
        pass

def run_test(test_num):
    global target
    global crash_num
    global devnull

    try:
        subprocess.check_call([target,"%d.png" % test_num,"out.jpg"],stderr=devnull)
    except subprocess.CalledProcessError as error:
        if error.returncode != 1:
            crash_num+=1
            save_test_file(test_num)
    
def main():
    global crash_num
    global devnull
    global good_data

    if len(sys.argv) != 2:
        print "Usage: %s num_test_cases" % sys.argv[0]
        sys.exit(0)
 
    print "Running %d test cases..." % int(sys.argv[1])

    crash_num = 0
    devnull = open(os.devnull, "w")

    good_file = open("good.png","r")
    good_data = good_file.read()
    good_file.close()

    random.seed(1337)

    for test_num in range(int(sys.argv[1])):
        if (test_num % 1000) == 0:
            print "Test %d of %s. %d crashes found so far." % (test_num,sys.argv[1],crash_num)

        create_test_file(test_num)
        run_test(test_num)
        remove_test_file(test_num)

    devnull.close()

    print "Fuzzing done. %d crashes found." % crash_num
                              
main()
