text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
words = text.split()
word_counts = {word: words.count(word) for word in words}
sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
top_words = dict(sorted_word_counts[:20])
print(top_words)