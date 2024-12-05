import joblib


class MLRepository:
    def __init__(self):
        self._model = joblib.load('ml/model_none_30k.pkl')
        self._vector = joblib.load('ml/vectorizer_30k.pkl')

    def censor_profane_words(self, text):
        words = text.split()
        censored_words = []

        for word in words:
            # Check if the word makes the text profane when removed
            modified_text = text.replace(word, '')
            vectorized_modified = self._vector.transform([modified_text])

            # Check original text classification
            original_classification = self._model.predict(self._vector.transform([text]))[0]

            # Check modified text classification
            modified_classification = self._model.predict(vectorized_modified)[0]

            # If removing the word changes the classification, replace with *
            if modified_classification != original_classification:
                censored_words.append('*' * len(word))
            else:
                censored_words.append(word)

        # Reconstruct the sentence
        return ' '.join(censored_words)