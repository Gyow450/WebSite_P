from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mini_blog.db'
db = SQLAlchemy(app)

class Message(db.Model):
    id   = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/hello/<name>')
def hello(name):
    return f'<h1>Hello {name}!</h1>'

@app.route('/say', methods=['GET', 'POST'])
def say():
    if request.method == 'POST':
        m = Message(body=request.form['words'])
        db.session.add(m)
        db.session.commit()
    messages = Message.query.all()          # 读出所有记录
    return render_template('form.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)