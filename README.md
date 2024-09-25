
## Objective

The goal of this project is to develop a Python-based API that processes customer reviews, performs sentiment analysis using the Groq API, and returns structured results in JSON format.

## Approach to Solving the Problem

The solution is built as a Flask-based API that accepts files containing customer reviews (in CSV or XLSX format) and returns a JSON response summarizing the sentiment of the reviews. The reviews are analyzed for sentiment using the Groq API's large language model (LLM). The API processes each review, classifies it as positive, negative, or neutral, and then aggregates the results to return a percentage distribution of each sentiment type.

### Key Features:
1. **File Handling**: The API supports both CSV and XLSX formats. It parses the input file, extracting customer reviews for analysis.
2. **Sentiment Analysis**: Each review is sent to the Groq API's LLM (), which classifies the review as positive, negative, or neutral.
3. **Error Handling**: Basic error handling is implemented for invalid file formats, missing 'review' columns, or API errors.
4. **Structured Response**: The API aggregates the sentiment analysis results into a structured JSON response, providing percentages of positive, negative, and neutral reviews.

## How the Structured Response is Implemented

1. **Input Parsing**: The API receives the file, checks its format (CSV or XLSX), and extracts the column containing the reviews. It supports case variations in the 'review' column header (e.g., 'review' or 'Review').
   
2. **Sentiment Analysis**: Each extracted review is passed to the `analyze_sentiment` function, which uses the Groq API to classify the review.

3. **Result Aggregation**: After processing all the reviews, the `aggregate_results` function counts how many reviews were positive, negative, or neutral. The results are then normalized to provide percentages.

4. **Final Output**: The API returns a structured JSON response in the format:
   ```json
   {
       "positive": score,
       "negative": score,
       "neutral": score
   }
   ```

## API Usage

### Example 1: Successful Sentiment Analysis (CSV File)

#### Sample Input 1:
```bash
curl -X POST http://localhost:5000/review-analysis \
-F 'file=@reviews.csv'
```

Assuming the CSV file contains the following data:

| review                                |
| ------------------------------------- |
| Great product, really happy with it!  |
| Very bad experience, won’t buy again. |
| It was okay, nothing special.         |

#### Sample Output 1:
```json
{
    "negative": 0.3333333333333333,
    "neutral": 0.3333333333333333,
    "positive": 0.3333333333333333
}
```

#### Sample Input 2:
```bash
curl -X POST http://localhost:5000/review-analysis \
-F 'file=@customer_reviews.xslx'
```

Assuming the Excel file contains the following data:

| Review                                         |
| ---------------------------------------------- |
| Great product, very useful!                    |
| Poor quality and bad customer service.😡       |
| Average performance, nothing special.          |
| Exceeded my expectations, fantastic!           |
| Terrible, not worth the money.😞               |
| Quite good, but could be improved.             |
| Mediocre at best, not recommended.             |
| Wonderful design, highly recommended!          |
| Awful experience, would not buy again.         |
| Solid product, good value for the price.       |
| Highly satisfied with the purchase.            |
| The product broke after a few uses.            |
| I would definitely buy this again!😄           |
| Not as described, very disappointed.           |
| Customer service was really helpful.           |
| It works perfectly as expected.                |
| I had a terrible experience with this.         |
| Well worth the money.                          |
| Waste of time and money.                       |
| Absolutely love this product!                  |
| It didn’t work as advertised.                  |
| Very reliable and easy to use.                 |
| I had higher expectations, sadly disappointed. |
| Delivered quickly, works as intended.          |
| Horrible quality, won’t buy again.             |
| This is the best purchase I’ve made.           |
| It stopped working after a month.              |
| I’m quite pleased with this product.           |
| Very cheap material, not durable.              |
| Fantastic performance for the price.           |
| Extremely frustrating experience.              |
| User-friendly and well-designed.               |
| Not worth the price at all.🙁                  |
| Better than expected!                          |
| The instructions were very unclear.            |
| Would definitely recommend to others.          |
| Very underwhelming experience.                 |
| Does the job, no complaints.                   |
| I regret purchasing this item.                 |
| Great value for money!😃                       |
| Arrived damaged, very disappointed.            |
| Exceeded my expectations!                      |
| Not what I was hoping for.                     |
| Happy with the purchase overall.               |
| Total waste of money.                          |
| Amazing product, highly satisfied!             |
| Not durable, broke after a few uses.           |
| Fantastic design and great quality.            |
| Wouldn’t recommend to others.                  |
| Excellent value, would buy again.              |
| Terrible product, avoid at all costs.          |

#### Sample Output 2:
```json
{
    "negative": 0.47058823529411764,
    "neutral": 0.0392156862745098,
    "positive": 0.49019607843137253
}
```

### Example 2: Error Handling (Invalid File Format)

#### Sample Input:
```bash
curl -X POST http://localhost:5000/review-analysis \
-F 'file=@reviews.txt'
```

#### Sample Output:
```json
{
   "error": "Invalid file format. Please upload CSV or XLSX files."
}
```

### Example 3: Error Handling (Missing 'review' Column)

#### Sample Input:
```bash
curl -X POST http://localhost:5000/review-analysis \
-F 'file=@wrong_structure.csv'
```

#### Sample Output:
```json
{
   "error": "No 'review' column found in the file."
}
```

## Analysis of Results

### Strengths:
1. **Modularity**: The code is structured in a modular fashion, separating the file handling, sentiment analysis, and result aggregation processes.
2. **Error Handling**: Basic error handling ensures that common issues (such as file format mismatches or missing data) are managed properly.
3. **Scalability**: The API can handle large input files (up to 100 reviews) and can be extended to integrate additional sentiment models.

### Limitations:
1. **API Request Size Limit**: The current implementation restricts the number of reviews to a maximum of 100 (50 mentioned in problem statement). Scaling this limit would require more robust handling of API rate limits and batch processing.
2. **Dependency on External API**: The performance and accuracy of the sentiment analysis rely heavily on the Groq API. Any downtime or latency in the external API will directly affect the API’s responsiveness.
3. **Output of LLM**: It might not be just one word, or might not capture the essence as good as expected, a lot of the times it gave more than one word error, which had to be fixed by taking precautionary "in" operator usage. 

## Potential Improvements:
1. **Batch Processing**: Implement batch processing to handle more than 100 reviews by sending requests in smaller batches to avoid API rate limits.
2. **Model Switching**: Allow dynamic switching between different sentiment analysis models to test accuracy or performance improvements over time.
3. **Caching Results**: For performance optimization, caching sentiment results of previously analyzed reviews could reduce API call frequency and improve response time.

## Additional Insights

1. The JSON mode is still in beta test and the documentation was only present in javascipt, which is why the implementation of a smarter prompt engineering approach was taken
2. We can parse the entire review array instead of passing it one by one, if the LLM model responds in a specific manner which can be solved by using the JSON mode

In summary, the API provides a flexible solution for sentiment analysis of customer reviews, integrating well with the Groq API for large language model processing, and offering clear, structured responses.
