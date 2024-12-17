import joblib
import re
import tensorflow as tf
from functools import lru_cache


class MLRepository:
    def __init__(self):
        self._model = joblib.load('ml/model_none_50k_different_vectorizer_contractions.pkl')
        self._vector = joblib.load('ml/vectorizer_50k_different_vectorizer_contractions.pkl')
        self._rnn_model = tf.keras.models.load_model('ml/profanity_filter_model_rnn.keras')
        self._tokenizer = joblib.load('ml/tokenizer.pkl')

    @lru_cache(maxsize=1000)
    def _predict_substring(self, substring):
        substring_vectorized = self._vector.transform([substring])
        return self._model.predict(substring_vectorized)[0]

    def _generate_substrings(self, token):
        for length in range(len(token), 1, -1):
            for start in range(len(token) - length + 1):
                substring = token[start:start + length]
                yield substring

    def censor_profane_words(self, text, whitelist=None, early_stop=True):
        if whitelist is None:
            whitelist = set()

        censored_text = text
        tokens = re.findall(r'\b\w+\b', text)

        for token in tokens:
            if token.lower() in whitelist:
                continue

            for substring in self._generate_substrings(token):
                try:
                    substring_classification = self._predict_substring(substring)

                    if substring_classification == 1:
                        censored_text = censored_text.replace(substring, '*' * len(substring))

                        if early_stop:
                            break

                except Exception as e:
                    print(f"Prediction error for substring {substring}: {e}")

        return censored_text

    def censor_profane_rnn(self, text: str, threshold=0.5):
        sequence = self._tokenizer.texts_to_sequences([text])
        padded = tf.keras.preprocessing.sequence.pad_sequences(sequence, maxlen=100, padding='post', truncating='post')

        # Get the model's prediction for the input text
        prediction = self._rnn_model.predict(padded)[0][0]

        # If the model predicts the text is offensive, mask the offensive word(s)
        if prediction > threshold:
            words = text.split()  # Split text into words
            masked_words = []
            for word in words:
                # Check each word's profanity likelihood individually
                word_sequence = self._tokenizer.texts_to_sequences([word])
                word_padded = tf.keras.preprocessing.sequence.pad_sequences(
                                            word_sequence, maxlen=100, padding='post',
                                            truncating='post')
                word_prediction = self._rnn_model.predict(word_padded)[0][0]
                if word_prediction > threshold:
                    # Mask the word
                    masked_words.append(f"{word[0]}{'*' * (len(word) - 1)}")
                else:
                    # Keep the word as is
                    masked_words.append(word)
            return ' '.join(masked_words)
        else:
            # If not profane, return the original text
            return text
