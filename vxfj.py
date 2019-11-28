from flask import Flask, render_template, request, flash
from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField
from flask.ext.sqlalchemy import SQLAlchemy

from wtforms import validators, ValidationError
app = Flask(__name__)
app.secret_key = 'development key'

class ContactForm(Form):
    language = SelectField('Languages', choices=[('cpp', 'C++'),
                                                 ('py', 'Python'),
                                                 ('js', 'JS')])

@app.route('/')
def main():
    form = ContactForm()
    return render_template('contact.html', form = form)

@app.route('/senddata')
def senddata():
    projectpath = request.values['language']
    print(projectpath)
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)