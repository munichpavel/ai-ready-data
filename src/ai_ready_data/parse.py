from pathlib import Path

import structlog

from pdfminer.high_level import extract_text

from .constants import DataManagementMode, RAW_DATA_DIRS, TARGET_DIRS


log = structlog.get_logger()

RAW_SUBDIR_NAMES = ['internal', 'personally-identifiable', 'public']


def parse(mode: DataManagementMode) -> None:
    log.info(f"Parsing in {mode} mode")
    if mode == DataManagementMode.basic:
        basic_parse()


def basic_parse() -> None:
    TARGET_DIRS[DataManagementMode.basic].mkdir(exist_ok=True, parents=True)
    for subdir_name in RAW_SUBDIR_NAMES:
        subdir = RAW_DATA_DIRS[DataManagementMode.basic] / subdir_name

        if not subdir.exists():
            log.warn(f"Subdir {subdir} does not exist, skipping")
            continue
        for raw_path in subdir.iterdir():
            log.info(f"Trying to parse {raw_path}")

            if raw_path.suffix == ".pdf":
                target_filename = raw_path.stem + '.txt'
                log.info("Basic pdf parsing")
                text = parse_pdf_to_text(source_path=raw_path)

                with open(TARGET_DIRS[DataManagementMode.basic] / target_filename, 'w') as fp:
                    fp.write(text)
            elif raw_path.suffix == ".csv" or raw_path.suffix == ".html":
                target_filename = raw_path.stem + raw_path.suffix
                log.info("Basic csv parsing")
                with open(raw_path) as fp:
                    csv_text = fp.read()
                with open(TARGET_DIRS[DataManagementMode.basic] / target_filename, 'w') as fp:
                    fp.write(csv_text)
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
