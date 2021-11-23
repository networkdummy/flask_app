from app import db, create_app
import os.path
#with app.app_context():
app = create_app()
app.app_context().push()
db.create_all()