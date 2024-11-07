import random
import string
import requests

# Base URL for the API
BASE_URL = "http://localhost:8000"


# ---------------------- User Registration and Login Functions ----------------------


# Helper function for user registration
def register_user(data):
    """
    Registers a new user with the provided data.

    Args:
        data (dict): A dictionary with user information for registration.

    Returns:
        Response: The response from the API after attempting registration.
    """
    return requests.post(f"{BASE_URL}/user/register", json=data)


# Helper function for user login
def login_user(data):
    """
    Logs in a user with the provided data.

    Args:
        data (dict): A dictionary with user credentials for login.

    Returns:
        Response: The response from the API after attempting login.
    """
    return requests.post(f"{BASE_URL}/user/login", data=data)


# ---------------------- Add Functions ----------------------


# Helper function to add a new alert
def add_alert(data):
    """
    Adds a new alert with the provided data.

    Args:
        data (dict): A dictionary containing the alert information.

    Returns:
        Response: The response from the API after adding the alert.
    """
    return requests.post(f"{BASE_URL}/add/alert", json=data)


# Helper function to add a new reminder
def add_reminder(data):
    """
    Adds a new reminder with the provided data.

    Args:
        data (dict): A dictionary containing the reminder information.

    Returns:
        Response: The response from the API after adding the reminder.
    """
    return requests.post(f"{BASE_URL}/add/reminder", json=data)


# Helper function to add a new revenue
def add_revenue(data):
    """
    Adds a new revenue entry with the provided data.

    Args:
        data (dict): A dictionary containing the revenue information.

    Returns:
        Response: The response from the API after adding the revenue.
    """
    return requests.post(f"{BASE_URL}/add/revenue", json=data)


# ---------------------- Visualization Functions ----------------------


# Helper function to add a new expenditure
def add_expenditure(data):
    """
    Adds a new expenditure entry with the provided data.

    Args:
        data (dict): A dictionary containing the expenditure information.

    Returns:
        Response: The response from the API after adding the expenditure.
    """
    return requests.post(f"{BASE_URL}/add/expenditure", json=data)


# Helper function to view an alert
def visualize_alert(data):
    """
    Retrieves the details of a specific alert.

    Args:
        data (dict): A dictionary with parameters to specify the alert.

    Returns:
        Response: The response from the API with alert details.
    """
    return requests.get(f"{BASE_URL}/visualization/alert", params=data)


# Helper function to view a revenue entry
def visualize_revenue(data):
    """
    Retrieves the details of a specific revenue entry.

    Args:
        data (dict): A dictionary with parameters to specify the revenue entry.

    Returns:
        Response: The response from the API with revenue details.
    """
    return requests.get(f"{BASE_URL}/visualization/revenue", params=data)


# Helper function to view a reminder
def visualize_reminder(data):
    """
    Retrieves the details of a specific reminder.

    Args:
        data (dict): A dictionary with parameters to specify the reminder.

    Returns:
        Response: The response from the API with reminder details.
    """
    return requests.get(f"{BASE_URL}/visualization/reminder", params=data)


# Helper function to view an expenditure entry
def visualize_expenditure(data):
    """
    Retrieves the details of a specific expenditure entry.

    Args:
        data (dict): A dictionary with parameters to specify the expenditure entry.

    Returns:
        Response: The response from the API with expenditure details.
    """
    return requests.get(f"{BASE_URL}/visualization/expenditure", params=data)


# ---------------------- Deletion Functions ----------------------


# Helper function to delete an alert
def delete_alert(data):
    """
    Deletes a specific alert.

    Args:
        data (dict): A dictionary with parameters to specify the alert to delete.

    Returns:
        Response: The response from the API after deleting the alert.
    """
    return requests.delete(f"{BASE_URL}/delete/alert", params=data)


# Helper function to delete a reminder
def delete_reminder(data):
    """
    Deletes a specific reminder.

    Args:
        data (dict): A dictionary with parameters to specify the reminder to delete.

    Returns:
        Response: The response from the API after deleting the reminder.
    """
    return requests.delete(f"{BASE_URL}/delete/reminder", params=data)


# Helper function to delete a revenue entry
def delete_revenue(data):
    """
    Deletes a specific revenue entry.

    Args:
        data (dict): A dictionary with parameters to specify the revenue entry to delete.

    Returns:
        Response: The response from the API after deleting the revenue.
    """
    return requests.delete(f"{BASE_URL}/delete/revenue", params=data)


# Helper function to delete an expenditure entry
def delete_expenditure(data):
    """
    Deletes a specific expenditure entry.

    Args:
        data (dict): A dictionary with parameters to specify the expenditure entry to delete.

    Returns:
        Response: The response from the API after deleting the expenditure.
    """
    return requests.delete(f"{BASE_URL}/delete/expenditure", params=data)


# ---------------------- Update Functions ----------------------


# Helper function to update an alert
def update_alert(data):
    """
    Updates a specific alert.

    Args:
        data (dict): A dictionary with parameters to specify the alert to update.

    Returns:
        Response: The response from the API after updating the alert.
    """
    return requests.put(f"{BASE_URL}/update/alert", json=data)


# Helper function to update a reminder
def update_reminder(data):
    """
    Updates a specific reminder.

    Args:
        data (dict): A dictionary with parameters to specify the reminder to update.

    Returns:
        Response: The response from the API after updating the reminder.
    """
    return requests.put(f"{BASE_URL}/update/reminder", json=data)


# Helper function to update a revenue entry
def update_revenue(data):
    """
    Updates a specific revenue entry.

    Args:
        data (dict): A dictionary with parameters to specify the revenue entry to update.

    Returns:
        Response: The response from the API after updating the revenue.
    """
    return requests.put(f"{BASE_URL}/update/revenue", json=data)


# Helper function to update an expenditure entry
def update_expenditure(data):
    """
    Updates a specific expenditure entry.

    Args:
        data (dict): A dictionary with parameters to specify the expenditure entry to update.

    Returns:
        Response: The response from the API after updating the expenditure.
    """
    return requests.put(f"{BASE_URL}/update/expenditure", json=data)


# ---------------------- Auxiliary Functions ----------------------


# Helper function to generate a random email
def generate_random_email():
    """
    Generates a random email for testing purposes.

    Returns:
        str: A randomly generated email address.
    """
    random_str = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{random_str}@gmail.com"


# Helper function to generate a random date
def generate_random_date():
    """
    Generates a random date for testing purposes.

    Returns:
        str: A randomly generated date in the format 'YYYY-MM-DD'.
    """
    random_day = random.randint(1, 28)
    random_month = random.randint(1, 12)
    random_year = random.randint(1900, 2021)
    return f"{random_year}-{random_month:02d}-{random_day:02d}"
