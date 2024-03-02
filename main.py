# 1. Import necessary modules.
from flask import Flask, render_template, request, redirect, url_for
from woocommerce import API
import json
import time
from datetime import datetime, timedelta

# 2. Define the WooCommerceAPI class.
class WooCommerceAPI:
    def __init__(self, url, consumer_key, consumer_secret):
        self.api = API(
            url=url,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            wp_api=True,
            version="wc/v3"
        )

    def get_orders(self):
        all_orders = []
        page = 1
        
        # Calculate the date 20 days ago
        twenty_days_ago = datetime.now() - timedelta(days=20)
        # Format it in the required format: '2023-10-10T00:00:00'
        after_date = twenty_days_ago.strftime('%Y-%m-%dT00:00:00')

        while True:
            response = self.api.get("orders", params={"per_page": 100, "page": page, "after": after_date}).json()
            if response:
                all_orders.extend(response)
                page += 1
            else:
                break
        return all_orders

    def update_order_status(self, order_id, status):
        data = {"status": status}
        return self.api.put(f"orders/{order_id}", data).json()

# 3. Set up the Flask app.
app = Flask(__name__)

# 4. Define the helper function get_tracking_info.
def get_tracking_info(order):
    for meta_data in order.get("meta_data", []):
        if meta_data["key"] == "_shipping_tracking_number":
            return meta_data["value"]
    return ""

def get_voucher_delivery_status(order):
    for meta_data in order.get("meta_data", []):
        if meta_data["key"] == 'voucher_delivery_status':
            return meta_data["value"]
    return ""  # Return an empty string if no voucher_delivery_status found


# 5. Configure Flask to recognize the helper function.
app.jinja_env.globals.update(get_tracking_info=get_tracking_info)
app.jinja_env.globals.update(get_voucher_delivery_status=get_voucher_delivery_status)



# 6. Create the Flask route for the main page.
@app.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # number of orders per page

    # Get all orders
    all_orders = api.get_orders()
    total_orders = len(all_orders)  # get total number of orders

    if request.method == 'POST':
        selected_orders = request.form.getlist('order_checkbox')
        new_status = request.form['status']
        for order_id in selected_orders:
            api.update_order_status(int(order_id), new_status)
        
            time.sleep(3)  # Introduce a delay of 3 seconds

        # Redirect back to the current page after updating
        return redirect(url_for('index', page=page))
    
    # Slicing the list of orders to achieve pagination
    start_idx = per_page * (page - 1)
    end_idx = start_idx + per_page
    orders = all_orders[start_idx:end_idx]
    return render_template('index.html', orders=orders, page=page, total_orders=total_orders, per_page=per_page)


@app.route('/update_order_status/<int:order_id>', methods=['POST'])
def update_order_status(order_id):
    order = next((o for o in api.get_orders() if o['id'] == order_id), None)
    if order and order['status'] in ['processing', 'on-hold']:
        api.update_order_status(order_id, 'completed')
    time.sleep(3)  # Introduce a delay of 3 seconds    
    return redirect(url_for('index'))


# 7. Define the get_api_credentials function.
def get_api_credentials():
    with open('api_credentials.json') as f:
        credentials = json.load(f)
    return credentials['url'], credentials['consumer_key'], credentials['consumer_secret']

@app.route('/run_script', methods=['POST'])
def run_script():
    import subprocess
    try:
        # Replace 'your_script.py' with the actual name of your Python script
        result = subprocess.check_output(['python', 'acs_print_tracking.py'], stderr=subprocess.STDOUT, text=True)
        return result
    except subprocess.CalledProcessError as e:
        return str(e.output)


# 8. Add the main execution code.
if __name__ == "__main__":
    url, consumer_key, consumer_secret = get_api_credentials()
    api = WooCommerceAPI(url, consumer_key, consumer_secret)
    app.run()
