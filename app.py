from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

@app.route('/')
def index():
    return render_template('index.html', batches=[])

@app.route('/process_srt', methods=['POST', 'OPTIONS'])
def process_srt():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        batches = []
        for i in range(0, len(data), 120):
            batches.append(data[i:i + 120])

        return jsonify({'batches': batches}), 200
    except Exception as e:
        app.logger.error(f"Error processing SRT: {str(e)}")
        return jsonify({'error': 'An error occurred while processing the file.'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
