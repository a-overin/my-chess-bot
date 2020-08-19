import os
import psycopg2
import logging


class UserDao:

    def __init__(self) -> None:
        self.sql_get_user = "select * from public.user where user_id = %(user_id)s"
        self.sql_create_user = "insert into public.user(user_id, rating) values(%(user_id)s, 1500)"
        self.connect = psycopg2.connect(user=os.environ.get("db_login"),
                                        password=os.environ.get("db_password"),
                                        host=os.environ.get("db_host"),
                                        dbname=os.environ.get("db_name"))

    def create_user(self, user_id: int):
        cur = self.connect.cursor()
        try:
            cur.execute(self.sql_create_user, {"user_id": user_id})
            self.connect.commit()
        except psycopg2.Error as e:
            self.connect.rollback()
            logging.error("error while create user", e)
        finally:
            if cur is not None:
                cur.close()

    def get_user(self, user_id: int) -> list:
        cur = self.connect.cursor()
        try:
            cur.execute(self.sql_get_user, {"user_id": user_id})
            data = cur.fetchall()
            if len(data) > 0:
                return data[0]
            else:
                return None
        except psycopg2.Error as e:
            logging.error("error while get user", e)
        finally:
            if cur is not None:
                cur.close()
