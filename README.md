
# digital_menu - Cookie Management System
(Literal cookies. Not website cookies.)

A full-stack digital menu system built with Django to manage my handmade cookie business in Niterói, Brazil.

## Roadmap

### Stage 1: Foundation & API (Current)
- [x] Data modeling (Category, MenuItem)
- [x] Project setup
- [ ] REST API with DRF
- [ ] Custom Django Admin
- [ ] Swagger/OpenAPI documentation

### Stage 2: Authentication & Security
- [ ] JWT authentication
- [ ] User profiles and addresses
- [ ] Granular permissions

### Stage 3: Cart & Orders
- [ ] Order models (Order, OrderItem)
- [ ] Atomic transactions
- [ ] Order state machine

### Stage 4: Payment Integration
- [ ] Stripe SDK integration
- [ ] Payment webhooks
- [ ] Error handling

### Stage 5: Automation (Celery + Redis)
- [ ] Asynchronous tasks
- [ ] Automated emails
- [ ] Loyalty system
- [ ] WhatsApp notifications

### Stage 6: Analytics Dashboard
- [ ] Sales reports
- [ ] Best-selling products tracking
- [ ] Recommendation algorithm

### Stage 7: DevOps & Production
- [ ] Automated tests
- [ ] Docker + docker-compose
- [ ] CI/CD pipeline
- [ ] Deployment (Railway/Render)

## Tech Stack

Django 5.1 • Python 3.13 • PostgreSQL • DRF • Git
Basic HTML, CSS and Javascript

## 🏃 Quick Start
```bash
# Clone the repository
git clone https://github.com/luccatrevisan/digital_menu.git
cd digital_menu

# Create and activate virtual environment
python -m venv venv

# Activate venv (choose your OS):
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows (CMD)
venv\Scripts\Activate.ps1     # Windows (PowerShell)

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env  # Linux/Mac
copy .env.example .env  # Windows
# Edit .env with your settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver
```

Access: `http://localhost:8000/admin`

## Key Decisions

**DecimalField for prices:** FloatField has precision errors in bigger scale (if there is even a cent wrong, it could mean incorrect information). DecimalField ensures that problem doesn't happen.  
**1:N Category→MenuItem:** Simplicity over flexibility. Can refactor to ManyToMany if needed.

## Documentation

Detailed DEVLOGs with decisions, challenges, and learnings: `/docs/devlogs/`

## ✉️ Contact

Lucca - [LinkedIn](https://www.linkedin.com/in/lucca-trevisan-86a181378/) | luccatrevisandev@gmail.com

---
**MIT License • Built with focus on learning and real-world problem solving**
