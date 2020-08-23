class UserModel:
    def __init__(self, telegram_id: int, rating: int, statistic: str) -> None:
        self.user_id = telegram_id
        self.rating = rating
        self.statistic = statistic

    def __repr__(self) -> str:
        return "user_id = {id}, rating = {rating}, stats = {stats}".format(id=self.user_id,
                                                                           rating=self.rating,
                                                                           stats=self.statistic)

    def __str__(self) -> str:
        return "user_id = {id}, rating = {rating}, stats = {stats}".format(id=self.user_id,
                                                                           rating=self.rating,
                                                                           stats=self.statistic)
