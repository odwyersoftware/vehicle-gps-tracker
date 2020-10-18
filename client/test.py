import os
from http.client import INTERNAL_SERVER_ERROR

from client.main import read_gps_coords, _write, main

SERVER_WRITE_ENDPOINT = os.environ['SERVER_WRITE_ENDPOINT']
MODULE = 'client.main'


def test_read_gps_coords(mocker):
    mock_gps3 = mocker.patch(f'{MODULE}.gps3')
    mock_gps3.GPSDSocket().__iter__.return_value = [mocker.Mock()]
    mock_gps3.DataStream().TPV = {'lat': 123, 'lon': 456}

    records = tuple(read_gps_coords())

    assert records == ((123, 456), )


def test_write(requests_mock):
    requests_mock.post(SERVER_WRITE_ENDPOINT, json={})

    result = _write(lat=123, lon=456)

    assert result is True


def test_write_returns_false_if_server_errors(requests_mock):
    requests_mock.post(
        SERVER_WRITE_ENDPOINT, status_code=INTERNAL_SERVER_ERROR
    )

    result = _write(lat=123, lon=456)

    assert result is False


def test_main(mocker):
    mock_read_gps_coords = mocker.patch(
        f'{MODULE}.read_gps_coords',
        return_value=(
            (111, 222),
            (333, 444),
            (555, 666),
        )
    )
    mock_write = mocker.patch(f'{MODULE}._write', return_value=True)

    main(break_after=2)

    assert mock_write.call_count == 2
    mock_write.call_args_list == [
        mocker.call(lat=111, lon=222),
        mocker.call(lat=333, lon=444),
        mocker.call(lat=555, lon=666),
    ]
    assert mock_read_gps_coords.call_count == 1
