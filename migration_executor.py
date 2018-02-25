from migration_parser import migration_parser
import argparse
import os

directory = '/home/jhonatan/projects/migrations'


def order_migrations(operation):
    if operation == "up" or operation == "up_to":
        return sorted(os.listdir(directory))
    elif operation == "down" or operation == "down_to":
        return sorted(os.listdir(directory), reverse=True)


def migration(operation, timestamp=None):
    migrations = order_migrations(operation)
    os.chdir(directory)

    for f in migrations:
        with open(f) as content:
            table = migration_parser(content.read())

            if operation == "up":
                table.insert()
            elif operation == "down":
                table.drop()
            elif operation == "up_to":
                table.less_then(timestamp) if timestamp is not None else print("timestamp vazio")
            elif operation == "down_to":
                table.greater_than(timestamp) if timestamp is not None else print("timestamp vazio")


parser = argparse.ArgumentParser(description='Python database migrator.')
parser.add_argument('--up', action='store_true', dest='up', help='Executa todas as operações de up das migrações.')
parser.add_argument('--down', action='store_true', help='Executa todas as operações de down das migrações.')
parser.add_argument('--up_to',  dest='up_to', nargs=1, help='Executa as operações de up até o timestamp informado.')
parser.add_argument('--down_to', dest='down_to', nargs=1, help='Executa as operações de down até o timestamp informado.')
args = parser.parse_args()

if args.up:
    migration("up")
elif args.down:
    migration("down")
elif args.up_to:
    migration("up_to", args.up_to[0])
elif args.down_to:
    migration("down_to", args.down_to[0])
