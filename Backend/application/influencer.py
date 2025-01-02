from flask import Blueprint,request,jsonify,current_app
from flask_jwt_extended import jwt_required,get_jwt_identity
from .model import User, Campaign, AdRequest,Ad
from . import db
from sqlalchemy.exc import IntegrityError




influencer = Blueprint('influencer', __name__)

#Influencer detail
@influencer.route("/dashboard/influencer_details", methods=["GET"])
@jwt_required()
def get_sponsor_details():
    user_id = get_jwt_identity()
    
    # Query the user from the database
    user = User.query.get(user_id)
    
    if not user or not user.is_influencer():
        return jsonify({'message': 'Unauthorized access'})

    sponsor_data = {
        'id': user.id,
        'username': user.username,
        'image': user.image,
        'email': user.email,
        'name': user.name,
        'socialmedia': user.socialmedia,
        'about': user.about,
        'role': user.role.name,
        'reach': user.reach,
        'niche' : user.niche,
        'date_created': user.date_created,
        'last_login': user.last_login
    }
    
    return jsonify(sponsor_data)

# Influencer updates details
@influencer.route("/updatedetail", methods=["PUT"])
@jwt_required()
def update_campaign():
    user_id = get_jwt_identity()  
    user = User.query.get(user_id)
    if not user or not user.is_influencer():
        return jsonify({'message': 'Unauthorized access'})

    data = request.json 

    user.name = data.get('name', user.name)
    user.username = data.get('username', user.username)
    user.email = data.get('email',user.email)
    user.socialmedia = data.get('socialmedia',user.socialmedia)
    user.reach = data.get('reach',user.reach)
    user.niche = data.get('niche',user.niche)
    user.about = data.get('about',user.about)

    db.session.commit()
    return jsonify({'message': 'Detail updated successfully'})

#get all campain
@influencer.route("/allcampaigns", methods=["GET"])
@jwt_required()
def get_all_campaigns():
    user_id = get_jwt_identity()  
    user = User.query.get(user_id)

    if not user or not user.is_influencer():
        return jsonify({'message': 'Unauthorized access'})

    
    # campaigns = Campaign.query.filter_by(flag=False).all()
    # campaigns = Campaign.query.filter_by( flag=False).all()
    campaigns = Campaign.query.filter(
    Campaign.flag == False,
    Campaign.sponsor.has(is_flagged=False)).all()

    
    campaign_list = []
    for campaign in campaigns:
        campaign_data = {
            'id': campaign.id,
            'name': campaign.name,
            'description': campaign.description,
            'start_date': campaign.start_date.strftime('%Y-%m-%d'),
            'end_date': campaign.end_date.strftime('%Y-%m-%d'),
            'budget': campaign.budget,
            'visibility': campaign.visibility,
            'goals': campaign.goals,
            'target': campaign.target,
            'image': campaign.image,
            'completion_percentage': campaign.completion_percentage(),
            'sponsor_id': campaign.sponsor_id,
        }
        campaign_list.append(campaign_data)

   
    return jsonify({'campaigns': campaign_list})

#  creates an ad request
@influencer.route("/make_ad_request", methods=["POST"])
@jwt_required()
def make_ad_request():
    user_id = get_jwt_identity()  
    user = User.query.get(user_id)
    if not user or not user.is_influencer():
        return jsonify({'message': 'Unauthorized access'})
    
    data = request.json
    # print(data)
    campaign = Campaign.query.get(data['campaign_id'])

    if not campaign:
        return jsonify({'message': 'Campaign not found'})
   
    existing_ad_request = AdRequest.query.filter_by(
        campaign_id=campaign.id,
        influencer_id=user.id
    ).first()

    if existing_ad_request:
        return jsonify({'message': 'Ad request already exists'})

    
    requirements = campaign.goals  
    if campaign.target > 0:
        payment_amount = campaign.budget // campaign.target 
    else:
        payment_amount = campaign.budget
      

    # Create a new ad request
    new_ad_request = AdRequest(
        campaign_id=campaign.id,
        influencer_id=user.id,
        requirements=requirements,
        sender_id=user_id,
        payment_amount=payment_amount,
        status='Pending'
    )

    try:
        db.session.add(new_ad_request)
        db.session.commit()
        return jsonify({'message': 'Ad request created successfully'})
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Ad request creation failed'})

#  deletes an existing ad request
@influencer.route("/ad_request_dellete/<int:ad_request_id>", methods=["DELETE"])
@jwt_required()
def delete_ad_request_inf( ad_request_id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    ad_request = AdRequest.query.get(ad_request_id)
    if ad_request.sender_id != current_user.id:
        return jsonify({'message': 'Unauthorized: Only the sender can delete this ad request'})
    
    db.session.delete(ad_request)
    db.session.commit()
    return jsonify({'message': 'Ad request deleted successfully'})
    

    
@influencer.route("/inf_ad_requests/received", methods=["GET"])
@jwt_required()
def get_received_ad_requests_inf():
    user_id = get_jwt_identity()  
    user = User.query.get(user_id)
    if not user or not user.is_influencer():
        return jsonify({'message': 'Unauthorized access'})
    
    received_requests = AdRequest.query.join(Campaign).filter(
        AdRequest.influencer_id == user_id,
        AdRequest.sender_id != user_id,  
        Campaign.flag == False, Campaign.sponsor.has(is_flagged=False),
        Campaign.visibility.in_(["public", "private"])    
    ).all()

    result = [
        {
            'ad_request_id': ad_request.id,
            'campaign_name': ad_request.campaign.name,
            'influencer_name': ad_request.influencer.name,
            'requirements': ad_request.requirements,
            'payment_amount': ad_request.payment_amount,
            'status': ad_request.status
        }
        for ad_request in received_requests
    ]

    return jsonify(result)

    
@influencer.route("/mywork", methods=["GET"])
@jwt_required()
def my_work():
    user_id = get_jwt_identity()  
    user = User.query.get(user_id)
    if not user or not user.is_influencer():
        return jsonify({'message': 'Unauthorized access'})
    accepted_requests = AdRequest.query.filter_by(
        influencer_id=user_id,
        status='Accepted'
    ).all()

    campaigns = []
    for ad_request in accepted_requests:
        if not ad_request.ads:
            campaign = Campaign.query.get(ad_request.campaign_id)
            if campaign and not campaign.flag and campaign.sponsor.is_flagged == False:  
                campaigns.append({
                    'ad_request_id': ad_request.id,
                    'campaign_id': campaign.id,
                    'name': campaign.name,
                    'description': campaign.description,
                    'start_date': campaign.start_date.strftime('%Y-%m-%d'),
                    'end_date': campaign.end_date.strftime('%Y-%m-%d'),
                    'budget': campaign.budget,
                    'visibility': campaign.visibility,
                    'completion_percentage': campaign.completion_percentage(),
                    'target': campaign.target,
                    'goals': campaign.goals,
                    'image': campaign.image,
                    'sponsor_name': campaign.sponsor.name
                })

    return jsonify(campaigns)

@influencer.route("/completemywork", methods=["GET"])
@jwt_required()
def my_complete_work():
    user_id = get_jwt_identity()  
    user = User.query.get(user_id)
    if not user or not user.is_influencer():
        return jsonify({'message': 'Unauthorized access'})
    accepted_requests = AdRequest.query.filter_by(
        influencer_id=user_id,
        status='Accepted'
    ).all()

    campaigns = []
    for ad_request in accepted_requests:
        if ad_request.ads:
            campaign = Campaign.query.get(ad_request.campaign_id)
            if campaign and not campaign.flag and campaign.sponsor.is_flagged == False:  
                campaigns.append({
                    'ad_request_id': ad_request.id,
                    'campaign_id': campaign.id,
                    'name': campaign.name,
                    'description': campaign.description,
                    'start_date': campaign.start_date.strftime('%Y-%m-%d'),
                    'end_date': campaign.end_date.strftime('%Y-%m-%d'),
                    'budget': campaign.budget,
                    'visibility': campaign.visibility,
                    'completion_percentage': campaign.completion_percentage(),
                    'target': campaign.target,
                    'goals': campaign.goals,
                    'image': campaign.image,
                    'sponsor_name': campaign.sponsor.name
                })

    return jsonify(campaigns)


@influencer.route("/create_ad", methods=["POST"])
@jwt_required()
def create_ad():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user.is_influencer():
        return jsonify({'message': 'Unauthorized access'})

    data = request.json
    ad_request_id = data.get('ad_request_id')
    name = data.get('name', '').strip()
    link = data.get('link', '').strip()

    if not ad_request_id or not name or not link:
        return jsonify({'message': 'Missing required fields'})

    ad_request = AdRequest.query.get(ad_request_id)
    if not ad_request:
        return jsonify({'message': 'Ad request not found'})

    if ad_request.influencer_id != current_user_id or ad_request.status != 'Accepted':
        return jsonify({'message': 'Ad request not valid for ad creation'})

    campaign = Campaign.query.get(ad_request.campaign_id)
    if not campaign or campaign.flag:
        return jsonify({'message': 'Campaign is not valid or is flagged'})

    existing_ad = Ad.query.filter_by(ad_request_id=ad_request_id).first()
    # print(existing_ad)
    if existing_ad:
        return jsonify({'message': 'Ad already exists for this ad request'})

    # Create the new ad
    new_ad = Ad(
        name=name,
        link=link,
        ad_request_id=ad_request_id,
        campaign_id=ad_request.campaign_id
    )

    try:
    
        db.session.add(new_ad)
        db.session.commit()
        return jsonify({'message': 'Ad created successfully', 'ad_id': new_ad.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to create ad', 'error': str(e)})
    
@influencer.route("/my_ads", methods=["GET"])
@jwt_required()
def get_my_ads():
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)

    if not current_user or not current_user.is_influencer():
        return jsonify({'message': 'Unauthorized access'})

    ad_requests = AdRequest.query.filter_by(influencer_id=user_id, status='Accepted').all()
    ads = []
    for ad_request in ad_requests:
        related_ads = Ad.query.filter_by(ad_request_id=ad_request.id).all()
        for ad in related_ads:
            ads.append({
                'ad_id': ad.id,
                'ad_name': ad.name,
                'ad_link': ad.link,
                'campaign_id': ad.campaign_id,
                'campaign_name': ad.campaign.name,
                'campaign_description': ad.campaign.description,
                'sponsor_name': ad.campaign.sponsor.name,
            })

    return jsonify(ads)
