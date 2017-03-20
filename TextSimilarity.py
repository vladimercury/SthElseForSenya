class TextSimilarity:  # Класс для определения косинусной близости абзацев текста
    def __init__(self):
        # Инициализация
        from sklearn.feature_extraction.text import TfidfVectorizer
        self.vectorizer = TfidfVectorizer(min_df=0.0)  # Класс для построения TF-IDF матрицы

    def get_cosine_similarity(self, text):
        # Возвращает матрицу косинусной близости
        from sklearn.metrics.pairwise import cosine_similarity
        # modified_text = self.get_modified_text(text)  # Получение модифицированного текста
        matrix = self.vectorizer.fit_transform(text)  # Получение TF-IDF матрицы
        cosine = cosine_similarity(matrix)  # Получение матрицы косинусной близости
        return cosine

    def get_cosine_similarity_tfidf(self, tfidf):
        from sklearn.metrics.pairwise import cosine_similarity
        cosine = cosine_similarity(tfidf)
        return cosine