from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/runcode', methods=['POST'])
def run_code():
    code = request.json['code']
    try:
        output = str(eval(code))
        return jsonify({'output': output})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
