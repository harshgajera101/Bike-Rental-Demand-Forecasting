from app import app, db
from sqlalchemy import inspect

with app.app_context():  # Ensure you're in the Flask app context
    # Create tables
    db.create_all()
    db.session.commit()
    print("Tables created successfully!")

    # Use SQLAlchemy Inspector to list tables
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()  # Get all table names
    print("Tables in the database:", tables)
