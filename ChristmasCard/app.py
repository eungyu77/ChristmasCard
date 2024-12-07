from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

letters = []

@app.route('/')
def index():
    return render_template('index.html', letters=letters)

@app.route('/write', methods=['GET', 'POST'])
def write_letter():
    if request.method == 'POST':
        name = request.form['name']
        content = request.form['content']
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        image = request.files['image']
        if image:
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{image.filename}"
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None
        
        letters.append({'name': name, 'content': content, 'date': date, 'image': filename})
        return redirect(url_for('index'))
    return render_template('write_letter.html')

if __name__ == '__main__':
    app.run(debug=True)