import os
import re
import matplotlib.pyplot as plt
from collections import Counter
import snowballstemmer
from nltk.tokenize import word_tokenize

stemmer = snowballstemmer.stemmer('hindi')

STOP_WORDS = set([
    "मैं", "मुझको", "मेरा", "अपने आप को", "हमने", "हमारा", "अपना", "हम", "आप", "आपका", "तुम्हारा", "अपने आप", "स्वयं", "वह", "इसे", "उसके", "खुद को", "कि वह", "उसकी", "उसका", "खुद ही", "यह", "इसके", "उन्होने", "अपने", "क्या", "जो", "किसे", "किसको", "कि", "ये", "हूँ", "होता है", "रहे", "थी", "थे", "होना", "गया", "किया जा रहा है", "किया है", "है", "पडा", "होने", "करना", "करता है", "किया", "रही", "एक", "लेकिन", "अगर", "या", "क्यूंकि", "जैसा", "जब तक", "जबकि", "की", "पर", "द्वारा", "के लिए", "साथ", "के बारे में", "खिलाफ", "बीच", "में", "के माध्यम से", "दौरान", "से पहले", "के बाद", "ऊपर", "नीचे", "को", "से", "तक", "से नीचे", "करने में", "निकल", "बंद", "से अधिक", "तहत", "दुबारा", "आगे", "फिर", "एक बार", "यहाँ", "वहाँ", "कब", "कहाँ", "क्यों", "कैसे", "सारे", "किसी", "दोनो", "प्रत्येक", "ज्यादा", "अधिकांश", "अन्य", "में कुछ", "ऐसा", "में कोई", "मात्र", "खुद", "समान", "इसलिए", "बहुत", "सकता", "जायेंगे", "जरा", "चाहिए", "अभी", "और", "कर दिया", "रखें", "का", "हैं", "इस", "होता", "करने", "ने", "बनी", "तो", "ही", "हो", "इसका", "था", "हुआ", "वाले", "बाद", "लिए", "सकते", "इसमें", "दो", "वे", "करते", "कहा", "वर्ग", "कई", "करें", "होती", "अपनी", "उनके", "यदि", "हुई", "जा", "कहते", "जब", "होते", "कोई", "हुए", "व", "जैसे", "सभी", "करता", "उनकी", "तरह", "उस", "आदि", "इसकी", "उनका", "इसी", "पे", "तथा", "भी", "परंतु", "इन", "कम", "दूर", "पूरे", "गये", "तुम", "मै", "यहां", "हुये", "कभी", "अथवा", "गयी", "प्रति", "जाता", "इन्हें", "गई", "अब", "जिसमें", "लिया", "बड़ा", "जाती", "तब", "उसे", "जाते", "लेकर", "बड़े", "दूसरे", "जाने", "बाहर", "स्थान", "उन्हें", "गए", "ऐसे", "जिससे", "समय", "दोनों", "किए", "रहती", "इनके", "इनका", "इनकी", "सकती", "आज", "कल", "जिन्हें", "जिन्हों", "तिन्हें", "तिन्हों", "किन्हों", "किन्हें", "इत्यादि", "इन्हों", "उन्हों", "बिलकुल", "निहायत", "इन्हीं", "उन्हीं", "जितना", "दूसरा", "कितना", "साबुत", "वग़ैरह", "कौनसा", "लिये", "दिया", "जिसे", "तिसे", "काफ़ी", "पहले", "बाला", "मानो", "अंदर", "भीतर", "पूरा", "सारा", "उनको", "वहीं", "जहाँ", "जीधर", "﻿के", "एवं", "कुछ", "कुल", "रहा", "जिस", "जिन", "तिस", "तिन", "कौन", "किस", "संग", "यही", "बही", "उसी", "मगर", "कर", "मे", "एस", "उन", "सो", "अत"
])

def clean_and_tokenize(text):
    """Clean and tokenize the input text."""
    text = re.sub(r'[^ऀ-ॿ\s]', '', text)
    words = word_tokenize(text)
    filtered_words = [word for word in words if word not in STOP_WORDS]
    return filtered_words

def process_amar_ujala(directory):
    """Process files in the Amar Ujala folder."""
    word_counts = Counter()
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                print(f"Skipping file due to encoding error: {file_path}")
                continue

            if not content.strip():
                print(f"Skipping empty file: {file_path}")
                continue

            print(f"Processing file: {file_path}")
            words = clean_and_tokenize(content)
            word_counts.update(words)
    return word_counts

def process_jagran(directory):
    """Process files in the Jagran folder."""
    word_counts = Counter()
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                print(f"Skipping file due to encoding error: {file_path}")
                continue

            if not content.strip():
                print(f"Skipping empty file: {file_path}")
                continue

            print(f"Processing file: {file_path}")
            words = clean_and_tokenize(content)
            word_counts.update(words)
    return word_counts

def plot_zipfs_law(word_counts, language):
    sorted_counts = sorted(word_counts.values(), reverse=True)
    ranks = range(1, len(sorted_counts) + 1)
    plt.figure(figsize=(10, 6))
    plt.loglog(ranks, sorted_counts, marker=".")
    plt.title(f"Zipf's Law for {language}")
    plt.xlabel("Rank")
    plt.ylabel("Frequency")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.show()

def stem_words(word_counts):
    """Stem the words and count unique stemmed words."""
    stemmed_word_counts = Counter()
    for word, count in word_counts.items():
        stemmed_word = stemmer.stemWord(word)
        stemmed_word_counts[stemmed_word] += count
    return stemmed_word_counts

amar_ujala_path = ".\dataset\hindi\hi.doc.2010\amar_ujala"
jagran_path = ".\dataset\hindi\hi.doc.2010\jagran"

print("Processing Amar Ujala files...")
amar_ujala_counts = process_amar_ujala(amar_ujala_path)
print("Processing Dainik Jagran files...")
jagran_counts = process_jagran(jagran_path)

print("Combining word counts...")
total_word_counts = amar_ujala_counts + jagran_counts

print("Plotting Zipf's Law...")
plot_zipfs_law(total_word_counts, "Hindi")

print("Stemming words...")
stemmed_counts = stem_words(total_word_counts)

print(f"Original unique words: {len(total_word_counts)}")
print(f"Stemmed unique words: {len(stemmed_counts)}")
with open("hindi_word_statistics.txt", "w", encoding="utf-8") as f:
    f.write(f"Original Unique Words: {len(total_word_counts)} \n")
    f.write(f"Stemmed Unique Words: {len(stemmed_counts)} \n")
    f.write("Top 5 Words (Original):\n")
    for word, count in total_word_counts.most_common(10):
        f.write(f"{word}: {count}\n")
    f.write("\nTop 5 Words (Stemmed):\n")
    for word, count in stemmed_counts.most_common(10):
        f.write(f"{word}: {count}\n")

