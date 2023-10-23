PRINTOUT = "printout"
ASSERT = "assert"


def printout(action_args, bindings):
    if 't' in action_args:
        output = ' '.join(bindings.get(arg, arg) for arg in action_args if arg != 't' and arg != 'crlf')
        if 'crlf' in action_args:
            output += '\n'
        print(output)
