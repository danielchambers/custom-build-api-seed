from flask import Flask, url_for, jsonify, request, render_template, redirect
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
        return url_for('get_student', user_id=self.id, _external=True)

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
    return redirect("/bmw/", code=302)


@app.route('/bmw/', methods=['GET'])
def get_students_api():
    bmw = BMWReddit.query.all()
    return render_template('index.html', bmw=bmw)


@app.route('/bmw/modifications/', methods=['GET'])
def get_student():
    return render_template('singlepage.html')


@app.route('/bmw/insert/', methods=['GET'])
def insert_record():
    return render_template('insert.html')


@app.route('/bmw/mostcomments/', methods=['GET'])
def most_comments():
    bmw = []
    results = BMWReddit.query.order_by(BMWReddit.comments.desc()).limit(10)
    for rbmw in results:
        bmw.append(rbmw.export_data())
    return render_template('mostcomments.html', bmw=bmw)


@app.route('/bmw/highestscore/', methods=['GET'])
def highest_score():
    bmw = []
    results = BMWReddit.query.order_by(BMWReddit.score.desc()).limit(10)
    for rbmw in results:
        bmw.append(rbmw.export_data())
    return render_template('highestscore.html', bmw=bmw)


@app.route('/bmw/lowestscore/', methods=['GET'])
def lowest_score():
    bmw = []
    results = BMWReddit.query.order_by(BMWReddit.score.asc()).limit(10)
    for rbmw in results:
        bmw.append(rbmw.export_data())
    return render_template('lowestscore.html', bmw=bmw)


##### API

@app.route('/bmw/api/documentation/', methods=['GET'])
def get_api():
    return render_template('api.html')


@app.route('/bmw/api/', methods=['GET'])
def get_students():
    return jsonify({'posts': [post.get_url() for post in BMWReddit.query.all()]})


@app.route('/bmw/api/<int:user_id>', methods=['GET'])
def get_student_api(user_id):
    return jsonify(BMWReddit.query.get_or_404(user_id).export_data())


@app.route('/bmw/api/', methods=['POST'])
def new_record():
    post = BMWReddit()
    post.import_data(request.json)
    db.session.add(post)
    db.session.commit()
    return jsonify({"status": "record added"})#, 201, {'Location': post.get_url()}


@app.route('/bmw/api/<int:user_id>', methods=['PUT'])
def edit_record(user_id):
    post = BMWReddit.query.get_or_404(user_id)
    post.import_data(request.json)
    db.session.add(post)
    db.session.commit()
    return jsonify({"status": "record updated"})


@app.route('/bmw/api/<int:user_id>', methods=['DELETE'])
def delete_record(user_id):
    record = BMWReddit.query.get_or_404(user_id)
    # print(record)
    db.session.delete(record)
    db.session.commit()
    return jsonify({"status": "record deleted"})


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)