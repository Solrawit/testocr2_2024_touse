from flask import Flask, render_template, request
from easyocr import Reader
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

processed_text = None

@app.route('/')
def index():
    return render_template('index.html', processed_text=processed_text)

@app.route('/upload', methods=['POST'])
def upload():
    global processed_text
    image_file = request.files['file']
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
    image_file.save(image_path)

    reader = Reader(['en', 'th'])
    results = reader.readtext(image_path)

    processed_text = '\n'.join([result[1] for result in results])

    return render_template('index.html', processed_text=processed_text)

@app.route('/edit', methods=['POST'])
def edit():
    global processed_text
    edited_text = request.form['edited_text']
    processed_text = edited_text
    return render_template('index.html', processed_text=processed_text)

if __name__ == '__main__':
    app.run(debug=True)

