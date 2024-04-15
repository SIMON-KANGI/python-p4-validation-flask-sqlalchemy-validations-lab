from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Name is required.')
        existing_name=Author.query.filter(Author.name ==name).first()
        if existing_name:
            raise ValueError('Name must be unique.')
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if not isinstance(phone_number, int) or len(phone_number) != 10:
            raise ValueError('Phone number must be exactly ten digits.')
        return phone_number
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    
    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError('Content is too short.')
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError('Summary is too log.')
        return summary

    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError('Category must be either Fiction or Non-Fiction.')
        return category

    @validates('title')
    def validate_title(self, key, title):
        clickbait_phrases = ['Won\'t Believe', 'Secret', 'Top', 'Guess']
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError('Title must contain at least one of the following: "Won\'t Believe", "Secret", "Top", "Guess"')
        return title


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
