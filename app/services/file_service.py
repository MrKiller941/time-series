import os

from dateutil.parser import parse
from flask import current_app as app


def is_date(string, fuzzy=False):
    """
    Проверяет, можно ли интерпретировать строку как дату

    :param string: str, строка, которую необходимо проверить на дату
    :param fuzzy: bool, игнорировать неизвестные токены в строке, если значение True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True
    except ValueError:
        return False


class FileService:
    @classmethod
    def list_datasets(cls):
        """Для перечисления возможных для анализа датасетов"""
        from swagger_schemas import ANALYZE_DATASET

        datasets_folder = cls.get_folder()
        ANALYZE_DATASET["parameters"][0]["enum"] = os.listdir(datasets_folder)

    @staticmethod
    def get_folder() -> os.path:
        """
        Для создания папки /datasets, если не создана

        :return: путь к папке с датасетами
        """
        datasets_folder = f"{os.path.dirname(os.path.dirname(__file__))}{app.config['FILE_UPLOAD_FOLDER']}"

        if not os.path.exists(datasets_folder):
            os.mkdir(datasets_folder)

        return datasets_folder
