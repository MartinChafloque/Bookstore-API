from django.core.management.base import BaseCommand
from django.db import connections, DEFAULT_DB_ALIAS
import os

class Command(BaseCommand):
    help = 'Poblar la base de datos con la plantilla SQL'

    def handle(self, *args, **options):
        sql_templates_dir = '/bookstore/sql/sql_templates.sql'

        database = options.get('database', DEFAULT_DB_ALIAS)
        connection = connections[database]

        for filename in os.listdir(sql_templates_dir):
            if filename.endswith('.sql'):
                with open(os.path.join(sql_templates_dir, filename), 'r') as sql_file:
                    with connection.cursor() as cursor:
                        sql_statements = sql_file.read().split(';')
                        for sql_statement in sql_statements:
                            if sql_statement.strip():
                                cursor.execute(sql_statement)

        self.stdout.write(self.style.SUCCESS('La base de datos fue plobada exitosamente'))
