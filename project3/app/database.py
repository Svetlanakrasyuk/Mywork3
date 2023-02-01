from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import redis

host = "localhost"
port = "5432"
user = "postgres"
password = "my_password"
db = "mydb"
dbtype = "postgresql"

# connect Docker DB
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:my_password@db:5432/mydb"

# connect localhost DB
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:my_password@localhost:5432/mydb"

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, executemany_mode='values_plus_batch',
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# decoded_connection = redis.Redis(decode_responses=True)
pool = redis.ConnectionPool(host='cashe', port=6379, db=0)
decoded_connection = redis.Redis(
    connection_pool=pool, decode_responses=True,
)
