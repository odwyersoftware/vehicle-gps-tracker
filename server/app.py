import os
from datetime import datetime, timezone
from http.client import BAD_REQUEST
import logging
import sys

from flask import Flask, request, jsonify, render_template
import sqlalchemy
import sqlalchemy_jsonfield
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger(__name__)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
SERVER_READ_ENDPOINT = os.environ['SERVER_READ_ENDPOINT']
db = SQLAlchemy(app)
MAX_RECORDS_RETURN = 500


def _configure_logging():
    handler = logging.StreamHandler(sys.stdout)
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


def _default_created_on():
    return datetime.now(timezone.utc)


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = sqlalchemy.Column(
        sqlalchemy_jsonfield.JSONField(
            enforce_string=True, enforce_unicode=False
        ),
        nullable=False,
    )
    created_on = sqlalchemy.Column(
        sqlalchemy.DateTime, default=_default_created_on
    )

    def __repr__(self):
        return f'<Location {self.data} {self.created_on}>'


@app.route('/')
def index():
    return render_template(
        'index.html', server_read_endpoint=SERVER_READ_ENDPOINT
    )


@app.route('/add_test_data')
def add_test_data():
    recs = [
        ('52.35279', '-1.300848'),
        ('52.352654', '-1.300954'),
        ('52.352821', '-1.30153'),
        ('52.352651', '-1.301685'),
        ('52.352633', '-1.301723'),
        ('52.352652', '-1.301934'),
        ('52.352884', '-1.303106'),
        ('52.352898', '-1.303262'),
        ('52.352782', '-1.303657'),
        ('52.352792', '-1.303865'),
        ('52.352825', '-1.304016'),
        ('52.352777', '-1.304322'),
        ('52.352504', '-1.304951'),
        ('52.352387', '-1.305275'),
        ('52.352294', '-1.305364'),
    ]
    for lat, lon in recs:
        new_record = Location(data={'lat': lat, 'lon': lon})
        db.session.add(new_record)
        db.session.commit()
    return ''


@app.route('/read')
def read():
    logger.info('Reading records...')
    records = tuple(
        {
            'data': r.data,
            'created_on': r.created_on.isoformat()
        } for r in db.session.query(Location).
        order_by(Location.created_on.desc()).all()[:MAX_RECORDS_RETURN]
    )
    return jsonify(records)


@app.route('/write', methods=['POST'])
def write():
    data = request.get_json()
    logger.info('Writing data %s', data)
    if data:
        if data['lat'] == 'n/a' or data['lon'] == 'n/a':
            return jsonify({'detail': 'invalid payload'}), BAD_REQUEST
        new_record = Location(data=data)
        db.session.add(new_record)
        db.session.commit()
        logger.info('New record written')
    return jsonify({})


db.create_all()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
