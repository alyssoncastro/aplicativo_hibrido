from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import db

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    tasks = relationship('Task', back_populates='user', cascade="all, delete")

    def __repr__(self):
        return f'<User:[id:{self.id}, name:{self.name}, email:{self.email}, password:{self.password}]>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "tasks": [task.serialize() for task in self.tasks]
        }

class Task(db.Model):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    description = Column(String(200), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='tasks')

    def __repr__(self):
        return f'<Task:[id:{self.id}, title:{self.title}, description:{self.description}, user_id:{self.user_id}]>'

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "user_id": self.user_id
        }
