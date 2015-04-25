from flask import Flask, url_for, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://daniel@localhost/mydb'

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


@app.route('/bmw/', methods=['GET'])
def get_students():
    return jsonify({'posts': [post.get_url() for post in BMWReddit.query.all()]})


@app.route('/bmw/<int:user_id>', methods=['GET'])
def get_student(user_id):
    return jsonify(BMWReddit.query.get_or_404(user_id).export_data())


@app.route('/bmw/', methods=['POST'])
def new_student():
    post = BMWReddit()
    post.import_data(request.json)
    db.session.add(post)
    db.session.commit()
    return jsonify({"status": "new record added"}), 201, {'Location': post.get_url()}


@app.route('/bmw/<int:user_id>', methods=['PUT'])
def edit_student(user_id):
    post = BMWReddit.query.get_or_404(user_id)
    post.import_data(request.json)
    db.session.add(post)
    db.session.commit()
    return jsonify({"status": "record updated"})


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
