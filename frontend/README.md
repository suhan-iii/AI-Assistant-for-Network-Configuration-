# 🌐 AutoNet Config - Streamlit Frontend

## Setup Instructions

### 1. Navigate to Frontend Directory
```bash
cd frontend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
# Edit .env to set your Django backend URL if not localhost:8000
```

### 5. Run Streamlit App
```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

---

## Features

### 🔧 Tab 1: Generate Config
- Enter natural language network commands
- Choose configuration type (VLAN, Firewall, etc.)
- Optional NLP (OpenAI) support
- Real-time config generation
- Export configs as .cfg files
- Validation and simulation

### 📋 Tab 2: History
- View all previously generated configurations
- Search by command or type
- Re-use past configurations
- View detailed config information

### 📊 Tab 3: Analytics
- Total configurations created
- Validation success rate
- Configuration types distribution
- Status breakdown (draft, validated, applied)
- Visual charts and metrics

### ℹ️ Tab 4: About
- Project documentation
- Feature overview
- Architecture details
- Supported config types
- Resources and links

---

## API Integration

The frontend connects to Django backend API endpoints:

- `POST /api/configs/generate/` - Generate configuration
- `GET /api/configs/` - List all configurations
- `POST /api/configs/{id}/export/` - Export config
- `POST /api/configs/{id}/apply/` - Apply simulation

---

## Environment Variables

```bash
# .env file
API_BASE_URL=http://localhost:8000  # Django backend URL
STREAMLIT_SERVER_PORT=8501           # Streamlit port
```

---

## Project Structure

```
frontend/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
├── .gitignore             # Git ignores
├── .streamlit/
│   └── config.toml        # Streamlit configuration
└── README.md              # This file
```

---

## Requirements

- Python 3.8+
- Streamlit 1.28.0+
- Requests library
- Running Django backend (http://localhost:8000)

---

## Troubleshooting

### Frontend can't connect to backend
- Ensure Django server is running: `python manage.py runserver`
- Check API_BASE_URL in .env file
- Verify CORS is enabled in Django settings

### Slow response times
- Check Django backend performance
- Ensure NLP is not enabled if OpenAI API is slow

### Port already in use
- Change port in `~/.streamlit/config.toml`
- Or run: `streamlit run app.py --server.port 8502`

---

## Next Steps

- [ ] Add user authentication
- [ ] Implement real-time config preview
- [ ] Add config comparison tool
- [ ] Mobile responsive design
- [ ] Dark mode support
- [ ] Export to multiple formats (JSON, YAML, etc.)

---

**Built with Streamlit | Powered by Django**
