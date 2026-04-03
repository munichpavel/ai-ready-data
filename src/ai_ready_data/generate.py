"""Generate data from sources or distributions"""
from dataclasses import dataclass
from pathlib import Path
import json

from polars import DataFrame


@dataclass
class SeedMeasurements:
    meter_metadata: dict
    values: list[dict]


@dataclass
class MeasurementData:
    metadata: dict
    values: DataFrame


def load_measurement_data(data_path: Path) -> SeedMeasurements:
    with open(data_path) as fp:
        raw = json.load(fp)

    measurement_data = SeedMeasurements(
        meter_metadata=raw['meter'],
        values=raw['values']
    )
    return measurement_data


def transform_measurements(seed_data: SeedMeasurements) -> MeasurementData:
    measurement_df = DataFrame(data=seed_data.values)

    return measurement_df


def obscure_measurement_semantics(df: DataFrame) -> DataFrame:
    hide_field_meaning_map = {
        'definition_id': 'type',
        'recorded_at': 'timestamp',
        "interval_seconds": "interval",
        'value': 'value'
    }

    hide_value_meaning_map = {
        'definition_id': {
            "active_energy_produced": "1",
            "active_energy_consumed": "2",
            "reactive_energy_consumed": "3",
            "reactive_energy_produced": "4",
            "active_power_produced": "10",
            "active_power_consumed": "11",
            "reactive_power_produced": "12",
            "reactive_power_consumed": "13"
        }
    }


def enhance_measurement_semantics(df: DataFrame) -> DataFrame:
    pass


if __name__ == '__main__':
    import os

    DATA_DIR = Path(os.environ['DATA_DIR'])
    SEED_DIR = DATA_DIR / '_seed'

    seed_paths = {
        'measurements': SEED_DIR / 'measurements-2025-09_10_11.json'
    }

    seed_measurement_data = load_measurement_data(data_path=seed_paths['measurements'])
    measurement_data = transform_measurements(seed_data=seed_measurement_data)
    print(measurement_data.head())
