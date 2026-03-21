from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# 1. Load the "Brain" (The O*NET + Mistral Cache)
CACHE_PATH = os.path.join('.', 'd1.json')

def load_cache():
    with open(CACHE_PATH, 'r') as f:
        return json.load(f)

# 2. Serve the Frontend
@app.route('/')
def index():
    return render_template('index.html')

# 3. The "Inference" API Endpoint
@app.route('/analyze', methods=['POST'])
def analyze():
    # In the demo, the user "uploads" a file
    # We grab the filename (which should be the ID, e.g., 16852973.pdf)
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    # Extract the ID from the filename (e.g., "16852973.pdf" -> "16852973")
    res_id = os.path.splitext(file.filename)[0]
    
    cache = load_cache()
    # print(cache)
    if res_id in cache:
        print(f"[BACKEND] Match found for ID: {res_id}. Serving cached AI inference.")
        return jsonify(cache[res_id])
    else:
        # Fallback for the "Orange Cat" or unknown files
        print(f"[BACKEND] ID {res_id} not in cache. Returning default 'Upskill' profile.")
        return jsonify(list(cache.values())[0]) # Give them the first one so it doesn't crash

if __name__ == '__main__':
    app.run(debug=True, port=5000)