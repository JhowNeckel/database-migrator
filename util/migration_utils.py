from model.fab_migration import Migration
import time
import yaml


def migration_parser(string):
    migration = yaml.load(string)

    return Migration(
        migration.get("description"),
        migration.get("authored_at"),
        migration.get("up"),
        migration.get("down")
    )


def date_to_timestamp(date):
    return (int(time.mktime(time.strptime(str(date), '%Y-%m-%d %H:%M:%S'))) - time.timezone) * 1000
