import flask, flask.views
from login import users

# будет обновлять информацию пользователя 
# а именно username и password
class Update(flask.views.MethodView):
    def get(self):
        return flask.render_template('update.html')
    
    def post(self):
        action = flask.request.form.get('action')
        username = flask.session['username']
        user_id = users.get_user_id(username)
        
        if action == 'update username':
            new_username = flask.request.form.get('new_username')
            if user_id is not None:
                users.update(user_id, 'username', new_username)
                flask.flash('Username updated successfully', 'info')
                flask.session.pop('username', None)
            
        elif action == 'update password':
            new_password = flask.request.form.get('new_password')
            if user_id is not None:
                users.update(user_id, 'password', new_password)
                flask.flash('Password updated successfully', 'info')
                flask.session.pop('username', None)
        
        return flask.redirect(flask.url_for('login'))

# будет обновлять портфолио пользователя 
class Update_portfolio(flask.views.MethodView):
    def get(self):
        return flask.render_template('update_portfolio.html')
    
    def post(self):
        action = flask.request.form.get('action')
        username = flask.session['username']
        user_id = users.get_user_id(username)
        
        if action == 'update full name':
            new_full_name = flask.request.form.get('new_full_name')
            if user_id is not None:
                users.update_portfolio(user_id, 'full_name', new_full_name)
                flask.flash('ФИО успешно обновлено', 'info')
            
        elif action == 'update email':
            new_email = flask.request.form.get('new_email')
            if user_id is not None:
                users.update_portfolio(user_id, 'email', new_email)
                flask.flash('Электронная почта успешно обновлена', 'info')
        
        elif action == 'update bio':
            new_bio = flask.request.form.get('new_bio')
            if user_id is not None:
                users.update_portfolio(user_id, 'bio', new_bio)
                flask.flash('Биография успешно обновлено', 'info')
            
        elif action == 'update phone number':
            new_phone_number = flask.request.form.get('new_phone_number')
            if user_id is not None:
                users.update_portfolio(user_id, 'phone_number', new_phone_number)
                flask.flash('Номер телефона успешно обновлена', 'info')
        
        return flask.redirect(flask.url_for('login'))