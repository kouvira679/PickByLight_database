import sqlite3

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

class LoginManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_user_by_username(self, username):
        # Query the database for username and return a User if the username exists, and None otherwise
        with sqlite3.connect(self.db_path) as conn:
            sql = "SELECT * FROM users WHERE username = ?"
            cur = conn.execute(sql, (username,))
            row = cur.fetchone() # Row comes in as a tuple (or None)
            if row is not None:
                # Map the user details to an instance of User
                user = User(row[0], row[1], row[2])
                return user
            return None

    def verify_credentials(self, username, password):
        user = self.get_user_by_username(username)
        if user is not None:
            if user.password == password:
                return user
        return None

    def add_user(self, username, password):
        if self.get_user_by_username(username) is None:
            with sqlite3.connect(self.db_path) as conn:
                sql = "INSERT INTO users (username, password) VALUES (?, ?)"
                cur = conn.execute(sql, (username, password))
                conn.commit()
            return True
        else:
            return None

    def update_password(self, username, password, new_password):
        # Verify username and password are correct
        if self.verify_credentials(username, password) is not None:
            with sqlite3.connect(self.db_path) as conn:
                sql = "UPDATE users SET password = ? WHERE username = ?"
                cur = conn.execute(sql, (new_password, username))
                conn.commit()
            return True
        else:
            return None
