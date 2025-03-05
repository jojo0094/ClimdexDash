from __future__ import annotations

import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Optional
from abc import ABC, abstractmethod
import psycopg2
import os
import dotenv

dotenv.load_dotenv() #WARNING: This will load the .env file in the current directory

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB_NAME = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")



def get_psycopg3_connection():
    connection_string = (
        f"host={POSTGRES_HOST} "
        f"port={POSTGRES_PORT} "
        f"dbname={POSTGRES_DB_NAME} "
        f"user={POSTGRES_USER} "
        f"password={POSTGRES_PASSWORD}"
    )
    return connection_string

def fake_timeseries_data() -> pd.DataFrame:
    """using numpy to generate Sine wave data for a year at hourly intervals"""
    time = pd.date_range(start="2022-01-01", end="2022-12-31", freq="h")
    data = np.sin(np.linspace(0, 2 * np.pi, len(time)))
    return pd.DataFrame({"time": time, "total_precipitation": data})


# Abstract Strategy
class DataSource(ABC):
    @abstractmethod
    def get_timeseries(self, lat: float, lon: float) -> pd.DataFrame:
        pass

# Concrete Strategy - CSV File Source
@dataclass
class CSVFileSource(DataSource):
    file_path: str

    def __post_init__(self):
        # self.data = pd.read_csv(self.file_path)
        self.data = fake_timeseries_data()

    def get_timeseries(self, lat: float, lon: float) -> pd.DataFrame:
        # df_filtered = self.data[(self.data["latitude"] == lat) & (self.data["longitude"] == lon)]
        df_filtered = self.data
        return df_filtered.sort_values(by="time")

# Concrete Strategy - Postgres Data Source
@dataclass
class PostgresDataSource(DataSource):
    connection_string: Optional[str] = None

    def __post_init__(self):
        self.connection_string = get_psycopg3_connection()

    def get_timeseries(self, lat: float, lon: float) -> pd.DataFrame:
        query = """
        WITH nearest_location AS (
            SELECT latitude, longitude, location_id
            FROM weather
            ORDER BY (latitude - %s)^2 + (longitude - %s)^2
            LIMIT 1
        )
        SELECT DISTINCT ON (w.time) w.time, w.total_precipitation, w.latitude, w.longitude, w.location_id
        FROM weather w
        JOIN nearest_location nl ON w.location_id = nl.location_id
        ORDER BY w.time;
        """
        
        with psycopg2.connect(self.connection_string) as conn:
            df = pd.read_sql(query, conn, params=(lat, lon))
        return df

# Concrete Strategy - netCDF File Source
@dataclass
class NetCDFFileSource(DataSource):
    file_path: str

    def __post_init__(self):
        self.data = fake_timeseries_data()

    def get_timeseries(self, lat: float, lon: float) -> pd.DataFrame:
        # Read netCDF file and extract data
        return pd.DataFrame()

# Context Class to Use Different Strategies
@dataclass
class TimeSeriesFetcher:
    data_source: DataSource

    def get_data(self, lat: float, lon: float) -> pd.DataFrame:
        return self.data_source.get_timeseries(lat, lon)

# Example Usage
if __name__ == "__main__":
    # CSV Example
    csv_source = CSVFileSource("data.csv")
    fetcher = TimeSeriesFetcher(csv_source)
    print(fetcher.get_data(40.7128, -74.0060))
    
    # Postgres Example
    pg_source = PostgresDataSource("dbname=test user=postgres password=secret host=localhost")
    fetcher = TimeSeriesFetcher(pg_source)
    print(fetcher.get_data(40.7128, -74.0060))

