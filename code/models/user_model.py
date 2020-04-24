import sqlite3


class UserModel:
    def __init__(self, user_id, image_file, image_id, text_id, text_phrase):
        self.user_id = user_id
        self.image_file = image_file
        self.image_id = image_id
        self.text_id = text_id
        self.text_phrase = text_phrase
        self.user_hash = hash(self.user_id + self.image_id + self.text_id)

    """
    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])
    """

    def return_all_attributes(self):
        return self.__dict__

    @staticmethod
    def create_table_for_users():
        connection = sqlite3.connect('users_data.db')
        cursor = connection.cursor()

        create_table = "CREATE TABLE IF NOT EXISTS temp_users (user_id int, image_file text, image_id int, text_id int, text_phrase text, hash_int int)"
        cursor.execute(create_table)
        connection.commit()
        connection.close()

    @staticmethod
    def retrieve_user_data(user_id, text_id):
        connection = sqlite3.connect('users_data.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        search_for_user = "SELECT * FROM temp_users WHERE user_id = ? AND text_id = ?"
        cursor.execute(search_for_user, (user_id, text_id))
        result = [dict(row) for row in cursor.fetchall()]

        connection.commit()
        connection.close()

        return result

    def save_user_to_database(self):
        connection = sqlite3.connect('users_data.db')
        cursor = connection.cursor()

        search_for_user = "SELECT * FROM temp_users WHERE hash_int = ?"
        cursor.execute(search_for_user, (self.user_hash,))
        data = cursor.fetchone()
        if data is None:
            new_user = "INSERT INTO temp_users VALUES (?, ?, ?, ?, ?, ?)"
            cursor.execute(new_user,
                           (self.user_id, self.image_file, self.image_id, self.text_id, self.text_phrase,
                            self.user_hash))
            connection.commit()
            connection.close()
        else:
            connection.commit()
            connection.close()
            return {'message': 'User already exists in temporary database!'}
