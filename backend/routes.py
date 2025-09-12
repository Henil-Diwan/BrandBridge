import os
import uuid
from datetime import datetime
from sqlite3 import IntegrityError
from flask import current_app, jsonify, request, send_from_directory, Blueprint, send_file
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity
from model import Ad_Request, Campaign, ChatMessage, Influencers, Messages, Rating, Saved, Sponsors, Users
from werkzeug.utils import secure_filename
from tasks import create_resource_csv
import pandas as pd
from flask import Response
from celery.result import AsyncResult

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/download_csv/<int:sponsorid>', methods=['GET'])
def download_csv(sponsorid):
    
    task = create_resource_csv.delay(sponsorid)
    return jsonify({'task_id':task.id})

@routes_bp.route('/get_csv/<string:taskid>', methods=['GET'])
def get_csv(taskid):
    
    res = AsyncResult(taskid)
    
    if res.ready():
        filename=res.result
        return send_file(filename, as_attachment=True)
    else:
        return jsonify({'message':"Task Pending"}), 400

@routes_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)

@routes_bp.route('/register', methods=['POST'])
def register():
    from app import db, bcrypt
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    user_type = data.get('type')

    if len(Users.query.filter_by(Email=email).all()) > 0:
        return jsonify(message="Username or email already exists"), 409
    
    if not username or not email or not password or not user_type:
        return jsonify(message="All fields are required"), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    new_user = Users(
        Username=username,
        Email=email,
        Password=hashed_password,
        Type=user_type
    )
    
    

    try:
        db.session.add(new_user)
        db.session.commit()
        added_user = Users.query.filter_by(Email=email).first()
        return jsonify(message="User registered successfully",
                    user_id=added_user.User_ID), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify(message="Username or email already exists"), 409

@routes_bp.route('/login', methods=['POST'])
def login():
    from app import bcrypt
    data = request.get_json()
    email = data['email']
    password = data['password']
    
    user = Users.query.filter_by(Email=email).first()

    if user:
            if user.Type == 'sponsor':
                sponsor = Sponsors.query.filter_by(Created_by=user.User_ID).first()
                if sponsor.Status != 'Approved':
                    return jsonify(message="Your account is pending approval by the admin."), 403
                if sponsor and sponsor.Flag == 'Yes':  # Check if the sponsor is flagged
                    return jsonify(message="Account is flagged, login denied"), 403
            elif user.Type == 'influencer':
                influencer = Influencers.query.filter_by(Created_by=user.User_ID).first()
                if influencer and influencer.Flag == 'Yes':  # Check if the influencer is flagged
                    return jsonify(message="Account is flagged, login denied"), 403


    if user and bcrypt.check_password_hash(user.Password, password):

        user_data = {
            'user_id': user.User_ID,
            'username': user.Username,
            'email': user.Email,
            'type': user.Type
        }

        access_token = create_access_token(identity=user_data)

        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message="Invalid credentials"), 401

@routes_bp.route('/sponsor_register', methods=['POST'])

def register_sponsor():
    from app import db
    data = request.get_json()
    name = data.get('name')
    budget = data.get('budget')
    industry = data.get('industry')
    creator = data.get('creator')
    
    if not name or not budget or not industry or not creator:
        return jsonify(message="All fields are required"), 400

    new_sponsor = Sponsors(Name=name, Budget=int(budget), Industry=industry, Created_by=str(creator))
    try:
        db.session.add(new_sponsor)
        db.session.commit()
        return jsonify(message="User registered successfully"), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify(message="Failed"), 409

@routes_bp.route('/influencer_register', methods=['POST'])
def register_influencer():
    from app import db
    name = request.form.get('name')
    about = request.form.get('about')
    category = request.form.get('category')
    niche = request.form.get('niche')
    reach = request.form.get('reach')
    creator = request.form.get('creator')
    picname=None
    
    profpic = request.files.get('ProfilePic') 

    if profpic:
            profpic = request.files['ProfilePic']

            print(profpic.filename)

            profpicname = secure_filename(profpic.filename)
            picname = str(uuid.uuid1()) + '_' + profpicname

            upload_folder = current_app.config['UPLOAD_FOLDER']
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

        # Create the full path to save the file
            file_path = os.path.join(upload_folder, picname)

            profpic.save(file_path)
    
    if not name or not about or not category or not creator or not reach:
        return jsonify(message="All fields are required"), 400

    new_influencer = Influencers(Name=name, Category=category, Niche=niche, Reach=reach, Created_by=str(creator), About = about, Profile_Pic=picname)
    try:
        db.session.add(new_influencer)
        db.session.commit()
        return jsonify(message="User registered successfully"), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify(message="Failed"), 409
    
@routes_bp.route('/protected', methods=['GET','POST'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    if current_user['type'] == 'sponsor':
        sponsor = Sponsors.query.filter_by(Created_by=current_user['user_id']).first()
        current_sponsor = {
            'id':sponsor.Sponser_ID,
            'name':sponsor.Name,
            'budget':sponsor.Budget,
            'industry':sponsor.Industry,
            'flag':sponsor.Flag,
            'created_at': sponsor.Created_at
        }
        return jsonify(logged_in_as=current_user , current_sponsor=current_sponsor), 200
    elif current_user['type'] == 'influencer':
        influencer = Influencers.query.filter_by(Created_by=current_user['user_id']).first()
        current_influencer = {
            'id': influencer.Infuencer_ID,
            'name': influencer.Name,
            'about': influencer.About,
            'profile_pic': influencer.Profile_Pic,
            'category': influencer.Category,
            'niche': influencer.Niche,
            'reach': influencer.Reach,
            'views': influencer.Views,
            'rating': influencer.Avg_Rating,
            'rating_no': influencer.Rating_No,
            'flag': influencer.Flag,
            'created_at': influencer.Created_at 
        }
        return jsonify(logged_in_as=current_user , current_influencer=current_influencer), 200
    else:
        return jsonify(logged_in_as=current_user), 200
    
@routes_bp.route('/create_campaign', methods=['POST'])
def create_campaign():
    from app import db
    data = request.get_json()


    name = data.get("Name")
    desc = data.get("Desc")
    pref_cat = data.get("Category")
    start = datetime.strptime(data.get("Start"), '%Y-%m-%dT%H:%M')
    end = datetime.strptime(data.get("End"), '%Y-%m-%dT%H:%M')
    budget = data.get("Budget")
    goals = data.get("Goals")
    visibility = data.get("Visi")
    created_by = data.get("Created_by")

    sponsor = Sponsors.query.filter_by(Sponser_ID=created_by).first()
    if not sponsor:
        return jsonify({"error": "Sponsor not found"}), 404

    new_campaign = Campaign(
        Name=name,
        Desc=desc,
        Preferred_Category=pref_cat,
        Start_Date=start,
        End_Date=end,
        Budget=budget,
        Goals=goals,
        Visibility=visibility,
        Created_by=created_by,
        Status='Open' 
    )
    try:
        db.session.add(new_campaign)
        db.session.commit()
        
        return jsonify({"message": "Campaign created successfully","Campaign_ID":new_campaign.Campaign_ID}), 201
    
    except IntegrityError:

        db.session.rollback()
        return jsonify(message="Failed"), 409

@routes_bp.route('/create_request', methods=['POST'])
def create_request():
    from app import db
    data = request.get_json()


    requirements = data.get("Requirements")
    payment = data.get("Payment")
    campaignid = data.get("Campaign")
    created = data.get("Created_by")

    sponsor = Sponsors.query.filter_by(Sponser_ID=created).first()
    if not sponsor:
        return jsonify({"error": "Sponsor not found"}), 404

    new_request = Ad_Request(Campaign=campaignid, Requirements=requirements, Payment=payment, Status='Open', Created_By=created)
    try:
        db.session.add(new_request)
        db.session.commit()
        
        return jsonify({"message": "Request created successfully"}), 201
    
    except IntegrityError:
        
        db.session.rollback()
        return jsonify(message="Failed"), 409


@routes_bp.route('/sponsor_dashboard', methods=['GET'])
def sponsor_dashboard():
    
    user_id = request.args.get('user_id')  # Or use request.form or request.json for POST requests if needed

    if not user_id:
        return jsonify({"message": "User ID is required"}), 400

    # Fetch sponsor information
    sponsor = Sponsors.query.filter_by(Created_by=user_id).first()
    if not sponsor:
        return jsonify({"message": "Sponsor not found"}), 404

    # Fetch influencers in the sponsor's industry
    influencers = Influencers.query.filter(
        Influencers.Flag == 'No',Influencers.Category == sponsor.Industry
    ).order_by(Influencers.Reach.desc(), Influencers.Created_at.desc())

    influencers_data = [{
        'id': influencer.Infuencer_ID,
        'name': influencer.Name,
        'about': influencer.About,
        'category': influencer.Category,
        'reach': influencer.Reach,
        'niche': influencer.Niche,
        'rating': influencer.Avg_Rating,
        'views': influencer.Views,
    } for influencer in influencers]

    # Fetch open campaigns in the sponsor's industry
    campaigns = Campaign.query.filter(
        (Campaign.Preferred_Category == sponsor.Industry) | (Campaign.Preferred_Category == 'Any'),
        Campaign.Status == 'Open',Campaign.Visibility=="All",Campaign.Start_Date <= datetime.now(),Campaign.End_Date >= datetime.now(),Campaign.Flag == 'No'
    ).order_by(Campaign.Created_at.desc()).limit(10)

    user_campaigns = Campaign.query.filter(
        Campaign.Status == 'Open',Campaign.Start_Date <= datetime.now(),Campaign.End_Date >= datetime.now(),Campaign.Flag == 'No', Campaign.Created_by==sponsor.Sponser_ID
    ).all()

    campaigns_data = [{
        'id': campaign.Campaign_ID,
        'name': campaign.Name,
        'desc': campaign.Desc[:20] + '...',  # Shorten description
        'start_date': campaign.Start_Date,
        'end_date': campaign.End_Date,
        'budget': campaign.Budget,
        'goals': campaign.Goals[:20],
        'visibility': campaign.Visibility,
        'category': campaign.Preferred_Category,
        'views': campaign.Views,
        'by': Sponsors.query.get(campaign.Created_by).Name
    } for campaign in campaigns]

    user_campaigns_data = [{
        'id': campaign.Campaign_ID,
        'name': campaign.Name,
        'desc': campaign.Desc[:20] + '...',  # Shorten description
        'start_date': campaign.Start_Date,
        'end_date': campaign.End_Date,
        'budget': campaign.Budget,
        'goals': campaign.Goals[:20],
        'visibility': campaign.Visibility,
        'category': campaign.Preferred_Category,
        'views': campaign.Views,
    } for campaign in user_campaigns]

    # Organize all data into a response object
    response_data = {
        'current_sponsor': {
            'id': sponsor.Sponser_ID,
            'name': sponsor.Name,
            'budget': sponsor.Budget,
            'industry': sponsor.Industry,
            'flag': sponsor.Flag,
            'created_at': sponsor.Created_at
        },
        'influencers': influencers_data,
        'campaigns': campaigns_data,
        'user_campaigns': user_campaigns_data

    }

    return jsonify(response_data), 200

@routes_bp.route('/rate', methods=['GET','POST'])
def rate():
    from app import db
    if request.method == 'POST':
        # Get data from the body (json)
        data = request.get_json()  # Access the POST data as JSON
        influencer_id = data.get('influencer_id')
        rating = data.get('rating')
        message = data.get('message')
        current_user_id = data.get('user_id')

        print(f"influencer_id: {influencer_id}, rating: {rating}, message: {message}, user_id: {current_user_id}")

        if not influencer_id:
            return jsonify({"message": "Influencer ID is required"}), 400

        current_influencer = Influencers.query.get(influencer_id)

        if not current_influencer:
            return jsonify({"message": "Influencer not found"}), 404

        try:
            current = Sponsors.query.filter_by(Created_by=current_user_id).first().Sponser_ID

            new_rating = Rating(
                Rating=rating,
                Message=message,
                To=influencer_id,
                By=current
            )
            db.session.add(new_rating)
            current_influencer.Avg_Rating = (current_influencer.Avg_Rating * current_influencer.Rating_No) + int(rating)
            current_influencer.Rating_No += 1
            current_influencer.Avg_Rating = current_influencer.Avg_Rating / current_influencer.Rating_No
            db.session.commit()

            return jsonify({"message": "Rating created successfully"}), 201

        except IntegrityError:
            db.session.rollback()
            return jsonify(message="Failed to create rating"), 409

    # For GET request
    influencer_id = request.args.get('influencer_id')
    if not influencer_id:
        return jsonify({"message": "Influencer ID is required"}), 400

    current_influencer = Influencers.query.get(influencer_id)

    influencer_data = {
        'id': current_influencer.Infuencer_ID,
        'name': current_influencer.Name,
        'about': current_influencer.About,
        'category': current_influencer.Category,
        'reach': current_influencer.Reach,
        'niche': current_influencer.Niche,
        'rating': current_influencer.Avg_Rating,
        'views': current_influencer.Views,
    }

    return jsonify({'rating_influencer': influencer_data}), 200

@routes_bp.route('/delete_campaign/<int:campaign_id>', methods=['DELETE'])
def delete_campaign(campaign_id):
    from app import db 
    camp = Campaign.query.get(campaign_id)
    if not camp:
        return jsonify({"error": "Campaign not found"}), 404
    
    # Deleting ad requests associated with the campaign
    ad_requests = Ad_Request.query.filter_by(Campaign=campaign_id).all()
    for ad in ad_requests:
        db.session.delete(ad)
    
    # Deleting the campaign
    db.session.delete(camp)
    db.session.commit()

    return jsonify({"message": "Campaign deleted successfully"}),200

@routes_bp.route('/my_campaigns', methods=['GET'])
def my_campaigns():
    
    user_id = request.args.get('user_id')  # Or use request.form or request.json for POST requests if needed

    if not user_id:
        return jsonify({"message": "User ID is required"}), 400

    # Fetch sponsor information
    sponsor = Sponsors.query.filter_by(Created_by=user_id).first()
    if not sponsor:
        return jsonify({"message": "Sponsor not found"}), 404

    user_campaigns = Campaign.query.filter(
        Campaign.Start_Date <= datetime.now(),Campaign.End_Date >= datetime.now(),Campaign.Flag == 'No', Campaign.Created_by==sponsor.Sponser_ID
    ).all()

    user_campaigns_data = [{
        'id': campaign.Campaign_ID,
        'name': campaign.Name,
        'desc': campaign.Desc[:20] + '...',  # Shorten description
        'start_date': campaign.Start_Date,
        'end_date': campaign.End_Date,
        'budget': campaign.Budget,
        'goals': campaign.Goals[:20],
        'visibility': campaign.Visibility,
        'category': campaign.Preferred_Category,
        'views': campaign.Views,
    } for campaign in user_campaigns]

    # Organize all data into a response object
    response_data = {
        'current_sponsor': {
            'id': sponsor.Sponser_ID,
            'name': sponsor.Name,
            'budget': sponsor.Budget,
            'industry': sponsor.Industry,
            'flag': sponsor.Flag,
            'created_at': sponsor.Created_at
        },
        'campaigns': user_campaigns_data

    }

    return jsonify(response_data), 200


@routes_bp.route('/update_campaign', methods=['GET','POST'])
def update():
    from app import db
    if request.method == 'POST':
        # Get data from the body (json)
        data = request.get_json()  # Access the POST data as JSON
        campaign_id = data.get('campaign_id')
        name = data.get("Name")
        desc = data.get("Desc")
        pref_cat = data.get("Category")
        end = datetime.strptime(data.get("End"), '%Y-%m-%dT%H:%M')
        budget = data.get("Budget")
        goals = data.get("Goals")
        visibility = data.get("Visi")
        current_campaign = Campaign.query.get(campaign_id)
        
        try:

            current_campaign.Name = name
            current_campaign.Preferred_Category = pref_cat
            current_campaign.Desc = desc
            current_campaign.Budget = budget
            current_campaign.Goals = goals
            current_campaign.Visibility = visibility
            current_campaign.End_Date = end
            db.session.commit()
            return jsonify({"message": "Campaign Updated successfully"}), 201

        except IntegrityError:
            db.session.rollback()
            return jsonify(message="Failed to update campaign"), 409

    # For GET request
    campaign_id = request.args.get('campaign_id')
    print(campaign_id)
    current_campaign = Campaign.query.get(campaign_id)
    ad_requests = Ad_Request.query.filter_by(Campaign=campaign_id).all()

    current_campaign_data = {
        'id': current_campaign.Campaign_ID,
        'name': current_campaign.Name,
        'desc': current_campaign.Desc,
        'start_date': current_campaign.Start_Date,
        'end_date': current_campaign.End_Date,
        'budget': current_campaign.Budget,
        'goals': current_campaign.Goals[:20],
        'visibility': current_campaign.Visibility,
        'category': current_campaign.Preferred_Category,
        'views': current_campaign.Views,
    }

    ad_data = [{
        'id':ad.Request_ID,
        'requirements':ad.Requirements,
        'payment':ad.Payment
    } for ad in ad_requests]

    

    return jsonify({'campaign': current_campaign_data,'ads':ad_data}), 200

@routes_bp.route('/delete_ad/<int:ad_id>', methods=['DELETE'])
def delete_ad(ad_id):
    from app import db
    ad = Ad_Request.query.get(ad_id)
    if not ad:
        return jsonify({"error": "Ad Request not found"}), 404
    

    try:
        db.session.delete(ad)
        db.session.commit()

        return jsonify({"message": "Campaign deleted successfully"}),200
    except IntegrityError:
            db.session.rollback()
            return jsonify(message="Failed to update campaign"), 409


@routes_bp.route('/sponsor_profile', methods=['GET'])
def sponsor_profile():
    from app import db
    # For GET request
    sponsor_id = request.args.get('sponsor_id')

    current_sponsor = Sponsors.query.get(sponsor_id)
    now = datetime.now()

    active_campaigns = db.session.query(Campaign).filter(
        Campaign.Created_by == sponsor_id,
        Campaign.Start_Date <= now, 
        Campaign.End_Date >= now,
        Campaign.Flag == 'No'
    ).all()
    data = {}
    data_prev = {}

    ended_campaigns = Campaign.query.filter(
        Campaign.Created_by==sponsor_id,
        Campaign.End_Date <= now,
        Campaign.Flag == 'No'
    ).all()



    requested_campaigns = Campaign.query.filter(
        Campaign.Created_by==sponsor_id,
        Campaign.Status == 'Requested_by',
        Campaign.Flag == 'No'
    ).all()
    
    for i in active_campaigns:
        if len(Ad_Request.query.filter(Ad_Request.Campaign == i.Campaign_ID).all()) != 0: 
            data[i] = 100*(len(Ad_Request.query.filter(Ad_Request.Campaign == i.Campaign_ID, Ad_Request.Status != 'Open').all())/len(Ad_Request.query.filter(Ad_Request.Campaign == i.Campaign_ID).all()))
        else:
            data[i]=0
    
    for i in ended_campaigns:
        if len(Ad_Request.query.filter(Ad_Request.Campaign == i.Campaign_ID).all()) != 0: 
            data_prev[i] = 100*(len(Ad_Request.query.filter(Ad_Request.Campaign == i.Campaign_ID, Ad_Request.Status != 'Open').all())/len(Ad_Request.query.filter(Ad_Request.Campaign == i.Campaign_ID).all()))
        else:
            data_prev[i]=0

    active_campaign_data = [{
        'id': current_campaign.Campaign_ID,
        'name': current_campaign.Name,
        'desc': current_campaign.Desc,
        'start_date': current_campaign.Start_Date,
        'end_date': current_campaign.End_Date,
        'budget': current_campaign.Budget,
        'goals': current_campaign.Goals[:20],
        'visibility': current_campaign.Visibility,
        'category': current_campaign.Preferred_Category,
        'views': current_campaign.Views,
        'status': current_campaign.Status,
        'completion':data[current_campaign]
    } for current_campaign in active_campaigns]

    requested_campaign_data = [{
        'id': current_campaign.Campaign_ID,
        'name': current_campaign.Name,
        'desc': current_campaign.Desc,
        'start_date': current_campaign.Start_Date,
        'end_date': current_campaign.End_Date,
        'budget': current_campaign.Budget,
        'goals': current_campaign.Goals[:20],
        'visibility': current_campaign.Visibility,
        'category': current_campaign.Preferred_Category,
        'views': current_campaign.Views,
        'status': current_campaign.Status,
        'influencer':current_campaign.Influencer,
        'influencer_name': Influencers.query.get(current_campaign.Influencer).Name
    } for current_campaign in requested_campaigns]

    prev_campaign_data = [{
        'id': current_campaign.Campaign_ID,
        'name': current_campaign.Name,
        'desc': current_campaign.Desc,
        'start_date': current_campaign.Start_Date,
        'end_date': current_campaign.End_Date,
        'budget': current_campaign.Budget,
        'goals': current_campaign.Goals[:20],
        'visibility': current_campaign.Visibility,
        'category': current_campaign.Preferred_Category,
        'views': current_campaign.Views,
        'status': current_campaign.Status,
        'completion':data[current_campaign]
    } for current_campaign in ended_campaigns]


    

    return jsonify({'active': active_campaign_data,'prev':prev_campaign_data,'requested':requested_campaign_data}), 200


@routes_bp.route('/accept_campaign/<int:campaignid>', methods=['POST'])
def accept_campaign(campaignid):
    from app import db
    try:
        # Fetch the campaign using the campaign ID
        current_campaign = Campaign.query.get(campaignid)
        if not current_campaign:
            return jsonify({'message': 'Campaign not found'}), 404
        
        # Change campaign status to 'Accepted'
        current_campaign.Status = 'Accepted'
        
        # Commit the changes to the database
        db.session.commit()

        # Redirect to the sponsor's profile after accepting
        return  jsonify({"message": "Ad Accepted successfully"}), 201
    except Exception as e:
        db.session.rollback()  # Rollback in case of any error
        return jsonify({'message': str(e)}), 500
    

@routes_bp.route('/reject_campaign/<int:campaignid>', methods=['POST'])
def reject_campaign(campaignid):
    from app import db
    try:
        # Fetch the campaign using the campaign ID
        current_campaign = Campaign.query.get(campaignid)
        if not current_campaign:
            return jsonify({'message': 'Campaign not found'}), 404
        
        # Change campaign status to 'Accepted'
        current_campaign.Status = 'Open'
        current_campaign.Influencer = None
        
        # Commit the changes to the database
        db.session.commit()

        # Redirect to the sponsor's profile after accepting
        return  jsonify({"message": "Ad Accepted successfully"}), 201
    except Exception as e:
        db.session.rollback()  # Rollback in case of any error
        return jsonify({'message': str(e)}), 500

@routes_bp.route('/request_to_influencer', methods=['POST'])
def request_to_influencer():
    from app import db
    try:
        data = request.get_json()
        campaign_ids = data.get('campaign_ids')
        influencer_id = data.get('influencer_id')

        if not influencer_id:
            return jsonify({'message': 'Influencer not found'}), 404

        for campaign_id in campaign_ids:
            campaign = Campaign.query.get(campaign_id)
            if campaign:
                campaign.Status = 'Requested_to'
                campaign.Influencer = influencer_id

        db.session.commit()
        return jsonify({"message": "Requests Sent successfully"}), 201

    except Exception as e:
        db.session.rollback()  # Rollback in case of any error
        return jsonify({'message': str(e)}), 500

@routes_bp.route('/sponsor_stats', methods=['GET'])
def stats():
    
    sponsorid=request.args.get('sponsor_id')
    current_sponsor = Sponsors.query.get(sponsorid)

    if not current_sponsor:
        return jsonify({"message": "Sponsor not found"}), 404

    campaigns = Campaign.query.filter_by(Created_by=sponsorid).all()
    payment_labels=[]
    payment_values=[]

    for i in campaigns:
        payment_labels.append(i.Name)
        payment_values.append(i.Budget)

    status_values = [0,0,0,0]
    status_values[0] = len(Campaign.query.filter_by(Created_by=sponsorid, Status='Open').all())
    status_values[1] = len(Campaign.query.filter_by(Created_by=sponsorid, Status='Requested_by').all())
    status_values[2] = len(Campaign.query.filter_by(Created_by=sponsorid, Status='Requested_to').all())
    status_values[3] = len(Campaign.query.filter_by(Created_by=sponsorid, Status='Accepted').all())

    flagged_values=[0,0]
    flagged_values[0] = len(Campaign.query.filter_by(Created_by=sponsorid, Flag='No').all())
    flagged_values[1] = len(Campaign.query.filter_by(Created_by=sponsorid, Flag='Yes').all())

    response_data = {
        'payment_values':payment_values,
        'payment_labels':payment_labels,
        'status_values':status_values,
        'flagged_values':flagged_values
    }

    return jsonify(response_data), 200

@routes_bp.route('/update_request', methods=['GET','POST'])
def update_request():
    from app import db

    if request.method == 'POST':
        # Get data from the body (json)
        data = request.get_json()  # Access the POST data as JSON
        ad_id = data.get('ad_id')
        requirements = data.get("Requirements")
        payment = data.get("Payment")
        current_ad = Ad_Request.query.get(ad_id)
        
        try:

            current_ad.Requirements = requirements
            current_ad.Payment = payment
            db.session.commit()
            return jsonify({"message": "Ad Updated successfully"}), 201

        except IntegrityError:
            db.session.rollback()
            return jsonify(message="Failed to update campaign"), 409

    # For GET request
    ad_id = request.args.get('ad_id')
    current_ad = Ad_Request.query.get(ad_id)
    
    ad_data = {
        'id':current_ad.Request_ID,
        'requirements':current_ad.Requirements,
        'payment':current_ad.Payment
    }

    

    return jsonify({'ad':ad_data}), 200



@routes_bp.route('/influencer_dashboard', methods=['GET'])
def influencer_dashboard():
    
    user_id = request.args.get('user_id')  # Or use request.form or request.json for POST requests if needed

    if not user_id:
        return jsonify({"message": "User ID is required"}), 400

    # Fetch sponsor information
    influencer = Influencers.query.filter_by(Created_by=user_id).first()
    if not influencer:
        return jsonify({"message": "Influencer not found"}), 404

    campaigns = Campaign.query.filter(
        (Campaign.Preferred_Category == influencer.Category) | (Campaign.Preferred_Category == 'Any'),
        Campaign.Status == 'Open',Campaign.Visibility=="All",Campaign.Start_Date <= datetime.now(),Campaign.End_Date >= datetime.now(),Campaign.Flag == 'No'
    ).order_by(Campaign.Created_at.desc()).limit(10)

    campaigns_data = [{
        'id': campaign.Campaign_ID,
        'name': campaign.Name,
        'desc': campaign.Desc[:20] + '...',  # Shorten description
        'start_date': campaign.Start_Date,
        'end_date': campaign.End_Date,
        'budget': campaign.Budget,
        'goals': campaign.Goals[:20],
        'visibility': campaign.Visibility,
        'category': campaign.Preferred_Category,
        'saved': 1 if Saved.query.filter_by(Saved=campaign.Campaign_ID,Of=influencer.Infuencer_ID).first() else 0,
        'views': campaign.Views,
    } for campaign in campaigns]



    # Organize all data into a response object
    response_data = {
        'campaigns': campaigns_data

    }
    return jsonify(response_data), 200

@routes_bp.route('/request_by_influencer', methods=['POST'])
def request_by_influencer():
    from app import db
    try:
        data = request.get_json()
        campaign_id = data.get('campaign_id')
        influencer_id = data.get('influencer_id')

        if not influencer_id:
            return jsonify({'message': 'Influencer not found'}), 404

        campaign = Campaign.query.get(campaign_id)
        if campaign:
            campaign.Status = 'Requested_by'
            campaign.Influencer = influencer_id

        db.session.commit()
        return jsonify({"message": "Requests Sent successfully"}), 201

    except Exception as e:
        db.session.rollback()  # Rollback in case of any error
        return jsonify({'message': str(e)}), 500
    
@routes_bp.route('/save_campaign', methods=['POST'])
def save_campaign():
    from app import db
    try:
        data = request.get_json()
        campaign_id = data.get('campaign_id')
        influencer_id = data.get('influencer_id')

        if not influencer_id:
            return jsonify({'message': 'Influencer not found'}), 404

        current_saved = Saved.query.filter_by(Of=influencer_id).all()
        for i in current_saved:
            if i.Saved == campaign_id:
                return jsonify({'message': 'Already Saved'}), 404
        
        new_save = Saved(Saved=campaign_id, Of=influencer_id)
        db.session.add(new_save)
        db.session.commit()
        return jsonify({"message": "Campaign Saved successfully"}), 201

    except Exception as e:
        db.session.rollback()  # Rollback in case of any error
        return jsonify({'message': str(e)}), 500


@routes_bp.route('/unsave_campaign', methods=['POST'])
def unsave_campaign():
    from app import db
    try:
        data = request.get_json()
        campaign_id = data.get('campaign_id')
        influencer_id = data.get('influencer_id')

        if not influencer_id:
            return jsonify({'message': 'Influencer not found'}), 404

        save_record = Saved.query.filter_by(Saved=campaign_id, Of=influencer_id).first()

        if not save_record:
            return jsonify({'message': 'Not Saved'}), 404
        

        db.session.delete(save_record)
        db.session.commit()
        return jsonify({"message": "Campaign Unsaved successfully"}), 201

    except Exception as e:
        db.session.rollback()  # Rollback in case of any error
        return jsonify({'message': str(e)}), 500


@routes_bp.route('/all_campaigns', methods=['GET'])
def all_campaigns():
    
    influencer_id = request.args.get('influencer_id')  # Or use request.form or request.json for POST requests if needed

    influencer = Influencers.query.get(influencer_id)
    if not influencer:
        return jsonify({"message": "Influencer not found"}), 404

    campaigns = Campaign.query.filter(
        Campaign.Status == 'Open',Campaign.Visibility=="All",Campaign.Start_Date <= datetime.now(),Campaign.End_Date >= datetime.now(),Campaign.Flag == 'No'
    ).order_by(Campaign.Created_at.desc()).limit(10)

    campaigns_data = [{
        'id': campaign.Campaign_ID,
        'name': campaign.Name,
        'desc': campaign.Desc[:20] + '...',  # Shorten description
        'start_date': campaign.Start_Date,
        'end_date': campaign.End_Date,
        'budget': campaign.Budget,
        'goals': campaign.Goals[:20],
        'visibility': campaign.Visibility,
        'category': campaign.Preferred_Category,
        'saved': 1 if Saved.query.filter_by(Saved=campaign.Campaign_ID,Of=influencer.Infuencer_ID).first() else 0,
        'views': campaign.Views,
    } for campaign in campaigns]



    # Organize all data into a response object
    response_data = {
        'campaigns': campaigns_data

    }
    return jsonify(response_data), 200


@routes_bp.route('/saved_campaigns', methods=['GET'])
def saved_campaigns():
    
    influencer_id = request.args.get('influencer_id')  # Or use request.form or request.json for POST requests if needed

    influencer = Influencers.query.get(influencer_id)
    if not influencer:
        return jsonify({"message": "Influencer not found"}), 404

    campaigns_query = Saved.query.filter_by(Of=influencer_id).all()
    
    campaigns = []
    for saved in campaigns_query:
        campaign = Campaign.query.filter_by(Campaign_ID=saved.Saved,Flag='No').first()
        if campaign:
            campaigns.append(campaign)

    campaigns_data = [{
        'id': campaign.Campaign_ID,
        'name': campaign.Name,
        'desc': campaign.Desc[:20] + '...',  # Shorten description
        'start_date': campaign.Start_Date,
        'end_date': campaign.End_Date,
        'budget': campaign.Budget,
        'goals': campaign.Goals[:20],
        'visibility': campaign.Visibility,
        'category': campaign.Preferred_Category,
        'saved': 1 if Saved.query.filter_by(Saved=campaign.Campaign_ID,Of=influencer.Infuencer_ID).first() else 0,
        'views': campaign.Views,
    } for campaign in campaigns]



    # Organize all data into a response object
    response_data = {
        'campaigns': campaigns_data

    }
    return jsonify(response_data), 200



@routes_bp.route('/influencer_stats', methods=['GET'])
def inf_stats():
    
    influencerid=request.args.get('influencer_id')
    current_influencer = Influencers.query.get(influencerid)

    campaigns = Campaign.query.filter_by(Influencer=influencerid, Status='Accepted').all()
    payment_labels=[]
    payment_values=[]

    if not current_influencer:
        return jsonify({"message": "Influencer not found"}), 404

    campaigns = Campaign.query.filter_by(Influencer=influencerid, Status='Accepted').all()
    payment_labels=[]
    payment_values=[]

    rating_values=[0,0,0,0,0,0]
    rating_values[0] = len(Rating.query.filter_by(To=influencerid,Rating=0).all())
    rating_values[1] = len(Rating.query.filter_by(To=influencerid,Rating=1).all())
    rating_values[2] = len(Rating.query.filter_by(To=influencerid,Rating=2).all())
    rating_values[3] = len(Rating.query.filter_by(To=influencerid,Rating=3).all())
    rating_values[4] = len(Rating.query.filter_by(To=influencerid,Rating=4).all())
    rating_values[5] = len(Rating.query.filter_by(To=influencerid,Rating=5).all())

    percent_complete=[]
    percent_incomplete=[]

    for i in campaigns:
        payment_labels.append(i.Name)
        payment_values.append(i.Budget)

        if len(Ad_Request.query.filter(Ad_Request.Campaign == i.Campaign_ID).all()) != 0: 
            temp = 100*(len(Ad_Request.query.filter(Ad_Request.Campaign == i.Campaign_ID, Ad_Request.Status == 'Open').all())/len(Ad_Request.query.filter(Ad_Request.Campaign == i.Campaign_ID).all()))
        else:
            temp=0
        
        
        percent_incomplete.append(temp)
        percent_complete.append((100-temp))

    response_data = {
        'payment_values':payment_values,
        'payment_labels':payment_labels,
        'rating_values':rating_values,
        'percent_complete':percent_complete,
        'percent_incomplete':percent_incomplete
    }


    return jsonify(response_data), 200


@routes_bp.route('/influencer_profile', methods=['GET'])
def influencer_profile():

    # For GET request
    influencer_id = request.args.get('influencer_id')

    current_influencer = Influencers.query.get(influencer_id)
    now = datetime.now()

    influencer_campaigns = Campaign.query.filter(Campaign.Influencer==influencer_id, Campaign.Status=='Accepted', Campaign.Start_Date <= now, Campaign.End_Date >= now, Campaign.Flag=='No')
    data = {}

    for i in influencer_campaigns:
        if len(Ad_Request.query.filter(Ad_Request.Campaign == i.Campaign_ID).all()) != 0: 
            data[i] = 100*(len(Ad_Request.query.filter(Ad_Request.Campaign == i.Campaign_ID, Ad_Request.Status != 'Open').all())/len(Ad_Request.query.filter(Ad_Request.Campaign == i.Campaign_ID).all()))
        else:
            data[i]=0

    requested_campaigns = Campaign.query.filter(
        Campaign.Influencer==influencer_id,
        Campaign.Status == 'Requested_to',
        Campaign.Flag == 'No'
    ).all()

    campaign_data = [{
        'id': current_campaign.Campaign_ID,
        'name': current_campaign.Name,
        'desc': current_campaign.Desc,
        'start_date': current_campaign.Start_Date,
        'end_date': current_campaign.End_Date,
        'budget': current_campaign.Budget,
        'goals': current_campaign.Goals[:20],
        'visibility': current_campaign.Visibility,
        'category': current_campaign.Preferred_Category,
        'views': current_campaign.Views,
        'status': current_campaign.Status,
        'completion':data[current_campaign]
    } for current_campaign in influencer_campaigns]

    requested_campaign_data = [{
        'id': current_campaign.Campaign_ID,
        'name': current_campaign.Name,
        'desc': current_campaign.Desc,
        'start_date': current_campaign.Start_Date,
        'end_date': current_campaign.End_Date,
        'budget': current_campaign.Budget,
        'goals': current_campaign.Goals[:20],
        'visibility': current_campaign.Visibility,
        'category': current_campaign.Preferred_Category,
        'views': current_campaign.Views,
        'status': current_campaign.Status,
        'influencer':current_campaign.Influencer,
        'sponsor_name': Sponsors.query.get(current_campaign.Created_by).Name
    } for current_campaign in requested_campaigns]

    return jsonify({'active': campaign_data,'requested':requested_campaign_data}), 200

@routes_bp.route('/update_influencer', methods=['GET','POST'])
def update_influencer():
    from app import db

    if request.method == 'POST':
        
        influencer_id = request.form.get('influencer_id')
        current_influencer = Influencers.query.get(influencer_id)

        name = request.form.get('name')
        about = request.form.get('about')
        category = request.form.get('category')
        niche = request.form.get('niche')
        reach = request.form.get('reach')
        picname=None

    
        profpic = request.files.get('ProfilePic') 

        if profpic:
            profpic = request.files['ProfilePic']

            print(profpic.filename)

            profpicname = secure_filename(profpic.filename)
            picname = str(uuid.uuid1()) + '_' + profpicname

            upload_folder = current_app.config['UPLOAD_FOLDER']

        # Create the full path to save the file
            file_path = os.path.join(upload_folder, picname)

            profpic.save(file_path)
        
        try:

            current_influencer.Name = name
            current_influencer.About = about
            current_influencer.Category = category
            current_influencer.Niche = niche
            current_influencer.Reach = reach

            if picname:
                current_influencer.Profile_Pic = picname
            
            db.session.commit()
            return jsonify({"message": "Profile Updated successfully"}), 201

        except IntegrityError:
            db.session.rollback()
            return jsonify(message="Failed to update Profile"), 409

    # For GET request
    influencer_id = request.args.get('influencer_id')
    current_influencer = Influencers.query.get(influencer_id)
    current_influencer_data = {
            'id': current_influencer.Infuencer_ID,
            'name': current_influencer.Name,
            'about': current_influencer.About,
            'profile_pic': current_influencer.Profile_Pic,
            'category': current_influencer.Category,
            'niche': current_influencer.Niche,
            'reach': current_influencer.Reach,
            'views': current_influencer.Views,
            'rating': current_influencer.Avg_Rating,
            'rating_no': current_influencer.Rating_No,
            'flag': current_influencer.Flag,
            'created_at': current_influencer.Created_at 
        }
    

    return jsonify({'current_influencer':current_influencer_data}), 200


@routes_bp.route('/change_campaign', methods=['GET'])
def change():
    from app import db

    # For GET request
    campaign_id = request.args.get('campaign_id')
    print(campaign_id)
    ad_requests = Ad_Request.query.filter_by(Campaign=campaign_id).all()

    ad_data = [{
        'id':ad.Request_ID,
        'requirements':ad.Requirements,
        'payment':ad.Payment,
        'status':ad.Status
    } for ad in ad_requests]

    return jsonify({'ads':ad_data}), 200

@routes_bp.route('/mark_ad/<int:adid>', methods=['POST'])
def mark_ad(adid):
    from app import db
    try:
        # Fetch the campaign using the campaign ID
        ad = Ad_Request.query.get(adid)
        
        if not ad:
            return jsonify({'message': 'Campaign not found'}), 404
        
        ad.Status = 'Completed'
        db.session.commit()

        return  jsonify({"message": "Ad Marked successfully"}), 201
    except Exception as e:
        db.session.rollback()  # Rollback in case of any error
        return jsonify({'message': str(e)}), 500
    
@routes_bp.route('/undo_ad/<int:adid>', methods=['POST'])
def undo_ad(adid):
    from app import db
    try:
        # Fetch the campaign using the campaign ID
        ad = Ad_Request.query.get(adid)
        
        if not ad:
            return jsonify({'message': 'Campaign not found'}), 404
        
        ad.Status = 'Open'
        db.session.commit()

        return  jsonify({"message": "Ad Unmarked successfully"}), 201
    except Exception as e:
        db.session.rollback()  # Rollback in case of any error
        return jsonify({'message': str(e)}), 500
    
@routes_bp.route('/admin_home', methods=['GET'])
def admin_home():
    
    Labels_Sponsors = [
            "Health & Wellness",
            "Travel & Food",
            "Finance & Business",
            "Technology",
            "Entertainment",
            "Gaming",
            "Education",
            "Lifestyle",
            "Other"]
        
    Values_Sponsors=[]
        
    for i in Labels_Sponsors:
        temp = len(Sponsors.query.filter_by(Industry = i).all())
        Values_Sponsors.append(temp)

    Values_Influencers=[]
        
    for i in Labels_Sponsors:
        temp = len(Influencers.query.filter_by(Category = i).all())
        Values_Influencers.append(temp)
        
    Labels_Campaigns = [
        'Any',
        "Health & Wellness",
        "Travel & Food",
        "Finance & Business",
        "Technology",
        "Entertainment",
        "Gaming",
        "Education",
        "Lifestyle",
        "Other"]
        
    Values_Campaigns=[]
        
    for i in Labels_Campaigns:
        temp = len(Campaign.query.filter_by(Preferred_Category = i).all())
        Values_Campaigns.append(temp)


    NonFlagged_Values = [0,0,0]
    NonFlagged_Values[0] = len(Campaign.query.filter_by(Flag='No').all())
    NonFlagged_Values[1] = len(Sponsors.query.filter_by(Flag='No').all())
    NonFlagged_Values[2] = len(Influencers.query.filter_by(Flag='No').all())

    Flagged_Values = [0,0,0]
    Flagged_Values[0] = len(Campaign.query.filter_by(Flag='Yes').all())
    Flagged_Values[1] = len(Sponsors.query.filter_by(Flag='Yes').all())
    Flagged_Values[2] = len(Influencers.query.filter_by(Flag='Yes').all())
    
    response_data = {
        'Labels_Sponsors': Labels_Sponsors,
        'Values_Sponsors': Values_Sponsors,
        'Values_Influencers': Values_Influencers,
        'Labels_Campaigns': Labels_Campaigns,
        'Values_Campaign': Values_Campaigns,
        'NonFlagged_Values': NonFlagged_Values,
        'Flagged_Values': Flagged_Values
    }

    return jsonify(response_data), 200

@routes_bp.route('/admin_campaigns', methods=['GET'])
def admin_campaigns():

    campaigns = Campaign.query.all()
    
    campaign_data = [{
        'id': current_campaign.Campaign_ID,
        'name': current_campaign.Name,
        'desc': current_campaign.Desc,
        'start_date': current_campaign.Start_Date,
        'end_date': current_campaign.End_Date,
        'budget': current_campaign.Budget,
        'goals': current_campaign.Goals[:20],
        'visibility': current_campaign.Visibility,
        'category': current_campaign.Preferred_Category,
        'views': current_campaign.Views,
        'status': current_campaign.Status,
        'flag': current_campaign.Flag
    } for current_campaign in campaigns]

    

    response_data = {
        'campaigns': campaign_data
    }

    

    return jsonify(response_data), 200

@routes_bp.route('/flag_campaign/<int:campaignid>', methods=['POST'])
def flag_campaign(campaignid):
    from app import db

    campaign = Campaign.query.get(campaignid)
    campaign.Flag = 'Yes'
    db.session.commit()
    return jsonify({'message': "Campaign Flagged"}), 200

@routes_bp.route('/unflag_campaign/<int:campaignid>', methods=['POST'])
def unflag_campaign(campaignid):
    from app import db

    campaign = Campaign.query.get(campaignid)
    campaign.Flag = 'No'
    db.session.commit()
    return jsonify({'message': "Campaign Unflagged"}), 200


@routes_bp.route('/admin_sponsors', methods=['GET'])
def admin_sponsors():

    sponsors = Sponsors.query.all()
    
    sponsors_data = [{
        'id': sponsor.Sponser_ID,
        'name': sponsor.Name,
        'budget': sponsor.Budget,
        'industry': sponsor.Industry,
        'flag': sponsor.Flag
    } for sponsor in sponsors]

    

    response_data = {
        'sponsors': sponsors_data
    }  

    return jsonify(response_data), 200

@routes_bp.route('/flag_sponsor/<int:sponsorid>', methods=['POST'])
def flag_sponsor(sponsorid):
    from app import db

    sponsor = Sponsors.query.get(sponsorid)
    sponsor.Flag = 'Yes'
    db.session.commit()
    return jsonify({'message': "Sponsor Flagged"}), 200

@routes_bp.route('/unflag_sponsor/<int:sponsorid>', methods=['POST'])
def unflag_sponsor(sponsorid):
    from app import db

    sponsor = Sponsors.query.get(sponsorid)
    sponsor.Flag = 'No'
    db.session.commit()
    return jsonify({'message': "Sponsor Unflagged"}), 200


    
@routes_bp.route('/admin_influencers', methods=['GET'])
def admin_influencers():

    influencers = Influencers.query.all()
    
    influencers_data = [{
        'id': influencer.Infuencer_ID,
        'name': influencer.Name,
        'about': influencer.About,
        'category': influencer.Category,
        'reach': influencer.Reach,
        'niche': influencer.Niche,
        'rating': influencer.Avg_Rating,
        'views': influencer.Views,
        'flag': influencer.Flag
    } for influencer in influencers]
    

    response_data = {
        'influencers': influencers_data
    }  

    return jsonify(response_data), 200

@routes_bp.route('/flag_influencer/<int:influencerid>', methods=['POST'])
def flag_influencer(influencerid):
    from app import db

    influencer = Influencers.query.get(influencerid)
    influencer.Flag = 'Yes'
    db.session.commit()
    return jsonify({'message': "Influencer Flagged"}), 200

@routes_bp.route('/unflag_influencer/<int:influencerid>', methods=['POST'])
def unflag_influencer(influencerid):
    from app import db

    influencer = Influencers.query.get(influencerid)
    influencer.Flag = 'No'
    db.session.commit()
    return jsonify({'message': "Influencer Unflagged"}), 200

@routes_bp.route('/admin_flagged', methods=['GET'])
def admin_flagged():

    influencers = Influencers.query.filter_by(Flag='Yes').all()
    campaigns = Campaign.query.filter_by(Flag='Yes').all()
    sponsors = Sponsors.query.filter_by(Flag='Yes').all()
    
    influencers_data = [{
        'id': influencer.Infuencer_ID,
        'name': influencer.Name,
        'about': influencer.About,
        'category': influencer.Category,
        'reach': influencer.Reach,
        'niche': influencer.Niche,
        'rating': influencer.Avg_Rating,
        'views': influencer.Views,
        'flag': influencer.Flag
    } for influencer in influencers]

    sponsors_data = [{
        'id': sponsor.Sponser_ID,
        'name': sponsor.Name,
        'budget': sponsor.Budget,
        'industry': sponsor.Industry,
        'flag': sponsor.Flag
    } for sponsor in sponsors]

    campaign_data = [{
        'id': current_campaign.Campaign_ID,
        'name': current_campaign.Name,
        'desc': current_campaign.Desc,
        'start_date': current_campaign.Start_Date,
        'end_date': current_campaign.End_Date,
        'budget': current_campaign.Budget,
        'goals': current_campaign.Goals[:20],
        'visibility': current_campaign.Visibility,
        'category': current_campaign.Preferred_Category,
        'views': current_campaign.Views,
        'status': current_campaign.Status,
        'flag': current_campaign.Flag
    } for current_campaign in campaigns]


    

    response_data = {
        'influencers': influencers_data,
        'campaigns': campaign_data,
        'sponsors': sponsors_data
    }  

    return jsonify(response_data), 200


@routes_bp.route('/View_influencer', methods=['GET'])
def influencer_view():
    from app import db

    # For GET request
    influencer_id = request.args.get('influencer_id')
    sponsor_id = request.args.get('sponsor_id')
    print(influencer_id)

    influencer = Influencers.query.get(influencer_id)
    influencer.Views = influencer.Views+1
    db.session.commit()
    now = datetime.now()
    
    user_campaigns_data=[]
    influencer_campaigns = Campaign.query.filter(Campaign.Influencer==influencer_id, Campaign.Status=='Accepted', Campaign.Start_Date <= now, Campaign.End_Date >= now, Campaign.Flag=='No')
    data = {}

    for i in influencer_campaigns:
        if len(Ad_Request.query.filter(Ad_Request.Campaign == i.Campaign_ID).all()) != 0: 
            data[i] = 100*(len(Ad_Request.query.filter(Ad_Request.Campaign == i.Campaign_ID, Ad_Request.Status != 'Open').all())/len(Ad_Request.query.filter(Ad_Request.Campaign == i.Campaign_ID).all()))
        else:
            data[i]=0

    ratings = Rating.query.filter_by(To=influencer_id).all()

    campaign_data = [{
        'id': current_campaign.Campaign_ID,
        'name': current_campaign.Name,
        'desc': current_campaign.Desc,
        'start_date': current_campaign.Start_Date,
        'end_date': current_campaign.End_Date,
        'budget': current_campaign.Budget,
        'goals': current_campaign.Goals[:20],
        'visibility': current_campaign.Visibility,
        'category': current_campaign.Preferred_Category,
        'views': current_campaign.Views,
        'status': current_campaign.Status,
        'completion':data[current_campaign]
    } for current_campaign in influencer_campaigns]

    influencer_data = {
        'id': influencer.Infuencer_ID,
        'name': influencer.Name,
        'about': influencer.About,
        'category': influencer.Category,
        'reach': influencer.Reach,
        'niche': influencer.Niche,
        'rating': influencer.Avg_Rating,
        'rating_no': influencer.Rating_No,
        'views': influencer.Views,
        'flag': influencer.Flag,
        'created_by': influencer.Created_by,
        'profile_pic': influencer.Profile_Pic
    }

    rating_data = [{

        'rating':rating.Rating,
        'message': rating.Message,
        'by': Sponsors.query.get(rating.By).Name,
        'rated_at': rating.Rated_At
    } for rating in ratings]


    if sponsor_id:
        user_campaigns = Campaign.query.filter(
        Campaign.Status == 'Open',Campaign.Start_Date <= datetime.now(),Campaign.End_Date >= datetime.now(),Campaign.Flag == 'No', Campaign.Created_by==sponsor_id
        ).all()

        user_campaigns_data = [{
            'id': campaign.Campaign_ID,
            'name': campaign.Name,
            'desc': campaign.Desc[:20] + '...',  # Shorten description
            'start_date': campaign.Start_Date,
            'end_date': campaign.End_Date,
            'budget': campaign.Budget,
            'goals': campaign.Goals[:20],
            'visibility': campaign.Visibility,
            'category': campaign.Preferred_Category,
            'views': campaign.Views,
        } for campaign in user_campaigns]        

    

    return jsonify({'active': campaign_data,'influencer': influencer_data,'ratings':rating_data,'user_campaigns':user_campaigns_data}), 200


@routes_bp.route('/show_campaign', methods=['GET','POST'])
def show():
    from app import db
    

    # For GET request
    campaign_id = request.args.get('campaign_id')
    influencer_id = request.args.get('influencer_id')
    current_campaign = Campaign.query.get(campaign_id)
    current_campaign.Views = current_campaign.Views+1
    db.session.commit()
    ad_requests = Ad_Request.query.filter_by(Campaign=campaign_id).all()

    current_campaign_data = {
        'id': current_campaign.Campaign_ID,
        'name': current_campaign.Name,
        'desc': current_campaign.Desc,
        'start_date': current_campaign.Start_Date,
        'end_date': current_campaign.End_Date,
        'budget': current_campaign.Budget,
        'goals': current_campaign.Goals,
        'visibility': current_campaign.Visibility,
        'category': current_campaign.Preferred_Category,
        'views': current_campaign.Views,
        'created_by': current_campaign.Created_by,
        'created_by_name': Sponsors.query.get(current_campaign.Created_by).Name,
        'created_by_user_id': Sponsors.query.get(current_campaign.Created_by).Created_by,
        'flag': current_campaign.Flag
    }

    ad_data = [{
        'id':ad.Request_ID,
        'requirements':ad.Requirements,
        'payment':ad.Payment,
        'status': ad.Status
    } for ad in ad_requests]

    messages = Messages.query.filter_by(Campaign=campaign_id).order_by(Messages.Date.asc()).all()

    message_data = [{
        'from': Sponsors.query.get(message.From).Name if message.To==1 else Influencers.query.get(message.From).Name,
        'message': message.Message,
        'date': message.Date
    } for message in messages]

    if influencer_id:
        saved_campaign = Saved.query.filter_by(Saved=campaign_id, Of=influencer_id).first()
        current_campaign_data['saved'] = 1 if saved_campaign else 0
    else:
        # If no influencer_id is provided, set saved as 0
        current_campaign_data['saved'] = 0

    

    return jsonify({'campaign': current_campaign_data,'ads':ad_data,'messages':message_data}), 200    

@routes_bp.route('/create_comment', methods=['POST'])
def create_commment():
    from app import db

    data = request.get_json()
    message = data.get('message')
    type = data.get('type')
    id = data.get('id')
    campaign = data.get('campaign')

    to = 1 if type=='sponsor' else 0
    
    if not data or not message or not id or not campaign:
        return jsonify(message="All fields are required"), 400

    new_message = Messages(
                Campaign=campaign,
                From=int(id),
                To = to,
                Message=message
            )
    try:
        db.session.add(new_message)
        db.session.commit()
        return jsonify(message="Commment successfully"), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify(message="Failed"), 409
    

@routes_bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    filter_type = request.args.get('filter')
    filter_category = request.args.get('category')
    search_results = []

    if query:

        if filter_type in ['campaign', 'all']:
            campaign_query = Campaign.query.filter(
                (Campaign.Name.ilike(f'%{query}%')) | (Campaign.Desc.ilike(f'%{query}%'))
            ).filter_by(Status='Open',Flag='No',Visibility='All')

            if filter_category:
                campaign_query = campaign_query.filter_by(Preferred_Category=filter_category)

            campaigns = campaign_query.all()

            for campaign in campaigns:
                score = 0
                if query.lower() in campaign.Name.lower():
                    score += 2
                if query.lower() in campaign.Desc.lower():
                    score += 1
                search_results.append({
                    'type': 'campaign',
                    'object': {
                        'Name': campaign.Name,
                        'Desc': campaign.Desc,
                        'Preferred_Category': campaign.Preferred_Category,
                        'Goals': campaign.Goals,
                        'Budget': campaign.Budget,
                        'Start_Date': campaign.Start_Date.isoformat(),
                        'End_Date': campaign.End_Date.isoformat(),
                        'Views': campaign.Views,
                        'Campaign_ID': campaign.Campaign_ID,
                        'Created_by': campaign.Created_by,
                        'Created_by_name': Sponsors.query.get(campaign.Created_by).Name
                    },
                    'score': score
                })


        if filter_type in ['influencer', 'all']:
            influencer_query = Influencers.query.filter(
                (Influencers.Name.ilike(f'%{query}%')) | (Influencers.About.ilike(f'%{query}%'))
            ).filter_by(Flag='No')

            if filter_category:
                influencer_query = influencer_query.filter_by(Category=filter_category)

            influencers = influencer_query.all()

            for influencer in influencers:
                score = 0
                if query.lower() in influencer.Name.lower():
                    score += 2
                if query.lower() in influencer.About.lower():
                    score += 1
                search_results.append({
                    'type': 'influencer',
                    'object': {
                        'Name': influencer.Name,
                        'About': influencer.About,
                        'Category': influencer.Category,
                        'Niche': influencer.Niche,
                        'Reach': influencer.Reach,
                        'Views': influencer.Views,
                        'Infuencer_ID': influencer.Infuencer_ID,
                        'Avg_Rating':influencer.Avg_Rating
                    },
                    'score': score
                })


        search_results = sorted(search_results, key=lambda x: x['score'], reverse=True)
    else:

        if filter_type in ['campaign', 'all']:
            campaign_query = Campaign.query.filter_by(Status='Open',Flag='No')

            if filter_category:
                campaign_query = campaign_query.filter_by(Preferred_Category=filter_category)

            campaigns = campaign_query.all()

            for campaign in campaigns:
                search_results.append({
                    'type': 'campaign',
                    'object': {
                        'Name': campaign.Name,
                        'Desc': campaign.Desc,
                        'Preferred_Category': campaign.Preferred_Category,
                        'Goals': campaign.Goals,
                        'Budget': campaign.Budget,
                        'Start_Date': campaign.Start_Date.isoformat(),
                        'End_Date': campaign.End_Date.isoformat(),
                        'Views': campaign.Views,
                        'Campaign_ID': campaign.Campaign_ID,
                        'Created_by': campaign.Created_by,
                        'Created_by_name': Sponsors.query.get(campaign.Created_by).Name
                    },
                    'score': 0
                })

        if filter_type in ['influencer', 'all']:
            influencer_query = Influencers.query.filter_by(Flag='No')

            if filter_category:
                influencer_query = influencer_query.filter_by(Category=filter_category)

            influencers = influencer_query.all()

            for influencer in influencers:
                search_results.append({
                    'type': 'influencer',
                    'object': {
                        'Name': influencer.Name,
                        'About': influencer.About,
                        'Category': influencer.Category,
                        'Niche': influencer.Niche,
                        'Reach': influencer.Reach,
                        'Views': influencer.Views,
                        'Infuencer_ID': influencer.Infuencer_ID
                    },
                    'score': 0
                })


    return jsonify(search_results),200


@routes_bp.route('/pending_sponsors', methods=['GET'])
def get_pending_sponsors():
    # Query the sponsors table to get all sponsors with the status 'pending'
    pending_sponsors = Sponsors.query.filter_by(Status='Pending').all()
    
    # Check if there are any pending sponsors
    
    # Serialize the sponsor data into a list of dictionaries
    sponsor_list = []
    if pending_sponsors:
        for sponsor in pending_sponsors:
            sponsor_list.append({
                'id': sponsor.Sponser_ID,
                'name': sponsor.Name,
                'budget': sponsor.Budget,
                'industry': sponsor.Industry,
                'creator': sponsor.Created_by,
                'created_at': sponsor.Created_at,
                'status': sponsor.Status
            })
    
    # Return the list of pending sponsors as a JSON response
    return jsonify(sponsors=sponsor_list), 200


@routes_bp.route('/approve_sponsor/<int:sponsor_id>', methods=['POST'])
def approve_sponsor(sponsor_id):
    from app import db
    sponsor = Sponsors.query.get_or_404(sponsor_id)
    sponsor.Status = 'Approved'  # Change the status to approved
    db.session.commit()

    return jsonify(message="Sponsor approved successfully"), 200




@routes_bp.route('/chat/<int:member1_id>/<int:member2_id>')
def get_messages(member1_id, member2_id):
    # Fetch messages between member1 and member2, considering reversed sender/receiver cases
    messages = ChatMessage.query.filter(
        ((ChatMessage.Sender_Id == member1_id) & (ChatMessage.Receiver_Id == member2_id)) |
        ((ChatMessage.Sender_Id == member2_id) & (ChatMessage.Receiver_Id == member1_id))
    ).order_by(ChatMessage.timestamp).all()

    # Function to get name based on user_id, by looking at the "created_by" field of Sponsor or Influencer
    def get_user_name(user_id):
        # Check if the user is a sponsor or influencer by trying to fetch from both tables
        if Users.query.get(user_id).Type == 'sponsor':
            sponsor = Sponsors.query.filter_by(Created_by=user_id).first()
            return sponsor.Name
        elif Users.query.get(user_id).Type == 'influencer':
            influencer = Influencers.query.filter_by(Created_by=user_id).first()
            return influencer.Name
        return None

    # Prepare message data including sender/receiver names and types
    message_data = []
    for msg in messages:
        # For each message, correctly assign sender and receiver names based on their IDs and types
        sender_name = get_user_name(msg.Sender_Id)
        receiver_name = get_user_name(msg.Receiver_Id)
        message_data.append({
            'sender_name': sender_name,
            'receiver_name': receiver_name,
            'message': msg.Message,
            'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        })

    # Get the names of person1 and person2 (senders and receivers)
    person1_name = get_user_name(member1_id)
    person2_name = get_user_name(member2_id)

    data = {
        'messages': message_data,
        'person1_name': person1_name,
        'person2_name': person2_name,
    }

    return jsonify(data), 200

@routes_bp.route('/send_message', methods=['POST'])
def send_message():
    from app import db
    data = request.json
    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    message = data.get('message')
    sender_type = data.get('sender_type')
    receiver_type = data.get('receiver_type')

    if not sender_id or not receiver_id or not message:
        return jsonify({'error': 'Missing required fields'}), 400

    new_message = ChatMessage(
        Sender_Id=sender_id,
        Sender_Type=sender_type,
        Receiver_Id=receiver_id,
        Receiver_Type=receiver_type,
        Message=message
    )

    db.session.add(new_message)
    db.session.commit()

    return jsonify({'status': 'Message sent'}), 200



@routes_bp.route('/')
def home():
    print("Hello")
    return 'Test'