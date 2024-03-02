<div class="container mt-5">

# Order Management System

👋 Welcome to the comprehensive README for the Order Management System. This document provides all necessary information for setting up, understanding, and using the application.

## 🌟 Features

This application combines a range of features to manage WooCommerce orders effectively:

*   📋 Order Listing: View all recent orders with details like Order ID, Customer, Status, and Total.
*   🔄 Order Status Update: Change the status of orders directly from the application.
*   🔍 Pagination: Navigate through orders in a paginated manner.
*   🖨️ Print Vouchers: Generate and print shipping labels for orders.
*   🔄 Automatic Status Refresh: Update and fetch the latest order statuses.
*   🔐 API Integration: Connect with WooCommerce API for real-time data access.
*   📦 Shipping Tracking: Fetch and display shipping tracking numbers for orders.
*   🖨 Print PDF with Chrome: Automatically print shipping labels using Google Chrome.

## 🚀 Installation & Setup

Ensure Python, Flask, WooCommerce, and necessary modules are installed. Set up your API credentials for WooCommerce and ACS courier services.

## 🖥️ Usage

Run the Flask application and navigate to the provided local URL to start managing orders. Utilize the additional scripts to handle specific tasks like printing shipping labels.

## 💡 Code Explanation

The system is built using Flask for the backend and HTML/CSS/JavaScript for the frontend. The additional Python script handles tasks such as API communication and PDF printing.

<div class="code">

<pre>from flask import Flask, render_template, request, redirect, url_for
from woocommerce import API
import json, os, requests, subprocess
...
app.run()</pre>

</div>

## 📄 Additional Notes

Before deploying the application, ensure all API credentials are correctly configured. Also, verify that Google Chrome is installed for the PDF printing feature.

## 🤝 Contribution

Contributions are welcome! Feel free to fork the repository, add new features, or improve existing ones.

## 📝 License

The project is available under the GPL-3.0 license.

</div>
