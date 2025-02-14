# Banking FAQ Chatbot

A smart banking assistant that helps users with common banking queries. The chatbot features a modern web interface similar to Bank of India's Smart Banking page and provides quick responses to banking-related questions.

## Features

- 🎯 Smart query matching for accurate responses
- 💬 Modern chat interface
- 🎨 Responsive web design
- 🏦 Banking-specific knowledge base
- 🔊 Voice interaction support
- 🌐 Web-based interface matching Bank of India's design

## Technologies Used

- Python 3.x
- Flask (Web Framework)
- HTML/CSS/JavaScript
- Bootstrap 5
- Font Awesome Icons
- pyttsx3 (Text-to-Speech)
- SpeechRecognition (Speech-to-Text)

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/banking-faq-bot.git
   cd banking-faq-bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your browser and visit:
   ```
   http://localhost:5000
   ```

## Project Structure

```
banking-faq-bot/
├── app.py              # Flask application
├── Bank FAQbot.py      # Core chatbot logic
├── requirements.txt    # Python dependencies
├── templates/         
│   └── index.html     # Web interface
├── static/            # Static assets
├── bank_faqs.json     # FAQ database
└── README.md          # Documentation
```

## Usage

1. Start the Flask server using `python app.py`
2. Open your web browser and navigate to `http://localhost:5000`
3. Type your banking-related questions in the chat interface
4. For voice interaction, click the microphone icon and speak your question

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
