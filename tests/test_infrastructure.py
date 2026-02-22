from chatapp.infrastructure.filename_utils import normalize_filename


def test_normalize_filename_decodes_and_strips_path():
    assert normalize_filename("nested%2Ff%20ile.txt") == "f ile.txt"
