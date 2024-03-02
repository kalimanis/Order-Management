import os
import json
import requests
from woocommerce import API
from datetime import datetime
import subprocess

def load_api_credentials(file_path):
    try:
        with open(file_path, "r") as file:
            credentials = json.load(file)
            return credentials
    except FileNotFoundError:
        print(f"API credentials file not found: {file_path}")
        return None

def print_pdf_with_chrome(pdf_filename):
    try:
        absolute_path = os.path.abspath(pdf_filename)
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        subprocess.run([chrome_path, "--print", absolute_path])
    except Exception as e:
        print(f"Failed to print {pdf_filename} with Chrome. Error: {str(e)}")

def fetch_shipping_tracking_number(order_id):
    response = wcapi.get(f"orders/{order_id}")
    if response.status_code == 200:
        order = response.json()
        for meta_data in order.get("meta_data", []):
            if meta_data["key"] == "_shipping_tracking_number":
                return meta_data["value"]
        print(f"No tracking number found for order {order_id}.")
    else:
        print(f"Failed to fetch order {order_id}.")
    return None

def fetch_completed_orders():
    response = wcapi.get("orders", params={"status": "completed"})
    if response.status_code == 200:
        all_completed_orders = response.json()
        today = datetime.utcnow().strftime("%Y-%m-%d")
        todays_completed_orders = [
            order for order in all_completed_orders
            if order.get('date_completed_gmt', '').startswith(today)
        ]
        return todays_completed_orders
    else:
        print(f"Failed to fetch completed orders.")
        return []

def download_pdf(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
    else:
        print("Failed to download PDF.")

if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.realpath(__file__))
    api_credentials_file = os.path.join(script_directory, "api_credentials.json")
    acs_api_credentials_file = os.path.join(script_directory, "acs_api_credentials.json")

    api_credentials = load_api_credentials(api_credentials_file)
    acs_api_credentials = load_api_credentials(acs_api_credentials_file)

    if not api_credentials or not acs_api_credentials:
        print("API credentials not found or invalid.")
        exit()

    wcapi = API(
        url=api_credentials.get("url"),
        consumer_key=api_credentials.get("consumer_key"),
        consumer_secret=api_credentials.get("consumer_secret"),
        version="wc/v3"
    )

    completed_orders = fetch_completed_orders()
    voucher_numbers = []

    for order in completed_orders:
        order_id = order["id"]
        tracking_number = fetch_shipping_tracking_number(order_id)
        if tracking_number:
            voucher_numbers.append(str(tracking_number))
    
    acs_url = (
        f"https://acs-eud2.acscourier.net/Eshops/GetVoucher.aspx"
        f"?MainID={acs_api_credentials['MainID']}"
        f"&MainPass={acs_api_credentials['MainPass']}"
        f"&UserID={acs_api_credentials['UserID']}"
        f"&UserPass={acs_api_credentials['UserPass']}"
        f"&voucherno={'|'.join(voucher_numbers)}"
        f"&PrintType=2"
        f"&StartFromNumber=1"
    )

    pdf_filename = "shipping_labels.pdf"
    download_pdf(acs_url, pdf_filename)
    
    print_pdf_with_chrome(pdf_filename)
