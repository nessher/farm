# 🌾 Commercial Site for KFH (Family Farm)

[![GitHub Pages](https://img.shields.io/badge/GitHub-Pages-blue)](https://nessher.github.io/farm/)
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0-green?logo=django)](https://www.djangoproject.com/)
[![HTML5](https://img.shields.io/badge/HTML5-70.5%25-orange?logo=html5)](https://developer.mozilla.org/en-US/docs/Web/HTML)

## 📖 Overview

This is a full-featured **online store** for a family farm. It serves as a commercial platform for selling agricultural products. The project demonstrates a complete e-commerce workflow, from product browsing to order management.

**Live Demo**: [https://nessher.github.io/farm/](https://nessher.github.io/farm/)

## ✨ Key Features

- **Product Catalog**: Browse products with detailed descriptions and images.
- **Shopping Cart**: Add/remove items and manage quantities.
- **User Authentication**: Separate roles for clients and staff.
- **Personal Cabinet**: 
  - **Clients**: View and track their order history and status.
  - **Staff/Managers**: Access a dedicated dashboard to manage and track all customer orders.
- **Order Management**: Full cycle from placing an order to status updates.
- **Database**: Uses PostgreSQL for production (configured via Docker).

## 🛠️ Tech Stack

- **Backend**: Python, Django (MVT architecture)
- **Frontend**: HTML5, CSS3, JavaScript (vanilla)
- **Database**: SQLite (development), PostgreSQL (production)
- **Server/Deployment**: Docker, Docker Compose, Gunicorn
- **Hosting**: Deployed on **GitHub Pages** (for static parts) and configured for dynamic hosting.

## 🗂️ Project Structure
  ```
  farm/
  ├── main/                 # Main application with core models and views
  ├── config/               # Project settings and URLs
  ├── media/                # User-uploaded product images
  ├── static/               # Static files (CSS, JS)
  ├── Dockerfile            # Docker configuration for containerization
  ├── docker-compose.yml    # Docker Compose for multi-container setup
  ├── manage.py             # Django management script
  └── requirements.txt      # Python dependencies
  ```

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Docker and Docker Compose (for production setup)
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

4. **Run database migrations**
   ```bash
   python manage.py migrate

5. **Create a superuser (for admin access)**
   ```bash
   python manage.py createsuperuser

6. **Start the development server**
   ```bash
   python manage.py runserver
  The site will be available at http://127.0.0.1:8000


  
### Running with Docker (Production-like)

1. **Build and run the containers**
   ```bash
   docker-compose up --build
2. **Access the application at http://localhost:8000.**


### 📦 Deployment
**The project is configured for deployment. The static frontend part is hosted on GitHub Pages, while the dynamic backend is designed to be containerized and deployed on a cloud platform (like AWS, Heroku, or any VPS) using Docker.**


### 🤝 Contributing
**This project is a portfolio piece and is not currently open for contributions.**


###📄 License
**This project is for portfolio purposes. All rights reserved.**


###👩‍💻 Authors
**Hanna Andrasiuk (nessher) and Kiryl Sharmetau (@krlxmnd)**

GitHub: nessher

Project Link: https://github.com/nessher/farm
