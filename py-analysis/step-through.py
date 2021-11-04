import sys, getopt
import subprocess
from program import Program
from ast_parser import ASTParser

argumentList = sys.argv[1:]
 
# Options
options = "al:"
 
# Long options
long_options = ["all", "lines="]
 
try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)
     
    # checking each argument
    for currentArgument, currentValue in arguments:
 
        if currentArgument in ("-l", "--lines"):

            #check input is correctly formatted ([start_line, end_line])
            if currentValue[0] != '[' or currentValue[-1] != ']' or "," in currentValue is False:
                print("usage: step-through.py [-l '[start_line, end_line]']"), exit() 

            #convert to list, continue error handling        
            input_lines = currentValue.replace("[","").replace("]","").split(",")
            if len(input_lines) != 2: 
                print("usage: step-through.py [-l '[start_line, end_line]']"), exit()

            for x in input_lines: 
                if x.isdigit() is False:
                    print("line numbers must be integers"), exit()
                elif int(x) <= 0:
                    print("line numbers must be positive"), exit()

            if int(input_lines[0]) > int(input_lines[1]):
                print("start line bust be less than end line"), exit()

            #if you reach here, the input is well formatted
            print("\n#### Extracting features for lines", input_lines[0], "through", input_lines[1], "###\n")

            #default, run on alexnet.py (change this later)
            start, end = int(input_lines[0]), int(input_lines[1])

            p = ASTParser("alexnet.py", start, end)
            p.extract_api_calls()
            

        elif currentArgument in ("-a", "--all"):
            print ("Whole program")
             
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))

if (len(argumentList) == 0):
    print("usage: step-through.py [-l '[start_line, end_line]'] ")
    print("usage: step-through.py [-a] (run on all lines)")