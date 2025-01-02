import os
from flask import Blueprint,request,jsonify,current_app
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from .model import User, Campaign, AdRequest, Role,Message
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required,get_jwt_identity,get_jwt
from . import db
import csv
from flask import send_file
from io import StringIO,BytesIO

sponsor = Blueprint('sponsor', __name__)

# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@sponsor.route("/dashboard/sponsor_details", methods=["GET"])
@jwt_required()
def get_sponsor_details():
    # Decode JWT manually
    jwt_data = get_jwt()
    user_id = jwt_data["sub"]
    
    # Query the user from the database
    user = User.query.get(user_id)
    
    if not user or not user.is_sponsor():
        return jsonify({'message': 'Unauthorized access'})

    sponsor_data = {
        'id': user.id,
        'username': user.username,
        'image': user.image,
        'email': user.email,
        'name': user.name,
        'company': user.company,
        'about': user.about,
        'role': user.role.name,
        'date_created': user.date_created,
        'last_login': user.last_login
    }
    
    return jsonify(sponsor_data)


@sponsor.route("/campaigns", methods=["GET"])
@jwt_required()
def get_all_campaigns():
    user_id = get_jwt_identity()  
    current_user = User.query.get(user_id)

    if not current_user.is_sponsor():
        return jsonify({'message': 'Unauthorized access'})

    
    # campaigns = Campaign.query.filter_by(flag=False).all()
    campaigns = Campaign.query.filter_by(sponsor_id=user_id, flag=False).all()

    
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

@sponsor.route("/flagcampaigns", methods=["GET"])
@jwt_required()
def get_all_flagcampaigns():
    user_id = get_jwt_identity()  
    current_user = User.query.get(user_id)

    if not current_user.is_sponsor():
        return jsonify({'message': 'Unauthorized access'})

    
    # campaigns = Campaign.query.filter_by(flag=False).all()
    campaigns = Campaign.query.filter_by(sponsor_id=user_id, flag=True).all()

    
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


# Sponsor creates a new campaign
@sponsor.route("/create_campaign", methods=["POST"])
@jwt_required()
def create_campaign():
    user_id = get_jwt_identity()  
    current_user = User.query.get(user_id)
    if not current_user.is_sponsor():
        return jsonify({'message': 'Unauthorized access'})

    
    if 'image' not in request.files:
        return jsonify({'message': 'No file part'})
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'message': 'No selected file'})
    
    filename = 'default.jpg'
    if file :
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        filename = f"{secure_filename(file.filename).split('.')[0]}_{timestamp}.jpg"
        upload_folder = current_app.config['UPLOAD_FOLDER']
        # campaign_upload_folder = os.path.join(upload_folder, 'Campaign')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

    data = request.form
    new_campaign = Campaign(
        name=data['name'],
        description=data['description'],
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
        end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date(),
        budget=data['budget'],
        visibility=data['visibility'],
        goals=data.get('goals'),
        target=data['target'],
        image=filename,  
        sponsor_id=current_user.id
    )
    try:
        db.session.add(new_campaign)
        db.session.commit()
        return jsonify({'message': 'Campaign created successfully'})
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Campaign creation failed'})
    


# Sponsor updates an existing campaign
@sponsor.route("/campaign/<int:campaign_id>", methods=["PUT"])
@jwt_required()
def update_campaign( campaign_id):
    user_id = get_jwt_identity()  
    current_user = User.query.get(user_id)
    if not current_user.is_sponsor():
        return jsonify({'message': 'Unauthorized access'})

    campaign = Campaign.query.get(campaign_id)
    if not campaign or campaign.sponsor_id != current_user.id:
        return jsonify({'message': 'Campaign not found'})

    data = request.form 
    

    campaign.name = data.get('name', campaign.name)
    campaign.description = data.get('description', campaign.description)
    campaign.start_date = datetime.strptime(data.get('start_date', campaign.start_date.strftime('%Y-%m-%d')), '%Y-%m-%d').date()
    campaign.end_date = datetime.strptime(data.get('end_date', campaign.end_date.strftime('%Y-%m-%d')), '%Y-%m-%d').date()
    campaign.budget = data.get('budget', campaign.budget)
    campaign.visibility = data.get('visibility', campaign.visibility)
    campaign.goals = data.get('goals', campaign.goals)
    campaign.target = data.get('target', campaign.target)

    
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '':
            # Delete the old image file if it exists
            if campaign.image and campaign.image != 'default.jpg':
                old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], campaign.image)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            
            # Save the new image file
            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
            filename = f"{secure_filename(file.filename).split('.')[0]}_{timestamp}.jpg"
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            campaign.image = filename  
    else:
        campaign.image = campaign.image  

    try:
        db.session.commit()
        return jsonify({'message': 'Campaign updated successfully'})
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Failed to update campaign'})

# Sponsor deletes an existing campaign
@sponsor.route("/campaign/<int:campaign_id>", methods=["DELETE"])
@jwt_required()
def delete_campaign( campaign_id):
    user_id = get_jwt_identity()  
    current_user = User.query.get(user_id)
    if not current_user.is_sponsor():
        return jsonify({'message': 'Unauthorized access'})

    campaign = Campaign.query.get(campaign_id)
    if not campaign or campaign.sponsor_id != current_user.id:
        return jsonify({'message': 'Campaign not found'})

    # Delete the campaign image if it is not the default image
    if campaign.image != 'default.jpg':
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], campaign.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(campaign)
    db.session.commit()
    return jsonify({'message': 'Campaign deleted successfully'})


@sponsor.route("/influencers", methods=["GET"])
@jwt_required()
def get_all_influencers():
    # influencers = User.query.filter_by(role_id=Role.query.filter_by(name='Influencer').first().id).all()
    influencers = User.query.filter_by(role_id=Role.query.filter_by(name='Influencer').first().id, is_flagged=False)
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
            

        }
        influencer_list.append(influencer_data)
    return jsonify(influencer_list)


#  creates an ad request
@sponsor.route("/ad_request", methods=["POST"])
@jwt_required()
def create_ad_request():
    user_id = get_jwt_identity()  
    current_user = User.query.get(user_id)
    

    data = request.json
    # print(data)
    campaign = Campaign.query.get(data['campaign_id'])
    influencer = User.query.get(data['influencer_id'])

    if not campaign:
        return jsonify({'message': 'Campaign not found'})
    if not influencer or not influencer.is_influencer():
        return jsonify({'message': 'Influencer not found or invalid'})
    existing_ad_request = AdRequest.query.filter_by(
        campaign_id=campaign.id,
        influencer_id=influencer.id
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
        influencer_id=influencer.id,
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
    

@sponsor.route("/ad_requests/sent", methods=["GET"])
@jwt_required()
def get_sent_ad_requests():
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)

    # sent_requests = AdRequest.query.filter(
    #     AdRequest.sender_id == user_id  
    # ).all()
    sent_requests = AdRequest.query.join(Campaign, AdRequest.campaign_id == Campaign.id).filter(
        AdRequest.sender_id == user_id,
        Campaign.flag == False  
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
        for ad_request in sent_requests
    ]

    return jsonify(result)

@sponsor.route("/ad_requests/received", methods=["GET"])
@jwt_required()
def get_received_ad_requests():
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)

    if not current_user.is_sponsor():
        return jsonify({'message': 'Unauthorized access'})

    campaigns = Campaign.query.filter_by(sponsor_id=user_id , flag=False).all()

    if not campaigns:
        return jsonify({'message': 'No campaigns found for this sponsor'})

    campaign_ids = [campaign.id for campaign in campaigns]

    received_requests = AdRequest.query.filter(
        AdRequest.campaign_id.in_(campaign_ids),
        AdRequest.sender_id == AdRequest.influencer_id
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



# Sponsor updates an existing ad request
@sponsor.route("/ad_request/<int:ad_request_id>", methods=["PUT"])
@jwt_required()
def update_ad_request( ad_request_id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    if not current_user.is_sponsor():
        return jsonify({'message': 'Unauthorized access'})

    ad_request = AdRequest.query.get(ad_request_id)
    campaign = Campaign.query.get(ad_request.campaign_id)
    if not ad_request or campaign.sponsor_id != current_user.id:
        return jsonify({'message': 'Ad request not found'})

    data = request.json
    ad_request.requirements = data.get('requirements', ad_request.requirements)
    ad_request.payment_amount = data.get('payment_amount', ad_request.payment_amount)
    db.session.commit()
    return jsonify({'message': 'Ad request updated successfully'})

# Sponsor deletes an existing ad request
@sponsor.route("/ad_request/<int:ad_request_id>", methods=["DELETE"])
@jwt_required()
def delete_ad_request( ad_request_id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    ad_request = AdRequest.query.get(ad_request_id)
    if ad_request.sender_id != current_user.id:
        return jsonify({'message': 'Unauthorized: Only the sender can delete this ad request'})
    campaign = Campaign.query.get(ad_request.campaign_id)
    if not ad_request or campaign.sponsor_id != current_user.id:
        return jsonify({'message': 'Ad request not found'})

    db.session.delete(ad_request)
    db.session.commit()
    return jsonify({'message': 'Ad request deleted successfully'})



@sponsor.route("/ad_request_accept/<int:ad_request_id>", methods=["PUT"])
@jwt_required()
def accept_ad_request(ad_request_id):
    ad_request = AdRequest.query.get(ad_request_id)
    
    if not ad_request:
        return jsonify({'message': 'Ad request not found'})

    campaign = Campaign.query.get(ad_request.campaign_id)
    if not campaign:
        return jsonify({'message': 'Campaign not found'})

    if ad_request.status == "Accepted":
        return jsonify({'message': 'This ad request is already accepted.'})
    elif ad_request.status == "Rejected":
        return jsonify({'message': 'This ad request has already been rejected.'})
    elif ad_request.status in ["Pending", "Negotiating"]:
        ad_request.status = "Accepted"
        db.session.commit()
        return jsonify({'message': 'Ad request accepted successfully'})
    else:
        return jsonify({'message': 'Invalid ad request status.'})

@sponsor.route("/ad_request_reject/<int:ad_request_id>", methods=["PUT"])
@jwt_required()
def reject_ad_request(ad_request_id):
    ad_request = AdRequest.query.get(ad_request_id)
    
    if not ad_request:
        return jsonify({'message': 'Ad request not found'})

    campaign = Campaign.query.get(ad_request.campaign_id)
    if not campaign:
        return jsonify({'message': 'Campaign not found, cannot reject this request'})

    if ad_request.status == "Rejected":
        return jsonify({'message': 'This ad request has already been rejected.'})
    elif ad_request.status == "Accepted":
        return jsonify({'message': 'This ad request has already been accepted, cannot reject.'})
    elif ad_request.status in ["Pending", "Negotiating"]:
        ad_request.status = "Rejected"
        db.session.commit()
        return jsonify({'message': 'Ad request rejected successfully'})
    else:
        return jsonify({'message': 'Invalid ad request status.'})


@sponsor.route("/ad_request/chat/<int:ad_request_id>/send", methods=["POST"])
@jwt_required()
def send_message(ad_request_id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)

    ad_request = AdRequest.query.get(ad_request_id)
    if not ad_request:
        return jsonify({"message": "Ad request not found"})

    campaign = Campaign.query.get(ad_request.campaign_id)
    if current_user.id not in [campaign.sponsor_id, ad_request.influencer_id]:
        return jsonify({"message": "Unauthorized"})
    
    # if ad_request.status in ["Accepted", "Rejected"]:
    #     return jsonify({"message": f"Messaging is not allowed when AdRequest status is '{ad_request.status}'"})
    if ad_request.status == "Pending":
        ad_request.status = "Negotiating"
        db.session.commit()

    data = request.json
    content = data.get("content", "").strip()
    if not content:
        return jsonify({"message": "Message content is required"})

    # Determine the receiver
    receiver_id = (
        campaign.sponsor_id if current_user.id == ad_request.influencer_id else ad_request.influencer_id
    )

    message = Message(
        content=content,
        sender_id=current_user.id,
        receiver_id=receiver_id,
        ad_request_id=ad_request_id
    )
    db.session.add(message)
    db.session.commit()

    return jsonify({"message": "Message sent successfully"})

@sponsor.route("/ad_request/chat/<int:ad_request_id>/messages", methods=["GET"])
@jwt_required()
def fetch_messages(ad_request_id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)

    ad_request = AdRequest.query.get(ad_request_id)
    if not ad_request:
        return jsonify({"message": "Ad request not found"})

    campaign = Campaign.query.get(ad_request.campaign_id)
    if current_user.id not in [campaign.sponsor_id, ad_request.influencer_id]:
        return jsonify({"message": "Unauthorized"})

    messages = Message.query.filter_by(ad_request_id=ad_request_id).order_by(Message.timestamp).all()

   
    messages_data = [
        {
            "id": message.id,
            "content": message.content,
            "sender_id": message.sender_id,
            "sender_name": message.sender.name if message.sender else "Unknown",
            "receiver_id": message.receiver_id,
            "receiver_name": message.receiver.name if message.receiver else "Unknown", 
            "timestamp": message.timestamp.isoformat(),
        }
        for message in messages
    ]

    return jsonify({"messages": messages_data})




@sponsor.route("/export_campaigns", methods=["POST"])
@jwt_required()
def export_campaigns():
    user_id = get_jwt_identity()
    sponsor = User.query.get(user_id)
    
    if not sponsor or not sponsor.is_sponsor():
        return jsonify({'message': 'Unauthorized access'})

    campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id).all()
    
    # Prepare CSV data
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Campaign ID', 'Name', 'Start Date', 'End Date', 'Budget', 'Visibility', 'Goals'])
    
    for campaign in campaigns:
        writer.writerow([
            campaign.id,
            campaign.name,
            campaign.start_date.strftime('%Y-%m-%d'),
            campaign.end_date.strftime('%Y-%m-%d'),
            campaign.budget,
            campaign.visibility,
            campaign.goals,
        ])
    
    output.seek(0)
    binary_output = BytesIO(output.getvalue().encode())
    
    return send_file(binary_output, mimetype='text/csv', as_attachment=True, download_name='campaigns.csv')
    
    # return send_file(output, mimetype='text/csv', as_attachment=True, download_name='campaigns.csv')





