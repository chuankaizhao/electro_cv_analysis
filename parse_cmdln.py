import json
import ast

def parse_list(list_str):
    return ast.literal_eval(list_str)

def parse_bool(bool_str):
    return json.loads(bool_str)

def parse_dict(dict_str):
    return json.loads(dict_str)

def parse_cmdln(inputFile):
    args = {}
        
    try:
        with open(inputFile) as f:
            for line in f:
                if line.strip() == "" or line[0] == '#':
                    continue
                line = line.split('#')[0]
                key, value = line.strip().split('=')
                if value[0] == '"' and value[-1] == '"':
                    value = value[1:len(value)-1]
                elif value[0] == '[' and value[-1] == ']':
                    value = parse_list(value)
                elif value[0] == '{' and value[-1] == '}':
                    value = parse_dict(value)
                else:
                    value = parse_bool(value)
                args[key] = value
        
        return args
    
    except Exception as e:
        print(f"Error: {e}")