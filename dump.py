import os
import random
import requests
from faker import Faker
import django

# Set the environment variable to point to your Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BlockAsset.settings")  # Change 'your_project_name' to your Django project name
django.setup()  # Setup Django

# Initialize Faker to generate fake data
fake = Faker()

def generate_user_data():
    """Generate random user data."""
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = f'{first_name.lower()}.{last_name.lower()}@example.com'
    username = f'{first_name.lower()}{random.randint(100, 999)}'

    # Create user data dictionary
    user_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "username": username,
        "password": fake.password(),
        "phone_number": fake.phone_number().replace(" ", "").replace("-", "")[:12],  # Up to 12 digits
        "profile_picture_url": fake.image_url(),
        "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%Y-%m-%d')
    }

    return user_data

def create_users(n=100):
    """Create users by sending requests to the API."""
    url = 'http://127.0.0.1:8000/api/user/signup'  # Change this to your API endpoint

    for i in range(n):
        user_data = generate_user_data()
        response = requests.post(url, json=user_data)

        if response.status_code == 201:
            print(f"User {i + 1} created successfully: {user_data['username']}")
        else:
            print(f"Failed to create user {i + 1}: {response.json()}")

if __name__ == "__main__":
    number_of_users = 100  # Set how many users to create
    create_users(number_of_users)
