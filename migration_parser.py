from fab_migration import Migration
import yaml


def parse(string):
    migration = yaml.load(string)

    return Migration(
        migration.get("description"),
        migration.get("authored_at"),
        migration.get("up"),
        migration.get("down")
    )
