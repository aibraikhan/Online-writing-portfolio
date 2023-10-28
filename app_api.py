from fastapi import FastAPI, HTTPException, Path, Query
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from models import db, Portfolio, User

app = FastAPI(
    title="WriteNow"
)

engine = create_engine('sqlite:///instance/Users.db')
Session = sessionmaker(bind=engine)

@app.get('/users/{user_id}')
def get_user(user_id: int = Path(..., title="User ID", description="The ID of the user")):
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    session.close()
    if user:
        user_dict = {'id': user.id, 'username': user.username, 'password': user.password}
        return user_dict
    raise HTTPException(status_code=404, detail="User not found")

@app.get('/users')
def get_users():
    session = Session()
    users = session.query(User).all()
    user_list = [{'id': user.id, 'username': user.username, 'password': user.password} for user in users]
    session.close()
    return user_list

@app.post('/users')
def create_user(username: str = Query(..., title="Username", description="The username of the user"),
                 password: str = Query(..., title="Password", description="The password of the user")):
    session = Session()
    new_user = User(username=username, password=password)
    session.add(new_user)
    session.commit()
    session.close()
    return {"message": "User created"}

@app.put('/users/{user_id}')
def update_user(
    user_id: int = Path(..., title="User ID", description="The ID of the user"),
    username: str = Query(None, title="New Username", description="The new username of the user"),
    password: str = Query(None, title="New Password", description="The new password of the user"),
):
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        session.close()
        raise HTTPException(status_code=404, detail="User not found")

    if username is not None:
        user.username = username
    if password is not None:
        user.password = password

    session.commit()
    session.close()
    return {"message": "User updated"}

@app.delete('/users/{user_id}')
def delete_user(user_id: int = Path(..., title="User ID", description="The ID of the user")):
    delete_porfolio(user_id)
    session = Session()
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        session.close()
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()
    session.close()
    return {"message": "User deleted"}


# Portfolio table.
@app.get('/portfolios/{user_id}')
def get_portfolio(user_id: int = Path(..., title="User ID", description="The ID of the user")):
    session = Session()
    portfolio_data = session.query(Portfolio).filter_by(user_id=user_id).first()
    session.close()
    if portfolio_data:
        portfolio = {
            'full_name': portfolio_data.full_name,
            'email': portfolio_data.email,
            'bio': portfolio_data.bio,
            'phone_number': portfolio_data.phone_number
        }
        return portfolio
    raise HTTPException(status_code=404, detail="Portfolio not found")


@app.get('/porfolios')
def get_porfolio():
    session = Session()
    portfolio_data = session.query(Portfolio).all()
    portfolio_list = [
        {
            'id': portfolio.id,
            'user_id': portfolio.user_id,
            'full_name': portfolio.full_name,
            'bio': portfolio.bio,
            'email': portfolio.email,
            'phone_number': portfolio.phone_number
        }
        for portfolio in portfolio_data
    ]
    session.close()
    return portfolio_list

@app.post('/porfolios')
def create_porfolio(user_id: int = Query(..., title="User ID", description="The user id of the user"),
                    full_name: str = Query(..., title="Full name", description="The full name of the user"),
                    bio: str = Query(..., title="Bio", description="The Bio of the user"),
                    email: str = Query(..., title="Email", description="The Email of the user"),
                    phone_number: str = Query(..., title="Phone number", description="The Phone Number of the user")):
    session = Session()
    new_portfolio = Portfolio(user_id=user_id, full_name=full_name, bio=bio, email=email, phone_number=phone_number)
    session.add(new_portfolio)
    session.commit()
    session.close()
    return {"message": "Portfolio created"}

@app.put('/porfolios/{user_id}')
def update_porfolio(
    user_id: int = Path(..., title="User ID", description="The ID of the user"),
    full_name: str = Query(None, title="New Full name", description="The new Full name of the user"),
    bio: str = Query(None, title="New Bio", description="The new Bio of the user"),
    email: str = Query(None, title="New Email", description="The new Email of the user"),
    phone_number: str = Query(None, title="New Phone number", description="The new Phone number of the user")
):
    session = Session()
    portfolio_data = session.query(Portfolio).filter_by(user_id=user_id).first()
    if not portfolio_data:
        session.close()
        raise HTTPException(status_code=404, detail="Portfolio not found")

    if full_name is not None:
        portfolio_data.full_name = full_name
    if bio is not None:
        portfolio_data.bio = bio
    if email is not None:
        portfolio_data.email = email
    if phone_number is not None:
        portfolio_data.phone_number = phone_number

    session.commit()
    session.close()
    return {"message": "Portfolio updated"}

@app.delete('/porfolios/{user_id}')
def delete_porfolio(user_id: int = Path(..., title="User ID", description="The ID of the user")):
    session = Session()
    portfolio_data = session.query(Portfolio).filter_by(user_id=user_id).first()
    if not portfolio_data:
        session.close()
        raise HTTPException(status_code=404, detail="Portfolio not found")

    session.delete(portfolio_data)
    session.commit()
    session.close()
    return {"message": "Portfolio deleted"}