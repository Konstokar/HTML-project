from add_news_form import AddNewsForm
from db import DB
from flask import Flask, redirect, render_template, session, request
from login_form import LoginForm
from news_model import NewsModel
from users_model import UsersModel
from register_form import RegisterModel

import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db = DB()
UsersModel(db.get_connection()).init_table()

flag_perm = False


def make_session_permanent():
    session.permanent = False


@app.route('/login', methods=['GET', 'POST'])
def login():
    global flag_perm
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        perm = form.remember_me.data
        user_model = UsersModel(db.get_connection())
        exists = user_model.exists(user_name, password)
        if exists[0]:
            session['username'] = user_name
            session['user_id'] = exists[1]
            if perm:
                session.permanent = True
                flag_perm = True
            else:
                session.permanent = False
                flag_perm = True
            return redirect("/index")
        else:
            return render_template('login.html', form=form, error=1)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')


@app.route('/')
@app.route('/index/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        if 'username' not in session or not flag_perm and not session.permanent:
            if "username" in session:
                return redirect("/logout")
            return redirect('/login')
        if request.method == 'GET':
            return '''<!doctype html>
                                <html lang="en">
                                  <head>
                                    <meta charset="utf-8">
                                    <meta name="viewport"
                                    content="width=device-width, initial-scale=1, shrink-to-fit=no">
                                    <link rel="stylesheet"
                                    href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                    integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                    crossorigin="anonymous">
                                    <title>Введение</title>
                                  </head>
                                  <body>
                                    <h1>Поздравляем с регистрацией в нашей системе отдыха и медитации! На нашем сайте Вы можете смотреть релаксационные фильмы и слушать расслабляющую музыку. Для того, чтобы начать отдыхать, выберите "Далее", если нет - выберите "Выход", и нажмите "Подтвердить".</h1>
                                    <form method="post">
                                        <div class="form-group">
                                            <label for="classSelect">Выберите, что Вы будете делать</label>
                                            <select class="form-control" id="classSelect" name="class">
                                              <option>Далее</option>
                                              <option>Выход</option>
                                            </select>
                                         </div>
                                        <button type="submit" class="btn btn-primary">Подтвердить</button>
                                    </form>
                                  </body>
                                </html>'''
    elif request.method == 'POST':
        if request.form['class'] == 'Далее':
            return redirect('/further')
        else:
            return redirect('/logout')


@app.route('/further', methods=['POST', 'GET'])
def further():
    if request.method == 'GET':
        return '''<!doctype html>
                                    <html lang="en">
                                      <head>
                                        <meta charset="utf-8">
                                        <meta name="viewport"
                                        content="width=device-width, initial-scale=1, shrink-to-fit=no">
                                        <link rel="stylesheet"
                                        href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                        integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                        crossorigin="anonymous">
                                        <title>Просмотр (прослушивание)</title>
                                      </head>
                                      <body>
                                        <h1>Просмотр (прослушивание)</h1>
                                        <form method="post">
                                            <div class="form-group">
                                                <label for="classSelect">Выберите, что Вы будете делать, и нажмите "Продолжить"</label>
                                                <select class="form-control" id="classSelect" name="class">
                                                  <option>Смотреть кино</option>
                                                  <option>Слушать музыку</option>
                                                  <option>Выйти</option>
                                                </select>
                                             </div>
                                            <button type="submit" class="btn btn-primary">Продолжить</button>
                                        </form>
                                      </body>
                                    </html>'''
    elif request.method == 'POST':
        if request.form['class'] == 'Смотреть кино':
            return redirect('/cinema')
        elif request.form['class'] == 'Слушать музыку':
            return redirect('/music')
        elif request.form['class'] == 'Выйти':
            return redirect('/logout')


@app.route('/cinema', methods=['POST', 'GET'])
def cinema():
    if request.method == 'GET':
        return '''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport"
                            content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                            href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                            integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                            crossorigin="anonymous">
                            <title>Кино</title>
                          </head>
                          <body>
                            <h1>Кино</h1>
                            <form method="post">
                                <div class="form-group">
                                    <label for="classSelect">Выберите фильм, который Вы хотите посмотреть</label>
                                    <select class="form-control" id="classSelect" name="class">
                                      <option>Ambra. Child of the Universe</option>
                                      <option>Ambra. Honour and Glory</option>
                                      <option>Симфония камня</option>
                                      <option>Спящая стихия</option>
                                      <option>Величие водопадов</option>
                                      <option>Faszination Natur</option>
                                      <option>Faszination Natur 2</option>
                                      <option>Faszination Natur 3</option>
                                    </select>
                                 </div>
                                 <button type="submit" class="btn btn-primary">Смотреть</button>
                            </form>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        if request.form['class'] == 'Ambra. Child of the Universe':
            return '''<!doctype html>
                                <html lang="en">
                                  <head>
                                    <meta charset="utf-8">
                                    <meta name="viewport" content="width=device-width,
                                    initial-scale=1, shrink-to-fit=no">
                                    <link rel="stylesheet"
                                    href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                    integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                    crossorigin="anonymous">
                                    <title>Ambra. Child of the Universe</title>
                                  </head>
                                  <body>
                <div class="embed-responsive embed-responsive-16by9">
                  <iframe width="723" height="409" src="https://www.youtube.com/embed/_ArftSx9B7o" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                </div>
                                  </body>
                                </html>
                '''
        if request.form['class'] == 'Ambra. Honour and Glory':
            return '''<!doctype html>
                    <html lang="en">
                      <head>
                        <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width,
                        initial-scale=1, shrink-to-fit=no">
                        <link rel="stylesheet"
                        href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                        integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                        crossorigin="anonymous">
                        <title>Ambra. Honour and Glory</title>
                      </head>
                      <body>
    <div class="embed-responsive embed-responsive-16by9">
      <iframe width="784" height="409" src="https://www.youtube.com/embed/PkJl8tcgrpM" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>
                      </body>
                    </html>
    '''
        if request.form['class'] == 'Симфония камня':
            return '''<!doctype html>
                                <html lang="en">
                                  <head>
                                    <meta charset="utf-8">
                                    <meta name="viewport" content="width=device-width,
                                    initial-scale=1, shrink-to-fit=no">
                                    <link rel="stylesheet"
                                    href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                    integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                    crossorigin="anonymous">
                                    <title>Симфония камня</title>
                                  </head>
                                  <body>
                <div class="embed-responsive embed-responsive-16by9">
                  <iframe width="545" height="409" src="https://www.youtube.com/embed/0Qcu4N6rH10" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                </div>
                                  </body>
                                </html>
                '''
        if request.form['class'] == 'Спящая стихия':
            return '''<!doctype html>
                                <html lang="en">
                                  <head>
                                    <meta charset="utf-8">
                                    <meta name="viewport" content="width=device-width,
                                    initial-scale=1, shrink-to-fit=no">
                                    <link rel="stylesheet"
                                    href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                    integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                    crossorigin="anonymous">
                                    <title>Спящая стихия</title>
                                  </head>
                                  <body>
                <div class="embed-responsive embed-responsive-16by9">
                  <iframe width="545" height="409" src="https://www.youtube.com/embed/0Qcu4N6rH10" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                </div>
                                  </body>
                                </html>
                '''
        if request.form['class'] == 'Величие водопадов':
            return '''<!doctype html>
                                <html lang="en">
                                  <head>
                                    <meta charset="utf-8">
                                    <meta name="viewport" content="width=device-width,
                                    initial-scale=1, shrink-to-fit=no">
                                    <link rel="stylesheet"
                                    href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                    integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                    crossorigin="anonymous">
                                    <title>Величие водопадов</title>
                                  </head>
                                  <body>
                <div class="embed-responsive embed-responsive-16by9">
                  <iframe width="559" height="409" src="https://www.youtube.com/embed/91Fmr52-SzQ" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                </div>
                                  </body>
                                </html>
                '''
        if request.form['class'] == 'Faszination Natur':
            return '''<!doctype html>
                                <html lang="en">
                                  <head>
                                    <meta charset="utf-8">
                                    <meta name="viewport" content="width=device-width,
                                    initial-scale=1, shrink-to-fit=no">
                                    <link rel="stylesheet"
                                    href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                    integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                    crossorigin="anonymous">
                                    <title>Faszination Natur</title>
                                  </head>
                                  <body>
                <div class="embed-responsive embed-responsive-16by9">
                  <iframe width="727" height="409" src="https://www.youtube.com/embed/Buu4ZHkuIuk" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                </div>
                                  </body>
                                </html>
                '''
        if request.form['class'] == 'Faszination Natur 2':
            return '''<!doctype html>
                                <html lang="en">
                                  <head>
                                    <meta charset="utf-8">
                                    <meta name="viewport" content="width=device-width,
                                    initial-scale=1, shrink-to-fit=no">
                                    <link rel="stylesheet"
                                    href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                    integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                    crossorigin="anonymous">
                                    <title>Faszination Natur 2</title>
                                  </head>
                                  <body>
                <div class="embed-responsive embed-responsive-16by9">
                  <iframe width="545" height="409" src="https://www.youtube.com/embed/yYrRYvDqscg" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                </div>
                                  </body>
                                </html>
                '''
        if request.form['class'] == 'Faszination Natur 3':
            return '''<!doctype html>
                                <html lang="en">
                                  <head>
                                    <meta charset="utf-8">
                                    <meta name="viewport" content="width=device-width,
                                    initial-scale=1, shrink-to-fit=no">
                                    <link rel="stylesheet"
                                    href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                    integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                    crossorigin="anonymous">
                                    <title>Faszination Natur 3</title>
                                  </head>
                                  <body>
                <div class="embed-responsive embed-responsive-16by9">
                  <iframe width="727" height="409" src="https://www.youtube.com/embed/QOaJbY6B0C8" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                </div>
                                  </body>
                                </html>
                '''


@app.route('/music', methods=['POST', 'GET'])
def music():
    if request.method == 'GET':
        return '''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <meta name="viewport"
                    content="width=device-width, initial-scale=1, shrink-to-fit=no">
                    <link rel="stylesheet"
                    href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                    integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                    crossorigin="anonymous">
                    <title>Music</title>
                  </head>
                  <body>
                    <h1>Музыка</h1>
                    <form method="post">
                        <div class="form-group">
                            <label for="classSelect">Какой альбом Вы хотите прослушать?</label>
                            <select class="form-control" id="classSelect" name="class">
                              <option>Best_of_Ambra</option>
                            </select>
                         </div>
                        <button type="submit" class="btn btn-primary">Слушать</button>
                    </form>
                  </body>
                </html>'''
    elif request.method == 'POST':
        if request.form['class'] == 'Best_of_Ambra':
            return redirect('/Best_of_Ambra')


@app.route('/Best_of_Ambra', methods=['POST', 'GET'])
def Best_of_Ambra():
    if request.method == 'GET':
        return '''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport"
                                content="width=device-width, initial-scale=1, shrink-to-fit=no">
                                <link rel="stylesheet"
                                href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                crossorigin="anonymous">
                                <title>Альбом</title>
                              </head>
                              <body>
                                <h1>Best of Ambra</h1>
                                <form method="post">
                                    <div class="form-group">
                                        <label for="classSelect">Какую песню Вы хотите прослушать?</label>
                                        <select class="form-control" id="classSelect" name="class">
                                          <option>The Rebirth of the Sun</option>
                                          <option>Paradise Lost</option>
                                          <option>Prism of Life</option>
                                          <option>Le Prisme De La Vie</option>
                                          <option>Caleidoscope, Pt. 2</option>
                                          <option>The Eye of the Storm</option>
                                          <option>Signs of Love</option>
                                          <option>Walking in the Air</option>
                                          <option>Wanderer Between the Worlds</option>
                                          <option>Saale-The Prophecy</option>
                                          <option>Enlighten</option>
                                          <option>The Futute</option>
                                          <option>Eclipse of the Moon</option>
                                          <option>Journey to Your Heart</option>
                                          <option>Jewel of Light</option>
                                          <option>Moments of Redemption</option>
                                        </select>
                                     </div>
                                    <button type="submit" class="btn btn-primary">Слушать</button>
                                </form>
                              </body>
                            </html>'''
    elif request.method == 'POST':
        if request.form['class'] == 'The Rebirth of the Sun':
            return '''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport" content="width=device-width,
                                initial-scale=1, shrink-to-fit=no">
                                <link rel="stylesheet"
                                href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                crossorigin="anonymous">
                                <title>Привет, Яндекс!</title>
                              </head>
                              <body>
                                <div class="embed-responsive embed-responsive-16by9">
              <iframe frameborder="0" style="border:none;width:600px;height:100px;" width="600" height="100" src="https://music.yandex.ru/iframe/#track/40304124/5235137/">Слушайте <a href='https://music.yandex.ru/album/5235137/track/40304124'>The Rebirth of the Sun</a> — <a href='https://music.yandex.ru/artist/809983'>Ambra</a> на Яндекс.Музыке</iframe>
            </div>
                              </body>
                            </html>
            '''
        elif request.form['class'] == 'Paradise Lost':
            return '''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport" content="width=device-width,
                                initial-scale=1, shrink-to-fit=no">
                                <link rel="stylesheet"
                                href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                crossorigin="anonymous">
                                <title>Привет, Яндекс!</title>
                              </head>
                              <body>
                                <div class="embed-responsive embed-responsive-16by9">
              <iframe frameborder="0" style="border:none;width:600px;height:100px;" width="600" height="100" src="https://music.yandex.ru/iframe/#track/40304125/5235137/">Слушайте <a href='https://music.yandex.ru/album/5235137/track/40304125'>Paradise Lost</a> — <a href='https://music.yandex.ru/artist/809983'>Ambra</a> на Яндекс.Музыке</iframe>
            </div>
                              </body>
                            </html>
            '''
        elif request.form['class'] == 'Prism of Life':
            return '''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport" content="width=device-width,
                                initial-scale=1, shrink-to-fit=no">
                                <link rel="stylesheet"
                                href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                crossorigin="anonymous">
                                <title>Привет, Яндекс!</title>
                              </head>
                              <body>
                                <div class="embed-responsive embed-responsive-16by9">
              <iframe frameborder="0" style="border:none;width:600px;height:100px;" width="600" height="100" src="https://music.yandex.ru/iframe/#track/40304126/5235137/">Слушайте <a href='https://music.yandex.ru/album/5235137/track/40304126'>Prism of Life</a> — <a href='https://music.yandex.ru/artist/809983'>Ambra</a> на Яндекс.Музыке</iframe>
            </div>
                              </body>
                            </html>
            '''
        elif request.form['class'] == 'Le Prisme De La Vie':
            return '''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport" content="width=device-width,
                                initial-scale=1, shrink-to-fit=no">
                                <link rel="stylesheet"
                                href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                crossorigin="anonymous">
                                <title>Привет, Яндекс!</title>
                              </head>
                              <body>
                                <div class="embed-responsive embed-responsive-16by9">
              <iframe frameborder="0" style="border:none;width:600px;height:100px;" width="600" height="100" src="https://music.yandex.ru/iframe/#track/40304127/5235137/">Слушайте <a href='https://music.yandex.ru/album/5235137/track/40304127'>Le Prisme De La Vie</a> — <a href='https://music.yandex.ru/artist/809983'>Ambra</a> на Яндекс.Музыке</iframe>
            </div>
                              </body>
                            </html>
            '''
        elif request.form['class'] == 'Caleidoscope, Pt. 2':
            return '''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport" content="width=device-width,
                                initial-scale=1, shrink-to-fit=no">
                                <link rel="stylesheet"
                                href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                crossorigin="anonymous">
                                <title>Привет, Яндекс!</title>
                              </head>
                              <body>
                                <div class="embed-responsive embed-responsive-16by9">
              <iframe frameborder="0" style="border:none;width:600px;height:100px;" width="600" height="100" src="https://music.yandex.ru/iframe/#track/40304128/5235137/">Слушайте <a href='https://music.yandex.ru/album/5235137/track/40304128'>Caleidoscope, Pt. 2</a> — <a href='https://music.yandex.ru/artist/809983'>Ambra</a> на Яндекс.Музыке</iframe>
            </div>
                              </body>
                            </html>
            '''
        elif request.form['class'] == 'The Eye of the Storm':
            return '''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport" content="width=device-width,
                                initial-scale=1, shrink-to-fit=no">
                                <link rel="stylesheet"
                                href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                crossorigin="anonymous">
                                <title>Привет, Яндекс!</title>
                              </head>
                              <body>
                                <div class="embed-responsive embed-responsive-16by9">
              <iframe frameborder="0" style="border:none;width:600px;height:100px;" width="600" height="100" src="https://music.yandex.ru/iframe/#track/40304129/5235137/">Слушайте <a href='https://music.yandex.ru/album/5235137/track/40304129'>The Eye of the Storm</a> — <a href='https://music.yandex.ru/artist/809983'>Ambra</a> на Яндекс.Музыке</iframe>
            </div>
                              </body>
                            </html>
            '''
        elif request.form['class'] == 'Signs of Love':
            return '''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport" content="width=device-width,
                                initial-scale=1, shrink-to-fit=no">
                                <link rel="stylesheet"
                                href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                crossorigin="anonymous">
                                <title>Привет, Яндекс!</title>
                              </head>
                              <body>
                                <div class="embed-responsive embed-responsive-16by9">
              <iframe frameborder="0" style="border:none;width:600px;height:100px;" width="600" height="100" src="https://music.yandex.ru/iframe/#track/40304130/5235137/">Слушайте <a href='https://music.yandex.ru/album/5235137/track/40304130'>Signs of Love</a> — <a href='https://music.yandex.ru/artist/809983'>Ambra</a> на Яндекс.Музыке</iframe>
            </div>
                              </body>
                            </html>
            '''
        elif request.form['class'] == 'Walking in the Air':
            return '''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport" content="width=device-width,
                                initial-scale=1, shrink-to-fit=no">
                                <link rel="stylesheet"
                                href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                crossorigin="anonymous">
                                <title>Привет, Яндекс!</title>
                              </head>
                              <body>
                                <div class="embed-responsive embed-responsive-16by9">
              <iframe frameborder="0" style="border:none;width:600px;height:100px;" width="600" height="100" src="https://music.yandex.ru/iframe/#track/40304131/5235137/">Слушайте <a href='https://music.yandex.ru/album/5235137/track/40304131'>Walking in the Air</a> — <a href='https://music.yandex.ru/artist/809983'>Ambra</a> на Яндекс.Музыке</iframe>
            </div>
                              </body>
                            </html>
            '''
        elif request.form['class'] == 'Wanderer Between the Worlds':
            return '''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport" content="width=device-width,
                                initial-scale=1, shrink-to-fit=no">
                                <link rel="stylesheet"
                                href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                crossorigin="anonymous">
                                <title>Привет, Яндекс!</title>
                              </head>
                              <body>
                                <div class="embed-responsive embed-responsive-16by9">
              <iframe frameborder="0" style="border:none;width:600px;height:100px;" width="600" height="100" src="https://music.yandex.ru/iframe/#track/40304132/5235137/">Слушайте <a href='https://music.yandex.ru/album/5235137/track/40304132'>Wanderer Between the Worlds</a> — <a href='https://music.yandex.ru/artist/809983'>Ambra</a> на Яндекс.Музыке</iframe>
            </div>
                              </body>
                            </html>
            '''
        elif request.form['class'] == 'Saale-The Prophecy':
            return '''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport" content="width=device-width,
                                initial-scale=1, shrink-to-fit=no">
                                <link rel="stylesheet"
                                href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                crossorigin="anonymous">
                                <title>Привет, Яндекс!</title>
                              </head>
                              <body>
                                <div class="embed-responsive embed-responsive-16by9">
              <iframe frameborder="0" style="border:none;width:600px;height:100px;" width="600" height="100" src="https://music.yandex.ru/iframe/#track/40304133/5235137/">Слушайте <a href='https://music.yandex.ru/album/5235137/track/40304133'>Saale-The Prophecy</a> — <a href='https://music.yandex.ru/artist/809983'>Ambra</a> на Яндекс.Музыке</iframe>
            </div>
                              </body>
                            </html>
            '''
        elif request.form['class'] == 'Enlighten':
            return '''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport" content="width=device-width,
                                initial-scale=1, shrink-to-fit=no">
                                <link rel="stylesheet"
                                href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                crossorigin="anonymous">
                                <title>Привет, Яндекс!</title>
                              </head>
                              <body>
                                <div class="embed-responsive embed-responsive-16by9">
              <iframe frameborder="0" style="border:none;width:600px;height:100px;" width="600" height="100" src="https://music.yandex.ru/iframe/#track/40304134/5235137/">Слушайте <a href='https://music.yandex.ru/album/5235137/track/40304134'>Enlighten</a> — <a href='https://music.yandex.ru/artist/809983'>Ambra</a> на Яндекс.Музыке</iframe>
            </div>
                              </body>
                            </html>
            '''
        elif request.form['class'] == 'The Futute':
            return '''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport" content="width=device-width,
                                initial-scale=1, shrink-to-fit=no">
                                <link rel="stylesheet"
                                href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                crossorigin="anonymous">
                                <title>Привет, Яндекс!</title>
                              </head>
                              <body>
                                <div class="embed-responsive embed-responsive-16by9">
              <iframe frameborder="0" style="border:none;width:600px;height:100px;" width="600" height="100" src="https://music.yandex.ru/iframe/#track/40304135/5235137/">Слушайте <a href='https://music.yandex.ru/album/5235137/track/40304135'>The Futute</a> — <a href='https://music.yandex.ru/artist/809983'>Ambra</a> на Яндекс.Музыке</iframe>
            </div>
                              </body>
                            </html>
            '''
        elif request.form['class'] == 'Eclipse of the Moon':
            return '''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport" content="width=device-width,
                                initial-scale=1, shrink-to-fit=no">
                                <link rel="stylesheet"
                                href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                crossorigin="anonymous">
                                <title>Привет, Яндекс!</title>
                              </head>
                              <body>
                                <div class="embed-responsive embed-responsive-16by9">
              <iframe frameborder="0" style="border:none;width:600px;height:100px;" width="600" height="100" src="https://music.yandex.ru/iframe/#track/40304136/5235137/">Слушайте <a href='https://music.yandex.ru/album/5235137/track/40304136'>Eclipse of the Moon</a> — <a href='https://music.yandex.ru/artist/809983'>Ambra</a> на Яндекс.Музыке</iframe>
            </div>
                              </body>
                            </html>
            '''
        elif request.form['class'] == 'Journey to Your Heart':
            return '''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport" content="width=device-width,
                                initial-scale=1, shrink-to-fit=no">
                                <link rel="stylesheet"
                                href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                crossorigin="anonymous">
                                <title>Привет, Яндекс!</title>
                              </head>
                              <body>
                                <div class="embed-responsive embed-responsive-16by9">
<iframe frameborder="0" style="border:none;width:600px;height:100px;" width="600" height="100" src="https://music.yandex.ru/iframe/#track/40304137/5235137/">Слушайте <a href='https://music.yandex.ru/album/5235137/track/40304137'>Journey to Your Heart</a> — <a href='https://music.yandex.ru/artist/809983'>Ambra</a> на Яндекс.Музыке</iframe>
            </div>
                              </body>
                            </html>
            '''
        elif request.form['class'] == 'Jewel of Light':
            return '''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport" content="width=device-width,
                                initial-scale=1, shrink-to-fit=no">
                                <link rel="stylesheet"
                                href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                crossorigin="anonymous">
                                <title>Привет, Яндекс!</title>
                              </head>
                              <body>
                                <div class="embed-responsive embed-responsive-16by9">
              <iframe frameborder="0" style="border:none;width:600px;height:100px;" width="600" height="100" src="https://music.yandex.ru/iframe/#track/40304138/5235137/">Слушайте <a href='https://music.yandex.ru/album/5235137/track/40304138'>Jewel of Light</a> — <a href='https://music.yandex.ru/artist/809983'>Ambra</a> на Яндекс.Музыке</iframe>
            </div>
                              </body>
                            </html>
            '''
        elif request.form['class'] == 'Moments of Redemption':
            return '''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport" content="width=device-width,
                                initial-scale=1, shrink-to-fit=no">
                                <link rel="stylesheet"
                                href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                crossorigin="anonymous">
                                <title>Привет, Яндекс!</title>
                              </head>
                              <body>
                                <div class="embed-responsive embed-responsive-16by9">
              <iframe frameborder="0" style="border:none;width:600px;height:100px;" width="600" height="100" src="https://music.yandex.ru/iframe/#track/40304139/5235137/">Слушайте <a href='https://music.yandex.ru/album/5235137/track/40304139'>Moments of Redemption</a> — <a href='https://music.yandex.ru/artist/809983'>Ambra</a> на Яндекс.Музыке</iframe>
            </div>
                              </body>
                            </html>
            '''


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
