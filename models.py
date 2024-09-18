import json
import sqlite3

from DTO import DTOCurrencyPOST


class Currencies:
    def __init__(self, db_name: str):
        self.db_name = db_name

    def get_one_data(self, code: str):
        with sqlite3.connect(self.db_name) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(f'SELECT * FROM Currencies WHERE Code = "{code}"')
            results = cursor.fetchone()
            return dict(results)

    def get_all_data(self):
        with sqlite3.connect(self.db_name) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(f'SELECT * FROM Currencies')
            results = cursor.fetchall()
            results = list(map(lambda x: dict(x), results))
            return results

    def add_one_data(self, dto: DTOCurrencyPOST):
        with sqlite3.connect(self.db_name) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(f'INSERT INTO Currencies (FullName, Code, Sign) VALUES (?, ?, ?)',
                           (dto.name, dto.code, dto.sign))


class ExchangeRates:
    def __init__(self, db_name: str):
        self.db_name = db_name

    def get_all_data(self) -> list:
        with sqlite3.connect(self.db_name) as connection:
            # connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("""SELECT ex.ID,
                                    ex.Rate,
                                    crs.ID,
                                    crs.Code,
                                    crs.FullName,
                                    crs.Sign,
                                    cr.ID,
                                    cr.Code,
                                    cr.FullName,
                                    cr.Sign
                                FROM ExchangeRates ex
                                JOIN Currencies crs
                                ON crs.id = ex.BaseCurrencyId
                                JOIN Currencies cr
                                ON cr.id = ex.TargetCurrencyId""")
            results = cursor.fetchall()
            return results

    def get_one_data(self, base_currency, target_currency):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            sql = """SELECT ex.ID,
                                    ex.Rate,
                                    crs.ID,
                                    crs.Code,
                                    crs.FullName,
                                    crs.Sign,
                                    cr.ID,
                                    cr.Code,
                                    cr.FullName,
                                    cr.Sign
                                FROM ExchangeRates ex
                                JOIN Currencies crs
                                ON crs.id = ex.BaseCurrencyId
                                JOIN Currencies cr
                                ON cr.id = ex.TargetCurrencyId
                                WHERE crs.Code =:base_curr AND cr.Code =:targ_curr"""
            cursor.execute(sql, {'base_curr': base_currency, 'targ_curr': target_currency})
            results = cursor.fetchone()
            return results
