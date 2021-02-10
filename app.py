from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'manga'

mysql = MySQL(app)

def category(name):
    cur = mysql.connection.cursor()
    query = 'select * from manga join manga_genre on manga_genre.manga_id = manga.ID join genre on genre.ID = manga_genre.genre_id where genre.Category =\'{0}\''.format(name)
    cur.execute(query)
    fetchdata = cur.fetchall()
    return fetchdata


@app.route('/')
@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/action.html')
def action():
    return render_template('action.html', data =  category('action'))

@app.route('/adventure.html')
def adventure():
    return render_template('adventure.html', data = category('adventure'))

@app.route('/comedy.html')
def comedy():
    return render_template('adventure.html', data = category('comedy'))

@app.route('/sport.html')
def sport():
    return render_template('sport.html', data = category('sport'))


if __name__ == "__main__":
    app.run(debug=True)