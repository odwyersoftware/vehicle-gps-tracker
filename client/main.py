import os
import time
import logging

import requests
from requests.exceptions import RequestException
from gps3 import gps3

logger = logging.getLogger('logger')
SERVER_WRITE_ENDPOINT = os.environ['SERVER_WRITE_ENDPOINT']
SLEEP_BETWEEN_GPS_READS = 5


def _configure_logging():
    handler = logging.FileHandler('/tmp/vehicle-tracker.log')
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(handler)
    logging.info('Configured logging')


_configure_logging()


def read_gps_coords():
    gps_socket = gps3.GPSDSocket()
    data_stream = gps3.DataStream()
    gps_socket.connect()
    gps_socket.watch()

    try:
        for new_data in gps_socket:
            if new_data:
                data_stream.unpack(new_data)
                lat = data_stream.TPV['lat']
                lon = data_stream.TPV['lon']
                time.sleep(SLEEP_BETWEEN_GPS_READS)
                yield lat, lon
    except OSError:
        logger.exception('Failed reading coords, retrying...')
        yield from read_gps_coords()


def _write(lat, lon):
    logger.info('Writing coords %s %s', lat, lon)
    resp = requests.post(SERVER_WRITE_ENDPOINT, json={'lat': lat, 'lon': lon})
    try:
        resp.raise_for_status()
    except RequestException:
        logger.exception('Failed to write data to the server')
    return resp.ok


def main(break_after=None):
    num_reads = 0
    for lat, lon in read_gps_coords():
        if break_after and num_reads == break_after:
            break
        _write(lat=lat, lon=lon)
        num_reads += 1


if __name__ == '__main__':
    main()
