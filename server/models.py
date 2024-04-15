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
        if len(name.strip()) == 0:
            raise ValueError("Name must be present")

        existing_author = Author.query.filter_by(name=name).first()
        if existing_author:
            raise ValueError("Name already exists")

        return name
    @validates("phone_number")
    def validate_number(self,key,phone_number):
        
        if len(phone_number) == 10:
             return phone_number
        raise ValueError('Phone number must be atleast 10 digits')
       

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

    # Add validators 
    @validates('content')
    def validate_content(self,key,content):
        if len(content)>=250:
            return content
        else:
            raise ValueError('Content too short test. Less than 250 chars')
        
    @validates('summary')
    def validate_summary(self,key,summary):
        if len(summary)>250:
            raise ValueError("Summary too long test. More than 250 chars.")
        return summary
     
    @validates('category')
    def validate_category(self,key,category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("category must be either Fiction or Non-Fiction")
        return category
    
    @validates('title')
    def validate_title(self,key,title):
        clickbait_y=["Won't Believe","Secret","Top","Guess"]
        if title not in clickbait_y:
            raise ValueError("Invalid Title")

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
