from app import app
from flask import render_template, flash, redirect, url_for
from main import *
from forms import LoginForm, RegistrationForm, RateForm
from flask_login import logout_user, login_required, login_user, current_user
from models import User
import logging

global user

@app.route('/')         # сюда можно переместить индекс, и заменить все ссылки func на index
def func():
    con.cursor()
    cur.execute("SELECT year, seasons, name, main_img, slug "
                "FROM serial")

    serials = cur.fetchall()
    serials_list = []
    for serial in serials:
        dict_serial = {'year': serial[0],
                       'season': serial[1],
                       'name': serial[2],
                       'main_img': serial[3],
                       'rate': get_rate(serial[2]),
                       'genre_name': get_genre(serial[2]),
                       'href': serial[4]
                       }
        serials_list.append(dict_serial)
    return render_template('index.html', serials=serials_list)


@app.route('/index')
@login_required # это чтобы сюда могли зайти только авторизированные пользователи
def index():
    return redirect(url_for('func'))


@app.route('/serials/<serial>')
def serial_detail(serial):
    cur.execute("SELECT * FROM serial WHERE slug = '{name}'".format(name=serial))
    information = cur.fetchall()
    serial_info = []
    for info in information:
        dict_info = {'name': info[0],
                     'year': info[1],
                     'rate': get_rate(info[0]),  # info[0] тк это имя сериала
                     'seasons': info[3],
                     'country': info[4],
                     'producer': info[5],
                     'screenwriter': info[6],
                     'plot': info[7],
                     'main_img': info[8],
                     'dop_img1': info[9],
                     'dop_img2': info[10],
                     'dop_img3': info[11],
                     'actors': get_actors_by_serial(info[0]),
                     'genre': get_genre(info[0])
                     }
        serial_info.append(dict_info)
    # думаю в этом роуте нужно сделать оценку сериала для зарег. пользователя

    if current_user.is_authenticated:
        r_form = RateForm()
        if r_form.validate_on_submit():
            try:
                cur.execute("INSERT INTO rate(rate, user_id, serial_name)" 
                "VALUES ('{}','{}','{}')".format(r_form.rate.data, current_user.id, serial_name))
                con.commit()
            except:
                logging.exception()
                cur.execute("ROLLBACK")
                con.commit()
            return redirect(url_for('serial_detail'))

    return render_template('serial_detail.html', serials = serial_info)


def get_actors_by_serial(serial_name):
    cur.execute("SELECT fio FROM actor_serial WHERE serial_name = '{serial_name}'".format(serial_name=serial_name))
    actors = cur.fetchall()
    actor_list = []
    for actor in actors:
        dict_actor = {'name': actor[0]}
        actor_list.append(dict_actor)
    return actor_list


def get_rate(serial_name):  # получается, что ты передашь в эту функцию название сериала, а по нему уже сделвешь запрос
    cur.execute("select AVG(rate) from rate where serial_name = '{serial_name}'".format(serial_name=serial_name))
    rate = cur.fetchone()  # fetchone тк у тебя будет 1 столбец всего 100%
    return round(rate[0], 1) # если у сериала нет ни одной оценки - ошибка, тк нельзя округлить NULL


def get_genre(serial_name):
    cur.execute("SELECT genre_name FROM genre_serial WHERE serial_name='{serial_name}'".format(serial_name=serial_name))
    genre = cur.fetchone()
    return genre[0]

####
""" def seasons(serial_name):
    cur.execute("SELECT * FROM season WHERE serial_name= '{serial_name}'".format(serial_name=serial_name))
    seasons = cur.fetchall()
    season_list = []
    for series in season:
        dict_season = {'number': season[0]}
        season_list.append(dict_season)
        cur.execute("SELECT * FROM series WHERE serial_name= '{serial_name}'".format(serial_name=serial_name))
        series_list = []
        for seria in series:
            dict_seria = {'name': seria[0],
                          'date': seria[3]}
            series_list.append(dict_seria)
            return series_list
        return season_list """
####

@app.route('/seasons')  #('/seasons/<serial name>')
def ss():
    season_list = ['1','2','3']
    season_list.append(season_list)

    series_list=['flby ldf','nhb','xtnsht']
    series_list.append(series_list)
    return render_template('season_series.html', seasons=season_list, series=series_list)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        cur.execute("SELECT * FROM username")  # [0] - id
        users = cur.fetchall()
        for a_user in users:
            print(a_user)
            if a_user[1] == username and a_user[2] == password:
                user = User(a_user[0])
                login_user(user, remember=login_form.remember_me.data)
                return redirect(url_for('index'))
    return render_template('login.html', form=login_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('func'))


@app.route('/register', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        print('form.register succeed')
        try:
            cur.execute("INSERT INTO username (username, password)"
                        "VALUES ('{}', '{}')".format(reg_form.username.data, reg_form.password.data))
            con.commit()
        except:
            logging.exception('')
            print('user not registered')
            cur.execute("ROLLBACK")
            con.commit()
        return redirect(url_for('login'))
    return render_template('registration.html', form=reg_form)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


# con.close()
