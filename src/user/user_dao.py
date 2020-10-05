import os
import logging
import psycopg2


class UserDao:

    def __init__(self) -> None:
        self.sql_get_user = "select * from public.user where user_id = %(user_id)s"
        self.sql_create_user = "insert into public.user(user_id, rating) values(%(user_id)s, 1500)"
        self.sql_change_rating = "update public.user set rating = rating + %(diff)s where user_id = %(user_id)s"
        self.connect = psycopg2.connect(user=os.environ.get("db_login"),
                                        password=os.environ.get("db_password"),
                                        host=os.environ.get("db_host"),
                                        dbname=os.environ.get("db_name"))

    def create_user(self, user_id: int):
        cur = self.connect.cursor()
        try:
            cur.execute(self.sql_create_user, {"user_id": user_id})
            self.connect.commit()
        except psycopg2.Error as error:
            self.connect.rollback()
            logging.error(error)
        finally:
            if cur is not None:
                cur.close()

    def change_rating(self, user_id: int, diff: int):
        cur = self.connect.cursor()
        try:
            cur.execute(self.sql_change_rating, {"user_id": user_id, "diff": diff})
            self.connect.commit()
        except psycopg2.Error as error:
            self.connect.rollback()
            logging.error(error)
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
            return []
        except psycopg2.Error as error:
            logging.error(error)
        finally:
            if cur is not None:
                cur.close()
