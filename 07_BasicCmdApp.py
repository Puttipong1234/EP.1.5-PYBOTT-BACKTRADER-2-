from __future__ import (absolute_import ,
                        division , 
                        print_function , 
                        unicode_literals)

import argparse

def parse_args(pargs=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=(
            'This is my First Cmd App'
        )
    )

    parser.add_argument("--num1",default='',required=True,
                        help='Please Define num1')
    
    parser.add_argument("--num2",default='',required=True,
                        help='Please Define num2')
    
    parser.add_argument("--op",default='+',required=True,
                        help='Please Define operations [+,-,*,/]')
    
    return parser.parse_args(pargs)

def run(args=None):
    args = parse_args(args)
    print("This is my first number",args.num1)
    print("This is my second number",args.num2)

    if args.op == "+":
        print("Result is :" ,float(args.num1) + float(args.num2) )
    
    if args.op == "-":
        print("Result is :" ,float(args.num1) - float(args.num2) )
    
    if args.op == "*":
        print("Result is :" ,float(args.num1) * float(args.num2) )
    
    if args.op == "/":
        print("Result is :" ,float(args.num1) / float(args.num2) )

if __name__ == "__main__":
    run()