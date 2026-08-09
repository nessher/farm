# 🌾 Commercial Site for KFH (Family Farm)

[![GitHub Pages](https://img.shields.io/badge/GitHub-Pages-blue)](https://nessher.github.io/farm/)
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0-green?logo=django)](https://www.djangoproject.com/)
[![HTML5](https://img.shields.io/badge/HTML5-70.5%25-orange?logo=html5)](https://developer.mozilla.org/en-US/docs/Web/HTML)

## 📖 Overview

This is a full-featured **online store** for a family farm (KFH). The project demonstrates a complete e-commerce workflow, from product browsing to order management, with a focus on practicality and security.

[![Live Demo](https://img.shields.io/badge/Live_Demo-VPS-green)](http://185.66.68.198:8000)

## ✨ Key Features

- **Product Catalog**: Browse products with detailed descriptions and images.
- **Shopping Cart**: Add/remove items and manage quantities.
- **User Authentication**: Separate roles for clients and staff.
- **Personal Cabinet**: 
  - **Clients**: View and track their order history and status.
  - **Staff/Managers**: Access a dedicated dashboard to manage and track all customer orders.
- **Order Management**: Full cycle from placing an order to status updates.
- **Secure Deployment**: Hosted on a **VPS** with Docker, PostgreSQL, and Nginx.
- **Telegram Notifications**: Instant notifications for new orders and inquiries.

## 🛠️ Tech Stack

- **Backend**: Python, Django (MVT architecture)
- **Frontend**: HTML5, CSS3, JavaScript (vanilla)
- **Database**: PostgreSQL (production), SQLite (development)
- **Server/Deployment**: Docker, Docker Compose, Nginx, Gunicorn
- **Hosting**: VPS (Support.by)
- **Other**: WhiteNoise for static files, Cloudinary (optional for media)

## 🗂️ Project Structure
  ```
  farm/
  ├── config/               # Project settings and URLs
  ├── main/                 # Main application with core models, views and logic
  │ ├── models.py
  │ ├── views.py
  │ ├── cart.py             # Shopping cart logic
  │ ├── telegram.py         # Telegram notification functions
  │ └── ...
  ├── media/                # User-uploaded product images (mounted as a Docker volume)
  ├── static/               # Static files (CSS, JS, images)
  ├── templates/            # HTML templates
  ├── Dockerfile            # Docker configuration for containerization
  ├── docker-compose.yml    # Docker Compose for multi-container setup
  ├── manage.py             # Django management script
  ├── .env                  # Environment variables (not in repository)
  └── requirements.txt      # Python dependencies
  ```

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Docker and Docker Compose
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/nessher/farm.git
   cd farm
   
2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt

4. **Configure environment variables:**
   Create a .env file in the root directory with the following variables:
   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True  # Set to False in production
   TELEGRAM_BOT_TOKEN=your-telegram-bot-token
   TELEGRAM_ADMIN_CHAT_ID=your-telegram-chat-id
   ALLOWED_HOSTS=localhost,127.0.0.1

5. **Run database migrations**
   ```bash
   python manage.py migrate

6. **Create a superuser (for admin access)**
   ```bash
   python manage.py createsuperuser

7. **Start the development server**
   ```bash
   python manage.py runserver
  The site will be available at http://127.0.0.1:8000


  
### Running with Docker (Production-like)

1. **Build and run the containers**
   ```bash
   docker compose up --build -d
2. **Access the application at http://localhost:8000.**
3. **Stop the containers**
   ```bash
   docker compose down


### 🌐 Deployment
**The project is deployed on a VPS server (Support.by) using Docker and PostgreSQL. The deployment process includes:**
  - Containerized application with Docker Compose.
  - PostgreSQL database running in a separate container.
  - Persistent storage for media files and postgres_data.
  - Automatic restart of containers (restart: always).
  - Security measures: secrets stored in .env, DEBUG=False in production.

### 📂 Important Files
  - docker-compose.yml: Defines the services (db and web), volumes, and ports.
  - Dockerfile: Builds the Django application image.
  - .env: Contains sensitive data (not tracked in Git).
  - .gitignore: Excludes __pycache__/, media/, .env, db.sqlite3, etc.

### 📋 Environment Variables
| Variable               | Description                                   |
| ---------------------- | --------------------------------------------- |
| SECRET_KEY             | Django secret key (keep private!)             |
| DEBUG                  | Set to False in production                    |
| ALLOWED_HOSTS          | Comma-separated list of allowed hosts         |
| TELEGRAM_BOT_TOKEN     | Token for the Telegram bot                    |
| TELEGRAM_ADMIN_CHAT_ID | Your Telegram chat ID for admin notifications |


### 👩‍💻 Authors
- Hanna Andrasiuk (@nessher) - [GitHub](https://github.com/nessher)
- Kiryl Sharmetau (@krlxmnd)


### 🤝 Contributing
**This project is a portfolio piece and is not currently open for contributions.**


### 📄 License
**This project is for portfolio purposes. All rights reserved.**
