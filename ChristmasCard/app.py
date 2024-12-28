from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

if not os.path.exists('static/uploads'):
    os.makedirs('static/uploads')

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

@app.route('/delete/<int:index>', methods=['POST'])
def delete_letter(index):
    if 0 <= index < len(letters):
        deleted_letter = letters.pop(index)
        if deleted_letter['image']:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], deleted_letter['image']))
    return redirect(url_for('index'))

@app.route('/edit_letter/<int:index>', methods=['GET', 'POST'])
def edit_letter(index):
    if request.method == 'POST':
        # 편지 수정 로직
        name = request.form['name']
        content = request.form['content']
        
        # 이미지 처리
        image = request.files['image']
        if image:
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{image.filename}"
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            letters[index]['image'] = filename
        
        letters[index]['name'] = name
        letters[index]['content'] = content
        
        return redirect(url_for('index'))
    
    # GET 요청 시 현재 편지 정보 전달
    letter = letters[index]
    return render_template('edit_letter.html', letter=letter, index=index)

if __name__ == '__main__':
    app.run(debug=True)

