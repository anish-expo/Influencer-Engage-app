from . import db
from datetime import datetime
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash



class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    users = db.relationship('User', back_populates='role')

    def __repr__(self):
        return f'<Role {self.name}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255), default='default.jpg')
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    company =db.Column(db.String(150),nullable =True)
    socialmedia = db.Column(db.String(150),nullable =True)
    reach = db.Column(db.String(100),nullable=True)
    niche = db.Column(db.String(100), nullable =True)
    about = db.Column(db.String(200),nullable =True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    last_login = db.Column(db.DateTime(timezone=True), default=None)
    is_approved = db.Column(db.Boolean, default=False)
    is_rejected = db.Column(db.Boolean, default=False)
    is_flagged = db.Column(db.Boolean, default=False)

    
    # Relationships
    campaigns = db.relationship('Campaign', back_populates='sponsor', passive_deletes=True, cascade="all, delete-orphan")
    ad_requests = db.relationship('AdRequest', back_populates='influencer', passive_deletes=True, cascade="all, delete-orphan")
    
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', back_populates='users')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def is_admin(self):
        return self.role.name == 'Admin'

    def is_sponsor(self):
        return self.role.name == 'Sponsor'

    def is_influencer(self):
        return self.role.name == 'Influencer'
    
    
    
class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    visibility = db.Column(db.String(50), nullable=False)  
    goals = db.Column(db.Text, nullable=True)
    target = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100), default='default.jpg')
    flag = db.Column(db.Boolean, default=False)

    # Foreign Key
    sponsor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationships
    ad_requests = db.relationship('AdRequest', back_populates='campaign', cascade="all, delete-orphan")
    ads = db.relationship('Ad', back_populates='campaign',  cascade="all, delete-orphan")
    sponsor = db.relationship('User', back_populates='campaigns')

    def __repr__(self):
        return f'<Campaign {self.name}>'
    
    def completion_percentage(self):
        total_ads = len(self.ads)  
        if self.target > 0:
            percentage = (total_ads / self.target) * 100
            percentage = round(percentage, 2)
            # return (total_ads / self.target) * 100
            return min(percentage, 100.00)
        return 0

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)  
    timestamp = db.Column(db.DateTime, default=func.now())  

   
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 

    
    sender = db.relationship('User', foreign_keys=[sender_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])

   
    ad_request_id = db.Column(db.Integer, db.ForeignKey('ad_request.id'), nullable=True)
    ad_request = db.relationship('AdRequest', back_populates='messages')

    def __repr__(self):
        return f'<Message from {self.sender.username} to {self.receiver.username}>'

class AdRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requirements = db.Column(db.Text, nullable=False)
    payment_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')  # Pending, Accepted, Rejected, Negotiating
    sender_id = db.Column(db.Integer,  nullable=False)

    # Foreign Keys
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

    # Relationships
    campaign = db.relationship('Campaign', back_populates='ad_requests')
    influencer = db.relationship('User', back_populates='ad_requests')
    
    
    ads = db.relationship('Ad', back_populates='ad_request',cascade="all, delete-orphan")
    messages = db.relationship('Message', back_populates='ad_request', cascade="all, delete-orphan")  

    def __repr__(self):
        return f'<AdRequest {self.id}>'


class Ad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)  # Name of the ad
    link = db.Column(db.String(255), nullable=False)  # Link to the ad

    # Foreign Keys
    ad_request_id = db.Column(db.Integer, db.ForeignKey('ad_request.id'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)

    # Relationships
    ad_request = db.relationship('AdRequest', back_populates='ads')
    campaign = db.relationship('Campaign', back_populates='ads')

    def __repr__(self):
        return f'<Ad {self.name}>'