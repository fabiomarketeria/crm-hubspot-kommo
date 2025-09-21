# CRM HubSpot-Kommo Integration

A full-stack CRM application built with Flask (backend) and React (frontend) that provides integration capabilities with HubSpot and Kommo CRM systems.

## 🚀 Features

- **Modern Stack**: Flask + SQLAlchemy + React + Vite + Tailwind CSS
- **RESTful API**: Complete CRUD operations for contacts, companies, and deals
- **Authentication**: JWT-based authentication with secure user management
- **Responsive UI**: Modern, mobile-friendly interface built with Tailwind CSS
- **Database Support**: SQLite for development, PostgreSQL for production
- **Docker Ready**: Complete containerization for easy deployment
- **Cloud Deployment**: Configured for cloud environments

## 🛠 Tech Stack

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Development database
- **PostgreSQL**: Production database
- **JWT**: Authentication tokens
- **Flask-CORS**: Cross-origin resource sharing
- **Flask-Migrate**: Database migrations

### Frontend
- **React 18**: Modern React with hooks
- **Vite**: Fast build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **React Router**: Client-side routing
- **Axios**: HTTP client for API calls
- **React Hook Form**: Form management
- **Headless UI**: Accessible UI components
- **Heroicons**: Beautiful SVG icons

## 📁 Project Structure

```
crm-hubspot-kommo/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration settings
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Backend Docker config
├── frontend/
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   ├── hooks/         # Custom React hooks
│   │   └── utils/         # Utility functions
│   ├── package.json       # Frontend dependencies
│   ├── vite.config.js     # Vite configuration
│   ├── tailwind.config.js # Tailwind configuration
│   └── Dockerfile         # Frontend Docker config
├── docker-compose.yml     # Production Docker setup
├── docker-compose.dev.yml # Development Docker setup
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional)

### Option 1: Docker Development Setup (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd crm-hubspot-kommo
   ```

2. **Start with Docker Compose**
   ```bash
   docker-compose -f docker-compose.dev.yml up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

### Option 2: Local Development Setup

#### Backend Setup
1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

#### Frontend Setup
1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

## 🌐 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### Contacts
- `GET /api/contacts` - Get all contacts
- `POST /api/contacts` - Create new contact
- `GET /api/contacts/:id` - Get contact by ID
- `PUT /api/contacts/:id` - Update contact
- `DELETE /api/contacts/:id` - Delete contact

### Companies
- `GET /api/companies` - Get all companies
- `POST /api/companies` - Create new company
- `PUT /api/companies/:id` - Update company
- `DELETE /api/companies/:id` - Delete company

### Deals
- `GET /api/deals` - Get all deals
- `POST /api/deals` - Create new deal
- `PUT /api/deals/:id` - Update deal
- `DELETE /api/deals/:id` - Delete deal

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///crm_database.db
# For production: postgresql://username:password@host:port/database
```

#### Frontend (.env)
```env
VITE_API_URL=http://localhost:5000/api
```

## 🚢 Production Deployment

### Docker Production Setup
1. **Build and run with production compose**
   ```bash
   docker-compose up --build -d
   ```

2. **Access application**
   - Application: http://localhost

### Cloud Deployment Options
- **AWS**: ECS, EKS, or Elastic Beanstalk
- **Google Cloud**: Cloud Run, GKE
- **Azure**: Container Instances, AKS
- **DigitalOcean**: App Platform, Kubernetes
- **Heroku**: Container deployment

## 🔗 Integration Capabilities

This CRM system is designed to integrate with:

### HubSpot
- Contact synchronization
- Deal pipeline management
- Company data integration

### Kommo (AmoCRM)
- Lead management
- Contact synchronization
- Deal tracking

*Note: Integration modules can be added as needed.*

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest
```

### Frontend Testing
```bash
cd frontend
npm run test
```

## 📝 Default Credentials

For development, you can create a user through the registration form or use the API directly.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions, please open an issue in the GitHub repository.

## 🔮 Future Enhancements

- [ ] Real-time notifications
- [ ] Advanced analytics dashboard
- [ ] Email integration
- [ ] Calendar synchronization
- [ ] Mobile app
- [ ] Advanced reporting
- [ ] Webhook support
- [ ] API rate limiting
- [ ] Role-based access control
- [ ] Multi-tenant support