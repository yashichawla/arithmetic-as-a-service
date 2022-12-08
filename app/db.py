import os
import pytz
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()
IST = pytz.timezone("Asia/Kolkata")


class LoggingDatabase:
    def __init__(self):
        DATABASE_URL = os.environ["DATABASE_URL"]
        self.Base = declarative_base()
        self.engine = create_engine(DATABASE_URL)
        self.connection = self.engine.connect()
        self.metadata = MetaData()
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        self.setup_tables()

        self.logging_table = Table(
            "logging", self.metadata, autoload=True, autoload_with=self.engine
        )

    def setup_tables(self):
        with open("app/setup_db.sql") as f:
            queries = f.read().strip().split("\n\n")
            for query in queries:
                try:
                    self.connection.execute(query)
                except Exception as e:
                    print("Error while executing query: ", query)

    def getlogginginfo(self):
        query = self.logging_table.select()
        result = self.connection.execute(query)
        return result

    def getCount(self, start_time):
        query = self.logging_table.select().where(
            self.logging_table.c.time > start_time
        )
        result = self.connection.execute(query)
        return result.rowcount

    def uniqueCount(self, start_time):
        query = (
            self.logging_table.select()
            .where(self.logging_table.c.time > start_time)
            .distinct(self.logging_table.c.ip)
        )
        result = self.connection.execute(query)
        return result.rowcount

    def log(self, site_name, request):
        query = self.logging_table.insert().values(
            site=site_name,
            time=datetime.now(IST),
            ip=(
                request.headers.getlist("X-Forwarded-For")[0]
                if request.headers.getlist("X-Forwarded-For")
                else request.remote_addr
            ),
            browser=request.user_agent.browser,
            platform=request.user_agent.platform,
        )
        result = self.connection.execute(query)
        return result
