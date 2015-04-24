from flask import Flask, url_for, jsonify, request, render_template, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from flask.ext.paginate import Pagination

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://daniel@localhost/mydb'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


class ValidationError(ValueError):
    pass


class BMWReddit(db.Model):
    __tablename__ = 'bmwreddit'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50))
    score = db.Column(db.Integer)
    domain = db.Column(db.String(100))
    title = db.Column(db.String(250))
    author = db.Column(db.String(50))
    upVote = db.Column(db.Integer)
    downVote = db.Column(db.Integer)
    comments = db.Column(db.Integer)

    def get_url(self):
        return url_for('get_student', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'date': self.date,
            'score': self.score,
            'domain': self.domain,
            'title': self.title,
            'author': self.author,
            'upVote': self.upVote,
            'downVote': self.downVote,
            'comments': self.comments
        }

    def import_data(self, data):
        try:
            self.date = data['date']
            self.score = data['score']
            self.domain = data['domain']
            self.title = data['title']
            self.author = data['author']
            self.upVote = data['upVote']
            self.downVote = data['downVote']
            self.comments = data['comments']
        except KeyError as e:
            raise ValidationError('Invalid student: missing ' + e.args[0])
        return self


@app.route('/', methods=['GET'])
def index():
    return redirect("/bmw/api/", code=302)


@app.route('/bmw/api/', methods=['GET'])
def get_students():
    return jsonify({'posts': [post.get_url() for post in BMWReddit.query.all()]})


@app.route('/bmw/wrostpost', methods=['GET'])
def worst_posts():
    bmw = []
    results = BMWReddit.query.order_by(BMWReddit.upVote.asc()).limit(10)
    for rbmw in results:
        bmw.append(rbmw.export_data())
    # print(mydata)
    return render_template('index.html', bmw=bmw)


@app.route('/bmw/', methods=['GET'])
def get_students_api():
    bmw = BMWReddit.query.all()
    return render_template('index.html', bmw=bmw)


@app.route('/bmw/<int:id>', methods=['GET'])
def get_student(id):
    return render_template('singlepage.html', bmw=BMWReddit.query.get_or_404(id).export_data())


@app.route('/bmw/api/<int:id>', methods=['GET'])
def get_student_api(id):
    return jsonify(BMWReddit.query.get_or_404(id).export_data())


@app.route('/bmw/', methods=['POST'])
def new_student():
    post = BMWReddit()
    post.import_data(request.json)
    db.session.add(post)
    db.session.commit()
    return jsonify({}), 201, {'Location': post.get_url()}


@app.route('/bmw/<int:id>', methods=['PUT'])
def edit_student(id):
    post = BMWReddit.query.get_or_404(id)
    post.import_data(request.json)
    db.session.add(post)
    db.session.commit()
    return jsonify({})


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
