import logging
from sqlalchemy import inspect
from .models import Base, User, Account, Category, Transaction

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("pocket_money_tracker.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def debug_database_state(engine):
    logger = setup_logging()
    inspector = inspect(engine)
    logger.debug("Database Tables: %s", inspector.get_table_names())
    
    with engine.connect() as connection:
        for table in inspector.get_table_names():
            result = connection.execute(f"SELECT COUNT(*) FROM {table}").scalar()
            logger.debug(f"Table {table} has {result} rows")

def debug_model_instances(session):
    logger = setup_logging()
    models = [User, Account, Category, Transaction]
    for model in models:
        count = session.query(model).count()
        logger.debug(f"{model.__name__} count: {count}")
        instances = session.query(model).all()
        for instance in instances:
            logger.debug(f"{model.__name__}: {instance}")

if __name__ == "__main__":
    from sqlalchemy import create_engine
    engine = create_engine("sqlite:///pocket_money_tracker.db")
    debug_database_state(engine)