import pandas as pd

# Create a list of reviews
reviews = [
"This product is amazing! It exceeded my expectations in every way.",
"I would never recommend this to anyone. It's a complete waste of money.",
"The service at this restaurant was exceptional. The staff was friendly and attentive.",
"I suspect that the positive reviews for this movie are fake. It was terrible.",
"The quality of the product is subpar. It broke after just a few uses.",
"I'm extremely satisfied with my purchase. The item arrived on time and in perfect condition.",
"The claims made by this company are misleading and deceptive. Don't fall for it.",
"This restaurant exceeded my expectations in every aspect.",
"csjncanasj",
"The food was absolutely delicious. with a perfect blend of flavors and high-quality ingredients.",
"The food was of good quality.",
"Bad Quality Food",
"Tasty and delicious"

]
print(len(reviews))
# Create a list of corresponding labels
labels = [
    "genuine",
    "fake",
    "genuine",
    "fake",
    "fake",
    "genuine",
    "fake",
    "geniune",
    "fake",
    "genuine",  
    "genuine",
    "genuine",
    "genuine"
]
print(len(labels))
# Create a DataFrame from the lists
df = pd.DataFrame({'review': reviews, 'label': labels})

# Save the DataFrame as a CSV file
df.to_csv('food_reviews_dataset.csv', index=False)
