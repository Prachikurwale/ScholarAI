from app import app, db

with app.app_context():
    print("Deleting old database tables...")
    db.drop_all()
    print("Creating new database tables with updated fields...")
    db.create_all()
    print("✅ Database reset successful!")