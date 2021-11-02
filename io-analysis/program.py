import subprocess
import re
import numpy as np
import tokenize, io
import ast
import astunparse
import ctypes
from visitor import Visitor
from interpreter import Interpreter
import os

test_cases = {'alexnet': np.random.rand(10, 3, 227, 227)}

class Program:
    def __init__(self, name : str, start : int, end : int) -> None:
        self.name = name
        self.start = start 
        self.end = end
        self.num_lines = None
        self.lines_under_test = None
        self.before_block = None
        self.before_line = None
        self.after_block = None
        self.after_line = None
        self.path = "examples/code/"+self.name
        self.comment_dict = None
        self.whitespace = None
        self.line_dict = None
        self.fun_def_dict = None
        self.class_def_dict = None
        self.import_dict = None
        self.input_shape = None
        self.output_shape = None
        self.input = np.random.rand(10, 3, 227, 227)
        self.interpreter = Interpreter()

    def count_lines(self):
        with open(self.path, 'r') as fp:
            for count, line in enumerate(fp):
                pass
        self.num_lines = count+1

    def run(self):
        subprocess.run(["python3", self.path])

    def load_example(self):
        with open(self.path, 'r') as fp:
            return fp.readlines()   

    def run_bench_before(self):
        line = self.before_block
        start = self.before_line
        line = line[line.find("=") + 1:]
        layer = self.interpreter.create_layer_tf(line)
        _, output = self.interpreter.tf_forward_pass(layer, self.input)
        self.input_shape = output.shape
        try:
            print("#### LINE BEFORE BLOCK = ", start)
            print("    API call = ", line.rstrip())
            print("    Output shape = ", output.shape)
            print("####\n")
        except:
            print(line)
            print(output)

    def run_benchmark(self):
        start = self.start
        for line in self.lines_under_test: 
            line = line[line.find("=") + 1:]
            layer = self.interpreter.create_layer_tf(line)
            _, output = self.interpreter.tf_forward_pass(layer, self.input)
            try:
                print("#", start)
                print("    API call = ", line.rstrip())
                print("    Output shape = ", output.shape)
            except:
                print(line)
                print(output)
            start += 1
        self.output_shape = output.shape
        print("\n")

    def get_lut(self):
        lines = []
        count = 0
        with open(self.path, 'r') as fp:
            for line in fp:
                if count >= self.start-1 and count <= self.end-1:
                    lines.append(line)
                count += 1
        self.lines_under_test = lines

    def pretty_print(self):
        lines = self.lines_under_test
        start_line = self.start
        print("\n#### Lines under Test ####\n")
        for line in lines:
            print(start_line, "    ", line.lstrip().rstrip())
            start_line += 1
        print("\n")

    def extract_comments(self):
        normal_comments, single_quote_comments, double_quote_comments = [],[],[]

        #extracting multi-line comments
        with open(self.path, "r") as fp:
            content = fp.read()
            single_quote = re.compile("(''')(.*?)(''')", re.DOTALL)
            double_quote = re.compile('(?:""")(.*?)(?:""")', re.DOTALL)
            single_quote_comments = single_quote.findall(content)
            double_quote_comments = double_quote.findall(content)
            quote_comments = single_quote_comments+double_quote_comments
        for i, x in enumerate(quote_comments):
            x = ''.join(x)
            quote_comments[i] = x

        #extracting single-line comments
        with open(self.path, 'r') as fp:
            for toktype, tok, start, end, line in tokenize.generate_tokens(fp.readline):
                if toktype == tokenize.COMMENT:
                    normal_comments.append(tok)
        return quote_comments+normal_comments

    def make_ast(self):
        r = open(self.path,'r')
        t = ast.parse(r.read())
        v = Visitor()
        v.visit(t)
        return t

    def import_dict_make(self):
        import_dict = {}
        self.make_line_dict()
        import_lines = self.import_lines(self.make_ast())
        for k,v in self.line_dict.items():
            clean = v.replace("\n", "")
            if clean in import_lines:
                import_dict[k] = clean
        self.import_dict = import_dict

    def import_lines(self, t):
        imports = []
        for node in ast.walk(t):
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                imports.append(astunparse.unparse(node).replace("\n", ""))
        return imports

    def class_def_dict_make(self):
        class_def_dict = {}
        self.make_line_dict()
        class_defs = self.class_def_lines(self.make_ast())
        for k,v in self.line_dict.items():
            clean = v.replace(':', '').lstrip().replace("\n", "")
            if clean in class_defs:
                class_def_dict[k] = clean
        self.class_def_dict = class_def_dict

    def class_def_lines(self, t):
        class_defs = []
        for node in ast.walk(t):
            if isinstance(node, ast.ClassDef):
                class_defs.append(astunparse.unparse(node).split(":")[0].replace("\n", ""))
        return class_defs

    def fun_def_dict_make(self):
        fun_def_dict = {}
        self.make_line_dict()
        fun_defs = self.fun_def_lines(self.make_ast())
        for k,v in self.line_dict.items():
            clean = v.replace(':', '').lstrip().replace("\n", "")
            if clean in fun_defs:
                fun_def_dict[k] = clean
        self.fun_def_dict = fun_def_dict

    def fun_def_lines(self, t):
        fun_defs = []
        for node in ast.walk(t):
            if isinstance(node, ast.FunctionDef):
                fun_defs.append(astunparse.unparse(node).split(":")[0].replace("\n", ""))
        return fun_defs

    def comment_dict_make(self):
        c, comment_dict = 0, {}
        comments = self.extract_comments()
        with open(self.path, "r") as fp:
            for line in fp:
                c+=1
                clean_line = line.strip("\n").lstrip()
                if clean_line in comments:
                    comment_dict[c] = clean_line
        self.comment_dict = comment_dict

    def whitespace_lines(self):
        count, whitespace = 0, []
        with open(self.path, 'r') as fp:
            for line in fp:
                count += 1
                if line.isspace():
                    whitespace.append(count)
        self.whitespace = whitespace

    def before_and_after(self):
        self.make_line_dict()
        self.before_block = self.before(self.line_dict)
        self.after_block = self.after(self.line_dict)
    
    def make_line_dict(self):
        lines, count = {}, 0
        with open(self.path, "r") as fp:
            for line in fp:
               count += 1
               lines[count] = line
        self.line_dict = lines

    def before(self, lines):
        offset, before_block = 1, None
        while(offset != self.start):
            begin = self.start - offset
            if begin not in self.comment_dict and begin not in self.whitespace \
                and begin not in self.fun_def_dict and begin not in self.class_def_dict \
                and begin not in self.import_dict:
                before_block = lines[self.start-offset]
                self.before_line = self.start-offset
                break
            offset+=1
        if before_block is None:
            return "SOF reached"
        else:
            return before_block 
    
    def after(self, lines):
        offset, after_block = 1, None
        while(offset+self.end <= len(lines)):
            begin = self.end + offset
            if begin not in self.comment_dict and begin not in self.whitespace \
                 and begin not in self.fun_def_dict and begin not in self.class_def_dict \
                and begin not in self.import_dict:
                after_block = lines[self.end+offset]
                break
            offset+=1
        if after_block is None:
            return "EOF reached"
        else:
            return after_block