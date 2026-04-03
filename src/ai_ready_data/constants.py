from enum import Enum
from pathlib import Path


class DataManagementMode(Enum):
    basic = 'basic'
    advanced = 'advanced'


DATA_ROOTS = {
    DataManagementMode.basic: Path(__file__).parents[2] / 'data-1',
    DataManagementMode.advanced: Path(__file__).parents[2] / 'data-2'
}

RAW_DATA_DIRS = {mode: path / 'raw' for mode, path in DATA_ROOTS.items()}
TARGET_DIRS = {mode: path / 'parsed' for mode, path in DATA_ROOTS.items()}