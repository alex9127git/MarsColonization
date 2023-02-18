import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, orm
from db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    team_leader = Column(Integer, ForeignKey("users.id"))
    job = Column(String, nullable=True)
    work_size = Column(Integer, nullable=True)
    collaborators = Column(String, nullable=True)
    start_date = Column(DateTime, default=datetime.datetime.now)
    end_date = Column(DateTime, default=datetime.datetime.now)
    is_finished = Column(Boolean, nullable=True)
    user = orm.relationship("User")

    def __repr__(self):
        return f"{self.team_leader} {self.job} {self.work_size} {self.collaborators} {self.is_finished}"
