
from flask_wtf import Form
from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
import dbconn

from add import AddForm
from search import SearchForm
from update import UpdateForm
from delete import DeleteForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fa7fa1cf88f94edca5d56dd702ebc64c'
app.debug = True

bootstrap = Bootstrap(app)


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


@app.route('/add', methods = ['GET', 'POST'])
def add():
    name = success = ''
    info = AddForm()

    if info.validate_on_submit():
        name = info.name.data
        english = info.english.data
        python = info.python.data
        java = info.java.data

        status = dbconn.insert(name, english, python, java)
        success = check(status)

    return render_template('add.html', form = info, name = name, success = success)


@app.route('/search', methods = ['GET', 'POST'])
def search():
    name = ''
    results = list()
    info = SearchForm()

    if info.validate_on_submit():
        name = info.name.data

        if name == '':
            results = dbconn.searchAll()
        else:
            infos = dict()
            result = dbconn.searchSingle(name)
            result = list(result)
            for _ in range(len(result)):
                infos['id'] = result[0]
                infos['name'] = result[1]
                infos['english'] = result[2]
                infos['python'] = result[3]
                infos['java'] = result[4]

            results.append(infos)

    return render_template('search.html', form = info, name = name, results = results)


@app.route('/update', methods = ['GET', 'POST'])
def update():
    name = ''
    info = UpdateForm()
    d = {}

    if info.validate_on_submit():
        name = info.name.data
        english = info.english.data
        python = info.python.data
        java = info.java.data


        d['stud_name'] = "'" + name + "'"
        d['english_score'] = english
        d['python_score'] = python
        d['java_score'] = java


        status = dbconn.update(name, d)
        success = check(status)
    else:
        success = check(-1)

    return render_template('update.html', form = info, name = name, success = success)


@app.route('/delete', methods = ['GET', 'POST'])
def delete():
    name = ''
    info = DeleteForm()

    if info.validate_on_submit():
        name = info.name.data

        status = dbconn.delete(name)
        success = check(status)
    else:
        success = check(-1)


    return render_template('delete.html', form = info, name = name, success = success)


def check(status):
    if status == 0:
        success = '成功'
    else:
        success = '失败'

    return success


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8081)
