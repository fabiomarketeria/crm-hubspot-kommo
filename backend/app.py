"""
CRM HubSpot-Kommo Integration Backend
Flask application with SQLAlchemy and RESTful API
"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 
    'sqlite:///crm_database.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

# Models
class User(db.Model):
    """User model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }

class Contact(db.Model):
    """Contact model for CRM"""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    hubspot_id = db.Column(db.String(50), unique=True)
    kommo_id = db.Column(db.String(50), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'company_id': self.company_id,
            'hubspot_id': self.hubspot_id,
            'kommo_id': self.kommo_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Company(db.Model):
    """Company model for CRM"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    domain = db.Column(db.String(100))
    industry = db.Column(db.String(50))
    size = db.Column(db.String(20))
    hubspot_id = db.Column(db.String(50), unique=True)
    kommo_id = db.Column(db.String(50), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    contacts = db.relationship('Contact', backref='company', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'domain': self.domain,
            'industry': self.industry,
            'size': self.size,
            'hubspot_id': self.hubspot_id,
            'kommo_id': self.kommo_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Deal(db.Model):
    """Deal model for CRM"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, default=0.0)
    stage = db.Column(db.String(50), default='new')
    probability = db.Column(db.Integer, default=0)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    hubspot_id = db.Column(db.String(50), unique=True)
    kommo_id = db.Column(db.String(50), unique=True)
    close_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'amount': self.amount,
            'stage': self.stage,
            'probability': self.probability,
            'contact_id': self.contact_id,
            'company_id': self.company_id,
            'hubspot_id': self.hubspot_id,
            'kommo_id': self.kommo_id,
            'close_date': self.close_date.isoformat() if self.close_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

# API Routes

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400
    
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow().timestamp() + 24 * 3600  # 24 hours
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'token': token,
            'user': user.to_dict()
        })
    
    return jsonify({'message': 'Invalid credentials'}), 401

# Contact routes
@app.route('/api/contacts', methods=['GET'])
@token_required
def get_contacts(current_user):
    """Get all contacts"""
    contacts = Contact.query.all()
    return jsonify([contact.to_dict() for contact in contacts])

@app.route('/api/contacts', methods=['POST'])
@token_required
def create_contact(current_user):
    """Create a new contact"""
    data = request.get_json()
    contact = Contact(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data.get('phone'),
        company_id=data.get('company_id')
    )
    
    db.session.add(contact)
    db.session.commit()
    
    return jsonify(contact.to_dict()), 201

@app.route('/api/contacts/<int:contact_id>', methods=['GET'])
@token_required
def get_contact(current_user, contact_id):
    """Get a specific contact"""
    contact = Contact.query.get_or_404(contact_id)
    return jsonify(contact.to_dict())

@app.route('/api/contacts/<int:contact_id>', methods=['PUT'])
@token_required
def update_contact(current_user, contact_id):
    """Update a contact"""
    contact = Contact.query.get_or_404(contact_id)
    data = request.get_json()
    
    contact.first_name = data.get('first_name', contact.first_name)
    contact.last_name = data.get('last_name', contact.last_name)
    contact.email = data.get('email', contact.email)
    contact.phone = data.get('phone', contact.phone)
    contact.company_id = data.get('company_id', contact.company_id)
    contact.updated_at = datetime.utcnow()
    
    db.session.commit()
    return jsonify(contact.to_dict())

@app.route('/api/contacts/<int:contact_id>', methods=['DELETE'])
@token_required
def delete_contact(current_user, contact_id):
    """Delete a contact"""
    contact = Contact.query.get_or_404(contact_id)
    db.session.delete(contact)
    db.session.commit()
    return jsonify({'message': 'Contact deleted successfully'})

# Company routes
@app.route('/api/companies', methods=['GET'])
@token_required
def get_companies(current_user):
    """Get all companies"""
    companies = Company.query.all()
    return jsonify([company.to_dict() for company in companies])

@app.route('/api/companies', methods=['POST'])
@token_required
def create_company(current_user):
    """Create a new company"""
    data = request.get_json()
    company = Company(
        name=data['name'],
        domain=data.get('domain'),
        industry=data.get('industry'),
        size=data.get('size')
    )
    
    db.session.add(company)
    db.session.commit()
    
    return jsonify(company.to_dict()), 201

# Deal routes
@app.route('/api/deals', methods=['GET'])
@token_required
def get_deals(current_user):
    """Get all deals"""
    deals = Deal.query.all()
    return jsonify([deal.to_dict() for deal in deals])

@app.route('/api/deals', methods=['POST'])
@token_required
def create_deal(current_user):
    """Create a new deal"""
    data = request.get_json()
    deal = Deal(
        name=data['name'],
        amount=data.get('amount', 0.0),
        stage=data.get('stage', 'new'),
        probability=data.get('probability', 0),
        contact_id=data.get('contact_id'),
        company_id=data.get('company_id')
    )
    
    db.session.add(deal)
    db.session.commit()
    
    return jsonify(deal.to_dict()), 201

# Health check
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)