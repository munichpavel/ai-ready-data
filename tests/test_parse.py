from pathlib import Path

from ai_ready_data.parse import parse_pdf_to_text


TEST_DATA_DIR = Path(__file__).parent / 'data'




def test_parse_pdf_to_text():
    source_path = TEST_DATA_DIR / 'basic-doc.pdf'
    expected_keywords = ['Jaz', 'pa', 'pojdem', 'in', 'zasejem', '1']

    res = parse_pdf_to_text(source_path)
    failures = []
    for a_keyword in expected_keywords:
        if a_keyword not in res:
            failures.append(a_keyword)

    assert not failures, 'Parsed text missing kewords ' + ', '.join(failures)
