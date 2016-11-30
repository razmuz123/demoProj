
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Read about sqlalchemy to understand the DB handling
class DBHandler:

    class PicData(Base):
        __tablename__ = 'picdata'
        picname = Column(String(length=200), primary_key=True)
        value = Column(String(length=200))


    __mapper_args__ = {
        "order_by": PicData.picname
    }


    def __repr__(self):
        return "<PicData:%s>" % (self.picname)


    # Create an engine that stores data in the local directory's
    # sqlalchemy_example.db file.
    engine = create_engine('sqlite:///sqlalchemy_picdata.db')
    # engine = create_engine('sqlite://')

    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)

    Base.metadata.bind = engine

    def setUpSession(self):

        DBSession = sessionmaker()
        DBSession.bind = DBHandler.engine
        return DBSession()


    def closeSession(self, session):

        session.close_all()


    def insertDataInDB(self, text, picname, session):

        pdata = DBHandler.PicData(picname = picname, value = text)
        session.add(pdata)
        print(pdata)

        try:
            session.commit()
        except Exception as e:
            print (e)

    # Query one
    def readDataFromDB(self, keyToRead):

        DBSession = sessionmaker()
        DBSession.bind = DBHandler.engine
        session = DBSession()

        arr = session.query(DBHandler.PicData).filter(DBHandler.PicData.picname == keyToRead)
        replies = []
        for r in arr:
            replies.append(r)
        return replies
