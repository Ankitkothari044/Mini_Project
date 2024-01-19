import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import classification_report
import pickle

# Load the dataset
df = pd.read_csv('food_reviews_dataset.csv')  

# Split the dataset into features (reviews) and labels
reviews = df['review']
labels = df['label']

# Preprocess the reviews
# Example: Lowercasing the text and removing punctuation
reviews = reviews.str.lower().replace('[^\w\s]', '', regex=True)

# Initialize the vectorizer
vectorizer = TfidfVectorizer()

# Fit and transform the reviews
reviews_vectorized = vectorizer.fit_transform(reviews)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    reviews_vectorized, labels, test_size=0.2, random_state=42)

# Train the Naive Bayes model
nb_model = MultinomialNB()
nb_model.fit(X_train, y_train)

# Train the Logistic Regression model
lr_model = LogisticRegression()
lr_model.fit(X_train, y_train)

# Create an ensemble of the models using VotingClassifier
ensemble_model = VotingClassifier(
    estimators=[('nb', nb_model), ('lr', lr_model)],
    voting='soft')  # Soft voting for probability-based predictions

# Train the ensemble model
ensemble_model.fit(X_train, y_train)

# Save the models and vectorizer as pickle files
with open('ensemble_model.pkl', 'wb') as file:
    pickle.dump(ensemble_model, file)

with open('vectorizer.pkl', 'wb') as file:
    pickle.dump(vectorizer, file)

# Evaluate the models on the testing set
y_test_pred = ensemble_model.predict(X_test)
print(classification_report(y_test, y_test_pred))
