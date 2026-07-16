from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Class that DB models inherit from
Base = declarative_base() 

class Walk(Base):
    __tablename__ = 'walks'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    date = Column(String)
    distance_km = Column(Float)
    duration = Column(String)
    pace = Column(String)
    elevation_gain = Column(Float)
    total_points = Column(Integer)
    filename = Column(String)

def get_engine():
    # Creates connections to SQLite DB file
    return create_engine('sqlite:///data/uploads/walks.db')

def initialise_db():
    # Creates actual database file and tables
    engine = get_engine()
    Base.metadata.create_all(engine)
    return engine

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

def save_walk(name, date, stats, filename):
    # Creates a Walk object with all the data, row in table
    session = get_session()
    walk = Walk(name=name, 
                date=date, 
                distance_km=stats['distance_km'], 
                duration=stats['duration'],
                pace=stats['pace'],
                elevation_gain=stats['elevation_gain_m'], 
                total_points=stats['total_points'],
                filename=filename)
    
    session.add(walk)
    session.commit()
    session.close()
    print(f"Saved walk: {name}") # Debugging

def get_walks():
    session = get_session()
    walks = session.query(Walk).all()
    session.close()
    return walks

def get_walk_id(walk_id):
    session = get_session()
    walk = session.query(Walk).filter(Walk.id == walk_id).first()
    session.close()
    return walk