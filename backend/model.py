from extensions import db

class Users(db.Model):
    __tablename__ = 'users'
    User_ID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    Username = db.Column(db.String(20), nullable=False)
    Email = db.Column(db.String(20), nullable=False)
    Password = db.Column(db.String(200), nullable=False)
    Type = db.Column(db.String(20), nullable=False)
    Created_at = db.Column(db.DateTime, default=db.func.now())

class Sponsors(db.Model):
    __tablename__ = 'sponsors'
    Sponser_ID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    Name = db.Column(db.String(20), nullable=False)
    Budget = db.Column(db.Integer)
    Industry = db.Column(db.String(20))
    Created_by = db.Column(db.Integer, db.ForeignKey('users.User_ID'))
    Created_at = db.Column(db.DateTime, default=db.func.now())
    Flag = db.Column(db.String(10), default="No")
    Status = db.Column(db.String(10), default="Pending")

class Influencers(db.Model):
    __tablename__ = 'influencers'
    Infuencer_ID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    Name = db.Column(db.String(20), nullable=False)
    About = db.Column(db.String(200), nullable=True)
    Profile_Pic = db.Column(db.String(), nullable=True)
    Category = db.Column(db.String(20), nullable=False)
    Niche = db.Column(db.String(20))
    Reach = db.Column(db.Integer, nullable=False)
    Created_by = db.Column(db.Integer, db.ForeignKey('users.User_ID'))
    Created_at = db.Column(db.DateTime, default=db.func.now())
    Views = db.Column(db.Integer, default=0)
    Avg_Rating = db.Column(db.Float,default=0.0)
    Rating_No = db.Column(db.Integer,default=0)
    Flag = db.Column(db.String(10), default="No")

class Campaign(db.Model):
    __tablename__ = 'campaign'
    Campaign_ID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    Name = db.Column(db.String(20), nullable=False)
    Desc = db.Column(db.String(100))
    Start_Date = db.Column(db.DateTime, nullable=False)
    End_Date = db.Column(db.DateTime, nullable=False)
    Budget = db.Column(db.Integer, nullable=False)
    Goals = db.Column(db.String(100))
    Created_by = db.Column(db.Integer, db.ForeignKey('sponsors.Sponser_ID'))
    Created_at = db.Column(db.DateTime, default=db.func.now())
    Influencer = db.Column(db.Integer, db.ForeignKey('influencers.Infuencer_ID'))
    Status = db.Column(db.String(20), nullable=False)
    Flag = db.Column(db.String(10), default="No")
    Views = db.Column(db.Integer, default=0)
    Preferred_Category = db.Column(db.String(20), nullable=False)
    Visibility = db.Column(db.String(20))

class Ad_Request(db.Model):
    __tablename__ = 'ad_request'
    Request_ID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    Campaign = db.Column(db.Integer, db.ForeignKey('campaign.Campaign_ID'))
    Requirements = db.Column(db.String(100), nullable=False)
    Payment = db.Column(db.Integer, nullable=False)
    Status = db.Column(db.String(20), nullable=False)
    Created_at = db.Column(db.DateTime, default=db.func.now())
    Created_By = db.Column(db.Integer, db.ForeignKey('sponsors.Sponser_ID'))

class Messages(db.Model):
    __tablename__ = 'messages'
    Message_ID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    Campaign = db.Column(db.Integer, db.ForeignKey('campaign.Campaign_ID'))
    To = db.Column(db.Integer)
    From = db.Column(db.Integer)
    Date = db.Column(db.DateTime, default=db.func.now())
    Message = db.Column(db.String(100), nullable=False)

class Rating(db.Model):
    __tablename__ = 'ratings'
    Rating_ID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    Rating = db.Column(db.Integer, nullable=False)
    Message = db.Column(db.String(100))
    To = db.Column(db.Integer, db.ForeignKey('influencers.Infuencer_ID'))
    By = db.Column(db.Integer, db.ForeignKey('sponsors.Sponser_ID'))
    Rated_At = db.Column(db.DateTime, default=db.func.now())

class Saved(db.Model):
    __tablename__ = 'saved'
    Save_ID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    Saved = db.Column(db.Integer, db.ForeignKey('campaign.Campaign_ID'),nullable=False)
    Of = db.Column(db.Integer, db.ForeignKey('influencers.Infuencer_ID'),nullable=False)
    Saved_At = db.Column(db.DateTime, default=db.func.now())

class ChatMessage(db.Model):
    Message_Id = db.Column(db.Integer, primary_key=True)
    Sender_Id = db.Column(db.Integer, nullable=False)
    Sender_Type = db.Column(db.String(40), nullable=False)
    Receiver_Id = db.Column(db.Integer, nullable=False)
    Receiver_Type = db.Column(db.String(40), nullable=False)
    Message = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())


    