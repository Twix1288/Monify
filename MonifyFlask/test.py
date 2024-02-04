from MonifyFlask.models import Users, db
from MonifyFlask import app

# Create an application context
with app.app_context():
    # Query all users
    all_users = Users.query.all()

    # Print user details
    for user in all_users:
        print(f"Username: {user.username}, Email: {user.email}, Age: {user.age}")