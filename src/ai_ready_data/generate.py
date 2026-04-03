"""Generate data from sources or distributions"""
from dataclasses import dataclass
from pathlib import Path
import json

import polars as pl


@dataclass
class SeedMeasurements:
    meter_metadata: dict
    values: list[dict]


@dataclass
class MeasurementData:
    metadata: dict
    values: pl.DataFrame


def load_measurement_data(data_path: Path) -> SeedMeasurements:
    with open(data_path) as fp:
        raw = json.load(fp)

    measurement_data = SeedMeasurements(
        meter_metadata=raw['meter'],
        values=raw['values']
    )
    return measurement_data


def transform_measurements(seed_data: SeedMeasurements) -> MeasurementData:
    measurement_data = MeasurementData(
        metadata={'meter': seed_data.meter_metadata},
        values=pl.DataFrame(data=seed_data.values)

    )

    return measurement_data


def obscure_measurement_semantics(df: pl.DataFrame) -> pl.DataFrame:
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

    for col, mapping in hide_value_meaning_map.items():
        df = df.with_columns(pl.col(col).replace(mapping))

    df = df.rename(hide_field_meaning_map)
    return df


def enhance_measurement_semantics(df: pl.DataFrame) -> pl.DataFrame:
    hide_field_meaning_map = {
        'definition_id': 'energy_or_power_type',
        'recorded_at': 'measurement_recorded_at_timestamp',
        "interval_seconds": "measurement_interval_seconds",
        'value': 'value'
    }


    df = df.rename(hide_field_meaning_map)

    map_value_units = {

        "active_energy_produced": "kilowatt-hours (kWh)",
        "active_energy_consumed": "kilowatt-hours (kWh)",
        "reactive_energy_consumed": "kilowatt-hours (kWh)",
        "reactive_energy_produced": "kilowatt-hours (kWh)",
        "active_power_produced": "kilowatt (kW)",
        "active_power_consumed": "kilowatt (kW)",
        "reactive_power_produced": "kilowatt (kW)",
        "reactive_power_consumed": "kilowatt (kW)"
    }

    enhanced_df = df.with_columns(
        pl.col("energy_or_power_type").replace(map_value_units).alias("value_unit")
    )

    return enhanced_df


if __name__ == '__main__':
    import os

    DATA_ROOT = Path(os.environ['DATA_DIR'])
    SEED_DIR = DATA_ROOT / '_seed'

    seed_paths = {
        'measurements': SEED_DIR / 'measurements-2025-09_10_11.json'
    }

    seed_measurement_data = load_measurement_data(data_path=seed_paths['measurements'])
    measurement_data = transform_measurements(seed_data=seed_measurement_data)

    obscured_measurements_df = obscure_measurement_semantics(df=measurement_data.values)
    TARGET_ROOT_1 = DATA_ROOT / 'raw_1'
    TARGET_ROOT_1.mkdir(exist_ok=True, parents=True)
    obscured_measurements_df.write_csv(TARGET_ROOT_1 / 'internal' / 'measurements.csv')

    enhanced_measurements_df = enhance_measurement_semantics(df=measurement_data.values)
    TARGET_ROOT_2 = DATA_ROOT / 'raw_2'
    TARGET_ROOT_2.mkdir(exist_ok=True, parents=True)
    enhanced_measurements_df.write_csv(TARGET_ROOT_2 / 'internal' / 'measurements.csv')


