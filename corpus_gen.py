import json
import pandas as pd

# Load main bank FAQs
with open('bank_faqs.json') as f:
    data = json.load(f)

# Load credit card FAQs
with open('credit_cards.json') as f:
    credit_data = json.load(f)

# Merge the data
data['bank']['credit_cards'] = credit_data['bank']['credit_cards']

bank_faq = pd.DataFrame(columns=['Question', 'Answer', 'Class'])

questions = []
answers = []
classes = []

for key in data['bank'].keys():
    for qnas in data['bank'][key]:
        questions.append(qnas[0])
        answers.append(qnas[1])
        classes.append(key)

bank_faq['Question'] = pd.Series(questions)
bank_faq['Answer'] = pd.Series(answers)
bank_faq['Class'] = pd.Series(classes)

bank_faq.to_csv("BankFAQs.csv", index=False)
