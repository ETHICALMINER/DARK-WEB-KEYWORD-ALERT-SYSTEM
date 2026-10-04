import os
import sqlite3

from flask import Flask, render_template_string

from config import DB_PATH

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Dark Web Monitor</title>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="10">
    <style>
        body { background:#050505; color:#00ff41; font-family:'Courier New',monospace; padding:20px; }
        h1 { border-bottom:2px solid #00ff41; padding-bottom:15px; }
        .stat-panel { background:#111; padding:15px; border:1px solid #333; margin-bottom:20px; }
        table { width:100%; border-collapse:collapse; font-size:0.9em; }
        th { background:#1a1a1a; color:#fff; text-align:left; padding:10px; border:1px solid #333; }
        td { border:1px solid #333; padding:8px; color:#ccc; word-break:break-all; }
        .kw { color:#ff3333; font-weight:bold; }
        .url { color:#0088ff; }
        .source-tag { background:#222; padding:2px 6px; border-radius:4px; font-size:0.8em; color:#aaa; }
    </style>
</head>
<body>
    <h1>DARK WEB INTELLIGENCE FEED</h1>

    <div class="stat-panel">
        <strong>SYSTEM:</strong> OPERATIONAL |
        <strong>TOTAL RECORDS:</strong> {{ total }} |
        <em>URLs are shown as text on purpose. Do not open them outside an isolated environment.</em>
    </div>

    <table>
        <tr>
            <th width="15%">TIMESTAMP</th>
            <th width="15%">KEYWORD</th>
            <th width="40%">URL (.ONION)</th>
            <th width="20%">SNIPPET</th>
            <th width="10%">SOURCE</th>
        </tr>
        {% for row in rows %}
        <tr>
            <td>{{ row[5] }}</td>
            <td class="kw">{{ row[1] }}</td>
            <td class="url">{{ row[2] }}</td>
            <td>{{ row[3] }}</td>
            <td><span class="source-tag">{{ row[4] }}</span></td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""


@app.route("/")
def index():
    if not os.path.exists(DB_PATH):
        return "<h3>Waiting for scanner... run: python3 scanner.py</h3>"

    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT * FROM alerts ORDER BY ts DESC").fetchall()
    conn.close()
    return render_template_string(HTML, rows=rows, total=len(rows))


if __name__ == "__main__":
    # Bound to localhost, debug off, so the dashboard isn't exposed on your network
    app.run(host="127.0.0.1", port=5000, debug=False)