#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import jsonify, session
from email.mime.text import MIMEText
from flask import render_template, request, escape, redirect, url_for
import sqlite3 #mysql.connector as
from werkzeug import generate_password_hash, check_password_hash
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext import admin
#from flask.ext import MYSql
from flask.ext.admin.contrib import sqla
from flask.ext.admin import expose
import smtplib
import random
import socket
from flask_wtf import FlaskForm
from wtforms import SelectField
import time
import datetime
import netifaces as nif

socket.gethostbyname(socket.gethostname())
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com", 80))
ip = str(s.getsockname()[0])
s.close()
# session.pop('visits', None)

app = Flask(__name__)


def filter(f, p, v, b, cursor, conn):
    projectpath2 = escape(session['username'])
    posts = []
    a = 1
    projectpath = request.values['projectFilepath2']
    for i in f:
        projectpath = projectpath.replace(i, p[b])
        b += 1
    for i in v:
        projectpath1 = projectpath
        d = projectpath1.find(i)
        i1 = i.upper()
        d1 = projectpath1.find(i1)
        if d != (-1) or d1 != (-1):
            projectpath = projectpath.replace(i, '#$#@')
            projectpath = projectpath.replace(i1, '#$#@')
            d = datetime.date.today()
            a2 = d.day + (30 * ((d.month) - 1))
            sql = "UPDATE albums7 SET block=('{}') WHERE title=('{}')".format(a2, projectpath2)
            cursor.execute(sql)
            conn.commit()
    a1 = time.ctime(time.time())
    a1 = str(a1)
    cursor.execute(
        "INSERT INTO albums6 (title, Post, time) VALUES ('{}', '{}', '{}')".format(projectpath2, projectpath, a1))
    conn.commit()
    cursor.execute("SELECT id FROM albums6")
    sql = cursor.fetchall()
    for row in sql:
        row = int(row[0])
        cursor.execute("SELECT title, Post, time FROM albums6 WHERE id = ({})".format(row))
        sql1 = cursor.fetchone()
        posts.append({
            'author': {'nickname': str(sql1[0] + ' ' + sql1[2])},
            'body': str(sql1[1])
        })
        a += 1
    cursor.close()
    conn.close()
    return posts


# TODO: сделать выпадающие списки при выбор классов
class ContactForm(FlaskForm):
    conn = sqlite3.connect("mydatabaseq1.db")  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    sql = "SELECT id FROM albums3"
    cursor.execute(sql)
    sql1 = cursor.fetchall()
    a = []

    for i in sql1:
        i = int(i[0])
        sql = "SELECT class FROM albums3 WHERE id=('{}')".format(int(i))
        cursor.execute(sql)
        sql = cursor.fetchone()
        a.append((str(sql[0]), str(sql[0])))
    language = SelectField('Класс', choices=a)
    cursor.close()
    conn.close()

@app.route('/')
def main():
    form = ContactForm()
    posts = ['7', '8', '9', '10', '11', 'учитель']
    return render_template('gfdj.html', form=form, option=posts)


@app.route('/log_out')
def log_out():
    form = ContactForm()
    session.pop('username', None)
    if 'visits' in session:
        session['visits'] = session.get('visits') - 1
    else:
        session['visits'] = 0
    return render_template('gfdj.html', form=form)


@app.route('/signUp', methods=['POST', 'GET'])
def signUp():
    try:
        projectpath = request.values['projectFilepath']
        projectpath0 = request.values['projectFilepath1']
        projectpath01 = request.values['projectFilepath2']
        projectpath03 = request.values['projectFilepath3']
        projectpath04 = request.values['projectFilepath4']
        projectpath05 = request.values['projectFilepath5']
        projectpath06 = request.values['language']
        conn = sqlite3.connect("mydatabaseq1.db")  # или :memory: чтобы сохранить в RAM
        cursor = conn.cursor()
        if projectpath != "" and projectpath0 != "" and projectpath06 != " ":
            if projectpath01 == projectpath0:
                projectpath1 = generate_password_hash(projectpath0)
                cursor.execute('INSERT INTO Block_diagramms (username, Class) VALUES ("{}", "{}")'.format(projectpath,
                                                                                                          projectpath06))
                cursor.execute(
                    "INSERT INTO albums7 (title, pass, E_mail, Name, Surname, Class) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(
                        projectpath, projectpath1, projectpath03, projectpath04, projectpath05, projectpath06))
                conn.commit()
                data = cursor.fetchall()

                if len(data) == 0:
                    conn.commit()
                    return render_template('ghy.html')
                else:
                    error = str(data[0])
                    return render_template('gfdj.html', error=error)
                    # return json.dumps({'error': str(data[0])})
            else:
                error = "Different values for 'Password' and 'Repeat password'"
                return render_template('gfdj.html', error=error)
        else:
            error = "Enter the required fields"
            return render_template('gfdj.html', error=error)

    except Exception as e:
        error = str(e)
        return render_template('gfdj.html', error=error)
    finally:
        cursor.close()
        conn.close()

@app.route('/signUpForT/', methods=['POST', 'GET'])
def signUpForT():
    try:
        projectpath = request.values['projectFilepath']
        projectpath0 = request.values['projectFilepath1']
        projectpath01 = request.values['projectFilepath2']
        projectpath03 = request.values['projectFilepath3']
        projectpath04 = request.values['projectFilepath4']
        projectpath05 = request.values['projectFilepath5']

        conn = sqlite3.connect("mydatabaseq1.db")  # или :memory: чтобы сохранить в RAM
        cursor = conn.cursor()
        if projectpath != "" and projectpath0 != "" :
            if projectpath01 == projectpath0:
                projectpath1 = generate_password_hash(projectpath0)
                cursor.execute('INSERT INTO Block_diagramms (username) VALUES ("{}")'.format(projectpath))
                cursor.execute(
                    "INSERT INTO albums7 (title, pass, E_mail, Name, Surname, role) VALUES ('{}', '{}', '{}', '{}', '{}', 0)".format(
                        projectpath, projectpath1, projectpath03, projectpath04, projectpath05))
                conn.commit()
                data = cursor.fetchall()
                session['registrperson'] = projectpath
                if len(data) == 0:
                    conn.commit()
                    return render_template('ghy.html')
                else:
                    error = str(data[0])
                    return render_template('gfdj.html', error=error)
                    # return json.dumps({'error': str(data[0])})
            else:
                error = "Different values for 'Password' and 'Repeat password'"
                return render_template('gfdj.html', error=error)
        else:
            error = "Enter the required fields"
            return render_template('gfdj.html', error=error)

    except Exception as e:
        error = str(e)
        return render_template('gfdj.html', error=error)
    finally:
        cursor.close()
        conn.close()

@app.route("/confirmrole")
def conRole():
    pass

@app.route('/showSignUp')
def showSignIn():
    return render_template('ghy.html')


@app.route('/signIn', methods=['POST', 'GET'])
def signIn():
    try:

        projectpath2 = request.values['projectFilepath2']
        projectpath02 = request.values['projectFilepath3']
        conn = sqlite3.connect("mydatabaseq1.db")
        cursor1 = conn.cursor()
        sql = "SELECT pass FROM albums7 WHERE title=('{}')".format(projectpath2)
        sql9 = "SELECT role FROM albums7 WHERE title=('{}')".format(projectpath2)
        sql3 = "SELECT Name, Surname, role FROM albums7 WHERE title=('{}')".format(projectpath2)
        cursor1.execute(sql)
        session['username'] = projectpath2
        sql1 = cursor1.fetchone()
        cursor1.execute(sql3)
        sql5 = cursor1.fetchone()
        session['role'] = str(sql5[2])
        cursor1.execute(sql9)
        sql9 = cursor1.fetchone()
        sql10 = str(sql1[0])
        sql50 = str(sql5[0]) + ' ' + str(sql5[1])
        if str(sql9[0]) == '2':
            if check_password_hash(sql10, projectpath02) == True:
                a = str(time.ctime(time.time()))
                b = request.remote_addr
                # musk = mac_for_ip(b)
                # print(musk)
                if 'visits' in session:
                    session['visits'] = session.get('visits') + 1
                else:
                    session['visits'] = 1
                cursor1.execute(
                    "INSERT INTO albums4 (title, title1, ip) VALUES ('{}', '{}', '{}')".format(projectpath2, a, b))
                conn.commit()
                return render_template('ggga.html', user=sql50)
            else:
                error = "Incorrect Login or Password"
                return render_template('ghy.html', error=error)
        elif str(sql9[0]) == '1':
            if check_password_hash(sql10, projectpath02) == True:
                a = str(time.ctime(time.time()))
                b = request.environ['REMOTE_ADDR']
                # musk = mac_for_ip(b)
                # print(musk)
                if 'visits' in session:
                    session['visits'] = session.get('visits') + 1
                else:
                    session['visits'] = 1
                cursor1.execute(
                    "INSERT INTO albums4 (title, title1, ip) VALUES ('{}', '{}', '{}')".format(projectpath2, a, b))
                conn.commit()
                return render_template('gggt.html', user=sql50)

            else:
                error = "Incorrect Login or Password"
                return render_template('ghy.html', error=error)
        else:
            if check_password_hash(sql10, projectpath02) == True:
                if 'visits' in session:
                    session['visits'] = session.get('visits') + 1
                else:
                    session['visits'] = 1
                return render_template('ggg.html', user=sql50)

            else:
                error = "Incorrect Login or Password"
                return render_template('ghy.html', error=error)
    except Exception as e:
        error = "Incorrect Login or Password"
        return render_template('ghy.html', error=error)
    finally:
        cursor1.close()
        conn.close()


app.config['SECRET_KEY'] = 'you_will_never_guess'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabaseq1.db'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


@app.route('/Admin')
def Admin():
    return '<a href="/admin1/">Click me to get to Admin!</a>'



class Users(db.Model):
    __tablename__ = 'albums7'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    E_mail = db.Column(db.String(100))
    Name = db.Column(db.String(100))
    Surname = db.Column(db.String(100))
    Class = db.Column(db.String(10))
    block = db.Column(db.Integer)
    role = db.Column(db.Integer)

    def __unicode__(self):
        return self.desc


class Messages(db.Model):
    __tablename__ = 'albums6'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    Post = db.Column(db.String(10000))
    time = db.Column(db.String(50))


class Marks(db.Model):
    __tablename__ = 'Block_diagramms'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Class = db.Column(db.String(10))
    username = db.Column(db.String(50))
    Task1 = db.Column(db.Integer)
    Task2 = db.Column(db.Integer)


class Logs(db.Model):
    __tablename__ = 'albums4'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    title1 = db.Column(db.String(50))
    ip = db.Column(db.String(50))


class GoHome(db.Model):
    __tablename__ = 'albums2'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


class Classes(db.Model):
    __tablename__ = 'albums3'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Class = db.Column(db.String(10))


class CarAdmin(sqla.ModelView):
    column_display_pk = True
    form_columns = ['id', 'title', 'E_mail', 'Name', 'Surname', 'block', 'Class', 'role']
    column_searchable_list = ('title', 'Class')


class CarAdmin2(sqla.ModelView):
    column_display_pk = True
    form_columns = ['id', 'title', 'title1', 'ip']
    column_searchable_list = ('title', 'title1')


class CarAdmin3(sqla.ModelView):
    column_display_pk = True
    form_columns = ['id']
    column_searchable_list = ('title', 'time')


class CarAdmin4(sqla.ModelView):
    column_display_pk = True
    form_columns = ['id', 'Class']
    # column_searchable_list = ('Class')


class CarAdmin5(sqla.ModelView):
    column_display_pk = True
    form_columns = ['id', 'username', 'Task1', 'Task2', 'Class']
    # column_searchable_list = ('Class')


class CarAdmin1(sqla.ModelView):

    @expose('/')
    def index(self):
        projectpath2 = escape(session['username'])
        conn = sqlite3.connect("mydatabaseq1.db")
        cursor1 = conn.cursor()
        sql3 = "SELECT Name, Surname FROM albums7 WHERE title=('{}')".format(projectpath2)
        cursor1.execute(sql3)
        sql5 = cursor1.fetchone()
        sql50 = str(sql5[0]) + ' ' + str(sql5[1])
        if projectpath2 == 'admin1' or projectpath2 == 'admin2':
            pass
        return render_template('ggga.html', user=sql50, admin=admin)


admin = admin.Admin(app, name='Admin')

admin.add_view(CarAdmin(Users, db.session))
admin.add_view(CarAdmin3(Messages, db.session))
admin.add_view(CarAdmin2(Logs, db.session))
admin.add_view(CarAdmin4(Classes, db.session))
admin.add_view(CarAdmin5(Marks, db.session))
admin.add_view(CarAdmin1(GoHome, db.session))


@app.route('/ShowRes_pass')
def ShowRes_pass():
    return render_template('ggg1.html')



@app.route('/Res_pass', methods=['POST', 'GET'])
def Res_pass():
    try:
        log = request.values['projectFilepath9']
        session['log'] = log
        conn = sqlite3.connect("mydatabaseq1.db")
        cursor1 = conn.cursor()
        sql9 = "SELECT E_mail FROM albums7 WHERE title=('{}')".format(log)
        cursor1.execute(sql9)
        adr = cursor1.fetchone()
        adr = str(adr[0])
        MAIL_SERVER = 'smtp.gmail.com'
        MAIL_PORT = 465

        MAIL_USERNAME = 'block.diagramms.com@gmail.com'
        MAIL_PASSWORD = 'Diagramma192'

        FROM = 'Block-diagrams.com'  # <kuteynikov.artyom@gmail.com>'
        TO = adr
        txtparam = str(random.randint(100001, 999999))
        session['txtparam'] = txtparam
        # теперь можно использовать кириллицу
        msg = 'Ваш код сброа пароля:{}. Если вы не запрашивали сброс пароля, удалите это сообшение и никому не сообщайте код.'.format(
            txtparam)
        msg = MIMEText('\n {}'.format(msg).encode('utf-8'), _charset='utf-8')

        smtpObj = smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT)
        smtpObj.ehlo()
        smtpObj.login(MAIL_USERNAME, MAIL_PASSWORD)

        smtpObj.sendmail(FROM, TO,
                         'Subject: Сброс пароля. \n{}'.format(msg).encode('utf-8'))
        smtpObj.quit()
        return render_template('ggg2.html')
    except Exception as e:
        error = str(e)
        return render_template('ggg1.html', error=error)
    finally:
        cursor1.close()
        conn.close()


@app.route('/Check_code', methods=['POST', 'GET'])
def Check_code():
    projectpath2 = request.values['projectFilepath']
    if projectpath2 == escape(session['txtparam']):
        return render_template('ghy1.html')
    else:
        error = "Incorrect code"
        return render_template('ggg2.html', error=error)


@app.route('/Upd_pass', methods=['POST', 'GET'])
def Upd_pass():
    try:
        log = escape(session['log'])
        projectpath2 = request.values['projectFilepath2']
        projectpath02 = request.values['projectFilepath3']
        conn = sqlite3.connect("mydatabaseq1.db")
        cursor2 = conn.cursor()
        if projectpath2 == projectpath02:
            projectpath12 = generate_password_hash(projectpath02)
            sql = "UPDATE albums7 SET pass=('{}') WHERE title=('{}')".format(projectpath12, log)
            cursor2.execute(sql)
            conn.commit()
        else:
            error = "Password isn't equal to repeated password"
            return render_template('ghy1.html', error=error)
        return render_template('ghy.html')
    except Exception as e:
        error = str(e)
        return render_template('ghy.html', error=error)
    finally:
        cursor2.close()
        conn.close()


@app.route('/Show_info', methods=['POST', 'GET'])
def Show_info():
    if 'username' in session:
        projectpath2 = escape(session['username'])
        sql = "SELECT Name, Surname, E_mail FROM albums7 WHERE title=('{}')".format(projectpath2)
        conn = sqlite3.connect("mydatabaseq1.db")
        cursor1 = conn.cursor()
        cursor1.execute(sql)
        sql1 = cursor1.fetchone()
        sql3 = str(sql1[0])
        sql4 = str(sql1[1])
        sql5 = str(sql1[2])
        sql6 = projectpath2
        cursor1.close()
        conn.close()
        return render_template('pro.html', user1=sql3, user2=sql4, user3=sql5, user4=sql6)
    else:
            return render_template('ghy.html')

@app.route('/ch_info1', methods=['POST', 'GET'])
def ch_info1():
    if 'username' in session:
        projectpath2 = escape(session['username'])
        sql = "SELECT Name, Surname, E_mail, Class FROM albums7 WHERE title=('{}')".format(projectpath2)
        conn = sqlite3.connect("mydatabaseq1.db")
        cursor1 = conn.cursor()
        cursor1.execute(sql)
        sql1 = cursor1.fetchone()
        form = ContactForm()
        sql3 = str(sql1[0])
        sql4 = str(sql1[1])
        sql5 = str(sql1[2])
        sql7 = str(sql1[3])
        sql6 = projectpath2
        cursor1.close()
        conn.close()
        return render_template('gfdj1.html', user1=sql3, user2=sql4, user3=sql5, user4=sql6, user5=sql7, form=form)
    else:
        return render_template('ghy.html')

@app.route('/ch_info2', methods=['POST', 'GET'])
def ch_info2():
    projectpath05 = request.values['projectFilepath']
    projectpath04 = request.values['projectFilepath3']
    projectpath = request.values['projectFilepath4']
    projectpath03 = request.values['projectFilepath5']
    projectpath01 = request.values['language']
    conn = sqlite3.connect("mydatabaseq1.db")
    cursor2 = conn.cursor()
    d = escape(session['username'])
    if projectpath != '':
        sql = "UPDATE albums7 SET Name=('{}') WHERE title=('{}')".format(projectpath, d)
        cursor2.execute(sql)
        conn.commit()
    if projectpath01 != ' ':
        sql = "UPDATE albums7 SET Class=('{}') WHERE title=('{}')".format(projectpath01, d)
        cursor2.execute(sql)
        conn.commit()
        sql = "UPDATE Block_diagramms SET Class=('{}') WHERE username=('{}')".format(projectpath01, d)
        cursor2.execute(sql)
        conn.commit()
        print(projectpath)
    if projectpath03 != '':
        sql = "UPDATE albums7 SET Surname=('{}') WHERE title=('{}')".format(projectpath03, d)
        cursor2.execute(sql)
        conn.commit()
    if projectpath04 != '':
        sql = "UPDATE albums7 SET E_mail=('{}') WHERE title=('{}')".format(projectpath04, d)
        cursor2.execute(sql)
        conn.commit()
    if projectpath05 != '':
        session.pop('username', None)
        session['username'] = projectpath05
        sql = "UPDATE albums7 SET title=('{}') WHERE title=('{}')".format(projectpath05, d)
        sql1 = "UPDATE Block_diagramms SET username=('{}') WHERE username=('{}')".format(projectpath05, d)
        cursor2.execute(sql)
        conn.commit()
        cursor2.execute(sql1)
        conn.commit()
    cursor2.close()
    conn.close()
    return render_template('pro1.html')


@app.route('/MyPage', methods=['POST', 'GET'])
def MyPage():
    if 'username' in session:
        projectpath2 = escape(session['username'])
        conn = sqlite3.connect("mydatabaseq1.db")
        cursor1 = conn.cursor()
        sql3 = "SELECT Name, Surname FROM albums7 WHERE title=('{}')".format(projectpath2)
        cursor1.execute(sql3)
        sql5 = cursor1.fetchone()
        sql9 = "SELECT role FROM albums7 WHERE title=('{}')".format(projectpath2)
        cursor1.execute(sql9)
        sql9 = cursor1.fetchone()
        sql50 = str(sql5[0]) + ' ' + str(sql5[1])
        if str(sql9[0]) == '2':
            return render_template('ggga.html', user=sql50, admin=admin)
        elif str(sql9[0]) == '1':
            return render_template('gggt.html', user=sql50)
        else:
            return render_template('ggg.html', user=sql50)
    else:
        return render_template('ghy.html')

@app.route('/Show_Marks', methods=['POST', 'GET'])
def Show_Marks():
    if 'username' in session:
        projectpath2 = escape(session['username'])
        sql1a1 = 0
        a = 0
        conn = sqlite3.connect("mydatabaseq1.db")
        cursor = conn.cursor()
        cursor.execute("SELECT Task1, Task2 FROM Block_diagramms WHERE username = ('{}')".format(projectpath2))
        sql1 = cursor.fetchone()
        sql11 = sql1[0]
        if sql11 != 0:
            sql1a1 += sql11
            a += 1
        sql12 = sql1[1]
        if sql12 != 0:
            sql1a1 += sql12
            a += 1
        if a != 0:
            sql1a = sql1a1 / a
        else:
            sql1a = 0
        return render_template('Marks.html', M1=sql11, M2=sql12, MA=sql1a)
    else:
        return render_template('ghy.html')

@app.route('/Ch_pass1', methods=['POST', 'GET'])
def Ch_pass1():
    if 'username' in session:
        return render_template('Ch_pass.html')
    else:
        return render_template('ghy.html')



@app.route('/Ch_pass2', methods=['POST', 'GET'])
def Ch_pass2():
    projectpath2 = escape(session['username'])
    projectpath1 = request.values['projectFilepath2']
    projectpath02 = request.values['projectFilepath3']
    projectpath3 = request.values['projectFilepath4']
    conn = sqlite3.connect("mydatabaseq1.db")
    cursor1 = conn.cursor()
    sql3 = "SELECT pass FROM albums7 WHERE title=('{}')".format(projectpath2)
    cursor1.execute(sql3)
    sql5 = cursor1.fetchone()
    sql50 = str(sql5[0])
    if check_password_hash(sql50, projectpath1) == True:
        if projectpath02 == projectpath3:
            projectpath12 = generate_password_hash(projectpath02)
            sql = "UPDATE albums7 SET pass=('{}') WHERE title=('{}')".format(projectpath12, projectpath2)
            cursor1.execute(sql)
            conn.commit()
            return render_template('nnn.html')
        else:
            error = 'Different values for new password and repeat password'
            return render_template('Ch_pass.html', error=error)
    else:
        error = 'Incorrect old password'
        return render_template('Ch_pass.html', error=error)


@app.route('/ConTS', methods=['POST', 'GET'])
def ConTS():
    if 'username' in session:
        try:
            posts = []
            conn = sqlite3.connect("mydatabaseq1.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM albums6")
            sql = cursor.fetchall()
            for row in sql:
                row = int(row[0])
                cursor.execute("SELECT title, Post, time FROM albums6 WHERE id = ('{}')".format(row))
                sql1 = cursor.fetchone()
                a1 = str(sql1[2])
                posts.append({
                    'author': {'nickname': str(sql1[0] + ' ' + a1)},
                    'body': str(sql1[1])
                })
            return render_template('techsup.html', posts=posts)
        except Exception as e:
            error = str(e)
            return render_template('techsup.html', error=error)
        finally:
            cursor.close()
            conn.close()
    else:
        return render_template('ghy.html')

@app.route('/ShowMag', methods=['POST', 'GET'])
def ShowMag():
    if 'username' in session:
        form = ContactForm()
        return render_template('MagS.html', form=form)
    else:
        return render_template('ghy.html')



@app.route('/ShowMag1', methods=['POST', 'GET'])
def ShowMag1():
    if 'username' in session:
        projectpath3 = str(request.values['language'])
        conn = sqlite3.connect("mydatabaseq1.db")
        cursor = conn.cursor()
        if 0 == 0:
            posts = []
            a = 1
            cursor.execute("SELECT id FROM albums7")
            sql = cursor.fetchall()
            for row in sql:
                row = int(row[0])
                cursor.execute("SELECT Class, Name, Surname, title FROM albums7 WHERE id = ({})".format(row))
                sql1 = cursor.fetchone()
                sql11 = str(sql1[0])
                print(str(sql1[3]))
                cursor.execute("SELECT Class, Task1, Task2 FROM Block_diagramms WHERE id = ({})".format(row))
                sql12 = cursor.fetchone()
                if sql11 == str(projectpath3):
                    b = 0
                    n = 0
                    print(sql12)
                    for i in range(2):
                        if int(sql12[i + 1]) != 0:
                            b += int(sql12[i + 1])
                            n += 1
                    if n != 0:
                        posts.append({
                            'author': {'nickname': str(sql1[1] + ' ' + sql1[2])},
                            'Task1': str(sql12[1]),
                            'Task2': str(sql12[2]),
                            'Average': (int(b)) / n
                        })
                    else:
                        posts.append({
                            'author': {'nickname': str(sql1[1] + ' ' + sql1[2])},
                            'Task1': str(sql12[1]),
                            'Task2': str(sql12[2]),
                            'Average': (int(0))
                        })
                a += 1
            cursor.close()
            conn.close()
            return render_template('Mag.html', posts=posts)
    else:
        return render_template('ghy.html')



@app.route('/ConTS1', methods=['POST', 'GET'])
def ConTS1():
    if 'username' in session:
        projectpath2 = escape(session['username'])
        conn = sqlite3.connect("mydatabaseq1.db")
        cursor = conn.cursor()
        cursor.execute("SELECT block FROM albums7 WHERE title = ('{}')".format(projectpath2))
        sql1 = cursor.fetchone()
        sql11 = sql1[0]
        f = ['o', 'a', 'e', 'p', 'k', 'x', 'c', 'E', 'T', 'O', 'P', 'A', 'H', 'K', 'X', 'C', 'B', 'M', "3"]
        p = ["о", "а", "е", "р", "к", "х", "с", "Е", "Т", "О", "Р", "А", "Н", "К", "Х", "С", "В", "М", "З"]
        v = ['морковь']
        b = 0
        if sql11 == 0:
            posts = filter(f, p, v, b, cursor, conn)
            return render_template('techsup.html', posts=posts)
        else:
            d = datetime.date.today()
            a2 = d.day + (30 * ((d.month) - 1))
            sql1 = int(sql11)
            if sql1 < 358:
                if sql1 < (a2 - 2):
                    posts = filter(f, p, v, b, cursor, conn)
                    return render_template('techsup.html', posts=posts)
                else:
                    error = 'Chat had been blocked for you'
                    return render_template('techsup.html', error=error)
            else:
                if 0 == 0:
                    if a2 == 2:
                        if 0 == 0:
                            posts = filter(f, p, v, b, cursor, conn)
                            return render_template('techsup.html', posts=posts)
                    else:
                        error = 'Chat had been blocked for you'
                        return render_template('techsup.html', error=error)
    else:
        return render_template('ghy.html')



@app.route('/ConTS11', methods=['POST', 'GET'])
def ConTS11():
    if 'username' in session:
        projectpath2 = escape(session['username'])
        conn = sqlite3.connect("mydatabaseq1.db")
        cursor = conn.cursor()
        cursor.execute("SELECT Name, Surname FROM albums7 WHERE title = ('{}')".format(projectpath2))
        sql1 = cursor.fetchone()
        projectpath20 = str(sql1[0] + ' ' + sql1[1])
        if 0 == 0:
            posts = []
            a = 1
            projectpath = request.values['projectFilepath2']
            a1 = time.ctime(time.time())
            a1 = str(a1)
            cursor.execute(
                "INSERT INTO albums5 (title, Post, time) VALUES ('{}', '{}', '{}')".format(projectpath20, projectpath,
                                                                                           a1))
            conn.commit()
            cursor.execute("SELECT id FROM albums5")
            sql = cursor.fetchall()
            for row in sql:
                row = int(row[0])
                cursor.execute("SELECT title, Post, time FROM albums5 WHERE id = ({})".format(row))
                sql1 = cursor.fetchone()
                a1 = str(sql1[2])
                posts.append({
                    'author': {'nickname': str(sql1[0] + ' ' + a1)},
                    'body': str(sql1[1])
                })
                a += 1
            cursor.close()
            conn.close()
            return render_template('techsup1.html', posts=posts)
        else:
            error = 'Chat had been blocked for you'
            return render_template('techsup1.html', error=error)
    else:
        return render_template('ghy.html')



@app.route('/ConTS0', methods=['POST', 'GET'])
def ConTS0():
    try:
        a = 1
        posts = []
        conn = sqlite3.connect("mydatabaseq1.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM albums5")
        sql = cursor.fetchall()
        for row in sql:
            row = int(row[0])
            cursor.execute("SELECT title, Post, time FROM albums5 WHERE id = ('{}')".format(row))
            sql1 = cursor.fetchone()
            a1 = str(sql1[2])
            posts.append({
                'author': {'nickname': str(sql1[0] + ' ' + a1)},
                'body': str(sql1[1])
            })
            a += 1
        return render_template('techsup1.html', posts=posts)
    except Exception as e:
        error = str(e)
        return render_template('techsup1.html', error=error)
    finally:
        cursor.close()
        conn.close()


@app.route('/FagLog', methods=['POST', 'GET'])
def FagLog():
    form = ContactForm()
    error = 'Да иди ты нафиг, регестрируйся заново, мне тебя как искать, по запаху!?'
    return render_template('gfdj.html', error=error, form=form)


@app.route('/cours')
def cours():
    return render_template('course.html')


@app.route('/ShowTasks')
def ShowTasks():
    return render_template('tasks.html')


@app.route('/ShowTheory')
def ShowTheory():
    return render_template('course.html')


@app.route('/AboutCourse')
def AboutCourse():
    return render_template('course.html')


class myclass:
    def __init__(self):
        pass

    def returnsmt(self, a):
        if 'username' in session:
            projectpath2 = escape(session['username'])
            conn = sqlite3.connect("mydatabaseq1.db")
            cursor = conn.cursor()
            cursor.execute("SELECT {} FROM Block_diagramms WHERE username = ('{}')".format(a, projectpath2))
            sql1 = cursor.fetchone()
            sql11 = sql1[0]
            sql11 = int(sql11)
            cursor.close()
            conn.close()
            if sql11 != 0:
                return render_template('{}.html'.format(a), a=sql11)
            else:
                return render_template('{}.html'.format(a), a='')
        else:
            return render_template('ghy.html')



mc = myclass()


@app.route('/Task1')
def Task1():
    return mc.returnsmt('Task1')

@app.route('/test')
def test():
    return render_template('Test.html')

@app.route('/Task2')
def Task2():
    return mc.returnsmt('Task2')


@app.route('/_add_numbers')
def add_numbers():
    if 'username' in session:
        projectpath2 = escape(session['username'])
        a = request.args.get('b', 0, type=float)
        print(a)
        b = request.args.get('c', 0, type=str)
        if a < 2:
            a = 2
        a = int(a)
        conn = sqlite3.connect("mydatabaseq1.db")
        cursor = conn.cursor()
        cursor.execute("SELECT {} FROM Block_diagramms WHERE username = ('{}')".format(b, projectpath2))
        sql1 = cursor.fetchone()
        sql11 = sql1[0]
        if sql11 == 0:
            sql = "UPDATE Block_diagramms SET {}=('{}') WHERE username=('{}')".format(b, a, projectpath2)
            cursor.execute(sql)
            conn.commit()
            return jsonify(result=a)
        else:
            return jsonify(result=sql11)
        cursor.close()
        conn.close()
    else:
        return render_template('ghy.html')



@app.route('/visits')
def visits():
    return "Total visits: {}".format(session.get('visits'))


@app.route('/delete_visits')
def delete_visits():
    session.pop('visits', None)
    return 'Visits deleted'


@app.route('/Show_Map')
def Show_Map():
    session.pop('visits', None)
    return render_template('mymap.html')

@app.route('/AddCourse')
def AddCourse():
    if 'username' in session:
        try:
        #if 1:
            name = request.values['CourseName']
            projectpath2 = escape(session['username'])
            conn = sqlite3.connect("mydatabaseq1.db")
            cursor = conn.cursor()
            cursor.execute("SELECT role FROM albums7 WHERE title = ('{}')".format(projectpath2))
            sql1 = cursor.fetchone()
            print(sql1[0])
            if str(sql1[0]) == '1':
                conn = sqlite3.connect('courseinfo.db')
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM allcourses")
                sql = cursor.fetchall()
                sql = sql[-1]
                number = int(sql[0])+1
                number = 'course'+str(number)

                cursor.execute("CREATE TABLE {} (id INTEGER PRIMARY KEY, module STRING (1000), lesson STRING(1000), type STRING (10),question STRING text,right_answer STRING (100))".format(number))
                conn.commit()

                cursor.execute("INSERT INTO allcourses (number, name, author) VALUES ('{}', '{}', '{}')".format(number, name, projectpath2))
                conn.commit()

                return render_template('addcourse.html', lessons=[], topics=[], modules=[], course = number)
            else:
                return "Ds yt vj;tnt cjplfnm rehc"
        except Exception as e:
            error = str(e)
            return render_template('techsup1.html', error = error)
        finally:
            cursor.close()
            conn.close()
    else:
        return render_template('ghy.html')
@app.route('/CreateModule/<course>')
def CreateModule(course):
    try:
        name = request.values['CourseName']
        #course = request.values['CourseName1']
        projectpath2 = escape(session['username'])
        conn = sqlite3.connect("courseinfo.db")
        cursor = conn.cursor()
        a = '-'
        cursor.execute("INSERT INTO {} (module, type, question, right_answer) VALUES ('{}', '{}', '{}', '{}')".format(course,name, a, a, a))
        conn.commit()
        cursor.execute("SELECT module FROM {} ".format(course))
        sql = cursor.fetchall()
        print(sql)
        modules = []
        for module in sql:
            modules.append(str(module[0]))
        return render_template('addcourse.html', lessons=[], topics=[], modules=modules, course = course)
    except Exception as e:
        error = str(e)
        return render_template('addcourse.html', error=error)
    finally:
        cursor.close()
        conn.close()


print('http://{}:5000/'.format(ip))
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

