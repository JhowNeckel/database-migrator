import os
from migration_parser import parse

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
            table = parse(content.read())

            if operation == "up":
                table.insert()
            elif operation == "down":
                table.drop()
            elif operation == "up_to":
                table.less_then(timestamp) if timestamp is not None else print("timestamp vazio")
            elif operation == "down_to":
                table.greater_than(timestamp) if timestamp is not None else print("timestamp vazio")


if __name__ == '__main__':
    migration("up_to", 1519491752000)
