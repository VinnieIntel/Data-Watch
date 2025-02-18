*Setup Guide*

# Prerequisites
- Git
- Node.js
- npm

Download it here if not done before: https://nodejs.org/en/

# 1. Clone the Repository

First, clone this repository to your local machine:
```
git clone https://github.com/VinnieIntel/Data-Watch.git
cd Data-Watch
```
<br/>

# 2. Backend Setup

## 2.1 Create a Virtual Environment

A virtual environment is recommended to manage dependencies.

For Windows (Command Prompt or PowerShell):

```
cd backend
python -m venv .venv
.venv\Scripts\activate
```

For macOS/Linux (Terminal):
```
cd backend
python3 -m venv .venv
source .venv/bin/activate
```

## 2.2 Install Dependencies

Once the virtual environment is activated, install the required dependencies:

```
pip install -r requirements.txt
```

## 2.3 Verify Installation

Check if dependencies are installed correctly:
```
python -m flask --version  # Example: Verify Flask installation
```

## 2.4 Running the Application

_To start the application:_
```
python app.py
```


## 2.5 Deactivate the Virtual Environment

When you're done, deactivate the virtual environment:

```
deactivate
```

<br/>

# 3. Frontend Setup
The frontend is built using React.js and requires npm for dependency management.

_Install Frontend Dependencies_
Navigate to the frontend directory and install dependencies:
```
cd frontend
npm install
```
_Running the Frontend_
Start the frontend development server:
```
npm run dev
```
This will launch the application in your default web browser.

<br/>

# Additional Notes

- If you install new dependencies for the backend, run:
```
pip freeze > requirements.txt
```
and commit the updated requirements.txt.

- If you install new dependencies for the frontend, update package.json and commit the changes.

- .venv/ is excluded from Git using .gitignore to prevent unnecessary file uploads.

#### Happy coding! :) ~Vinnie