from typing import Optional, Dict
import pandas as pd
from pathlib import Path
import numpy as np
from abc import ABC, abstractmethod
from chalicelib.data_schemas import DailySleep, DailyWeight, DailyActivity, HourlyActivity
from datetime import datetime


class DataError(Exception):
    pass


class DataInterface(ABC):

    _data_types = ("dailySleep", "dailyWeight", "dailyActivity", "hourlyActivity")

    _schema_mapping = {
        "dailySleep": DailySleep,
        "dailyWeight": DailyWeight,
        "dailyActivity": DailyActivity,
        "hourlyActivity": HourlyActivity
    }

    def validate_request(self, table: str):
        if table not in self._data_types:
            raise DataError("Incorrect table defined")

    @abstractmethod
    def get_k_last(self, table: str, user: str, k: int, exclude_pred: bool = False):
        raise NotImplementedError()

    @abstractmethod
    def get_after(self, table: str, user: str, time: datetime):
        raise NotImplementedError()


class CSVData(DataInterface):

    def __init__(self, csv_folder: str):
        csv_files = list(Path(csv_folder).rglob("*.csv"))
        _data = {k.parts[-1].replace(".csv", ""): pd.read_csv(k) for k in csv_files}
        self._data: Dict[str, pd.DataFrame] = {}
        for dd in self._data_types:
            for key, value in _data.items():
                if dd in key:
                    self._data.update({dd: value})
                    break
        self._convert_to_datetime()
        self.all_users = self.get_all_users()

    def _convert_to_datetime(self):
        for key, data in self._data.items():
            column_names = data.columns
            if "datetime" not in column_names:
                date_col = next(k for k in data.columns if k.endswith("Date") or k.endswith("Hour"))
                data.rename(columns={date_col: "datetime"}, inplace=True)
            data["datetime"] = pd.to_datetime(data["datetime"], infer_datetime_format=True)
            data["datetime"] = data["datetime"].values.astype(np.datetime64)
            data.sort_values(by='datetime', inplace=True)

    def get_k_last(self, table: str, user: str, k: int, exclude_pred: bool = False):
        tab: pd.DataFrame = self._data[table]
        dd = tab.query(f"Id == {user}")
        if exclude_pred:
            columns = [k for k in dd.columns if not any(u in k for u in ("mean", "upper", "lower"))]
            dd = dd.dropna(subset=columns)
        if k > 0:
            dd = dd.tail(k)
        schema = self._schema_mapping[table]
        dd_dict = [schema(**v) for k, v in dd.iterrows()]
        return dd_dict

    def get_after(self, table: str, user: str, time: datetime, end_time: datetime = None):
        if end_time is None:
            end_time = datetime.utcnow()
        tab: pd.DataFrame = self._data[table]
        dd = tab.query(f"Id == {user}")
        dd = dd[time <= dd.datetime <= end_time]
        schema = self._schema_mapping[table]
        dd_dict = [schema(**v) for k, v in dd.iterrows()]
        return dd_dict

    def get_all_users(self, table: Optional[str] = None):
        if table is None:
            users = []
            for k, v in self._data.items():
                users.extend(v['Id'].values.tolist())
            users = [str(k) for k in users]
            return list(set(users))
        users = [str(k) for k in self._data[table]['Id'].values.tolist()]
        return list(set(users))

    def get_latest_prediction(self, user: str, table: str):
        tab: pd.DataFrame = self._data[table]
        dd = tab.query(f"Id == {user} & has_prediction == 1 & has_values == 0")
        schema = self._schema_mapping[table]
        dd_dict = [schema(**v) for k, v in dd.iterrows()]
        return dd_dict

    def get_variable_names(self, table: str):
        tab: pd.DataFrame = self._data[table]
        cols = tab.columns
        return [k for k in cols if not any(u in k for u in ('mean', 'upper', 'lower', 'Id', 'datetime', 'has_value', 'has_prediction'))]



if __name__ == '__main__':
    interface = CSVData("prediction_test")
    user = "8053475328"
    table = "hourlyActivity"
    print(interface.get_k_last(table, user, 24))




