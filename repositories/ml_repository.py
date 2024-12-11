import joblib
import re
from functools import lru_cache


class MLRepository:
    def __init__(self):
        self._model = joblib.load('ml/model_none_50k_different_vectorizer_contractions.pkl')
        self._vector = joblib.load('ml/vectorizer_50k_different_vectorizer_contractions.pkl')

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
