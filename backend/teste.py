import sqlite3

def teste(user_email):

    connection = sqlite3.connect("backend/TrackIt.db")
    cursor = connection.cursor()

    cursor.execute("SELECT id_user FROM usuario WHERE email = ?", (user_email,))

    user = cursor.fetchone()

    return user

print(teste("juliaguerra2701@gmail.com"))