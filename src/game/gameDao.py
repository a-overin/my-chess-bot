from .gameSettings import GameStatuses
from datetime import datetime
import os
import psycopg2
import logging


class GameDao:

    def __init__(self) -> None:
        self.sql_edit_game = "update public.game set game_status = %s, start_date = COALESCE(%s, start_date)," \
                             "end_date = COALESCE(%s, end_date) where id = %s"
        self.sql_create_game = "insert into public.game(game_type, game_room_id, game_status) values(%s, %s, %s)" \
                               "returning id"
        self.sql_get_game = "select * from public.game where game_room_id = %s and game_status = %s"
        self.connect = psycopg2.connect(user=os.environ.get("db_login"),
                                        password=os.environ.get("db_password"),
                                        host=os.environ.get("db_host"),
                                        dbname=os.environ.get("db_name"))

    def get_game_for_room(self, room_id: int, game_status: int) -> dict:
        cur = self.connect.cursor()
        try:
            cur.execute(self.sql_get_game, (room_id, game_status))
            data = cur.fetchone()
            if data is not None:
                col_names = [desc[0] for desc in cur.description]
                return {col_names[i]: data[i] for i in range(len(col_names))}
        except psycopg2.Error as e:
            logging.error("error while get game for room={0}".format(room_id), e)
            self.connect.rollback()
            return {}
        finally:
            if cur is not None:
                cur.close()
        return {}

    def create_game_for_room(self, room_id: int, game_type: int) -> int:
        cur = self.connect.cursor()
        game_id = None
        try:
            cur.execute(self.sql_create_game, (game_type, room_id, GameStatuses.created()))
            game_id = cur.fetchone()[0]
            self.connect.commit()
        except psycopg2.Error as e:
            logging.error("error while create game for room={0}".format(room_id), e)
            self.connect.rollback()
        finally:
            if cur is not None:
                cur.close()
        return game_id

    def edit_game(self, game_id: int, game_status: int, start_time: datetime = None, end_time: datetime = None):
        cur = self.connect.cursor()
        try:
            cur.execute(self.sql_edit_game, (game_status, start_time, end_time, game_id))
            self.connect.commit()
        except psycopg2.Error as e:
            logging.error("error while edit game id={0}".format(game_id), e)
            self.connect.rollback()
        finally:
            if cur is not None:
                cur.close()

    def add_user_for_game(self, game_id: int, user_id: int):
        cur = self.connect.cursor()
        try:
            cur.execute(self.sql_create_game, (game_id, user_id))
            self.connect.commit()
        except psycopg2.Error as e:
            logging.error("error while add user={0} for game={1}".format(user_id, game_id), e)
            self.connect.rollback()
        finally:
            if cur is not None:
                cur.close()
