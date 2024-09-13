from flask import Flask, render_template, request
import torch
from transformers import BertTokenizer, BertForSequenceClassification

app = Flask(__name__)

# Load the trained model and tokenizer
loaded_model = BertForSequenceClassification.from_pretrained('bert_sentiment_model')
loaded_tokenizer = BertTokenizer.from_pretrained('bert_sentiment_model')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        user_review = request.form['review']

        # Tokenize and preprocess the user input
        def tokenize_user_input(review, max_length=128):
            encoded_dict = loaded_tokenizer.encode_plus(
                review,
                add_special_tokens=True,
                max_length=max_length,
                padding='max_length',
                truncation=True,
                return_tensors='pt',
            )

            return encoded_dict['input_ids'], encoded_dict['attention_mask']

        user_input_ids, user_attention_mask = tokenize_user_input(user_review)

        # Make the prediction
        with torch.no_grad():
            output = loaded_model(user_input_ids, attention_mask=user_attention_mask)
            prediction = torch.argmax(output.logits, dim=1).item() + 1  # Adding 1 to convert back to original rating scale

        return render_template('index.html', review=user_review, prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
