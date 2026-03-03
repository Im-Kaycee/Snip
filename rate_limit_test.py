import requests
import time
from concurrent.futures import ThreadPoolExecutor

# --- Configuration ---
URL = "http://localhost:8000/api/shorten"
ORIGINAL_URL = "https://example.com"
REQUESTS_PER_USER = 15   # total requests per simulated user
DELAY_BETWEEN_REQUESTS = 0.5  # seconds
CONCURRENT_USERS = 3     # simulate multiple IPs (threads)

# --- Function to make requests ---
def make_requests(user_id):
    for i in range(REQUESTS_PER_USER):
        try:
            r = requests.post(
                URL,
                json={"original_url": ORIGINAL_URL},
                timeout=5
            )
            status = r.status_code
            if status == 200:
                print(f"[User {user_id}] {i+1}: SUCCESS -> {r.json()['short_url']}")
            elif status == 429:
                print(f"[User {user_id}] {i+1}: RATE LIMITED")
            else:
                print(f"[User {user_id}] {i+1}: {status} -> {r.text}")
        except Exception as e:
            print(f"[User {user_id}] {i+1}: ERROR -> {e}")
        time.sleep(DELAY_BETWEEN_REQUESTS)

# --- Run concurrent users ---
if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=CONCURRENT_USERS) as executor:
        for u in range(1, CONCURRENT_USERS + 1):
            executor.submit(make_requests, u)