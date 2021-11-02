import ast
from os import name 
import os
import sys
import tokenize
import astunparse
import astpretty
from visitor import Visitor
import re
import io

apis = []
tensorflow_alias = "tensorflow"

def PrintUsage():
    sys.stderr.write("""
Usage:
    parse_python.py <file>

""")
    exit(1)

def read_file_to_string(filename):
    f = open(filename, 'rt')
    s = f.read()
    f.close()
    return s

def read_fp_to_string(fp):
    s = fp.read()
    fp.close()
    return s

def find_comments(filename):
    with open(filename, "r") as fp:
            content = fp.read()
            single_quote = re.compile("(''')(.*?)(''')", re.DOTALL)
            single_quote_comments = single_quote.findall(content)
    for i, x in enumerate(single_quote_comments):
        x = ''.join(x)
        single_quote_comments[i] = x

def find_start_end(filename):
    new_file, source_structure = "", False
    with open(filename, "r") as fp:
        for line in fp:
            if line.strip() == "'''[SOURCE STRUCTURE CODE STARTS HERE]'''":
                print(line.strip())
                source_structure = True
                continue
            if line.strip() == "'''[SOURCE STRUCTURE CODE ENDS HERE]'''":
                print(line.strip())
                source_structure = False
            if source_structure is True: 
                new_file += line.lstrip()
    
    fp = io.StringIO(new_file)
    print(fp.read())
    return fp
    
    

def parse_file(filename):
    #filename = "~/feature-extract/examples/code/alexnet.py"
    #filename = "alexnet"
    #filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testcases', filename + '.py')
    #print(filename)
    tensorflow_alias = "tensorflow"
    tree = ast.parse(read_file_to_string(filename), filename)

    fp = find_start_end(filename)
    sub_tree = ast.parse(read_fp_to_string(fp))

    for node in ast.walk(tree):
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            imports = astunparse.unparse(node).replace("\n", "")
            api = imports.split(" ")[1]
            for i in node.names:
                if isinstance(i, ast.alias):
                    alias = i.asname
                    if alias is None:
                        apis.append(api)
                    else: 
                        if api == 'tensorflow':
                            tensorflow_alias = alias  
                        apis.append(alias)

    for node in ast.walk(sub_tree):
        if isinstance(node, ast.Assign):
            assign = astunparse.unparse(node).replace("\n", "")
            if tensorflow_alias+"." in assign:
                assign = assign[assign.find("=") + 1:]
                print(assign)
                q = assign.split('(')[0].strip()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        PrintUsage()
    parse_file(sys.argv[1])

