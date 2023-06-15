# PFE_CODE

This repository contains a Django project that showcases the following features:

- Creating a virtual environment
- Installing packages from requirements
- Running the Django server

## Getting Started

Follow the steps below to set up and run the Django project locally.

### Prerequisites

- Python 3.10 installed on your system
- pip package manager (included with Python)

### Installation

```shell
# Clone the repository to your local machine
git clone https://github.com/your-username/your-repo.git

# Navigate to the project's root directory
cd your-repo

# Create a virtual environment
python -m venv env

# Activate the virtual environment
# On Windows
.\env\Scripts\activate
# On macOS and Linux
source env/bin/activate

# Install project dependencies from the requirements file
pip install -r requirements.txt

### Running the server
# Apply database migrations
python manage.py migrate

# Start the Django development server
python manage.py runserver

