import ast 
import io
import collections
import astunparse

class ASTParser:
    def __init__(self, name, start, end):
        self.path = "examples/code/"+name
        self.start = start
        self.end = end
        self.tree = None
        self.sub_tree = None
        self.imports = {}
        self.imports_from = {}
        self.prefixes = []

    def extract_api_calls(self):
        self.create_ast()
        self.extract_imports()
        self.clean_imports()
        self.get_prefix_calls()
    
    def create_ast(self):
        fp = self.extract_lines()
        self.tree = ast.parse(self.read_file_to_string())
        self.sub_tree = ast.parse(self.read_fp_to_string(fp))
    
    def extract_lines(self):
        new_file, count = "", 0
        with open(self.path, "r") as fp:
            for line in fp:
                if count >= self.start and count <= self.end:
                    new_file += line #update this to fix whitespace handling
                count += 1
        fp = io.StringIO(new_file)
        return fp

    def extract_imports(self):
        c, c1 = 0, 0
        tree = self.tree
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for i in node.names:
                    if isinstance(i, ast.alias):
                        self.imports[c] = (i.name, i.asname)
                        c += 1
            if isinstance(node, ast.ImportFrom):
                for i in node.names:
                    if isinstance(i, ast.alias):
                        self.imports_from[c1] = (node.module, i.name, i.asname)
                        c1 += 1

    def clean_imports(self):
        for idx, val in self.imports.items():
            self.prefixes.append(val[0] if val[1] is None else val[1])
        for idx, val in self.imports_from.items():
            self.prefixes.append(val[1] if val[2] is None else val[2])

    def get_prefix_calls(self):
        api_calls = {}
        for node in ast.walk(self.sub_tree):
            if isinstance(node, ast.Call):
                assign = astunparse.unparse(node).replace("\n", "")
                for child_node in ast.walk(node):
                    if isinstance(child_node, ast.Name):
                        if child_node.id in self.prefixes:
                            if child_node.id in api_calls:
                                api_calls[child_node.id].append(assign)
                            else:
                                api_calls[child_node.id] = [assign]

        for k,v in api_calls.items():
            print("### Calls to", k)
            for x in v:
                print(x)
            print("\n")


        
    def read_fp_to_string(self, fp):
        s = fp.read()
        fp.close()
        return s

    def read_file_to_string(self):
        f = open(self.path, 'rt')
        s = f.read()
        f.close()
        return s