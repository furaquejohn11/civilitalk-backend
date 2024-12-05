from sqlmodel import create_engine, SQLModel, Session

sqlite_file_name = "db/civilitalk.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)


def get_session():
    """Generates a database session to be used in route functions."""
    with Session(engine) as session:
        yield session
