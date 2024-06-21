from flask import Flask, render_template, redirect, url_for, request,session
import sqlite3


app = Flask("__main__")
app.secret_key = 'your_secret_key'

genres = ["Romance", "Drama", "Comedy", "Detective", "Recommended"]
genre_images = {
    'Romance': 'notebook.jpg',
    'Drama': 'damien.jpg',
    'Comedy': 'smiths.jpg',
    'Detective': 'shvidi.jpg',
    'Recommended': 'xuti.jpg'
}

users = {
    'username': 'password'
}



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users[username] = password  # Store in memory (replace with database logic)

        # Redirect to login page after signup
        return redirect(url_for('login'))

    return render_template('signup.html')

# Login route and form handling
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username exists and passwords match
        if username in users and users[username] == password:
            session['username'] = username  # Store username in session
            return redirect(url_for('home'))  # Redirect to home page or dashboard

        # Add error handling or redirect back to login with a message
        return redirect(url_for('login'))

    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('login'))
@app.route('/')
def home():
    default_genre = 'Romance'

    image_file = genre_images.get(default_genre, 'static/gaiqca.jpg')
    return render_template("home.html", genres=genres, active_genre=default_genre, image_file=image_file)

@app.route('/genres/<genre>')
def genre(genre):
    image_file = genre_images.get(genre, 'static/gaiqca.jpg')
    return render_template("home.html", genres=genres, active_genre=genre, image_file=image_file)

@app.route("/add")
def add():
    return render_template("cinephile.html")


@app.route("/addrec", methods=['POST', 'GET'])
def addrec():
    global msg
    if request.method == 'POST':
        try:
            nickname = request.form['nickname']
            fav_movie = request.form['fav movie']
            country = request.form['country']
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO members (nickname, fav_movie, country) VALUES (?,?,?,?)",
                            (nickname, fav_movie, country,))

                con.commit()
                msg = "Record successfully added to database"
        except:
            con.rollback()
            msg = "Error in the INSERT"

        finally:
            con.close()
            return render_template('result.html', msg=msg)

@app.route('/list')
def list():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT rowid, * FROM members")

    rows = cur.fetchall()
    con.close()
    return render_template("list.html",rows=rows)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
@app.route('/')
def list_students():
    conn = get_db_connection()
    cursor = conn.execute('SELECT rowid, name, fav_movie, country FROM students')
    students = cursor.fetchall()
    conn.close()
    return render_template('list.html', rows=students)




@app.route("/edit", methods=['POST','GET'])
def edit():
    if request.method == 'POST':
        try:
            # Use the hidden input value of id from the form to get the rowid
            id = request.form['id']
            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("SELECT rowid, * FROM students WHERE rowid = " + id)

            rows = cur.fetchall()
        except:
            id=None
        finally:
            con.close()
            # Send the specific record of data to edit.html
            return render_template("edit.html",rows=rows)

# Route used to execute the UPDATE statement on a specific record in the database
@app.route("/editrec", methods=['POST','GET'])
def editrec():
    # Data will be available from POST submitted by the form
    global nm
    if request.method == 'POST':
        try:
            # Use the hidden input value of id from the form to get the rowid
            rowid = request.form['rowid']
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            zip = request.form['zip']

            # UPDATE a specific record in the database based on the rowid
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("UPDATE students SET name='"+nm+"', addr='"+addr+"', city='"+city+"', zip='"+zip+"' WHERE rowid="+rowid)

                con.commit()
                msg = "Record successfully edited in the database"
        except:
            con.rollback()
            msg = "Error in the Edit: UPDATE students SET name="+nm+", addr="+addr+", city="+city+", zip="+zip+" WHERE rowid="+rowid

        finally:
            con.close()
            # Send the transaction message to result.html
            return render_template('result.html',msg=msg)

@app.route("/delete", methods=['POST','GET'])
def delete():
    if request.method == 'POST':
        try:
             # Use the hidden input value of id from the form to get the rowid
            rowid = request.form['id']
            # Connect to the database and DELETE a specific record based on rowid
            with sqlite3.connect('database.db') as con:
                    cur = con.cursor()
                    cur.execute("DELETE FROM students WHERE rowid="+rowid)

                    con.commit()
                    msg = "Record successfully deleted from the database"
        except:
            con.rollback()
            msg = "Error in the DELETE"

        finally:
            con.close()
            # Send the transaction message to result.html
            return render_template('result.html',msg=msg)


if __name__ == "__main__":
    app.run(debug=True)
