import os
from flask import Blueprint,request,jsonify,current_app
from . import db
from .model import User, Role
from werkzeug.security import check_password_hash,generate_password_hash
from werkzeug.utils import secure_filename
from flask_jwt_extended import create_access_token, create_refresh_token,decode_token,jwt_required,unset_jwt_cookies
from datetime import datetime, timedelta
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func

auth = Blueprint("auth",__name__)


# Function to generate JWT token
def generate_token(user_id, user_role,user_username):
    token =create_access_token(
                identity=user_id,
                additional_claims={'role': user_role, 'username': user_username},
               
            )
   
    return token

# Function to generate JWT refresh token
def generate_refresh_token(user_id,user_role,user_name):
    
    refresh_token = create_refresh_token(
                        identity=user_id,
                        additional_claims={'role': user_role, 'username': user_name},
                        expires_delta=timedelta(days=30) 
                        
                    )
    return refresh_token

# Refresh token endpoint
@auth.route('/refresh-token', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
   
        refresh_token = request.json.get('refresh_token')
        # print(refresh_token)

        # Verify the refresh token
        payload = decode_token(refresh_token)
        # print(payload)
        user_id = payload['sub']
        user_role = payload['role']
        user_name = payload['username']

        # Generate a new access token
        access_token = generate_token(user_id,user_role,user_name)

        return jsonify({'access_token': access_token})
    
    

# Login api  route
@auth.route("/admin_login", methods=["POST"])
def admin_login():
    if request.method == "POST":
        data = request.json
        login_identifier = data.get("username")
        password = data.get("password")

        # Check if login_identifier is email or username
        user = User.query.filter((User.email == login_identifier) | (User.username == login_identifier)).first()

        if user and check_password_hash(user.password, password) and user.role.name == 'Admin':
            user.last_login = datetime.now()
            db.session.commit()
            # Generate tokens
            access_token = generate_token(user.id, user.role.name, user.username)
            refresh_token = generate_refresh_token(user.id, user.role_id, user.username)
            username = user.username

            return jsonify({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'username': username
            })
        else:
            return jsonify({'message': 'Invalid credentials'})
    else:
        return jsonify({'message': 'This endpoint supports only POST requests for login.'})
    

@auth.route("/other_login", methods=["POST"])
def other_login():
    if request.method == "POST":
        data = request.json
        login_identifier = data.get("username")
        password = data.get("password")

        # Check if login_identifier is email or username
        user = User.query.filter((User.email == login_identifier) | (User.username == login_identifier)).first()
        if user:
            if user.is_flagged:
                return jsonify({'message': 'User is flagged and cannot log in.'})
            elif not user.is_approved:
                return jsonify({'message': 'User is not approved.'})

        if user and check_password_hash(user.password, password) and (user.role.name in ['Sponsor', 'Influencer']) and user.is_approved and not user.is_flagged:
            user.last_login = datetime.now()
            db.session.commit()
            # Generate tokens
            access_token = generate_token(user.id, user.role.name, user.username)
            refresh_token = generate_refresh_token(user.id, user.role_id, user.username)
            username = user.username

            return jsonify({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'username': username,
                'message' : 'Successfully Loged in.'
            })
        
        else:
            return jsonify({'message': 'Invalid credentials '})
    else:
        return jsonify({'message': 'no POST request.'})
    
    

@auth.route("/sponsor_signup", methods=["POST"])
def sign_up2():
    if request.method == "POST":
        
        image_data = request.files.get("image")
        email = request.form.get("email")
        name = request.form.get("name")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        role_name = request.form.get("role_name")
        company = request.form.get("company")
        about = request.form.get("about")

        # Validate form data
        if not email or not username or not password1 or not password2 or not name:
            return jsonify({"message": "All fields are required"})

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            return jsonify({"message": "Email is already in use"})
        if username_exists:
            return jsonify({"message": "Username is already in use"})
        if password1 != password2:
            return jsonify({"message": "Passwords don't match"})
        if len(password1) < 6:
            return jsonify({"message": "Password must be at least 6 characters long"})
        if len(username) < 3:
            return jsonify({"message": "Username is too short"})
        if not name:
            return jsonify({"message": "Name is required"})

        # Handle image upload
        filename = 'default.jpg'
        if image_data:
            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
            filename = f"{secure_filename(image_data.filename).split('.')[0]}_{timestamp}.jpg"
            upload_folder = current_app.config['UPLOAD_FOLDER']
            
            filepath = os.path.join(upload_folder, filename)
            image_data.save(filepath)

        # Find the role ID based on the role name
        role = Role.query.filter(func.lower(Role.name) == func.lower(role_name)).first()
        if not role:
            return jsonify({"message": "Role not found"})

        # Ensure the role is "Sponsor"
        if role.name.lower() != 'sponsor':
            return jsonify({"message": "Invalid role for this signup"})

        # Create a new user instance
        new_user = User(
            image=filename,  # Save only the filename
            name=name,
            email=email,
            username=username,
            role_id=role.id,
            company = company,
            about = about,
            is_approved=False  # Set to False as sponsors need admin approval
        )
        new_user.password = generate_password_hash(password1)  # Hash the password

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User created successfully, pending admin approval"})
    

@auth.route("/influencer_signup", methods=["POST"])  
def sign_up1():
    if request.method == "POST":
        image_data = request.files.get("image")
        email = request.form.get("email")
        name = request.form.get("name")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        role_name = request.form.get("role_name") 
        socialmedia = request.form.get("socialmedia")
        reach = request.form.get("reach")
        niche = request.form.get("niche")
        about =request.form.get("about")
         

        # Validate form data
        if not email or not username or not password1 or not password2 or not name:
            return jsonify({"message": "All fields are required"})

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            return jsonify({"message": "Email is already in use"})
        if username_exists:
            return jsonify({"message": "Username is already in use"})
        if password1 != password2:
            return jsonify({"message": "Passwords don't match"})
        if len(password1) < 6:
            return jsonify({"message": "Password must be at least 6 characters long"})
        if len(username) < 3:
            return jsonify({"message": "Username is too short"})
        if not name:
            return jsonify({"message":"Name is required"})

        # Handle image upload
        filename = 'default.jpg'
        if image_data:
            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
            filename = f"{secure_filename(image_data.filename).split('.')[0]}_{timestamp}.jpg"
            upload_folder = current_app.config['UPLOAD_FOLDER']
            
            filepath = os.path.join(upload_folder, filename)
            image_data.save(filepath)

        # Find the role ID based on the role name
        role = Role.query.filter(func.lower(Role.name) == func.lower(role_name)).first()
        if not role:
            return jsonify({"message": "Role not found"})

        # Create a new user instance
        new_user = User(
            image=filename,  # Save only the filename
            name=name,
            email=email,
            username=username,
            role_id=role.id,
            socialmedia=socialmedia,
            reach=reach,
            niche=niche,
            about = about,
            is_approved=True
        )
        new_user.password = generate_password_hash(password1)  # Hash the password

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User created successfully"})

@auth.route("/logout")
@jwt_required()
def logout():
    try:
        # Perform logout actions
        return jsonify({"message": "Logout successful"})
    except Exception as e:
        # Handle any exceptions that might occur during logout
        return jsonify({"error": str(e)})