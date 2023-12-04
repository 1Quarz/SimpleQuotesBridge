import databases
import sqlalchemy


#DATABASE
DATABASE_URL = "sqlite:///./quotes.db"
engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = sqlalchemy.MetaData()

database = databases.Database(DATABASE_URL)

quotesDB = sqlalchemy.Table(
    "quotes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("quote", sqlalchemy.String, unique=True),
    sqlalchemy.Column("author", sqlalchemy.String),
    sqlalchemy.Column("timestamp", sqlalchemy.DateTime)
)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)
