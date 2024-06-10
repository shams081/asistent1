from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('template.html')


@app.route('/get-answer', methods=['POST'])
def get_answer():
    data = request.get_json()
    question = data.get('question', '')
    answer = search_internet(question)
    return jsonify({'answer': answer})


def search_internet(query):
    try:
        # Выполнение поиска в интернете
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        search_url = f"https://www.google.com/search?q={query}"
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Парсинг результатов поиска
        snippets = soup.select('.BNeawe.s3v9rd.AP7Wnd')
        if snippets:
            return snippets[0].text
        else:
            return "Извините, я не нашел ответа на ваш вопрос."
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)
