from stoplight import main as stoplight
import json


def test_parse_config_opens_expected_file(mocker):
    mock_open = mocker.mock_open(read_data=json.dumps({}))
    mocker.patch('builtins.open', mock_open)
    stoplight.parse_config()
    mock_open.assert_called_once_with('config.json')


def test_generate_headers_contains_expected_keys():
    headers = stoplight.generate_headers('', '')
    assert 'Authorization' in headers
    assert 'Accept' in headers
