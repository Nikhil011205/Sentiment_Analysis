from flask import Flask, request, jsonify
import pandas as pd
import os
from groq import Client

app = Flask(__name__)

client = Client(api_key=os.environ.get("GROQ_API_KEY")) 

@app.route('/review-analysis', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if not (file.filename.endswith('.csv') or file.filename.endswith('.xlsx')):
        return jsonify({"error": "Invalid file format. Please upload CSV or XLSX files."}), 400
    
    try:
        if file.filename.endswith('.csv'):
            reviews_df = pd.read_csv(file)
        else:  
            reviews_df = pd.read_excel(file)

        if 'review' not in reviews_df.columns and 'Review' not in reviews_df.columns:
            return jsonify({"error": "No 'review' column found in the file."}), 400
        if 'review' in reviews_df.columns :
            reviews = reviews_df['review'].tolist()
        else : 
            reviews = reviews_df['Review'].tolist()
        if len(reviews) > 100:
            return jsonify({"error": "File contains more than 50 reviews"}), 400
        # print(reviews)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    results = []
    for review in reviews:
        result = analyze_sentiment(review)
        results.append(result)

    final_result = aggregate_results(results)
    return jsonify(final_result), 200

def analyze_sentiment(review):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Analyze the following review and classify it strictly as 'positive', 'negative' or 'neutral'. Your output must be one of these three words only:{review}"
                }
            ],
            model="llama-3.1-70b-versatile",
        )
        sentiment = chat_completion.choices[0].message.content  
        return sentiment
    except Exception as e:
        return {"error": "Analysis error: " + str(e)}

def aggregate_results(results):
    pos = 0
    neg = 0
    neutral = 0
    final = {'positive':0,'negative':0,'neutral':0}
    for i in results :
        # print(i)
        if 'positive' in i.lower() : 
            pos+=1
        elif 'negative' in i.lower() :
            neg+=1
        elif 'neutral' in i.lower() :
            neutral+=1
    total = len(results)
    final['positive'] = pos/total
    final['negative'] = neg/total
    final['neutral'] = neutral/total
    # print(final['positive']+final['negative']+final['neutral'])
    return final

if __name__ == '__main__':
    app.run(debug=True)
