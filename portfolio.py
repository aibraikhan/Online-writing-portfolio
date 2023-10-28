import flask, flask.views
from models import db, Portfolio
from login import users

class PortfolioForm(flask.views.MethodView):
    def get(self):
        # Проверка есть ли у пользователя портфолио 
        # если есть то направляем на done_portfolio 
        # еслт нет то на portfolio_form
        username = flask.session['username']
        user_id = users.get_user_id(username)
        portfolio_data = Portfolio.query.filter_by(user_id=user_id).first()
        if portfolio_data:
            return flask.redirect(flask.url_for('done_portfolio'))
        
        return flask.render_template('portfolio_form.html')

    def post(self):
        # Получение данных формы
        full_name = flask.request.form['full_name']
        bio = flask.request.form['bio']
        email = flask.request.form['email']
        phone_number = flask.request.form['phone_number']

        username = flask.session['username']
        user_id = users.get_user_id(username)
        
        # Хранение данных в базе данных
        new_portfolio = Portfolio(user_id=user_id, full_name=full_name,
                                  bio=bio, email=email, phone_number=phone_number)
        db.session.add(new_portfolio)
        db.session.commit()

        flask.flash('Данные портфолио успешно представлены', 'success')
        return flask.redirect(flask.url_for('done_portfolio'))

class Data(flask.views.MethodView):
    def get(self, page=None):
        username = flask.session['username']
        user_id = users.get_user_id(username)
        
        portfolio_data = Portfolio.query.filter_by(user_id=user_id).first()
        if portfolio_data is None:
            # Если нет портфолио
            return flask.redirect(flask.url_for('portfolio_form'))
        else:
            # Если есть портфолио
            return flask.render_template('done_portfolio.html', name=portfolio_data.full_name,
                                         email=portfolio_data.email, bio=portfolio_data.bio,
                                         phone=portfolio_data.phone_number)
