from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
from difflib import get_close_matches

app = Flask(__name__)
CORS(app)

# Load FAQ data from JSON file
def load_faqs():
    with open('bank_faqs.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Convert the nested structure into a flat list of Q&A pairs
    faqs_list = []
    for category, qa_list in data['bank'].items():
        for qa_pair in qa_list:
            if len(qa_pair) >= 2:  # Ensure we have both question and answer
                faqs_list.append({
                    'question': qa_pair[0],
                    'answer': qa_pair[1],
                    'category': category
                })
    return faqs_list

# Load FAQs on startup
try:
    all_faqs = load_faqs()
except Exception as e:
    print(f"Error loading FAQs: {e}")
    all_faqs = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message'].lower()
        
        # Get all questions for matching
        questions = [faq['question'].lower() for faq in all_faqs]
        
        # Find closest matching questions
        matches = get_close_matches(user_message, questions, n=3, cutoff=0.6)
        
        if matches:
            # Get the best match
            best_match = matches[0]
            # Find the corresponding FAQ
            for faq in all_faqs:
                if faq['question'].lower() == best_match:
                    return jsonify({
                        'response': faq['answer'],
                        'confidence': 'high' if len(matches) == 1 else 'medium'
                    })
        
        # Fallback to keyword matching if no close matches
        for faq in all_faqs:
            if any(keyword in user_message for keyword in faq['question'].lower().split()):
                return jsonify({
                    'response': faq['answer'],
                    'confidence': 'low'
                })
        
        return jsonify({
            'response': "I apologize, but I couldn't find specific information about that. Please try asking in a different way or contact our customer service.",
            'confidence': 'none'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
