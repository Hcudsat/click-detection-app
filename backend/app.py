from datetime import datetime
from pathlib import Path
import sqlite3

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_PATH = Path(__file__).with_name("clicks.db")


def _initialize_database() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS click_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                x REAL NOT NULL,
                y REAL NOT NULL,
                client_timestamp REAL NOT NULL,
                server_timestamp TEXT NOT NULL
            )
            """
        )


_initialize_database()


@app.post("/api/click")
def register_click():
    payload = request.get_json(silent=True) or {}
    try:
        x = float(payload["x"])
        y = float(payload["y"])
        client_timestamp = float(payload["t"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Invalid payload. Expected numeric 'x', 'y', and 't' fields."}), 400

    server_timestamp = datetime.utcnow().isoformat(timespec="milliseconds") + "Z"

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            INSERT INTO click_events (x, y, client_timestamp, server_timestamp)
            VALUES (?, ?, ?, ?)
            """,
            (x, y, client_timestamp, server_timestamp),
        )
        count = connection.execute("SELECT COUNT(*) FROM click_events").fetchone()[0]

    return jsonify({"status": "ok", "count": count}), 201


@app.get("/api/stats")
def get_stats():
    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row
        events = connection.execute(
            """
            SELECT x, y, client_timestamp, server_timestamp
            FROM click_events
            ORDER BY id ASC
            """
        ).fetchall()

    return jsonify(
        {
            "count": len(events),
            "clicks": [dict(event) for event in events],
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
