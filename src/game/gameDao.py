from ..exceptions import GameSavePositionException
from .gameSettings import GameStatuses
from datetime import datetime as dt
import os
import psycopg2
import logging


class GameDao:

    def __init__(self) -> None:
        self.sql_save_table_positions = "insert into public.game_history(game_id, turn_number, user_id, table_position, turn_time)" \
                                        "values(%s, %s, %s, %s, %s)"
        self.sql_get_table_positions = """select g.id
                                               , coalesce(gh.table_position, gt.table_start_position) table_position
                                               , coalesce(gu.user_id, gud.user_id) user_id
                                               , coalesce(gu.user_color, gud.user_color) user_color
                                               , coalesce(gh.turn_number, 0) turn_number
                                            from public.game g
                                            join public.game_type gt on g.game_type = gt.id
                                            left join public.game_user gud on gud.game_id = g.id and gud.user_color is true
                                            left join public.game_history gh on gh.game_id = g.id
                                            left join public.game_user gu on gu.game_id = gh.game_id and gu.user_id != gh.user_id
                                           where g.id = %s
                                           order by turn_time desc
                                           limit 1"""
        self.sql_add_user = "insert into public.game_user values(%s, %s, %s)"
        self.sql_get_users = "select user_id, user_color from public.game_user where game_id = %s"
        self.sql_edit_game = "update public.game set game_status = %s, start_date = COALESCE(%s, start_date)," \
                             "end_date = COALESCE(%s, end_date) where id = %s"
        self.sql_create_game = "insert into public.game(game_type, game_room_id, game_status) values(%s, %s, %s)" \
                               "returning id"
        self.sql_get_game = "select * from public.game where game_room_id = %s and game_status in (0, 5)"
        self.connect = psycopg2.connect(user=os.environ.get("db_login"),
                                        password=os.environ.get("db_password"),
                                        host=os.environ.get("db_host"),
                                        dbname=os.environ.get("db_name"))

    def get_game_for_room(self, room_id: int) -> dict:
        cur = self.connect.cursor()
        logging.info("try get game for room id=" + str(room_id))
        try:
            cur.execute(self.sql_get_game, (room_id, ))
            data = cur.fetchone()
            logging.debug("found game=" + str(data))
            if data is not None:
                col_names = [desc[0] for desc in cur.description]
                return {col_names[i]: data[i] for i in range(len(col_names))}
            else:
                logging.info("no found game for room id=" + str(room_id))
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

    def edit_game(self, game_id: int, game_status: int, start_time: dt = None, end_time: dt = None):
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

    def add_user_for_game(self, game_id: int, user_id: int, user_color: bool):
        cur = self.connect.cursor()
        try:
            cur.execute(self.sql_add_user, (game_id, user_id, user_color == 1))
            self.connect.commit()
        except psycopg2.Error as e:
            logging.error("error while add user={0} for game={1}".format(user_id, game_id), e)
            self.connect.rollback()
        finally:
            if cur is not None:
                cur.close()

    def get_game_users(self, game_id: int) -> list:
        cur = self.connect.cursor()
        try:
            cur.execute(self.sql_get_users, (game_id,))
            data = cur.fetchall()
            if data is not None:
                col_names = [desc[0] for desc in cur.description]
                return [{col_names[col]: user[col] for col in range(len(col_names))} for user in data]
            else:
                return []
        except psycopg2.Error as e:
            logging.error("error while get game={} users".format(game_id), e)
            self.connect.rollback()
            return []
        finally:
            if cur is not None:
                cur.close()

    def get_table_positions(self, game_id: int) -> {}:
        cur = self.connect.cursor()
        try:
            cur.execute(self.sql_get_table_positions, (game_id,))
            data = cur.fetchone()
            if data is not None:
                col_names = [desc[0] for desc in cur.description]
                return {col_names[col]: data[col] for col in range(len(col_names))}
            else:
                return {}
        except psycopg2.Error as error:
            logging.error("error while get game={} users".format(game_id), error)
            self.connect.rollback()
            return {}
        finally:
            if cur is not None:
                cur.close()

    def save_table_positions(self, game_id: int, turn_number: int, user_id: int, pos: str):
        cur = self.connect.cursor()
        try:
            cur.execute(self.sql_save_table_positions, (game_id, turn_number, user_id, pos, dt.now()))
            self.connect.commit()
        except psycopg2.Error as error:
            self.connect.rollback()
            logging.error(error)
            raise GameSavePositionException()

