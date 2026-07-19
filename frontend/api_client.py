import requests

API_URL = "http://localhost:4000"

class APIClient:
  @staticmethod
  def get_users():
    response = requests.get(f"{API_URL}/users")
    return response.json()

  @staticmethod
  def create_user(data):
    return requests.post(f"{API_URL}/users", json=data)

  @staticmethod
  def update_user(user_id, data):
    return requests.put(f"{API_URL}/users/{user_id}", json=data)

  @staticmethod
  def delete_user(user_id):
    return requests.delete(f"{API_URL}/users/{user_id}")
