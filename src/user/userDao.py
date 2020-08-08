import os
import psycopg2
import logging


class UserDao:

    def __init__(self) -> None:
        self.sql_create_user = ""
        self.connect = psycopg2.connect(user=os.environ.get("db_login"),
                                        password=os.environ.get("db_password"),
                                        host=os.environ.get("db_host"),
                                        dbname=os.environ.get("db_name"))

    def create_user(self, telegram_id: int):
        cur = self.connect.cursor()
        try:
            cur.execute(self.sql_create_user, telegram_id)
            self.connect.commit()
        except psycopg2.Error as e:
            self.connect.rollback()
            logging.error("error while create user", e)
        finally:
            if cur is not None:
                cur.close()
