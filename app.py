from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/movie.db'
# 动态追踪数据库的修改. 性能不好. 且未来版本中会移除. 目前只是为了解决控制台的提示才写的
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Movie(db.Model):
    __tablename__  = 'movie250'
    id = db.Column(db.Integer, primary_key=True)
    info_link = db.Column(db.Text)
    pic_link = db.Column(db.Text)
    zh_title = db.Column(db.String(120))
    oth_title = db.Column(db.String(120))
    score = db.Column(db.Integer)
    rated = db.Column(db.Float)
    instroduction = db.Column(db.Text)
    info = db.Column(db.Text)

    def __repr__(self):
        return '<Movie %r>' % self.id

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/movie')
def movie():
    # 获取page参数 默认为1
    page = int(request.args.get('page', 1))
    # 获取每页显示数据条数默认为25
    per_page = 25
    # 从数据库查询数据
    pagination = Movie.query.order_by('id').paginate(page, per_page, error_out=False)
    content = pagination.items
    return render_template('movie.html', content = content, pagination = pagination)

@app.route('/score')
def score():
    return render_template('score.html')

@app.route('/word')
def word():
    return render_template('word.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()