import os
import re
from collections import Counter
import matplotlib.pyplot as plt
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# path
dataset_path = ".\dataset\english" 

ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

def clean_and_tokenize(text):
    text = re.sub(r'<[^>]+>', '', text)  
    text = re.sub(r'[^a-zA-Z]', ' ', text)  
    words = word_tokenize(text.lower())  
    words = [word for word in words if word not in stop_words and len(word) > 1]  
    return words

# processessing files nd extracting word frequencies
def process_files(directory):
    word_counts = Counter()
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print(f"Reading file contents: {file_path}")
            except UnicodeDecodeError:
                print(f"Skipping file due to encoding error: {file_path}")
                continue

            if not content.strip():
                print(f"Skipping empty file: {file_path}")
                continue

            print(f"Processing file: {file_path}")
            words = clean_and_tokenize(content)
            if not words:
                print(f"No words found in file: {file_path}")
                continue

            print(f"Tokenized {len(words)} words from file: {file_path}")
            word_counts.update(words)
    return word_counts


print("Processing files...")
word_counts = process_files(dataset_path)

sorted_word_counts = word_counts.most_common()

ranks = range(1, len(sorted_word_counts) + 1)
frequencies = [freq for _, freq in sorted_word_counts]

# Zipf's Law
plt.figure(figsize=(10, 6))
plt.loglog(ranks, frequencies, marker=".")
plt.title("Word Frequency vs Rank (Log-Log Scale)")
plt.xlabel("Rank")
plt.ylabel("Frequency")
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.show()

print("Stemming words...")
stemmed_word_counts = Counter()
for word, count in word_counts.items():
    stemmed_word = ps.stem(word)
    stemmed_word_counts[stemmed_word] += count
 
original_unique_words = len(word_counts)
stemmed_unique_words = len(stemmed_word_counts)

print("Original unique words:", original_unique_words)
print("Stemmed unique words:", stemmed_unique_words)

with open("word_statistics.txt", "w") as f:
    f.write("Original Unique Words: " + str(original_unique_words) + "\n")
    f.write("Stemmed Unique Words: " + str(stemmed_unique_words) + "\n")
    f.write("Top 5 Words (Original):\n")
    for word, count in sorted_word_counts[:10]:
        f.write(f"{word}: {count}\n")
    f.write("\nTop 5 Words (Stemmed):\n")
    for word, count in stemmed_word_counts.most_common(10):
        f.write(f"{word}: {count}\n")
