# server

The server recieves data from the Vehicle tracking device.

It also provides a web interface to view that live data on.

## Installation


```bash
pip install -r requirements-dev.txt
```

## Running

```bash
make start-deps
export DATABASE_URL=postgresql://user:pass@localhost:5432/tracker-web-db
export SERVER_READ_ENDPOINT=http://161.35.32.54:8080/read
sh run.sh
```

Then visit http://localhost:8080/
