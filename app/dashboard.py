from flask import Flask, render_template, jsonify, request
from database import get_db_connection
from scraper import get_ai_analysis_for_tool
import os

app = Flask(__name__)

@app.route('/')
def index():
    conn = get_db_connection()
    news = conn.execute('SELECT * FROM news ORDER BY published_date DESC LIMIT 25').fetchall()
    conn.close()
    return render_template('index.html', news=news)

@app.route('/api/data')
def api_data():
    conn = get_db_connection()
    news = [dict(row) for row in conn.execute('SELECT * FROM news ORDER BY published_date DESC LIMIT 25').fetchall()]
    stats = conn.execute('SELECT criticality, COUNT(*) as count FROM news GROUP BY criticality').fetchall()
    conn.close()
    return jsonify({"news": news, "chart": {row['criticality']: row['count'] for row in stats}})

@app.route('/api/tool', methods=['POST'])
def tool_query():
    data = request.json
    result = get_ai_analysis_for_tool(data.get('type'), data.get('value'))
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
