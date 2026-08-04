# Sinema — Movie & TV Discovery & Review Platform

![Project Status](https://img.shields.io/badge/status-maintained-blue)
![Python](https://img.shields.io/badge/Python-Flask-blue)
![Database](https://img.shields.io/badge/Database-SQLite%20%7C%20SQLAlchemy-green)
![Deployment](https://img.shields.io/badge/Deployment-Vercel-purple)

# Overview

Sinema is a full-stack movie and TV review platform that allows users to discover, save, rate, and review media through an interactive web experience.

The application integrates the **TMDB API** for movie and TV data and uses **OpenRouter AI** to provide natural language media discovery. Built with **Flask, SQLAlchemy, SQLite, JavaScript, and Bootstrap**, Sinema demonstrates experience with API integration, authentication systems, database-driven applications, and modular web architecture.

Originally developed as a collaborative software development project, Sinema has continued to evolve through additional feature development, improvements, and maintenance.

---

# Live Demo

Explore the application:

https://sinema-sigma.vercel.app

---

# Screenshots

## Homepage/Search
![Home Screenshot](link)
![Search Screenshot](link)

## AI Search Feature
![AI_Search Screenshot](link)

## Media Info
![Media_Info1 Screenshot](link)
![Media_Info2 Screenshot](link)
![Media_Info3 Screenshot](link)

## User Profile
![User Profile1 Screenshot](link)
![User Profile2 Screenshot](link)

---

# Key Features

## Media Discovery

* Search movies and TV shows using TMDB
* View detailed media pages with:

  * Ratings
  * Descriptions
  * Runtime
  * Posters
  * Trailers
* Dynamic routing for individual media content

## AI-Powered Search

* Natural language media discovery using OpenRouter AI
* Supports conversational queries such as:

  * "Recommend recent science fiction movies"
  * "Show action TV series"

## User Features

* User registration and authentication
* Secure session-based authorization
* Save favorite movies and TV shows
* Rate media
* Write and manage reviews
* Personal profile pages

## Reliability & User Experience

* Handles missing API data gracefully
* Responsive Bootstrap interface
* Modular Flask architecture for maintainability

---

# Key Contributions

## Backend Development & API Integration

* Designed and developed the initial Flask backend foundation
* Integrated TMDB API workflows for movie and TV search
* Implemented dynamic media routes using TMDB identifiers
* Processed API responses into user-facing media pages

## Database & User Functionality

* Integrated SQLite database functionality with frontend features
* Implemented favorites, ratings, reviews, and user profiles
* Added validation to maintain database consistency

## Team Support & Documentation

* Created onboarding documentation for Flask development
* Established backend patterns to support team feature development
* Contributed to project architecture and continued improvements

---

# Project Collaboration

Sinema was originally developed as a collaborative software development project using an Agile workflow. The project emphasized team-based development, iterative improvements, and feature integration.

## Original Contributors

- ahaynes02
- sxc83640
- schugart
- xa7ier

## Continued Development

Following the initial team project, **Sphere Moghadami** continued development by expanding backend functionality, improving API integrations, refining user features, and maintaining the application.

---

# Technology Stack

## Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap 5

## Backend

* Python
* Flask
* SQLAlchemy

## Database

* SQLite

## APIs

* TMDB API
* OpenRouter API

## Tools

* Git/GitHub
* Postman
* VS Code
* Flask Debugger
* Browser Developer Tools

## Deployment

* Vercel

---

# Application Architecture

Sinema follows a modular Flask architecture separating application layers into routes, models, services, templates, and static resources. This separation improves maintainability by isolating application logic, database operations, API communication, and frontend presentation.

```text
app/
├── routes/
├── models/
├── services/
├── templates/
└── static/
```

This structure improves maintainability and allows features such as authentication, API communication, and user interactions to evolve independently.

---

# Technical Highlights

## API Integration

TMDB provides movie and TV metadata including:

* Search results
* Media details
* Posters
* Ratings
* Trailer information

OpenRouter AI expands search functionality by allowing users to discover media through natural language requests.

## Authentication & Security

The application includes:

* Session-based authentication
* Protected user routes
* Duplicate account prevention
* Review validation
* Authorization checks to prevent unauthorized access to user data

## Data Validation

Application workflows were tested across:

* Authentication
* Search functionality
* Dynamic routing
* Favorites
* Ratings
* Reviews
* Missing API data scenarios

---

# Running Locally

## Requirements

* Python 3.10+
* Git
* TMDB API key
* OpenRouter API key

## Setup

Clone the repository:

```bash
git clone https://github.com/SethMoga/Sinema.git
cd Sinema/sinema
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
TMDB_API_KEY=your_tmdb_api_key
```

Start the application:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

# Future Improvements

Potential enhancements include:

* Personalized recommendations
* Social features
* Advanced filtering
* Password recovery
* Expanded automated testing
* Additional accessibility improvements

---

# Repository

GitHub:
https://github.com/SethMoga/Sinema

## Developer

**Sphere Moghadami**
