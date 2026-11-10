import os
from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb


class Database:
    """PostgreSQL access layer for the car catalog."""

    def __init__(self):
        self.connection_string = os.getenv(
            'DATABASE_URL',
            'host=localhost port=5432 dbname=car_catalog user=postgres '
            'password=2811',
        )
        self.initialize()

    @contextmanager
    def connection(self):
        connection = psycopg.connect(
            self.connection_string,
            row_factory=dict_row,
        )
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def initialize(self):
        with self.connection() as connection:
            connection.execute(
                '''
                CREATE TABLE IF NOT EXISTS cars (
                    id BIGSERIAL PRIMARY KEY,
                    car_type VARCHAR(30) NOT NULL,
                    parameters JSONB NOT NULL
                )
                '''
            )

    def is_empty(self):
        with self.connection() as connection:
            row = connection.execute(
                'SELECT EXISTS (SELECT 1 FROM cars)'
            ).fetchone()
        return not row['exists']

    def insert_car(self, car_type, parameters):
        with self.connection() as connection:
            row = connection.execute(
                '''
                INSERT INTO cars (car_type, parameters)
                VALUES (%s, %s)
                RETURNING id
                ''',
                (car_type, Jsonb(parameters)),
            ).fetchone()
        return row['id']

    def update_car(self, car_id, car_type, parameters):
        with self.connection() as connection:
            connection.execute(
                '''
                UPDATE cars
                SET car_type = %s, parameters = %s
                WHERE id = %s
                ''',
                (car_type, Jsonb(parameters), car_id),
            )

    def delete_car(self, car_id):
        with self.connection() as connection:
            connection.execute('DELETE FROM cars WHERE id = %s', (car_id,))

    def fetch_cars(self, order_by='year', descending=False, car_type=None):
        allowed_columns = {
            'year': "parameters->>'year'",
            'brand': "parameters->>'brand'",
            'model': "parameters->>'model'",
            'type': 'car_type',
        }
        column = allowed_columns.get(order_by, allowed_columns['year'])
        direction = 'DESC' if descending else 'ASC'
        query = f'''
            SELECT id, car_type, parameters
            FROM cars
            {'WHERE car_type = %s' if car_type else ''}
            ORDER BY {column} {direction}
        '''
        with self.connection() as connection:
            cursor = connection.execute(
                query,
                (car_type,) if car_type else (),
            )
            return cursor.fetchall()

    def fetch_statistics(self):
        with self.connection() as connection:
            row = connection.execute(
                '''
                SELECT
                    COUNT(*) AS total,
                    COALESCE(MIN((parameters->>'year')::int), 0) AS first_year,
                    COALESCE(MAX((parameters->>'year')::int), 0) AS last_year
                FROM cars
                '''
            ).fetchone()
            fastest = connection.execute(
                '''
                SELECT parameters->>'brand' AS brand,
                       parameters->>'model' AS model,
                       (parameters->>'max_speed')::float AS speed
                FROM cars
                WHERE parameters ? 'max_speed'
                ORDER BY (parameters->>'max_speed')::float DESC
                LIMIT 1
                '''
            ).fetchone()
        return row, fastest

    def fetch_distribution(self, expression):
        expressions = {
            'type': 'car_type',
            'year': "(parameters->>'year')",
            'model': "(parameters->>'model')",
        }
        selected = expressions[expression]
        with self.connection() as connection:
            rows = connection.execute(
                f'''
                SELECT {selected} AS name, COUNT(*) AS amount
                FROM cars
                GROUP BY {selected}
                ORDER BY name
                '''
            ).fetchall()
        return {row['name']: row['amount'] for row in rows}

    def fetch_performance(self):
        with self.connection() as connection:
            rows = connection.execute(
                '''
                SELECT parameters->>'model' AS model,
                       parameters->>'brand' AS brand,
                       (parameters->>'max_speed')::float AS speed,
                       (parameters->>'acceleration')::float AS acceleration,
                       car_type AS type
                FROM cars
                WHERE parameters ? 'max_speed'
                ORDER BY model
                '''
            ).fetchall()
        return rows
