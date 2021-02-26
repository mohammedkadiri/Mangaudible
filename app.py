from flask import Flask, render_template, request
from flask.json import jsonify
from flask_mysqldb import MySQL
from gcs import page_count, retrieve_url
import json

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'manga'

mysql = MySQL(app)



def getData(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    fetchdata = cur.fetchall()
    return fetchdata

def categoryQuery(category):
    query = 'select * from manga join manga_genre on manga_genre.manga_id = manga.ID join genre on genre.ID = manga_genre.genre_id where genre.Category =\'{0}\''.format(category)
    return query

def mangaQuery(name):
    query = 'select * from manga where manga.Name = \'{0}\''.format(name)
    return query




@app.route('/')
@app.route('/index.html')
@app.route('/manga/index.html')
def home():
    return render_template('index.html')


@app.route('/action.html')
@app.route('/manga/action.html')
@app.route('/manga/<comic>/<chapters>/action.html')
def action(comic = None, chapters= None):
    query = categoryQuery('action')
    return render_template('action.html', data = getData(query))

@app.route('/adventure.html')
@app.route('/manga/adventure.html')
@app.route('/manga/<comic>/<chapters>/adventure.html')
def adventure(comic = None, chapters=None):
    query = categoryQuery('adventure')
    return render_template('adventure.html', data = getData(query))

@app.route('/comedy.html')
@app.route('/manga/comedy.html')
@app.route('/manga/<comic>/<chapters>/comedy.html')
def comedy(comic = None, chapters= None):
    query = categoryQuery('comedy')
    return render_template('adventure.html', data = getData(query))

@app.route('/sport.html')
@app.route('/manga/sport.html')
@app.route('/manga/<comic>/<chapters>/sport.html')
def sport(comic = None, chapters= None):
    query = categoryQuery('sport')
    return render_template('sport.html', data = getData(query))

@app.route('/manga/<string:manga_name>')
def manga(manga_name):
    query = mangaQuery(manga_name)
    return render_template('manga.html', data = getData(query))


@app.route('/manga/<string:manga_name>/<string:chapter>/<string:page>')
def chapter(manga_name, chapter, page):
    manga_name = manga_name.replace("%", " ")
    pages = page_count("mangaudible", manga_name, chapter);
    url = retrieve_url("mangaudible", manga_name, chapter, page)
    url = url.replace(" ", "%20")
    values = [manga_name, chapter, page, url, pages]
    return render_template('chapter.html', data = values)

@app.route('/process',methods=['GET', 'POST'])
def process():
    rf = request.form
    for key in rf.keys():
        data = key
    data_dic = json.loads(data)
    temp = data_dic['value']
    resp_dic = {'msg': temp + 'hi'}
    resp = jsonify(resp_dic)
    resp.headers['Access-Control-Allow-Origin']='*'
    return resp



if __name__ == "__main__":
    app.run(debug=True)