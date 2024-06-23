from flask import Flask, render_template, request
from scraper import scrape_all_sites

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = {'amazon': [], 'ebay': []}
    if request.method == 'POST':
        product_name = request.form['product_name']
        results = scrape_all_sites(product_name)
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
