import flask, flask.views
from models import db, User, Portfolio

# саздаю функций для того чтобы просто призвать их 
# при нужде и в других файлах
class Users:
    def __init__(self):
        self.users = {}

    def user_checker(self, username):
        return User.query.filter_by(username=username).count() > 0

    def password_checker(self, username, password):
        return User.query.filter_by(username=username, password=password).count() > 0

    def register_new_user(self, username, password):
        if self.user_checker(username):
            return 'Пользователь уже существует'
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return "Пользователь зарегистрирован"

    def login(self, username, password):
        user = User.query.filter_by(username=username, password=password).first()
        return user is not None

    def delete_account(self, id):
        user = User.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()

    def delete_portfolio(self, user_id):
        Portfolio.query.filter_by(user_id=user_id).delete()
        db.session.commit()

    def update(self, id, arg, new):
        user = User.query.get(id)
        if user:
            setattr(user, arg, new)
            db.session.commit()

    def update_portfolio(self, user_id, arg, new):
        portfolio = Portfolio.query.get(user_id)
        if portfolio:
            setattr(portfolio, arg, new)
            db.session.commit()

    def read(self, user_id):
        user = User.query.get(user_id)
        if user:
            return user.password
        return None
    
    def get_user_id(self, username):
        user = User.query.filter_by(username=username).first()
        if user:
            return user.id
        return None
# Управлять этими функциями
users = Users()

class Login(flask.views.MethodView):
    
    def get(self):
        return flask.render_template('login.html')

    def post(self):
        action = flask.request.form.get('action')

        # Выйти с аккаунта
        if action == 'logout':
            flask.session.pop('username', None)
            return flask.redirect(flask.url_for('login'))

        elif action == 'read':
            # Read operation
            username = flask.session['username']
            user_id = users.get_user_id(username)
            if user_id is not None:
                password = users.read(user_id)
                flask.flash(f'Имя пользователя: {username}, Пароль: {password}', 'info')
            else:
                flask.flash('Пользователь не найден', 'error')
            return flask.redirect(flask.url_for('login'))
        
        elif action == 'update_account':
            # Update account operation
            return flask.redirect(flask.url_for('update'))
        
        elif action == 'update_portfolio':
            # Update portfolio operation
            return flask.redirect(flask.url_for('update_portfolio'))

        elif action == 'delete portfolio':
            # Delete portfolio operation
            username = flask.session['username']
            user_id = users.get_user_id(username)

            if user_id is not None:
                users.delete_portfolio(user_id)
                flask.flash('Портфолио пользователя успешно удалено', 'info')
                return flask.redirect(flask.url_for('login'))
                
            flask.flash('Портфолио не найдено', 'error')
        
        elif action == 'delete account':
            # Delete account operation
            username = flask.session['username']
            user_id = users.get_user_id(username)

            if user_id is not None:
                # Удаляем и его портфолио чтобы оно не засоряло базу данных
                users.delete_portfolio(user_id)
                users.delete_account(user_id)
                flask.session.pop('username', None)
                flask.flash('Учетная запись пользователя успешно удалена', 'info')
                return flask.redirect(flask.url_for('login'))
                
            flask.flash('Пользователь не найден', 'error')

        # обрабатывает POST-запрос, который отправляется при входе пользователя 
        # выполняет аутентификацию пользователя
        else:
            required = ['username', 'passwd']
            for r in required:
                if r not in flask.request.form:
                    flask.flash("Ошибка: {0} требуется.".format(r))
                    return flask.redirect(flask.url_for('login'))
            username = flask.request.form['username']
            passwd = flask.request.form['passwd']

            if users.user_checker(username):
                if users.login(username, passwd):
                    flask.session['username'] = username
                else:
                    flask.flash("имя пользователя не существует или неверный пароль")
            else:
                flask.flash("имя пользователя не существует или неверный пароль")
            return flask.redirect(flask.url_for('login'))