# 🚀 AutoNet Config

**AutoNet Config** is an AI-powered network configuration assistant that translates natural language requirements into validated device configuration scripts. It simplifies network automation by enabling users to describe desired network setups in plain English, which are then converted into `.cfg` files ready for deployment.

---

## ✨ Features

- 📝 **Natural Language Input** — Describe your networking needs in plain English  
  _Example: "create VLAN for Sales, IP range 10.0.0.0/24"_

- ⚡ **Instant Config Generation**
  - Regex- and rule-based parsing (MVP)
  - Beautiful dashboard to preview output
  - Export as `.cfg` files
  - Real-time validation

- 🚀 **Advanced Capabilities** (Coming Soon)
  - NLP parsing using OpenAI or HuggingFace
  - Comprehensive syntax validation
  - Configuration history & tracking
  - Mock network environment for "Apply Config" simulation
  - User authentication & multi-user support

---

## 🏗️ Architecture

**100% Python-Based Stack:**

```
┌─────────────────────────────────────────┐
│      Streamlit Frontend (Python)        │
│   - Dashboard & UI                      │
│   - Configuration preview               │
│   - History & Analytics                 │
└──────────────┬──────────────────────────┘
               │ API Requests
┌──────────────▼──────────────────────────┐
│    Django 4.2 REST Backend (Python)     │
│   - Config Parser & Generator           │
│   - Syntax Validator                    │
│   - Config History (Database)           │
│   - Mock Environment Simulator          │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│        SQLite / PostgreSQL              │
│   - Configuration Storage               │
│   - History & Metadata                  │
└─────────────────────────────────────────┘
```

---

## 📚 Tech Stack

- **Backend:** Django 4.2 + Django REST Framework
- **Frontend:** Streamlit (Pure Python)
- **Database:** SQLite (dev) / PostgreSQL (production)
- **Parser:** Regex-based (MVP) + NLP-ready (OpenAI/HuggingFace)
- **Validator:** Built-in syntax validation
- **Network Automation:** Netmiko (optional, for mock environment)

---

## ⚡ Setup & Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/suhan-iii/AI-Assistant-for-Network-Configuration-.git
cd AI-Assistant-for-Network-Configuration-
```

### 2️⃣ Setup Backend (Django)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate           # Linux/Mac
# venv\Scripts\activate            # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings (optional)

# Run database migrations
python manage.py migrate

# Create superuser (optional, for admin panel)
python manage.py createsuperuser

# Start backend server
python manage.py runserver
```

**Backend API will run at:** `http://localhost:8000`

### 3️⃣ Setup Frontend (Streamlit)

```bash
cd ../frontend

# Create virtual environment
python -m venv venv
source venv/bin/activate           # Linux/Mac
# venv\Scripts\activate            # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env if your backend is on a different URL

# Start Streamlit dashboard
streamlit run app.py
```

**Dashboard will open at:** `http://localhost:8501`

---

## 🖥️ Usage Flow

### Step 1: Open Dashboard
Navigate to `http://localhost:8501` in your browser

### Step 2: Enter a Network Command
In the **"Generate Config"** tab, enter a natural language command:
```
Create VLAN for Sales, IP range 10.0.0.0/24
```

### Step 3: Generate Configuration
Click the **"Generate Config"** button

### Step 4: Preview Output
See the generated configuration:
```
vlan 10
 name Sales
interface vlan 10
 ip address 10.0.0.1 255.255.255.0
 no shutdown
```

### Step 5: Take Action
Choose one of these actions:
- **Export** → Download as `.cfg` file
- **Validate** → Check syntax validity
- **Apply** → Simulate in mock environment
- **View History** → Check past configurations

---

## 📊 Dashboard Tabs

| Tab | Purpose |
|-----|---------|
| 🔧 **Generate Config** | Input natural language, generate configs, export, validate, simulate |
| 📋 **History** | Browse all previously generated configurations |
| 📊 **Analytics** | View statistics, charts, and distribution of configurations |
| ℹ️ **About** | Project documentation, features, and resources |

---

## 🔌 API Endpoints

### Generate Configuration
**POST** `/api/configs/generate/`
```json
{
  "command": "create VLAN for Sales, IP range 10.0.0.0/24",
  "use_nlp": false
}
```

**Response:**
```json
{
  "id": 1,
  "config": "vlan 10\n name Sales\n...",
  "config_type": "vlan",
  "status": "validated",
  "is_valid": true,
  "validation_errors": {}
}
```

### List All Configurations
**GET** `/api/configs/`

### Export Configuration
**POST** `/api/configs/{id}/export/`

### Apply Configuration
**POST** `/api/configs/{id}/apply/`

---

## 📂 Project Structure

```
AI-Assistant-for-Network-Configuration-/
├── backend/                         # Django Backend
│   ├── config/                      # Django project settings
│   │   ├── settings.py             # Configuration
│   │   ├── urls.py                 # API routing
│   │   └── wsgi.py                 # WSGI app
│   ├── config_app/                 # Main application
│   │   ├── models.py               # Database models
│   │   ├── views.py                # API viewsets
│   │   ├── serializers.py          # DRF serializers
│   │   ├── services.py             # Business logic
│   │   ├── admin.py                # Admin panel
│   │   └── tests.py                # Unit tests
│   ├── manage.py                   # Django CLI
│   ├── requirements.txt            # Dependencies
│   ├── .env.example                # Environment template
│   └── README.md                   # Backend docs
│
├── frontend/                        # Streamlit Frontend
│   ├── app.py                      # Main dashboard
│   ├── requirements.txt            # Dependencies
│   ├── .streamlit/
│   │   └── config.toml             # Streamlit config
│   ├── .env.example                # Environment template
│   └── README.md                   # Frontend docs
│
├── README.md                        # This file
├── gitignore                        # Git ignore rules
└── .gitignore
```

---

## 🤖 Supported Config Types

| Type | Description | Example |
|------|---|---|
| **VLAN** | Virtual LAN configuration | Sales VLAN with IP range |
| **Firewall** | Firewall rules and ACLs | Block specific ports |
| **Routing** | Route configuration | Set static routes |
| **Access-List** | Access control lists | Layer 3 filtering |

---

## 📚 Resources

- 🐍 [Python Documentation](https://www.python.org/doc/)
- 🎸 [Django Documentation](https://docs.djangoproject.com/)
- 📊 [Streamlit Documentation](https://docs.streamlit.io/)
- 🤖 [OpenAI API](https://platform.openai.com/docs/)
- 🔌 [Django REST Framework](https://www.django-rest-framework.org/)
- 🌐 [Netmiko Documentation](https://github.com/ktbyers/netmiko)
