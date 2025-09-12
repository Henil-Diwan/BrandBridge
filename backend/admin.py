from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView



def setup_admin(app, db):
    from model import Users, Sponsors, Influencers, Campaign, Ad_Request, Messages, Rating, Saved, ChatMessage


    admin = Admin(app, url='/database')  

    admin.add_view(ModelView(Users, db.session))
    admin.add_view(ModelView(Sponsors, db.session))
    admin.add_view(ModelView(Influencers, db.session))
    admin.add_view(ModelView(Campaign, db.session))
    admin.add_view(ModelView(Ad_Request, db.session))
    admin.add_view(ModelView(Messages, db.session))
    admin.add_view(ModelView(Rating, db.session))
    admin.add_view(ModelView(Saved, db.session))
    admin.add_view(ModelView(ChatMessage, db.session))