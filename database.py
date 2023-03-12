from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine = create_engine("sqlite:///inventory.db", echo=True)
base = declarative_base()
Session = sessionmaker()
local_session = Session(bind=engine)


class Product(base):

    __tablename__ = "product_list"

    product_id = Column(Integer, primary_key = True)
    product_name = Column(String(100), nullable=False, unique=True)
    product_qty = Column(Integer, nullable=False)
    date_added = Column(DateTime, default=datetime.now())

    def __repr__(self):
        return f"product_list(product_id={self.product_id} product_name={self.product_name} product_qty={self.product_qty} date_added = {self.date_added})"


class Location(base):

    __tablename__ = "location_list"

    location_id = Column(Integer, primary_key = True)
    location_name = Column(String(100), nullable=False, unique=True)
    date_added = Column(DateTime, default=datetime.now())

    def __repr__(self):
        return f"location_list(location_id={self.location_id} location_name={self.location_name} date_added={self.date_added})"


class Movement(base):

    __tablename__ = "movement_list"
    movement_id = Column(Integer, primary_key = True)
    timestamp = Column(DateTime, default=datetime.now())
    product_name = Column(String(100), nullable=False)
    product_qty = Column(Integer, nullable=False)
    from_location = Column(String(100), default="Warehouse")
    to_location = Column(String(100), default="Warehouse")

    def __repr__(self):
        return f"movement_list(movement_id={self.movement_id} from_location={self.from_location} to_location={self.to_location} timestamp={self.timestamp} product_id={self.product_id} product_qty={self.product_qty})"

base.metadata.create_all(engine)  