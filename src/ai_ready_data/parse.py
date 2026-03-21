from enum import Enum
from pathlib import Path

import structlog

from pdfminer.high_level import extract_text


log = structlog.get_logger()

DATA_ROOT = Path(__file__).parents[2] / 'data'
RAW_DATA_ROOT = DATA_ROOT / 'raw'
TARGET_DIR = DATA_ROOT / 'parsed' / 'plain'


RAW_SUBDIR_NAMES = ['internal', 'personally-identifiable', 'public']


class Mode(Enum):
    plain = 'plain'


def parse(mode: Mode) -> None:
    log.info(f"Parsing in {mode} mode")
    if mode == Mode.plain:
        plain_parse()


def plain_parse() -> None:
    TARGET_DIR.mkdir(exist_ok=True, parents=True)
    for subdir_name in RAW_SUBDIR_NAMES:
        subdir = RAW_DATA_ROOT / subdir_name

        for raw_path in subdir.iterdir():
            target_filename = raw_path.stem + '.txt'
            if raw_path.suffix == ".pdf":
                log.info("Plain pdf parsing")
                text = parse_pdf_to_text(source_path=raw_path)

                with open(TARGET_DIR / target_filename, 'w') as fp:
                    fp.write(text)
            else:
                log.warn(f"Parsing of {raw_path.suffix} not yet supported")


def parse_pdf_to_text(source_path: Path) -> str:
    text = extract_text(source_path)
    return text


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, help="Mode of parsing")
    args = parser.parse_args()

    mode = Mode[args.mode]

    parse(mode=mode)
