import re
from datetime import datetime, timedelta

from merlion.models.defaults import DefaultDetector, DefaultDetectorConfig, DefaultForecaster, DefaultForecasterConfig
from merlion.utils import TimeSeries
from merlion.transform.resample import TemporalResample
from merlion.transform.normalize import MinMaxNormalize

import pandas as pd
import psycopg2
from exceptions import FileExtensionError, NotTimeSeriesError
from services.file_service import is_date
from werkzeug.datastructures import FileStorage


class GraphicService:
    @classmethod
    def query_graphic(cls, graphic_id: str) -> dict:
        conn = psycopg2.connect(
            host="series", database="diploma", user="diploma", password="diploma"
        )
        cur = conn.cursor()

        select_query = f"""
            SELECT *
            FROM {graphic_id}
            ORDER BY time
        """
        cur.execute(select_query)
        rows = cur.fetchall()
        return rows

    @classmethod
    def get_graphic(cls, graphic_id: str) -> dict:

        rows = GraphicService.query_graphic(graphic_id)

        data = []
        for row in rows:
            time_str = row[0].strftime("%Y-%m-%dT%H:%M:%S")
            values = [{"time": time_str, "value": value} for value in row[1:]]
            data.append({"name": graphic_id, "values": values})

        meta = {}
        response = {
            "analysis_id": graphic_id,
            "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "data": data,
            "meta": meta,
        }
        return response

    @classmethod
    def get_graphic_prediction(cls, graphic_id: str) -> dict:

        rows = GraphicService.query_graphic(graphic_id)
        times = [row[0] for row in rows]
        values = [row[1] for row in rows]

        ts = TimeSeries.from_pd(pd.DataFrame({"time": times, "value": values}))
        resampler = TemporalResample(granularity="1d")
        ts_resampled = resampler(ts)
        normalizer = MinMaxNormalize()
        ts_normalized = normalizer(ts_resampled)
        forecaster = DefaultForecaster(DefaultForecasterConfig())
        forecaster.train(ts_normalized)
        forecast_horizon = 7
        predictions = forecaster.forecast(forecast_horizon)
        predicted_values = normalizer.invert(predictions)
        data = []
        for i in range(forecast_horizon):
            time_str = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%dT%H:%M:%S")
            value = predicted_values[i]
            data.append({"time": time_str, "value": value})

        meta = {}
        response = {
            "analysis_id": "prediction_id",
            "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "data": data,
            "meta": meta,
        }
        return response

    @classmethod
    def get_graphic_anomaly(cls, graphic_id: str) -> dict:

        rows = GraphicService.query_graphic(graphic_id)
        times = [row[0] for row in rows]
        values = [row[1] for row in rows]

        ts = TimeSeries.from_pd(pd.DataFrame({"time": times, "value": values}))
        resampler = TemporalResample(granularity="1d")
        ts_resampled = resampler(ts)

        normalizer = MinMaxNormalize()
        ts_normalized = normalizer(ts_resampled)
        anomaly_detector = DefaultDetector(DefaultDetectorConfig())
        anomaly_detector.train(ts_normalized)
        anomaly_scores = anomaly_detector.detect(ts_normalized)

        data = []
        for i in range(len(times)):
            time_str = times[i].strftime("%Y-%m-%dT%H:%M:%S")
            value = values[i]
            anomaly_score = anomaly_scores[i]
            data.append({"time": time_str, "value": value, "anomaly_score": anomaly_score})

        meta = {}
        response = {
            "analysis_id": "anomaly_detection_id",
            "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "data": data,
            "meta": meta,
        }
        return response

    @classmethod
    def save_file(cls, uploaded_file: FileStorage) -> str:
        """
        Сохранение нового датасета

        :param uploaded_file: загруженный файл
        :return: имя файла в случае успешной загрузки
        """
        if not re.search(r"\.csv$", uploaded_file.filename):
            # если загрузили файл не .csv формата, возвращаем ошибку
            raise FileExtensionError(uploaded_file.filename)

        datasets_folder = cls.get_folder()
        new_df = pd.read_csv(uploaded_file)

        # тк анализируем временные ряды, если в первой колонке НЕ даты - ошибка
        first_column = [str(x) for x in new_df.iloc[:, 0]]
        first_column = list(map(lambda x: is_date(x), first_column))
        if not all(first_column):
            raise NotTimeSeriesError

        conn = psycopg2.connect(
            host="series", database="diploma", user="diploma", password="diploma"
        )
        cur = conn.cursor()

        # Создание таблицы для хранения данных
        table_name = uploaded_file.filename.split(".")[
            0
        ]  # Используем имя файла без расширения
        columns = ", ".join([f"{col} DOUBLE PRECISION" for col in new_df.columns[1:]])
        create_table_query = f"""
                  CREATE TABLE IF NOT EXISTS {table_name} (
                      time TIMESTAMP NOT NULL,
                      {columns},
                      PRIMARY KEY(time)
                  );
              """
        cur.execute(create_table_query)

        # Вставка данных в таблицу
        insert_query = f"""
                  INSERT INTO {table_name} (time, {', '.join(new_df.columns[1:])})
                  VALUES %s
              """
        data = [tuple(row) for _, row in new_df.iterrows()]
        psycopg2.extras.execute_values(cur, insert_query, data)

        # обновление списка доступных датасетов
        cls.list_datasets()

        return uploaded_file.filename
