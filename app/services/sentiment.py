from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer # type: ignore

analyzer = SentimentIntensityAnalyzer()

def evaluate_sentiment(review):
    scores = analyzer.polarity_scores(review.body)
    compound = scores["compound"]
    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"
    return label, compound



    
