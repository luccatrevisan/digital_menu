
# digital_menu - Cookie Management System
(Literal cookies. Not website cookies.)

A digital menu system built with Django to manage my handmade cookie business in Brazil.

## Roadmap
This project follows a structured approach, divided into logical tiers, from data modeling to DevOps. Below is the high-level roadmap of the project and you can keep up with my progress [here on tldraw](https://www.tldraw.com/f/Y5b2nbWQnTV7kjM88x4iu?d=v-397.-238.2636.1299.page)

![ROADMAP](docs/img/roadmap.png)

I am also using Kanban methodology to manage my tasks on Notion, where you can see my live workflow.
[👉 View Project Board on Notion](https://www.notion.so/digital_menu-2f77457680e780f5a107d98ab68e2dd1?source=copy_link)

## Tech Stack

Django 5.1 • Python 3.13 • PostgreSQL • DRF • Git • Basic HTML, CSS and Javascript

## Quick Start
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

## Key Decisions

**DecimalField for prices:** FloatField has precision errors in bigger scale (if there is even a cent wrong, it could mean incorrect information). DecimalField ensures that problem doesn't happen.  
**1:N Category→MenuItem:** Simplicity over flexibility. Can refactor to ManyToMany if needed.

## Documentation

Detailed DEVLOGs with decisions, challenges, and learnings (in Brazilian Portuguese): `/docs/devlogs/`

## ✉️ Contact

Lucca - [LinkedIn](https://www.linkedin.com/in/lucca-trevisan-86a181378/) | luccatrevisandev@gmail.com

---
**MIT License • Built with focus on learning and real-world problem solving**
