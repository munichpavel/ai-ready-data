from enum import Enum
from pathlib import Path

import structlog

from pdfminer.high_level import extract_text


log = structlog.get_logger()

class DataManagementMode(Enum):
    basic = 'basic'

DATA_ROOTS = {
    DataManagementMode.basic: Path(__file__).parents[2] / 'data-1'
}
RAW_DATA_DIRS = {mode: path / 'raw' for mode, path in DATA_ROOTS.items()}
TARGET_DIRS = {mode: path / 'parsed' for mode, path in DATA_ROOTS.items()}


RAW_SUBDIR_NAMES = ['internal', 'personally-identifiable', 'public']


def parse(mode: DataManagementMode) -> None:
    log.info(f"Parsing in {mode} mode")
    if mode == DataManagementMode.basic:
        basic_parse()


def basic_parse() -> None:
    TARGET_DIRS[DataManagementMode.basic].mkdir(exist_ok=True, parents=True)
    for subdir_name in RAW_SUBDIR_NAMES:
        subdir = RAW_DATA_DIRS[DataManagementMode.basic] / subdir_name

        for raw_path in subdir.iterdir():
            target_filename = raw_path.stem + '.txt'
            if raw_path.suffix == ".pdf":
                log.info("Plain pdf parsing")
                text = parse_pdf_to_text(source_path=raw_path)

                with open(TARGET_DIRS[DataManagementMode.basic] / target_filename, 'w') as fp:
                    fp.write(text)
            else:
                log.warn(f"Parsing of {raw_path.suffix} not yet supported")


def parse_pdf_to_text(source_path: Path) -> str:
    text = extract_text(source_path)
    return text


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, help="DataManagementMode of parsing")
    args = parser.parse_args()

    mode = DataManagementMode[args.mode]

    parse(mode=mode)
