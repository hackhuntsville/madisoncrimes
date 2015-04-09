import os

basedir = os.path.abspath(os.path.dirname(__file__))

db_ip = os.environ['DB_IP']
SQLALCHEMY_DATABASE_URI = 'postgres://docker:docker@' + db_ip + ':5432/madison_gis'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
