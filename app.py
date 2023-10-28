import flask
from models import db
from index import Index
from login import Login
from registration import Register
from portfolio import PortfolioForm, Data
from update import Update, Update_portfolio



app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.db'
db.init_app(app)
app.secret_key = "bacon"

with app.app_context():
    db.create_all()



# Routes
app.add_url_rule('/',
                 view_func=Index.as_view('main'),
                 methods=["GET"])
app.add_url_rule('/<page>/',
                 view_func=Index.as_view('page'),
                 methods=["GET"])
app.add_url_rule('/login/',
                 view_func=Login.as_view('login'),
                 methods=["GET", "POST"])
app.add_url_rule('/registration/',
                 view_func=Register.as_view('registration'),
                 methods=['GET', 'POST'])
app.add_url_rule('/portfolio_form/',
                 view_func=PortfolioForm.as_view('portfolio_form'),
                 methods=['GET', 'POST'])
app.add_url_rule('/done_portfolio/',
                 view_func=Data.as_view('done_portfolio'),
                 methods=['GET', 'POST'])
app.add_url_rule('/update/',
                 view_func=Update.as_view('update'),
                 methods=['GET', 'POST'])
app.add_url_rule('/update_portfolio/',
                 view_func=Update_portfolio.as_view('update_portfolio'),
                 methods=['GET', 'POST'])

@app.errorhandler(404)
def page_not_found(error):
    return flask.render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
