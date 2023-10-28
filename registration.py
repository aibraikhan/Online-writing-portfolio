import flask, flask.views
from login import users

# регистрация пользователя
class Register(flask.views.MethodView):
    def get(self):
        return flask.render_template('registration.html')
    def post(self):
        required = ['username', 'password']
        for r in required:
            if r not in flask.request.form:
                flask.flash("Ошибка: {0} требуется.".format(r))
                return flask.redirect(flask.url_for('registration'))
        username = flask.request.form['username']
        passwd = flask.request.form['password']

        if users.user_checker(username):
            flask.flash("Имя пользователя уже существует. Пожалуйста, выберите другое имя пользователя.")
            return flask.redirect(flask.url_for('registration'))

        result = users.register_new_user(username, passwd)
        flask.flash(result)
        return flask.redirect(flask.url_for('login'))
