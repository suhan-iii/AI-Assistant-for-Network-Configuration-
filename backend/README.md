# AutoNet Config - Django Backend

## Setup Instructions

### 1. Create Virtual Environment
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

Server will run at `http://127.0.0.1:8000`

## API Endpoints

### Generate Configuration
**POST** `/api/configs/generate/`
```json
{
  "command": "create VLAN for Sales, IP range 10.0.0.0/24",
  "use_nlp": false
}
```

### List Configurations
**GET** `/api/configs/`

### Export Config
**POST** `/api/configs/{id}/export/`

### Apply Config
**POST** `/api/configs/{id}/apply/`

## Project Structure

```
backend/
├── config/              Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── config_app/          Main application
│   ├── models.py        Database models
│   ├── views.py         API views/viewsets
│   ├── serializers.py   DRF serializers
│   ├── services.py      Business logic (Parser, Validator)
│   ├── tests.py         Unit tests
│   └── admin.py         Django admin
├── manage.py
├── requirements.txt
└── .env.example
```

## Features

✅ Django 4.2 with DRF
✅ CORS enabled for frontend integration
✅ Database models for config history
✅ Config parser (regex-based MVP, NLP-ready)
✅ Config validator
✅ Admin panel
✅ Unit tests
✅ Environment configuration

## Next Steps

- [ ] Implement NLP parsing with OpenAI
- [ ] Add Netmiko integration for mock environment
- [ ] Implement config export to .cfg files
- [ ] Add authentication & user permissions
- [ ] Add more comprehensive validators
- [ ] Set up CI/CD pipeline
