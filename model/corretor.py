import pandas as pd
from fuzzywuzzy import fuzz
from spellchecker import SpellChecker

class Corrector():
    def __init__(self, text, df):
        self.text = text.split()
        self.df = df
        self.word_dict = self.create_word_dict()

    def create_word_dict(self):
        word_dict = {}
        for _, row in self.df.iterrows():
            word = row[0]
            list_words = row[1].split(',')
            word_dict[word] = list_words
        return word_dict

    def custom_corrector(self):
        results = []
        for text in self.text:
            max_similarity = 0
            max_class = text
            max_average = 0
            for word, list_words in self.word_dict.items():
                average = 0
                for word_ref in list_words:
                    similarity = fuzz.ratio(text.lower(), word_ref.lower())
                    average += similarity
                    if similarity > max_similarity and similarity > 85:
                        max_similarity = similarity
                        max_class = word
                average = average / len(list_words)
                if average > max_average and average > 70.0:
                    max_average = average
                    max_class = word
                    print(max_class)
            result = {'class': max_class, 'probability': max_similarity}
            results.append(result)

        spell_pt = SpellChecker(language='pt')
        for i, result in enumerate(results):
            if result['probability'] == 0:
                correction = spell_pt.correction(result['class'])
                if correction != None:
                    results[i] = {'class': correction, 'probability': 0.9}

        return results


df_erradas = pd.read_excel(r'model\palavras_erradas.xlsx')
df = df_erradas.drop('Unnamed: 0', axis=1)
corrige = Corrector('Estou entrando em contato para relatar um problma que um cliente encontrou com a conexão de internet via WiFi. O usuáriu está reclamando que a conexão intermitente e tem quedas frequentes. Ele diz que a conexão fica lenta e que às vezes nem consegue se conectr. Isso está causandu muita frustação para o usuáriu, que precisa da internet para realizar suas atividades diárias.', df)
a = corrige.custom_corrector()

classes = [result['class'] for result in a]
print(' '.join(classes))
