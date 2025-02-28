import flask
from flask import Flask
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tttsite.db'
db.init_app(app)


@app.route('/')
def index():
    return flask.render_template('/pages/index.html', title='Hello World', content='Hello World!')


if __name__ == '__main__':
    app.run()
