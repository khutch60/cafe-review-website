from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import URL, Length, InputRequired
from wtforms.fields import URLField
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = '12345'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafe-data.db"

db = SQLAlchemy()
db.init_app(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    website = db.Column(db.String(1000), unique=False, nullable=False)
    photo = db.Column(db.String(1000), unique=False, nullable=False)
    review = db.Column(db.String(1000), unique=False, nullable=False)
    rating = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return f"cafe - {self.name}"


class NewCafe(FlaskForm):
    name = StringField("Cafe Name", validators=[InputRequired()], render_kw={"placeholder": "Cafe Name"})
    website = URLField("Website", validators=[InputRequired()], render_kw={"placeholder": "Website"})
    photo = URLField("Website", validators=[InputRequired(), URL()], render_kw={"placeholder": "Photo URL"})
    review = TextAreaField(validators=[InputRequired(), Length(min=1, max=900, message="You have reached the character limit")], render_kw={"placeholder": "Write your review here"})
    rating = SelectField("Rating", choices=[('1', '*'), ('2', '**'), ('3', '***'), ('4', '****'), ('5', '*****')])
    submit = SubmitField()


@app.route('/')
def home():
    cafe_db = Cafe.query.all()
    return render_template('index.html', cafes=cafe_db)


@app.route('/new-cafe', methods=["GET", "POST"])
def new_post():
    form = NewCafe()
    if form.validate_on_submit():
        name = form.name.data.title()
        website = form.website.data
        photo = form.photo.data
        review = form.review.data
        rating = int(form.rating.data.split()[0]) * "⭐"
        new_cafe = Cafe(
            name=name,
            website=website,
            photo=photo,
            review=review,
            rating=rating
        )

        with app.app_context():
            check_name = Cafe.query.filter_by(name=name).first()
        if check_name is None:
            db.session.add(new_cafe)
            db.session.commit()
            return redirect("/")

        else:
            form.name.data = "Cafe already posted! Try another"
            return render_template("new-cafe.html", form=form)

    return render_template("new-cafe.html", form=form)



if __name__ == '__main__':
    app.run(debug=True)
