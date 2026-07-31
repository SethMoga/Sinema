# Sinema - Movie & TV Review Platform

![Project Status](https://img.shields.io/badge/status-active%20development-yellow)
![Python](https://img.shields.io/badge/Python-Flask-blue)
![Database](https://img.shields.io/badge/Database-SQLite%20%7C%20SQLAlchemy-green)
![Deployment](https://img.shields.io/badge/Deployment-Vercel-purple)

## Overview

A modular full-stack Flask web application for discovering, reviewing, and managing your favorite movies and TV shows. **Sinema** combines TMDB's extensive media database with AI-powered natural language search to provide an engaging and intuitive user experience.

Originally developed as a collaborative team project, Sinema has continued to evolve through additional feature development, improvements, and refinements. The application emphasizes clean architecture, maintainability, secure authentication, and reliable API integration.

## 🌐 Live Demo

**Application:** https://sinema-sigma.vercel.app

---

## Project Background

Sinema is a build-off and continued development of an original team project created for a software development course. The original project was developed using an Agile methodology, emphasizing collaboration, iterative development, task management, and continuous improvement throughout the development process.

---

## Key Contributions

### Backend Architecture & TMDB API Integration
- Developed the initial Flask backend foundation that enabled movie and TV show searching through the TMDB API.
- Implemented the search workflow where user input from the search bar is passed as a query to TMDB, processes the JSON response, and displays the returned media results.
- Designed dynamic routing for individual media pages using TMDB IDs (e.g., `/movies/405`, `/tv-series/803`), allowing the team to expand functionality and display additional media information such as ratings, descriptions, runtime, and media type.

### Database & User Interaction Integration
- Integrated SQLite user account functionality with the frontend experience by reviewing and adapting existing database logic to work with updated UI interactions.
- Implemented synchronization between user actions and database state, ensuring features such as favorites correctly add/remove entries and reflect the current status in the interface.

### Developer Documentation & Team Support
- Created onboarding documentation explaining how to install, create, and run a Flask application.
- Provided example Flask code to help teammates understand framework structure, syntax, and development workflow.
- Supported the team by establishing backend patterns that allowed further frontend and feature development.

---

## Credits

Original team contributors:
- ahaynes02
- sxc83640
- schugart
- xa7ier

Continued development and maintenance:
- Seth Moga

---

## Features

* 🔍 Search movies and TV series using TMDB
* 🤖 AI-powered natural language search via OpenRouter API
* 👤 User registration and secure authentication
* ❤️ Save favorite movies and TV shows
* ⭐ Rate movies and TV series
* ✍️ Write and manage reviews
* 📺 Dynamic media detail pages
* 🎬 Embedded YouTube trailers when available
* 🖼️ Graceful fallback handling for missing media content
* 🔐 Session-based authentication and authorization
* 📱 Responsive user interface built with Bootstrap 5
* 🧩 Modular Flask architecture for maintainability

---

## Tech Stack

### Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap 5

### Backend

* Python
* Flask

### Database

* SQLite

### APIs

* TMDB API
* OpenRouter API

### Deployment

* Vercel

### Development Tools

* Git
* GitHub
* Postman
* VS Code
* Flask Debugger
* Browser Developer Tools

---

## Architecture

The application follows a modular Flask architecture that separates routing, business logic, database models, templates, and static assets.

```text
app/
├── routes/
├── models/
├── services/
├── templates/
└── static/
```

This structure improves maintainability, scalability, and collaboration by allowing different application layers to evolve independently.

---

## Installation

### Prerequisites

* **Python 3.10 or later** (download from https://www.python.org/downloads/)
* Git

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/SethMoga/Sinema.git
   ```

2. Navigate to the project directory:

   ```bash
   cd Sinema/sinema
   ```

3. Create and activate a virtual environment (strongly recommended).

   **Windows**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

   **macOS/Linux**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the project root (`Sinema/sinema`) and add the following environment variables:

   ```env
   OPENROUTER_API_KEY=your_openrouter_api_key
   TMDB_API_KEY=your_tmdb_api_key
   ```

   Obtain your API keys from:

   * **OpenRouter:** https://openrouter.ai/keys
   * **The Movie Database (TMDB):** https://developer.themoviedb.org/docs/getting-started

6. Start the Flask application:

   ```bash
   python app.py
   ```

7. Open your browser and visit the local URL displayed in the terminal (typically `http://127.0.0.1:5000`).

---

## Running the Project

Start the development server:

```bash
npm run dev
```

Or, depending on your setup:

```bash
npm start
```

---

## Usage

1. Open the live application: **https://sinema-sigma.vercel.app**

2. Click **Login**.

3. On the login page, click **Create Account** (or **Register**).

4. On the registration page, enter your **username**, **email address**, and **password** (enter the password twice for confirmation), then click **Create Account**. After successful registration, you will be redirected to the homepage.

5. Use the search bar at the top of the homepage to search for a movie or TV show, then click **Search**.

6. From the search results page:

   * Click any movie or TV show to open its information page.
   * Use the **Sort By** dropdown to organize results by **latest release year** or **alphabetical order**.
   * Use the filter options to display **All Media**, **Movies Only**, or **TV Shows Only**.

7. On a media information page:

   * Click **Add to Favorites** to save the title to your profile.
   * Scroll down and click **Write Review** to open the review form.
   * Complete the form and click **Post Review** to submit your review.

8. Hover over the **user profile** icon in the upper-right corner and select **My Profile** to view your saved favorites, ratings, and reviews.

9. Click the **SINEMA** logo in the upper-left corner to return to the homepage, then click **Try AI Search Feature**.

10. Select one of the predefined prompts or enter your own natural language query. The AI-powered assistant will generate relevant movie and TV show recommendations based on your request.

---

## API Integrations

### TMDB API

The application integrates with the TMDB API to provide:

* Movie search
* TV series search
* Media metadata
* Poster artwork
* YouTube trailer links
* Detailed media information

API responses were inspected and validated before implementation. Required fields such as media IDs and titles were verified first before expanding functionality to include posters, trailers, and additional metadata.

Missing API data is handled gracefully by:

* Displaying placeholder images when posters are unavailable
* Omitting the YouTube player when no trailer exists
* Preventing incomplete API responses from affecting the user experience

Validated routes include:

```text
/search?q=batman
/movies/<id>
/tv-series/<id>
```

### OpenRouter API

OpenRouter AI powers flexible natural language media search.

Example prompts include:

* "Show me recent movies featuring Tom Hanks."
* "Display action TV shows."
* "Recommend recent science fiction movies."

The AI integration expands traditional keyword search into a conversational discovery experience while maintaining relevant search results.

---

## Database & Security

The application includes persistent user functionality such as:

* User registration
* Secure login
* Favorites
* Ratings
* Reviews

Several validation rules help maintain database integrity.

### Duplicate Account Prevention

* Prevents duplicate usernames
* Prevents duplicate email registrations

### Review Validation

Users may submit only one review per movie or TV show, preventing duplicate reviews and review spam.

### Session Authentication

* Session-based authentication
* Protected routes for authenticated users
* Automatic redirects for unauthorized actions

### Authorization

The application includes authorization checks that prevent Broken Object Level Authorization (BOLA) attacks by ensuring users cannot access or manipulate another user's account through force browsing.

---

## Testing & Validation

Development emphasized continuous manual testing throughout implementation.

### Core Workflow Validation

The application's primary navigation flow was verified repeatedly during development.

```text
Homepage
    ↓
Search (/search)
    ↓
Dynamic Search Results
    ↓
Movie or TV Detail Page
```

### Functional Testing

Verified:

* Dynamic routing
* Search functionality
* Authentication
* User permissions
* Favorites
* Ratings
* Reviews
* Media navigation
* API requests

### User Scenario Testing

Test cases included:

* Saving favorites while logged out
* Posting reviews without authentication
* Invalid search queries
* Authentication redirects
* Dynamic URL generation
* Missing API data

Regression testing was performed after implementing new features to ensure existing functionality remained stable.

---

## Debugging & Troubleshooting

Application issues were diagnosed using several debugging techniques.

### Flask

* Flask error output
* Server-side logging
* Console output

### VS Code

* Python debugger
* Variable inspection
* Breakpoints

### Browser Developer Tools

* Session cookie inspection
* Client-side debugging
* Network requests

### API Debugging

Postman and Flask debugging tools were used to:

* Inspect JSON responses
* Verify required response fields
* Validate HTTP status codes
* Test API-dependent routes
* Confirm fallback behavior for incomplete API responses

---

## Git Workflow & Collaboration

This project was developed collaboratively using Git and GitHub.

### Version Control

Development began by creating a stable application foundation consisting of:

* Homepage
* Search page
* Dynamic routing
* Media detail pages

Additional functionality was built incrementally on top of this foundation.

### Feature Branches

Feature branches were used to isolate development work before merging into the main branch.

One example involved integrating the YouTube IFrame API in a separate branch while resolving:

* CORS policy issues
* Browser navigation behavior
* Back button inconsistencies

### Commit Practices

* Regular commits
* Descriptive commit messages
* Incremental feature development

---

## Future Improvements

Potential enhancements include:

* Personalized recommendations
* Social features
* Advanced filtering and sorting
* Email verification
* Password recovery
* Improved AI-assisted recommendations
* Additional accessibility improvements
* Improve mobile responsive design
* Expanded automated testing

---

## Contributing

Contributions are welcome. Fork the repository, create a feature branch, commit your changes, and open a pull request.

---

## Author

**Sphere Moghadami**

GitHub: https://github.com/SethMoga
