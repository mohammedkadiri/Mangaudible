"""Illustration of good import statement styling.

Note that the imports come after the docstring.

"""

# Standard library imports
import base64
import io
import json

# Third party imports
from flask import Flask, render_template, request
from flask.helpers import url_for
from flask.json import jsonify
from PIL import Image
from flask_mysqldb import MySQL
from werkzeug.utils import redirect

# Local application imports
from modules.gcs import page_count, retrieve_url
from modules.PanelExtractor import retrieve_panel_text, detect_document_uri, calculate_accuracy, translate_ocr_text, process_image



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
    query = 'select * from manga where manga.Name  = \'{0}\''.format(name)
    return query

# @main.template_filter('replace_space')
# def replace_space(url):
#     url = url.replace("%20", " ")
#     return url





@app.route('/')
@app.route('/index.html')
@app.route('/manga/index.html')
@app.route('/manga/<path:subpath>/index.html')
def home(subpath = None):
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



@app.route('/manga/<string:manga_name>', methods=['GET', 'POST'])
def manga(manga_name = None):
    query = mangaQuery(manga_name)
    data =  getData(query)
    # print(manga_name)
    if len(data) == 0:
        return redirect(url_for('unavailable')) 
    return render_template('manga.html', data = data)

@app.route('/unavailable')
def unavailable():
    return render_template('unavailable.html')


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
    temp = temp.replace(" ", "%20")
    temp = temp.replace("cloud.google", "googleapis")
    # panel_text = retrieve_panel_text(temp)
    # google_ocr_text = detect_document_uri(temp)
    # accuracy = calculate_accuracy(panel_text, google_ocr_text)
    # translated_panel_text = translate_ocr_text(google_ocr_text)
    img = process_image(temp)
    im_pil = Image.fromarray(img)
    data = io.BytesIO()
    im_pil.save(data, "PNG")
    encoded_img_data = base64.b64encode(data.getvalue())
    img_data=encoded_img_data.decode('utf-8')
    # print(encoded_img_data)
    # resp_dic = {'msg': "Accuracy: " + str(accuracy) +"%Text:\n" + translated_panel_text}
    resp_dic = {'msg': img_data}
    resp = jsonify(resp_dic)
    resp.headers['Access-Control-Allow-Origin']='*'
    return resp



if __name__ == "__main__":
    app.run(debug=True)