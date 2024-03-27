
import time
import streamlit as st
import random

# Define a dictionary mapping user queries to responses
responses = {
    "hello": ["Hi there! How can I help you today?", "Hello! What can I assist you with?", "Hey! How can I help?"],
    "website features": ["Our website offers a range of features including browsing products, making purchases, and contacting customer support.", "You can explore various features on our website like browsing products, making purchases, and contacting support."],
    "contact": ["You can contact us through our customer support email: support@example.com", "Feel free to contact our customer support at support@example.com"],
    "payment methods": ["We accept various payment methods including credit cards, PayPal, and bank transfers.", "We offer multiple payment options such as credit cards, PayPal, and bank transfers."],
    "shipping information": ["Our standard shipping takes 3-5 business days. For expedited shipping, please contact our customer support.", "Standard shipping typically takes 3-5 business days. Contact support for expedited options."],
    "return policy": ["We have a 30-day return policy. If you are not satisfied with your purchase, you can return it within 30 days for a full refund.", "Our return policy allows returns within 30 days for a full refund."],
    "bye": ["Goodbye! Have a great day!", "See you later! If you need anything else, feel free to ask."],
    "default": ["Sorry, I didn't quite catch that. Could you please rephrase?", "I'm not sure I understand. Can you please provide more details?", "I'm sorry, I couldn't find an appropriate response. How about asking something else?"],
    "discounts": ["We frequently offer discounts on various products. You can check our website or subscribe to our newsletter for updates.", "Discounts are often available on selected items. Keep an eye on our website for promotions."],
    "product availability": ["Our website offers a wide range of products. If a specific product is out of stock, you can sign up for notifications or contact our support team for assistance.", "Product availability may vary. Please check our website or contact support for the most up-to-date information."],
    "privacy policy": ["We take your privacy seriously. You can view our privacy policy on our website for more details.", "Our privacy policy outlines how we collect, use, and protect your personal information. You can find it on our website."],
    "account creation": ["You can create an account on our website by clicking on the 'Sign Up' or 'Register' button and following the instructions.", "To create an account, simply visit our website and click on 'Sign Up' to get started."],
    "order tracking": ["You can track your order by logging into your account on our website and navigating to the 'Order History' section.", "To track your order, go to the 'Order History' page after logging in to your account on our website."],
    "mobile app": ["We currently do not have a mobile app. However, our website is optimized for mobile browsing for your convenience.", "At the moment, we do not have a mobile app. You can access our website from any mobile device using a web browser."],
    "customer feedback": ["We value your feedback! You can provide feedback through our website's contact form or by reaching out to our customer support team.", "We appreciate your feedback! Feel free to share your thoughts through our website or contact our support team for assistance."],
    "product recommendations": ["Our website offers personalized product recommendations based on your browsing history and preferences. You can explore recommended products on your account dashboard.", "For personalized product recommendations, log in to your account and check out the recommended products section on your dashboard."],
    "FAQ": ["We have a comprehensive FAQ section on our website where you can find answers to commonly asked questions. You can access it through the main menu.", "Our FAQ section contains answers to frequently asked questions. You can find it in the main menu of our website."],
    "security measures": ["We implement strict security measures to protect your information. These include encryption, secure connections, and regular security audits to ensure data safety.", "Your security is our top priority. We employ various measures such as encryption and secure connections to safeguard your information."],
}

# Function to simulate bot typing
def simulate_typing():
    typing_message = "Bot is typing..."
    for i in range(0):  # Simulate typing for 3 seconds
        st.text_area("Bot:", f"{typing_message} {i}", key=f"typing_{i}")
        time.sleep(1)

# Streamlit app layout
def main():
    st.title("Website Chatbot")
    st.write("Welcome to our website chatbot. How can I assist you today?")
    
    # User input
    user_input = st.text_input("You:", "")

    # Bot response
    if user_input.strip().lower() in responses:
        responses_list = responses[user_input.strip().lower()]
        bot_response = random.choice(responses_list)
        simulate_typing()
        st.text_area("Bot:", bot_response)
    elif user_input.strip() != "":
        simulate_typing()
        st.text_area("Bot:", random.choice(responses["default"]))

if __name__ == "__main__":
    main()
