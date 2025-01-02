import os
from flask import Blueprint,request,jsonify,current_app,send_from_directory
from .model import Role,User, Campaign, AdRequest
from flask_jwt_extended import jwt_required,get_jwt_identity,current_user,get_jwt
from . import db
from application import cache


admin = Blueprint('admin', __name__)

@admin.route('/show/<filename>', methods=['GET'])
def show(filename):
    # app_root = os.path.dirname(os.path.abspath(__file__))
    app_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # print('approot:',app_root)
    file_path = os.path.join(app_root, 'static', 'upload', filename)
    # print('file path:', file_path)

    if os.path.exists(file_path):
        return send_from_directory(os.path.join(app_root, 'static', 'upload'), filename)
    else:
        # print('File not found:', filename)
        return 'File not found'
    
@admin.route("/dashboard/admin_details", methods=["GET"])
@cache.cached(timeout=20)
@jwt_required()
def get_admin_details():
    # Decode JWT manually
    jwt_data = get_jwt()
    user_id = jwt_data["sub"]
    
    # Query the user from the database
    user = User.query.get(user_id)
    
    if not user or not user.is_admin():
        return jsonify({'message': 'Unauthorized access'}), 403

    admin_data = {
        'id': user.id,
        'username': user.username,
        'image': user.image,
        'email': user.email,
        'name': user.name,
        'role': user.role.name,
        'date_created': user.date_created,
        'last_login': user.last_login
    }
    return jsonify(admin_data)

@admin.route("/dashboard/new_sponsors", methods=["GET"])
@jwt_required()
def new_sponsors():
    try:
        # Query for users with the 'Sponsor' role who are not approved
        sponsors_role = Role.query.filter_by(name='Sponsor').first()
        
        if not sponsors_role:
            return jsonify({"error": "Sponsor role not found"}), 404
        
        new_sponsors = User.query.filter_by(
            role_id=sponsors_role.id,
            is_approved=False
        ).all()
        
        
        sponsor_list = []
        for sponsor in new_sponsors:
            sponsor_data = {
                'id': sponsor.id,
                'name': sponsor.name,
                'image':sponsor.image,
                'email': sponsor.email,
                'company':sponsor.company,
                'about': sponsor.about,
                'username': sponsor.username,
                'date_created': sponsor.date_created,
                'last_login': sponsor.last_login
            }
            sponsor_list.append(sponsor_data)
        
        return jsonify(sponsor_list)
    
    except Exception as e:
        return jsonify({"error": str(e)})

@admin.route("/approve_sponsor/<int:user_id>", methods=["POST"])
@jwt_required()
def approve_sponsor(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"})

    if user.role.name != 'Sponsor':
        return jsonify({"message": "User is not a sponsor"})

    user.is_approved = True
    db.session.commit()
    
    return jsonify({"message": "Sponsor approved successfully"})

@admin.route("/reject_sponsor/<int:user_id>", methods=["POST"])
@jwt_required()
def reject_sponsor(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"})

    if user.role.name != 'Sponsor':
        return jsonify({"message": "User is not a sponsor"})

    user.is_rejected = True
    db.session.commit()
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({"message": "Sponsor rejected successfully"})



@admin.route("/dashboard/sponsors", methods=["GET"])
@jwt_required()
def get_all_sponsors():
    # Get all approved sponsors
    role_id = Role.query.filter_by(name='Sponsor').first().id
    sponsors = User.query.filter_by(role_id=role_id, is_approved=True).all()

    sponsor_list = []
    for sponsor in sponsors:
        
        campaigns = []
        for campaign in sponsor.campaigns: 
            if not campaign.flag:  
                campaign_data = {
                    'id': campaign.id,
                    'name': campaign.name,
                    'description': campaign.description,
                    'start_date': campaign.start_date,
                    'end_date': campaign.end_date,
                    'budget': campaign.budget,
                    'visibility': campaign.visibility,
                    'goals': campaign.goals,
                    'target': campaign.target,
                    'image': campaign.image,
                    'flag': campaign.flag
                }
                campaigns.append(campaign_data)
        
        # Sponsor data
        sponsor_data = {
            'id': sponsor.id,
            'username': sponsor.username,
            'email': sponsor.email,
            'name': sponsor.name,
            'image': sponsor.image,
            'company': sponsor.company,
            'about': sponsor.about,
            'date_created': sponsor.date_created,
            'last_login': sponsor.last_login,
            'campaigns': campaigns,
            'is_flagged' : sponsor.is_flagged 

        }
        sponsor_list.append(sponsor_data)

    return jsonify(sponsor_list)

@admin.route('/dashboard/users/<int:user_id>/toggle-flag', methods=['POST'])
@jwt_required()
def toggle_sponsor_flag(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"})
    
    user.is_flagged = not user.is_flagged
    db.session.commit()
    flag=user.is_flagged

    if user.is_sponsor() :
        for campaign in user.campaigns:
            campaign.flag = flag
    db.session.commit() 
    return jsonify({
        "id": user.id,
        "is_flagged": user.is_flagged
    })

@admin.route('/dashboard/campaigns/<int:campaign_id>/toggle-flag', methods=['POST'])
@jwt_required()
def toggle_campaign_flag(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    
    if not campaign:
        return jsonify({"msg": "campaign not found"})
    
   
    campaign.flag = not campaign.flag
    db.session.commit()
    
    return jsonify({
        "id": campaign.id,
        "flag": campaign.flag
    })

# @admin.route("/dashboard/sponsors", methods=["GET"])
# @jwt_required()
# def get_all_sponsors():
#     # sponsors = User.query.filter_by(role_id=Role.query.filter_by(name='Sponsor').first().id).all()
#     sponsors = User.query.filter_by(role_id=Role.query.filter_by(name='Sponsor').first().id, is_approved=True).all() 
#     sponsor_list = []
#     for sponsor in sponsors:
#         sponsor_data = {
#             'id': sponsor.id,
#             'username': sponsor.username,
#             'email': sponsor.email,
#             'name': sponsor.name,
#             'image': sponsor.image,
#             'company': sponsor.company,
#             'about' : sponsor.about,
#             'date_created': sponsor.date_created,
#             'last_login': sponsor.last_login
#         }
#         sponsor_list.append(sponsor_data)
#     return jsonify(sponsor_list)

@admin.route("/dashboard/influencers", methods=["GET"])
@jwt_required()
def get_all_influencers():
    influencers = User.query.filter_by(role_id=Role.query.filter_by(name='Influencer').first().id).all()
    influencer_list = []
    for influencer in influencers:
        influencer_data = {
            'id': influencer.id,
            'username': influencer.username,
            'email': influencer.email,
            'name': influencer.name,
            'image': influencer.image,
            'reach' : influencer.reach,
            'niche' : influencer.niche,
            'about' : influencer.about,
            'socialmedia': influencer.socialmedia,
            'date_created': influencer.date_created,
            'last_login': influencer.last_login,
            'is_flagged' : influencer.is_flagged

        }
        influencer_list.append(influencer_data)
    return jsonify(influencer_list)


@admin.route("/dashboard/campaigns", methods=["GET"])
@jwt_required()
def get_all_campaigns():
    campaigns = Campaign.query.all()
    campaign_list = []
    for campaign in campaigns:
        campaign_data = {
            'id': campaign.id,
            'name': campaign.name,
            'description': campaign.description,
            'start_date': campaign.start_date,
            'end_date': campaign.end_date,
            'budget': campaign.budget,
            'visibility': campaign.visibility,
            'goals': campaign.goals,
            'target': campaign.target,
            'sponsor_id': campaign.sponsor_id,
            'image': campaign.image,
            'flag': campaign.flag,
            'completion_percentage': campaign.completion_percentage()
        }
        campaign_list.append(campaign_data)
    return jsonify(campaign_list)

@admin.route("/dashboard/ad_requests", methods=["GET"])
@jwt_required()
def get_all_ad_requests():
    ad_requests = AdRequest.query.all()
    ad_request_list = []
    for ad_request in ad_requests:
        ad_request_data = {
            'id': ad_request.id,
            'requirements': ad_request.requirements,
            'payment_amount': ad_request.payment_amount,
            'status': ad_request.status,
            'campaign_id': ad_request.campaign_id,
            'influencer_id': ad_request.influencer_id
        }
        ad_request_list.append(ad_request_data)
    return jsonify(ad_request_list)


# @admin.route("/dashboard/users/<int:user_id>", methods=["GET"])
# @jwt_required()
# def get_user_details(user_id):
#     user = User.query.get(user_id)
#     if not user:
#         return jsonify({'message': 'User not found'})

#     user_data = {
#         'id': user.id,
#         'username': user.username,
#         'email': user.email,
#         'name': user.name,
#         'role': user.role.name,
#         'is_approved': user.is_approved,
#         'date_created': user.date_created,
#         'last_login': user.last_login
#     }
#     return jsonify(user_data)


# @admin.route("/dashboard/campaigns/<int:campaign_id>", methods=["GET"])
# @jwt_required()
# def get_campaign_details(campaign_id):
#     campaign = Campaign.query.get(campaign_id)
#     if not campaign:
#         return jsonify({'message': 'Campaign not found'})

#     campaign_data = {
#         'id': campaign.id,
#         'name': campaign.name,
#         'description': campaign.description,
#         'start_date': campaign.start_date,
#         'end_date': campaign.end_date,
#         'budget': campaign.budget,
#         'visibility': campaign.visibility,
#         'goals': campaign.goals,
#         'target': campaign.target,
#         'sponsor_id': campaign.sponsor_id,
#         'completion_percentage': campaign.completion_percentage()
#     }
#     return jsonify(campaign_data)

# @admin.route("/dashboard/ad_requests/<int:ad_request_id>", methods=["GET"])
# @jwt_required()
# def get_ad_request_details(ad_request_id):
#     ad_request = AdRequest.query.get(ad_request_id)
#     if not ad_request:
#         return jsonify({'message': 'Ad request not found'})

#     ad_request_data = {
#         'id': ad_request.id,
#         'requirements': ad_request.requirements,
#         'payment_amount': ad_request.payment_amount,
#         'status': ad_request.status,
#         'campaign_id': ad_request.campaign_id,
#         'influencer_id': ad_request.influencer_id
#     }
#     return jsonify(ad_request_data)