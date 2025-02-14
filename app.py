from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Sample FAQ data
faqs = {
    "general": [
        {
            "question": "What are your banking hours?",
            "answer": "Our branches are typically open from 9:30 AM to 4:30 PM Monday through Friday. Online banking is available 24/7."
        },
        {
            "question": "How do I open a new account?",
            "answer": "You can open a new account by visiting any of our branches with valid ID proof and address proof, or through our online banking portal."
        }
    ],
    "online_banking": [
        {
            "question": "How do I register for online banking?",
            "answer": "You can register for online banking through our website using your account number and debit card details, or visit any branch for assistance."
        },
        {
            "question": "What if I forget my password?",
            "answer": "You can reset your password using the 'Forgot Password' option on the login page. You'll need your registered mobile number and account details."
        }
    ],
    "credit_cards": [
        {
            "question": "What credit cards do you offer?",
            "answer": "We offer various credit cards including Platinum, Gold, and Business credit cards. Each comes with unique benefits and rewards programs."
        },
        {
            "question": "How do I apply for a credit card?",
            "answer": "You can apply for a credit card through our website, mobile app, or by visiting any branch. You'll need to provide income proof and ID documents."
        }
    ]
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message'].lower()
        
        # Simple keyword matching
        response = "I apologize, but I couldn't find specific information about that. Please try asking in a different way or contact our customer service."
        
        for category, qa_pairs in faqs.items():
            for qa in qa_pairs:
                if any(keyword in user_message for keyword in qa['question'].lower().split()):
                    response = qa['answer']
                    break
        
        return jsonify({
            'response': response
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
