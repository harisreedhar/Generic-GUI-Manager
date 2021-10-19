import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add two numbers')
    parser.add_argument('--a', metavar='a', default=0, type=int, help='first number')
    parser.add_argument('--b', metavar='b', default=0, type=int, help='second number')
    parser.add_argument('--op', metavar='op', default='sum', type=str, help='operation')
    args = parser.parse_args()

    if args.op == 'sum':
        result = args.a + args.b
    elif args.op == 'product':
        result = args.a * args.b
    elif args.op == 'sub':
        result = args.a - args.b

    print(f"result = {result}")
