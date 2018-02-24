from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import time

host = ['172.17.0.3']
auth = PlainTextAuthProvider(username='cassandra', password='cassandra')

cluster = Cluster(host, auth_provider=auth)
session = cluster.connect('mayhem')


def execute_query(query):
    session.prepare(query)
    try:
        session.execute(query)
        return True
    except Exception as e:
        print("Erro ao executar query, %s" % e)
        return False


def create_migration_table():
    query = "CREATE TABLE IF NOT EXISTS applied_migrations (authored_at timestamp,description text,applied_at " \
            "timestamp, PRIMARY KEY (authored_at, description)) "
    execute_query(query)


def apply_migration(authoredat, description, appliedat):
    create_migration_table()
    query = "INSERT INTO applied_migrations (authored_at, description, applied_at) VALUES ('%s', '%s', '%s')" \
            % (authoredat, description, appliedat)
    execute_query(query)


def remove_migration(authoredat, description):
    query = "DELETE FROM applied_migrations WHERE authored_at='%a' and description='%s'" % (authoredat, description)
    execute_query(query)


def date_to_timestamp(date):
    return (int(time.mktime(time.strptime(str(date), '%Y-%m-%d %H:%M:%S'))) - time.timezone) * 1000


def atual_position():
    create_migration_table()
    query = "SELECT * FROM applied_migrations"
    rows = session.execute(query)
    rows.current_rows.sort(reverse=True)
    data = rows.current_rows.pop(0) if rows.current_rows.__len__() != 0 else None
    return date_to_timestamp(data.authored_at) if data is not None else 0


if __name__ == '__main__':
    print(atual_position())
