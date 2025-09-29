from flask import Blueprint, request, jsonify, current_app
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from marshmallow import Schema, fields, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime

# Blueprint for API
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)

# Marshmallow Schemas for serialization
class PromptSchema(Schema):
    id = fields.UUID(dump_only=True)
    project_name = fields.Str(required=True)
    project_description = fields.Str(required=True)
    project_objectives = fields.Str(required=True)
    category = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)

    # Text fields
    language = fields.Str()
    temperature = fields.Str()
    tone = fields.Str()
    persona = fields.Str()
    protocols = fields.Str()

    # Image fields
    positive_prompt = fields.Str()
    negative_prompt = fields.Str()
    style = fields.Str()
    material = fields.Str()
    surface_texture = fields.Str()
    lighting_type = fields.Str()
    lighting_intensity = fields.Str()
    lighting_direction = fields.Str()
    primary_color = fields.Str()
    post_processing = fields.Str()

    # Audio fields
    audio_duration = fields.Str()
    audio_genre = fields.Str()
    audio_mood = fields.Str()
    audio_instruments = fields.Str()

    # Code fields
    code_language = fields.Str()
    code_framework = fields.Str()
    code_complexity = fields.Str()
    code_purpose = fields.Str()

    # Video fields
    video_duration = fields.Str()
    video_style = fields.Str()
    video_resolution = fields.Str()
    video_frame_rate = fields.Str()
    video_aspect_ratio = fields.Str()

    # Document fields
    doc_type = fields.Str()
    doc_length = fields.Str()
    doc_format = fields.Str()
    doc_audience = fields.Str()

    # Presentation fields
    pres_slides = fields.Str()
    pres_audience = fields.Str()
    pres_style = fields.Str()
    pres_duration = fields.Str()

    # Infographic fields
    info_data_type = fields.Str()
    info_viz_type = fields.Str()
    info_theme = fields.Str()
    info_elements = fields.Str()

    # Animation fields
    anim_style = fields.Str()
    anim_duration = fields.Str()
    anim_characters = fields.Str()
    anim_technique = fields.Str()

    # Website fields
    web_type = fields.Str()
    web_technologies = fields.Str()
    web_features = fields.Str()
    web_responsive = fields.Str()

    # Data fields
    data_source = fields.Str()
    data_analysis_type = fields.Str()
    data_viz_tools = fields.Str()
    data_output_format = fields.Str()

    # Translation fields
    trans_source_lang = fields.Str()
    trans_target_lang = fields.Str()
    trans_domain = fields.Str()
    trans_tone = fields.Str()

    # Summary fields
    sum_source_type = fields.Str()
    sum_length = fields.Str()
    sum_key_points = fields.Str()
    sum_format = fields.Str()

    # Marketing fields
    market_campaign_type = fields.Str()
    market_target_audience = fields.Str()
    market_platform = fields.Str()
    market_objective = fields.Str()

    # Education fields
    edu_level = fields.Str()
    edu_subject = fields.Str()
    edu_format = fields.Str()
    edu_duration = fields.Str()

prompt_schema = PromptSchema()
prompts_schema = PromptSchema(many=True)

# User Schema
class UserSchema(Schema):
    id = fields.UUID(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    is_active = fields.Bool(dump_only=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Login/Register Schemas
class UserRegisterSchema(Schema):
    username = fields.Str(required=True, validate=lambda x: len(x) >= 3)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=lambda x: len(x) >= 6)

class UserLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

user_register_schema = UserRegisterSchema()
user_login_schema = UserLoginSchema()

# Required and optional fields
required_fields = ['project_name', 'project_description', 'project_objectives', 'category']
optional_fields = [
    'language', 'temperature', 'tone', 'persona', 'protocols',
    'positive_prompt', 'negative_prompt', 'style', 'material', 'surface_texture',
    'lighting_type', 'lighting_intensity', 'lighting_direction', 'primary_color', 'post_processing',
    'audio_duration', 'audio_genre', 'audio_mood', 'audio_instruments',
    'code_language', 'code_framework', 'code_complexity', 'code_purpose',
    'video_duration', 'video_style', 'video_resolution', 'video_frame_rate', 'video_aspect_ratio',
    'doc_type', 'doc_length', 'doc_format', 'doc_audience',
    'pres_slides', 'pres_audience', 'pres_style', 'pres_duration',
    'info_data_type', 'info_viz_type', 'info_theme', 'info_elements',
    'anim_style', 'anim_duration', 'anim_characters', 'anim_technique',
    'web_type', 'web_technologies', 'web_features', 'web_responsive',
    'data_source', 'data_analysis_type', 'data_viz_tools', 'data_output_format',
    'trans_source_lang', 'trans_target_lang', 'trans_domain', 'trans_tone',
    'sum_source_type', 'sum_length', 'sum_key_points', 'sum_format',
    'market_campaign_type', 'market_target_audience', 'market_platform', 'market_objective',
    'edu_level', 'edu_subject', 'edu_format', 'edu_duration'
]

class PromptListResource(Resource):
    def get(self):
        """Get all prompts"""
        try:
            db = current_app.db
            Prompt = current_app.Prompt
            prompts = Prompt.query.order_by(Prompt.created_at.desc()).all()
            return prompts_schema.dump(prompts), 200
        except Exception as e:
            return {'error': str(e)}, 500

    def post(self):
        """Create a new prompt"""
        try:
            db = current_app.db
            Prompt = current_app.Prompt

            # Try to get JSON data first, fallback to form data
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form.to_dict()

            prompt = Prompt()

            # Set required fields
            prompt.project_name = data.get('project_name')
            prompt.project_description = data.get('project_description')
            prompt.project_objectives = data.get('project_objectives')
            prompt.category = data.get('category')

            # Set optional fields dynamically
            for field in optional_fields:
                if data.get(field) is not None:
                    setattr(prompt, field, data[field])

            db.session.add(prompt)
            db.session.commit()

            return prompt_schema.dump(prompt), 201
        except ValidationError as e:
            return {'error': e.messages}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

class PromptResource(Resource):
    def get(self, prompt_id):
        """Get a specific prompt by ID"""
        try:
            from app import db, Prompt
            prompt = Prompt.query.get_or_404(uuid.UUID(prompt_id))
            return prompt_schema.dump(prompt), 200
        except Exception as e:
            return {'error': str(e)}, 404

    def put(self, prompt_id):
        """Update a specific prompt"""
        try:
            from app import db, Prompt
            prompt = Prompt.query.get_or_404(uuid.UUID(prompt_id))

            # Try to get JSON data first, fallback to form data
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form.to_dict()

            # Update fields
            for field in ['project_name', 'project_description', 'project_objectives', 'category'] + optional_fields:
                if data.get(field) is not None:
                    setattr(prompt, field, data[field])

            db.session.commit()
            return prompt_schema.dump(prompt), 200
        except ValidationError as e:
            return {'error': e.messages}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def delete(self, prompt_id):
        """Delete a specific prompt"""
        try:
            from app import db, Prompt
            prompt = Prompt.query.get_or_404(uuid.UUID(prompt_id))
            db.session.delete(prompt)
            db.session.commit()
            return {'message': 'Prompt deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

class PromptExportResource(Resource):
    def get(self, prompt_id):
        """Export a prompt in JSON format"""
        try:
            from app import db, Prompt
            prompt = Prompt.query.get_or_404(uuid.UUID(prompt_id))
            data = prompt_schema.dump(prompt)
            return data, 200
        except Exception as e:
            return {'error': str(e)}, 404

# Authentication Resources
class UserRegisterResource(Resource):
    def post(self):
        """Register a new user"""
        try:
            db = current_app.db
            User = current_app.User
            data = request.get_json()

            # Validate input
            errors = user_register_schema.validate(data)
            if errors:
                return {'error': 'Validation failed', 'details': errors}, 400

            # Check if user already exists
            if User.query.filter_by(username=data['username']).first():
                return {'error': 'Username already exists'}, 400
            if User.query.filter_by(email=data['email']).first():
                return {'error': 'Email already exists'}, 400

            # Create new user
            user = User(username=data['username'], email=data['email'])
            user.set_password(data['password'])

            db.session.add(user)
            db.session.commit()

            return {'message': 'User registered successfully', 'user': user_schema.dump(user)}, 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

class UserLoginResource(Resource):
    def post(self):
        """Login user and return JWT token"""
        try:
            User = current_app.User
            data = request.get_json()

            # Validate input
            errors = user_login_schema.validate(data)
            if errors:
                return {'error': 'Validation failed', 'details': errors}, 400

            # Find user
            user = User.query.filter_by(username=data['username']).first()
            if not user or not user.check_password(data['password']):
                return {'error': 'Invalid username or password'}, 401

            if not user.is_active:
                return {'error': 'Account is deactivated'}, 401

            # Create access token
            access_token = create_access_token(identity=str(user.id))
            return {
                'message': 'Login successful',
                'access_token': access_token,
                'user': user_schema.dump(user)
            }, 200
        except Exception as e:
            return {'error': str(e)}, 500

class UserProfileResource(Resource):
    @jwt_required()
    def get(self):
        """Get current user profile"""
        try:
            User = current_app.User
            user_id = get_jwt_identity()
            user = User.query.get_or_404(uuid.UUID(user_id))
            return user_schema.dump(user), 200
        except Exception as e:
            return {'error': str(e)}, 500

    @jwt_required()
    def put(self):
        """Update user profile"""
        try:
            db = current_app.db
            User = current_app.User
            user_id = get_jwt_identity()
            user = User.query.get_or_404(uuid.UUID(user_id))

            data = request.get_json()
            # Only allow updating certain fields
            if 'email' in data:
                # Check if email is already taken
                existing = User.query.filter_by(email=data['email']).first()
                if existing and existing.id != user.id:
                    return {'error': 'Email already exists'}, 400
                user.email = data['email']

            db.session.commit()
            return {'message': 'Profile updated successfully', 'user': user_schema.dump(user)}, 200
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

# Register resources
api.add_resource(PromptListResource, '/prompts')
api.add_resource(PromptResource, '/prompts/<string:prompt_id>')
api.add_resource(PromptExportResource, '/prompts/<string:prompt_id>/export')

# Authentication routes
api.add_resource(UserRegisterResource, '/auth/register')
api.add_resource(UserLoginResource, '/auth/login')
api.add_resource(UserProfileResource, '/auth/profile')