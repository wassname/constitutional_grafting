"""CPU-only native argparse validation for stage stubs; executes parser definitions, never model code. -- PI/OpenAI (Sol)"""
import argparse
import ast
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=None)
def native_parser(path):
    path=Path(path);tree=ast.parse(path.read_text())
    bodies=[node.body for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=='main']
    bodies += [node.body for node in tree.body if isinstance(node,ast.If) and '__main__' in ast.unparse(node.test)]
    for body in bodies:
        prefix=[];parser_name=None
        for statement in body:
            parse_calls=[node for node in ast.walk(statement) if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=='parse_args']
            if parse_calls:
                assert len(parse_calls)==1 and isinstance(parse_calls[0].func.value,ast.Name),path
                parser_name=parse_calls[0].func.value.id;break
            prefix.append(statement)
        if parser_name:
            namespace={'argparse':argparse,'Path':Path,'__doc__':ast.get_docstring(tree)}
            exec(compile(ast.Module(body=prefix,type_ignores=[]),str(path),'exec'),namespace)
            return namespace[parser_name]
    raise AssertionError('No native argparse definition found: '+str(path))



def validate_argv(path,argv):
    return native_parser(str(Path(path).resolve())).parse_args(list(map(str,argv)))
