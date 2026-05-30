from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from IST03_Petrova.Alchemy_Petrova.database import Base

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now)
    pots = relationship("Post",back_populates="author",cascade="all, delete-orphan")
    def __repr__(self):
        return f"<Author(name='{self.name}', email='{self.email}')>"

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, unique=True)
    content = Column(Text, nullable=False)
    published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    author = relationship("Author", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    def __repr__(self):
        return f"<Post(title='{self.title}', published='{self.content}')>"
class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    author_name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    post = relationship("Post", back_populates="comments")
    def __repr__(self):
        return f"<Comment(text='{self.text}', author_name='{self.author_name}')>"

if __name__=="__main__":
    from IST03_Petrova.Alchemy_Petrova.database import engine, Base
    Base.metadata.create_all(bind=engine)
    print("Таблицы созданы")
