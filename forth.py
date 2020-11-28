from typing import List, Union, Tuple, NewType, Dict
from dataclasses import dataclass

@dataclass
class SubProgram:
    '''Defines a subprogram (function)
    
    :param name: subprogram name'''
    name : str
    '''subprogram name'''
    body : List['Lexem']
    '''list of lexems in the subprogram'''
Lexem = Union[str,int, SubProgram]
def parse(program : str) -> List[Lexem]:
    """Parses input program into a list of either command or number
    
    :param program: program text"""
    number = None
    command = None
    lexems : List[Lexem] = []
    program = program.strip()
    while program[0] == ':':
        program = program[1:].strip()
        func, program = program.split(';', 1)
        name, body = func.split(' ', 1)
        lexems.append(SubProgram(name, parse(body)))
    for letter in program:
        if letter.isdigit():
            if number is None:
                number = int(letter)
            else:
                number = 10*number + int(letter)
        else:
            if number is not None:
                lexems.append(number)
            number = None
        if not letter.isdigit() and not letter.isspace():
            if command is None:
                command = letter
            else:
                command += letter
        else:
            if command is not None:
                lexems.append(command)
            command = None
    if number is not None:
        lexems.append(number)
    if command is not None:
        lexems.append(command)
    return lexems

def execute(lexems : List[Lexem],
            stack: List[int] = []) -> List[int]:
    """Execute a Forth program written as a list of lexems"""
    stack = stack.copy()
    subs : Dict[str,List[Lexem]] = {}
    for lexem in lexems:
        if isinstance(lexem, SubProgram):
            subs[lexem.name] = lexem.body
        elif isinstance(lexem, int):
            stack.append(lexem)
        elif lexem == '+':
            stack.append(stack.pop() + stack.pop())
        elif lexem == '*':
            stack.append(stack.pop() * stack.pop())
        elif lexem in subs:
            stack = execute(subs[lexem], stack)
        elif lexem == 'DROP':
            stack.pop()
        elif lexem == 'DUP':
            stack.append(stack[-1])
        else:
            raise NotImplementedError('Unknown command ' + lexem)
    return stack

if __name__ == "__main__":
    import sys
    program = input('Enter Forth program: ')
    lexems = parse(program)
    stack = execute(lexems, [])
    if len(stack) > 1:
        print('Bad program. After its execution stack should only contain one item')
        sys.exit(-1)
    print(stack[0])