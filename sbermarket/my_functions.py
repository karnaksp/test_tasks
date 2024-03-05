import polars as pl
import pandas as pd
import sys
from collections import Counter
from typing import Tuple


class MarketDataProcessor:
    """_Преобразования тренировочного датасета из задачи recsys в binary_"""

    def __init__(self, train: pd.DataFrame, test: pd.DataFrame, k: int = 25):
        """
        Инициализирует объект с заданными необработанными данными,
        дополнительными данными и необязательным значением k.

        Parameters:
            train (pd.DataFrame): история покупок пользователей в формате
            (user_id `int`| order_completed_at `datetime` |	cart `int`).
            test (pd.DataFrame): пустой сабмит (id `str: user_id;cart`| target `int`).
            k (int, необязательно): значение k для инициализации. По умолчанию 25.

        Returns:
            None
        """
        self.train_data = train
        self.test_data = test
        self.k = k
        self.filtered_train = None
        self.filtered_test = None
        self.proportion = None
        self.ohe_data = None
        self.processed_data = None

    def filter_train_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, float]:
        """
        Фильтрует необработанные данные на основе частоты появления пользо\
        Returns:
            Tuple[pd.DataFrame, pd.DataFrame, float]: Отфильтрованные данные истории покупок по заданному условию k, отфильтрованный датафрейм по test, и процент наблюдений, используемых в итоге для обучения.
        """
        users = map(int, (x.split(";")[0] for x in self.test_data["id"]))
        user_counts = Counter(users)
        frequent_users = {user for user, count in user_counts.items() if count > self.k}
        test_users = {user for user, _ in user_counts.items()}
        self.filtered_train = self.train_data[
            self.train_data["user_id"].isin(frequent_users)
        ]
        self.filtered_test = self.train_data[
            self.train_data["user_id"].isin(test_users)
        ]
        total_count = sum(user_counts.values())
        frequent_count = sum(
            count for user, count in user_counts.items() if user in frequent_users
        )
        self.proportion = frequent_count / total_count

        return self.filtered_train, self.filtered_test, self.proportion

    def get_dummies_matrix(self):
        """
        Вовращает dummies матрицу для категорий(cart). Таким образом для каждой категории, если она была в установленное время в заказе у пользователя, будет 1
        Returns:
            (tpl.DataFrame).
        """
        train_train = pd.get_dummies(self.train_data, columns=["cart"])
        train_train = pl.from_pandas(train_train)
        train_train = train_train.group_by(["user_id", "order_completed_at"]).max()
        self.ohe_data = train_train.sort(["user_id", "order_completed_at"])

    def generate_time_features(self):
        """
        Генерирует временные фичи на основе столбца order_completed_at.
        Returns:
            pl.DataFrame: Обработанный DataFrame для train.
        """

        # Вычисление переменных времени
        self.ohe_data = self.ohe_data.with_columns(
            pl.col("order_completed_at").str.to_datetime()
        )
        self.ohe_data = self.ohe_data.with_columns(
            [
                (pl.col("user_id").cum_count() - pl.lit(1))
                .over(["user_id"])
                .alias("order_number"),
                pl.col("order_completed_at").dt.weekday().alias("weekday"),
                pl.col("order_completed_at").dt.month().alias("month"),
            ]
        )
        self.processed_data = self.ohe_data.drop("order_completed_at")

    def compile_dataset(self, history_flag: int = 0) -> pd.DataFrame:
        """
        Компилирует историю заказов в укомплектованный тренировочный DataFrame "Train".

        Args:
            history_flag (int): Флаг 0 - тренировочный датасет,
                                1 - общий (тестовый) датасет без таргета.

        Returns:
            pd.DataFrame: X + Y for model/ or just X.
        """
        _, _, last_order = self._separate_last_order()

        train_tmp, val_data = self._split_train_and_valid(last_order)

        train_set = self._transform_to_long_format(train_tmp, history_flag)

        order_number_df, dl_tmp = self._calculate_order_and_category_counts(
            train_set, val_data, history_flag
        )

        train_set = self._join_order_and_category_counts(
            train_set, order_number_df, dl_tmp
        )

        train_set = self._calculate_ratings(train_set)

        rating_per_weekday = self._calculate_rating_per_time(train_set, "weekday")
        rating_per_month = self._calculate_rating_per_time(train_set, "month")

        train_set = self._join_rating_per_time(
            train_set,
            rating_per_weekday,
            rating_per_month,
        )

        if not history_flag:
            train_set = self._join_target(train_set, val_data)

        # Преобразование в pandas DataFrame
        train_set = train_set.to_pandas()
        train_set["id"] = train_set["id"].str.replace("cart_", "")
        train_set["category"] = train_set["category"].str.replace("cart_", "")

        return train_set

    def _separate_last_order(self):
        """
        This function separates the last order from the processed data
        and returns grouped, merged, and last_order.
        """
        grouped = self.processed_data.group_by("user_id").agg(
            pl.max("order_number").alias("max_order_number")
        )
        merged = self.processed_data.join(grouped, on="user_id")
        last_order = merged["max_order_number"] == merged["order_number"]
        return grouped, merged, last_order

    def _split_train_and_valid(self, last_order):
        """
        Splits the processed data into training and validation sets based on the last order.

        Parameters:
        - last_order: boolean array indicating whether each record is part of the last order

        Returns:
        - train_tmp: training data excluding the last order
        - val_data: validation data excluding specific time-related columns
        """
        train_tmp = self.processed_data.filter(~last_order)
        val_data = self.processed_data.filter(last_order).drop(
            "hour", "week", "weekday", "day", "month", "year"
        )
        return train_tmp, val_data

    def _transform_to_long_format(self, train_tmp, history_flag):
        """
        Transforms the input data into long format, based on the 'history_flag' parameter.
        Parameters:
            train_tmp: the input data frame
            history_flag: a flag indicating whether to use the 'train_tmp' or 'self.processed_data'
        Returns:
            train_melt: the data frame in long format
        """
        if not history_flag:
            train_melt = train_tmp.drop("order_number").melt(
                id_vars=["user_id", "weekday", "month"],
                variable_name="category",
                value_name="ordered",
            )
        elif history_flag == 1:
            train_melt = self.processed_data.drop("order_number").melt(
                id_vars=["user_id", "weekday", "month"],
                variable_name="category",
                value_name="ordered",
            )
        else:
            print("Invalid history flag. Exiting...")
            sys.exit()
        return train_melt

    def _calculate_order_and_category_counts(self, train_set, val_data, history_flag):
        """
        Calculate order and category counts based on the provided training
        and validation data and a history flag.

        Args:
            train_set: The training dataset.
            val_data: The validation data.
            history_flag: Flag indicating whether to consider historical data.

        Returns:
            order_number_df: DataFrame containing user IDs and order numbers.
            dl_tmp: Aggregated DataFrame with category and ordered item counts.
        """
        order_number_df = val_data.select(["user_id", "order_number"]).unique()
        dl_tmp = train_set.group_by("category").agg(pl.col(["ordered"]).sum())
        if history_flag == 1:
            order_number_df = order_number_df.with_columns(pl.col("order_number") + 1)
            dl_tmp = train_set.group_by("category").agg(pl.col(["ordered"]).sum() + 1)
        return order_number_df, dl_tmp

    def _join_order_and_category_counts(self, train_set, order_number_df, dl_tmp):
        """
        Joins order and category counts to the train_set and returns the updated train_set.

        Parameters:
        - train_set: The original train set dataframe.
        - order_number_df: The dataframe containing order number information.
        - dl_tmp: The temporary dataframe used for joining category information.

        Returns:
        - train_set: The updated train set dataframe.
        - unique_users_count: unique users count
        """
        train_set = train_set.join(order_number_df, on="user_id").rename(
            {"order_number": "total_order_num"}
        )
        train_set = train_set.join(dl_tmp, on="category").rename(
            {"ordered_right": "total_order_in_cat"}
        )
        return train_set

    def _calculate_ratings(self, train_set):
        """
        Calculate the rating statistics for the train set and return the modified train set.
        """
        unique_users_count = train_set.select("user_id").n_unique()
        unique_cat_count = train_set.select("category").n_unique()
        train_set = train_set.with_columns(
            [
                (pl.col("ordered") / pl.col("total_order_num")).alias("rating"),
                (
                    pl.col("total_order_num")
                    * (pl.col("total_order_in_cat") / unique_users_count)
                ).alias("total_rating"),
                (
                    pl.col("total_order_num")
                    * (pl.col("total_order_in_cat") / unique_cat_count)
                ).alias("total_rating_cat"),
                (pl.col("user_id").cast(pl.Utf8) + ";" + pl.col("category")).alias(
                    "id"
                ),
            ]
        )
        train_set = train_set.group_by("user_id", "category", "id").agg(
            pl.col(["weekday"]).mean().name.suffix("_mean"),
            pl.col(["weekday"]).max().name.suffix("_max"),
            pl.col(["weekday"]).min().name.suffix("_min"),
            pl.col(["weekday"]).std().name.suffix("_std"),
            pl.col(["month"]).mean().name.suffix("_mean"),
            pl.col(["month"]).max().name.suffix("_max"),
            pl.col(["month"]).min().name.suffix("_min"),
            pl.col(["month"]).std().name.suffix("_std"),
            pl.col(["total_rating"]).mean().name.suffix("_mean"),
            pl.col(["total_rating"]).max().name.suffix("_max"),
            pl.col(["total_rating"]).min().name.suffix("_min"),
            pl.col(["total_rating"]).std().name.suffix("_std"),
            pl.col(["rating"]).mean().name.suffix("_mean"),
            pl.col(["rating"]).max().name.suffix("_max"),
            pl.col(["rating"]).min().name.suffix("_min"),
            pl.col(["rating"]).std().name.suffix("_std"),
            pl.col(["total_rating_cat"]).mean().name.suffix("_mean"),
            pl.col(["total_rating_cat"]).max().name.suffix("_max"),
            pl.col(["total_rating_cat"]).min().name.suffix("_min"),
            pl.col(["total_rating_cat"]).std().name.suffix("_std"),
            pl.col(["ordered"]).mean().name.suffix("_mean"),
            pl.col(["ordered"]).max().name.suffix("_max"),
            pl.col(["ordered"]).min().name.suffix("_min"),
            pl.col(["ordered"]).std().name.suffix("_std"),
            pl.col(["total_order_in_cat"]).mean().name.suffix("_mean"),
            pl.col(["total_order_in_cat"]).max().name.suffix("_max"),
            pl.col(["total_order_in_cat"]).min().name.suffix("_min"),
            pl.col(["total_order_in_cat"]).std().name.suffix("_std"),
            pl.col(["total_order_num"]).mean().name.suffix("_mean"),
            pl.col(["total_order_num"]).max().name.suffix("_max"),
            pl.col(["total_order_num"]).min().name.suffix("_min"),
            pl.col(["total_order_num"]).std().name.suffix("_std"),
        )
        return train_set

    def _calculate_rating_per_time(self, train_set, time_column):
        """
        Calculate rating per time for the given train set and time column.

        Parameters:
            train_set (DataFrame): The input train set data.
            time_column (str): The name of the time column.

        Returns:
            DataFrame: The calculated rating per time.
        """
        rating_per_time = train_set.group_by([f"{time_column}_mean", "user_id"]).agg(
            ((pl.col("total_rating_mean").mean()) * 100).alias(
                f"t_rating_per_{time_column}_mean"
            ),
            ((pl.col("total_rating_mean").std()) * 100).alias(
                f"t_rating_per_{time_column}_std"
            ),
            ((pl.col("total_rating_mean").sum())).alias(
                f"t_rating_per_{time_column}_sum"
            ),
            ((pl.col("total_rating_mean").median()) * 100).alias(
                f"t_rating_per_{time_column}_median"
            ),
            ((pl.col("rating_mean").mean()) * 100).alias(
                f"rating_per_{time_column}_mean"
            ),
            ((pl.col("rating_mean").std()) * 100).alias(
                f"rating_per_{time_column}_std"
            ),
            ((pl.col("rating_mean").sum())).alias(f"rating_per_{time_column}_sum"),
            ((pl.col("rating_mean").median()) * 100).alias(
                f"rating_per_{time_column}_median"
            ),
            ((pl.col("total_rating_cat_mean").mean()) * 100).alias(
                f"tc_rating_per_{time_column}_mean"
            ),
            ((pl.col("total_rating_cat_mean").std()) * 100).alias(
                f"tc_rating_per_{time_column}_std"
            ),
            ((pl.col("total_rating_cat_mean").sum())).alias(
                f"tc_rating_per_{time_column}_sum"
            ),
            ((pl.col("total_rating_cat_mean").median()) * 100).alias(
                f"tc_rating_per_{time_column}_median"
            ),
        )
        return rating_per_time

    def _join_rating_per_time(
        self,
        train_set,
        rating_per_weekday,
        rating_per_month,
    ):
        """
        Joins rating data per time period to the given train_set dataframe using the
        provided rating data per hour, per weekday, per day, and per month.

        Args:
            train_set: The input train_set dataframe to which the rating data will be joined.
            rating_per_weekday: The dataframe containing rating data per weekday.
            rating_per_month: The dataframe containing rating data per month.

        Returns:
            The train_set dataframe with rating data joined for each time period.
        """
        train_set = train_set.join(rating_per_month, on=["month_mean", "user_id"])
        train_set = train_set.join(
            rating_per_weekday,
            on=["weekday_mean", "user_id"],
        )
        return train_set

    def _join_target(self, train_set, val_data):
        """
        Joins the target data from the validation set to the training
        set based on user_id and category.
        Parameters:
            train_set: The training set DataFrame.
            val_data: The validation set DataFrame.
        Return:
            The updated training set DataFrame with the target data joined.
        """
        valid_melt = val_data.drop(
            "order_number",
        ).melt(
            id_vars=[
                "user_id",
            ],
            variable_name="category",
            value_name="target",
        )
        train_set = train_set.join(valid_melt, on=["user_id", "category"])
        return train_set


## Рейтинг товара для юзера должен считаться как количество этого товара
# в корзине пользователя за всю историю,
# умноженное на (количество этого товара, заказанное всеми пользователями за всю историю,
# деленное на количество пользователей)
## А если это за время t? Тогда то же самое, только агреггированное по t.
