from bin.database_migrator import execute_query, apply_migration, remove_migration, atual_position
import time


class Migration(object):

    def __init__(self, description, authored_at, up, down):
        self.description = description
        self.authored_at = authored_at
        self.up = up
        self.down = down

    def insert(self):
        if execute_query(self.up):
            print("Inserir migração '%s' executada com sucesso" % self.description)
            apply_migration(self.authored_at, self.description, self.applied_time())

    def drop(self):
        if execute_query(self.down):
            print("Remover migração '%s' executada com sucesso" % self.description)
            remove_migration(self.authored_at, self.description)

    def less_then(self, timestamp):
        db_position = atual_position()
        if int(timestamp) >= self.authored_at > db_position:
            self.insert()

    def greater_than(self, timestamp):
        db_position = atual_position()
        if int(timestamp) < self.authored_at <= db_position:
            self.drop()

    @staticmethod
    def applied_time():
        return int(time.time()) * 1000
