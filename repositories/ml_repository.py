import joblib
import re


class MLRepository:
    def __init__(self):
        self._model = joblib.load('ml/model_none_30k.pkl')
        self._vector = joblib.load('ml/vectorizer_30k.pkl')

    def censor_profane_words(self, text, whitelist=None):
        if whitelist is None:
            whitelist = set()  # Default to an empty whitelist

        censored_text = text  # Start with the original text

        # Tokenize text into potential words (spaces and non-spaces included)
        tokens = re.findall(r'\b\w+\b', text)  # Finds words while keeping non-word characters separate

        for token in tokens:
            # Skip whitelisted words
            if token.lower() in whitelist:
                continue

            # Check if the token contains potential profane words
            for i in range(len(token)):
                for j in range(i + 1, len(token) + 1):
                    substring = token[i:j]

                    # Vectorize the substring
                    substring_vectorized = self._vector.transform([substring])

                    # Predict if the substring is profane
                    substring_classification = self._model.predict(substring_vectorized)[0]

                    # If the substring is profane, censor it in the original text
                    if substring_classification == 1:  # Assuming 1 indicates a profane word
                        censored_text = censored_text.replace(substring, '*' * len(substring))

        return censored_text
