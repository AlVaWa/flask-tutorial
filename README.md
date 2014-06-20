# What is this?
This is code form a short workshop I attended in EVRY. 
It contains the solution given in the workshop as well as me and my college solution.

This code has no code review, and this is my first flask/python code :)

The rest of this file is directly from the workshop.



## Hva trenger vi?
* [Python](https://www.python.org/downloads)
* [PIP](https://pip.pypa.io/en/latest/installing.html)
* [Virtualenv](http://virtualenv.readthedocs.org/en/latest)

På OSX er (sannsynligvis) Python allerede installert. På Windows må vi installere Python selv.

Når Python og PIP er installert kan vi installere virtualenv.

###### Windows:

    > \Python27\Scripts\pip.exe install virtualenv

###### *NIX/OSX:

    > pip install virtualenv

## Editor/IDE
* [Notapad++](http://notepad-plus-plus.org)
* [Sublime Text](http://www.sublimetext.com)
* [PyCharm](http://www.jetbrains.com/pycharm) (IDE)
* [Python Tools for Visual Studio](http://pytools.codeplex.com)

---
## Sette opp utviklingsmiljøet

    > cd path/to/my/projects
    > git clone https://github.com/finnchr/flask-workshop.git
    > cd flask-workshop

###### Windows:

    > \Python27\Scripts\virtualenv.exe ENV
    > ENV\Scripts\activate.bat

###### *NIX/OSX:

    > [sudo] virtualenv ENV
    > [sudo] source ENV/bin/activate

Vi har nå laget og aktivert et lokalt pythonmiljø - nå kan vi installere pakker applikasjonen trenger.

    > pip install flask
    > pip install flask-sqlalchemy

Testene bruker pakken `requests` (for å kjøre spørringer mot server) så vi må installere denne pakken også.

    > pip install requests

---
## Start applikasjonen

	> [sudo] python simple_todo_api.py

Når applikasjonen har startet skal du se dette i konsollvinduet:

    --------------------------------------------------------------------------------
    DEBUG in simple_todo_api [simple_todo_api.py:43]:
    Create database and add example data
    --------------------------------------------------------------------------------
     * Running on http://localhost:5000/
     * Restarting with reloader

Naviger til [http://localhost:5000](http://localhost:5000)

---
## Kjøre integrasjonstester mot server

	> python simple_todo_api_it.py

---
## Oppgave

Åpne filen `simple_todo_api.py`

Kun GET `/api/todos` er implementert. Implementer resten av nødvendige api-kall:

* GET `/api/todos/<id>`
* POST `/api/todos`
* PUT `/api/todos/<id>`
* DELETE `/api/todos/<id>`

#### Ekstraoppgave

Det er pt. ikke mulig å prioritere oppgaver. Legg til funksjonalitet for å prioritere oppgavene.

---
## Lynkurs i Python

    l = [1,2,3,4] # liste
    t = (1,2,3,4) # tuple
    s = ‘Hello world’
    s = ‘Hello ‘ + ‘World’
    s = ‘Hello %s’ % (‘World’)
    s = ‘Tallet er %d’ % (3)
    c = s[0] # c == ‘T’
    d = dict(a=1, b=2, c=3)
    d = {‘a’: 1, ‘b’: 2, ‘c’: 3}
    n = d[‘a’] # n == 1
    n = d.get(‘a’) # n == 1
    n = d.get(‘x’) # n == None
    n = d.get(‘x’, 0) # n == 0


    n1, n2, n3 = (1, 2, 3) # n1 == 1, n2 == 2, n3 == 3


    if 1 == 1 or 2 == 2:
       pass
    elif 1 == 2:
       pass
    else:
       pass


    while True and n < 100:
       n += 1


    for n in [1, 2, 3, 4]:
       pass


    def my_function():
       pass

    def add(a, b):
       return a + b

    def write_message(msg='Hello world'):
       print(msg)

---
## Lynkurs i Flask og Flask-Sqlalchemy

###### Hente ut todo basert på id:

    todo = db.session.query(Todo).get(id)

###### Opprette ny todo:

    todo = Todo('Lære meg Python og Flask')
    db.session.add(todo)

###### Slette todo:

    db.session.delete(todo)

###### Lagre endringer til databasen:

    db.session.commit()

##### Litt hjelp til Flask:

###### Hente ut json-dokument fra request body:

    payload = flask.request.get_json()
    text = payload.get('text', 'Default text')

###### Routing og parametre:

    @app.route('/my/path/<int:num>', methods=['GET', 'POST'])
    def handler(num):
        name = flask.request.args.get('name', 'Ola Normann')
        return 'Navnet er %s og tallet er %d' % (name, num)

Typen til path-parameteren kan være *string* (default), *int*, *float* eller *path* (tilsvarende string, men aksepterer også slash).

    @app.route('/my/path/<int:num>/<string:name>', methods=['GET', 'POST'])
    def handler(num, name):
        return 'Navnet er %s og tallet er %d' % (name, num)

---
## Dokumentasjon

* [Python v2.7.7 documentation](https://docs.python.org/2)
* [The Python Language Reference](https://docs.python.org/3/reference)
* [Flask documentation](http://flask.pocoo.org/docs)
* [Flask API](http://flask.pocoo.org/docs/api)
* [Flask quickstart](http://flask.pocoo.org/docs/quickstart)
