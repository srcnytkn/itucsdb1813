import os
import sys

import psycopg2 as dbapi2

DATABASE_URL = 'postgres://ddzwibxvysqwgx:9e0edae8756536ffdba78314ebde69e2d019e58a2c05dfbad508b5eb657ac9e7@ec2-54-247-101-205.eu-west-1.compute.amazonaws.com:5432/d8o6dthnk5anke'

INIT_STATEMENTS = [
    """
        CREATE TABLE IF NOT EXISTS person
            (
                username character varying(20) PRIMARY KEY,
                fullname character varying(50) NOT NULL,
                emailaddress character varying(70) NOT NULL,
                userrole "char" NOT NULL,
                balance numeric(7,2) NOT NULL DEFAULT 0,
                CONSTRAINT person_fkey FOREIGN KEY (username)
                    REFERENCES users (username)
                    ON UPDATE RESTRICT
                    ON DELETE CASCADE
            )
    """,
    """
        CREATE TABLE IF NOT EXISTS users
            (
                username character varying(20) PRIMARY KEY,
                password character varying(50) NOT NULL
            )
    """,
    """
        CREATE TABLE IF NOT EXISTS posts
            (   postid SERIAL PRIMARY KEY,
                poster character varying(20) NOT NULL,
                content character varying(400) NOT NULL,
                date date,
                "time" time without time zone,
                CONSTRAINT posts_fkey FOREIGN KEY (poster)
                    REFERENCES users (username)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            )
    """,
    """
        CREATE TABLE IF NOT EXISTS payments
            (   paymentid SERIAL PRIMARY KEY,
                username character varying(20) NOT NULL,
                amount numeric(7,2) NOT NULL,
                approved char NOT NULL DEFAULT '0',
                approved_by character varying(20),
                CONSTRAINT payments_fkey FOREIGN KEY (username)
                    REFERENCES users (username)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,
                CONSTRAINT payments_fkey2 FOREIGN KEY (approved_by)
                    REFERENCES users (username)
                    ON UPDATE CASCADE
                    ON DELETE NO ACTION
            )
    """,
    """
        INSERT INTO users
        SELECT 'admin', 'admin' WHERE NOT EXISTS(select * from users where username='admin')
    """,
    """
        INSERT INTO person
        SELECT 'admin','Administrator', 'admin@airlinesss.com', 'A' WHERE NOT EXISTS(select * from person where username='admin')
    """,
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
