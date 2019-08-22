# main.py

from getArticleInfo import getArticlesFromSearch, getArticleInfo, collectArticleInfo
from NDRM_form import ResearchSearchForm
from flask import flash, render_template, request, redirect
from flask import Flask, request, render_template

token = ''
##################################################
app = Flask(__name__)
app.secret_key = "flask rocks!"

@app.route('/', methods=['GET', 'POST'])
def index():
    search = ResearchSearchForm(request.form)
    if request.method == 'POST':
        flash(f"Please Wait")
        return search_results(search)

    return render_template('index.html', form=search)


@app.route('/results')
def search_results(search):
    global token
    results = []
    query = search.data['search']
    type = search.data['select']

    topic = query if type == 'Topic' else ""
    author = query if type == 'Author' else ""
    urlList = []

    if query == '':
        flash(f"Please enter a search query")
        return redirect('/')
    else:
        #display results
        flash(f'Searching for "{query}" as {type}')

        while len(urlList) == 0:
            urlList = getArticlesFromSearch(topic, author, year=2019, show=25, sort="date", token=token)
            flash(f"Retrieved {len(urlList)} Research Papers...")

        flash(f"Now scraping...")

        resultList = collectArticleInfo(urlList, numArticles=3, token=token)
        flash(f"Results = {resultList}")

        return redirect('/')
        #return render_template('results.html', results=results)


    #if not results:
    #    flash(f"No results found for: {search.data['search']}!")
    #    return redirect('/')
    #else:
    #    # display results
    #    return render_template('results.html', results=results)


if __name__ == '__main__':
    app.run()