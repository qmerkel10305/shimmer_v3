from orm.database import get_db
from utils.tools import create_test_data

if __name__ == "__main__":
    """
    Script to create test flights in database
    """
    db = get_db()
    create_test_data(db)
