def filter_raw_data(
    raw: pd.DataFrame, sub: pd.DataFrame, k: int = 25
) -> Tuple[pd.DataFrame, pd.DataFrame, float]:
    """
    Фильтрует необработанные данные на основе частоты появления пользователей в подмножестве.

    Args:
        raw (pd.DataFrame): Raw DataFrame содержит историю покупок пользователей.
        sub (pd.DataFrame): Submission DataFrame содержит последовательность сочетаний юзер-категория, которые нужно предсказать.
        k (int): порог количества товаров у пользователя в корзине, выше которого берем пользователя в обучение.
    Returns:
        Tuple[pd.DataFrame, pd.DataFrame, float]: Отфильтрованные данные истории покупок по заданному условию k, отфильтрованный датафрейм по sub, и процент наблюдений, используемых в итоге для обучения.
    """
    users = map(int, (x.split(";")[0] for x in sub["id"]))
    user_counts = Counter(users)
    frequent_users = {user for user, count in user_counts.items() if count > k}
    sub_users = {user for user, count in user_counts.items()}
    filtered_raw = raw[raw["user_id"].isin(frequent_users)]
    filtered_sub = raw[raw["user_id"].isin(sub_users)]
    total_count = sum(user_counts.values())
    frequent_count = sum(
        count for user, count in user_counts.items() if user in frequent_users
    )
    proportion = frequent_count / total_count

    return filtered_raw, filtered_sub, proportion


def ohe_data(raw: pd.DataFrame) -> pl.DataFrame:
    """
    Вовращает ohe матрицу для категорий.

    Args:
        raw (pd.DataFrame): Pandas DataFrame.

    Returns:
        (tpl.DataFrame).
    """

    # OHE 'cart', группировка по юзеру и дате заказа по максимальным значениям
    # Таким образом для каждой категории, если она была в этот день в заказе у пользователя, будет 1
    train_raw = pd.get_dummies(raw, columns=["cart"])
    train_raw = pl.from_pandas(train_raw)
    train_raw = train_raw.group_by(["user_id", "order_completed_at"]).max()
    train_raw = train_raw.sort(["user_id", "order_completed_at"])

    return train_raw


def full_history(train_raw: pl.DataFrame) -> pl.DataFrame:
    """
    Обрабатывает датафрейм polars и возвращает весь датасет.

    Args:
        raw (pl.DataFrame): Polars DataFrame для обработки.

    Returns:
        pl.DataFrame: Обработанный DataFrame для train.
    """

    # Вычисление переменных времени
    train_raw = train_raw.with_columns(pl.col("order_completed_at").str.to_datetime())
    train_raw = train_raw.with_columns(
        [
            (pl.col("user_id").cum_count() - pl.lit(1))
            .over(["user_id"])
            .alias("order_number"),
            pl.col("order_completed_at").dt.hour().alias("hour"),
            pl.col("order_completed_at").dt.week().alias("week"),
            pl.col("order_completed_at").dt.weekday().alias("weekday"),
            pl.col("order_completed_at").dt.day().alias("day"),
            pl.col("order_completed_at").dt.month().alias("month"),
            pl.col("order_completed_at").dt.year().alias("year"),
        ]
    )
    train_raw = train_raw.drop("order_completed_at")

    return train_raw


def create_dataset(train_data: pl.DataFrame, history_flag: int = 0) -> pd.DataFrame:
    """
    Компилирует историю заказов (train_data) в укомплектованный тренировочный pd.Dataframe "Train".

    Args:
        train_data (pl.DataFrame): история заказов (корзина на каждого юзера).
        history_flag (int): флаг 0 - Тренировочный датасет, 1 - общий (тестовый) датасет без таргета.

    Returns:
        pd.DataFrame: X + Y for model/ or just X.
    """
    # Сепарация последнего заказа из истории заказов
    grouped = train_data.group_by("user_id").agg(
        pl.max("order_number").alias("max_order_number")
    )
    merged = train_data.join(grouped, on="user_id")
    last_order = merged["max_order_number"] == merged["order_number"]

    # Разделение на train_data (заказы, кроме последнего) и valid_data (последний заказ) .group_by('user_id').sum()
    train_tmp = train_data.filter(~last_order)
    val_data = train_data.filter(last_order).drop(
        "hour", "week", "weekday", "day", "month", "year"
    )
    # Преобразование в длинный формат юзера и категории товара
    if not history_flag:
        train_melt = train_tmp.drop("order_number").melt(
            id_vars=["user_id", "hour", "week", "weekday", "day", "month", "year"],
            variable_name="category",
            value_name="ordered",
        )
    elif history_flag == 1:
        train_melt = train_data.drop("order_number").melt(
            id_vars=["user_id", "hour", "week", "weekday", "day", "month", "year"],
            variable_name="category",
            value_name="ordered",
        )
    else:
        print("Invalid history flag. Exiting...")
        exit()
    # Тренировочный датасет
    Train = train_melt

    order_number_df = val_data.select(
        ["user_id", "order_number"]
    ).unique()  # Количество заказов у юзера
    dl_tmp = Train.group_by("category").agg(
        pl.col(["ordered"]).sum()
    )  # Количество заказов по категории
    if history_flag == 1:
        order_number_df = order_number_df.with_columns(pl.col("order_number") + 1)
        dl_tmp = Train.group_by("category").agg(pl.col(["ordered"]).sum() + 1)
    Train = Train.join(order_number_df, on="user_id").rename(
        {"order_number": "total_order_num"}
    )
    Train = Train.join(dl_tmp, on="category").rename(
        {"ordered_right": "total_order_in_cat"}
    )
    # Вычисление рейтинга для каждой записи !!?? Как еще можно рассчитывать рейтинг
    Train = Train.with_columns(
        [
            (pl.col("ordered") / pl.col("total_order_num")).alias("total_rating"),
            (pl.col("user_id").cast(pl.Utf8) + ";" + pl.col("category")).alias("id"),
        ]
    )
    Train = Train.group_by("user_id", "category", "id").agg(
        pl.col(["hour"]).mean().name.suffix("_mean"),
        pl.col(["hour"]).max().name.suffix("_max"),
        pl.col(["hour"]).min().name.suffix("_min"),
        pl.col(["hour"]).std().name.suffix("_std"),
        pl.col(["week"]).mean().name.suffix("_mean"),
        pl.col(["week"]).max().name.suffix("_max"),
        pl.col(["week"]).min().name.suffix("_min"),
        pl.col(["week"]).std().name.suffix("_std"),
        pl.col(["weekday"]).mean().name.suffix("_mean"),
        pl.col(["weekday"]).max().name.suffix("_max"),
        pl.col(["weekday"]).min().name.suffix("_min"),
        pl.col(["weekday"]).std().name.suffix("_std"),
        pl.col(["day"]).mean().name.suffix("_mean"),
        pl.col(["day"]).max().name.suffix("_max"),
        pl.col(["day"]).min().name.suffix("_min"),
        pl.col(["day"]).std().name.suffix("_std"),
        pl.col(["month"]).mean().name.suffix("_mean"),
        pl.col(["month"]).max().name.suffix("_max"),
        pl.col(["month"]).min().name.suffix("_min"),
        pl.col(["month"]).std().name.suffix("_std"),
        pl.col(["year"]).mean().name.suffix("_mean"),
        pl.col(["year"]).max().name.suffix("_max"),
        pl.col(["year"]).min().name.suffix("_min"),
        pl.col(["year"]).std().name.suffix("_std"),
        pl.col(["total_rating"]).mean().name.suffix("_mean"),
        pl.col(["total_rating"]).max().name.suffix("_max"),
        pl.col(["total_rating"]).min().name.suffix("_min"),
        pl.col(["total_rating"]).std().name.suffix("_std"),
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
    # Вычисление рейтинга по времени
    rating_per_hour = Train.group_by(
        ["year_mean", "month_mean", "hour_mean", "user_id"]
    ).agg(
        ((pl.col("total_rating_mean").mean()) * 100).alias("rating_per_hour_mean"),
        ((pl.col("total_rating_mean").std()) * 100).alias("rating_per_hour_std"),
        ((pl.col("total_rating_mean").sum())).alias("rating_per_hour_sum"),
        ((pl.col("total_rating_mean").median()) * 100).alias("rating_per_hour_median"),
    )

    rating_per_weekday = Train.group_by(
        ["year_mean", "month_mean", "weekday_mean", "user_id"]
    ).agg(
        ((pl.col("total_rating_mean").mean()) * 100).alias("rating_per_w_mean"),
        ((pl.col("total_rating_mean").std()) * 100).alias("rating_per_w_std"),
        ((pl.col("total_rating_mean").sum())).alias("rating_per_w_sum"),
        ((pl.col("total_rating_mean").median()) * 100).alias("rating_per_w_median"),
    )
    rating_per_day = Train.group_by(
        ["year_mean", "month_mean", "day_mean", "user_id"]
    ).agg(
        ((pl.col("total_rating_mean").mean()) * 100).alias("rating_per_d_mean"),
        ((pl.col("total_rating_mean").std()) * 100).alias("rating_per_d_std"),
        ((pl.col("total_rating_mean").sum())).alias("rating_per_d_sum"),
        ((pl.col("total_rating_mean").median()) * 100).alias("rating_per_d_median"),
    )

    rating_per_month = Train.group_by(["year_mean", "month_mean", "user_id"]).agg(
        ((pl.col("total_rating_mean").mean()) * 100).alias("rating_per_m_mean"),
        ((pl.col("total_rating_mean").std()) * 100).alias("rating_per_m_std"),
        ((pl.col("total_rating_mean").sum())).alias("rating_per_m_sum"),
        ((pl.col("total_rating_mean").median()) * 100).alias("rating_per_m_median"),
    )

    Train = Train.join(rating_per_month, on=["year_mean", "month_mean", "user_id"])
    Train = Train.join(
        rating_per_weekday, on=["year_mean", "month_mean", "weekday_mean", "user_id"]
    )
    Train = Train.join(
        rating_per_day, on=["year_mean", "month_mean", "day_mean", "user_id"]
    )
    Train = Train.join(
        rating_per_hour, on=["year_mean", "month_mean", "hour_mean", "user_id"]
    )

    if not history_flag:
        # Присоединение целевой переменной из valid_melt к Train
        valid_melt = val_data.drop(
            "order_number",
        ).melt(
            id_vars=[
                "user_id",
            ],
            variable_name="category",
            value_name="target",
        )
        Train = Train.join(valid_melt, on=["user_id", "category"])
    #     Train = Train.drop('user_id', 'category')

    # Преобразование в pandas DataFrame
    Train = Train.to_pandas()
    Train["id"] = Train["id"].str.replace("cart_", "")
    Train["category"] = Train["category"].str.replace("cart_", "")

    return Train
