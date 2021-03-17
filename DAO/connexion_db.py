import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os.path


fn = os.path.join(os.path.dirname(__file__), '../stocksdeals.db')

engine = create_engine(f"sqlite:///{fn}")
# conn = sqlite3.connect('../stocksdeas.bd')
Base = declarative_base()
Session = sessionmaker(bind=engine)



