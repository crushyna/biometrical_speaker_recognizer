import sqlite3
import requests


class UserModel:
    '''
    def __init__(self, user_id, image_file, image_id, text_id, text_phrase):
        self.user_id = user_id
        self.image_file = image_file
        self.image_id = image_id
        self.text_id = text_id
        self.text_phrase = text_phrase
        self.user_hash = hash(self.user_id * self.image_id * self.text_id)
    '''

    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

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
    def _retrieve_user_data(user_id, text_id):
        connection = sqlite3.connect('users_data.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        search_for_user = "SELECT * FROM temp_users WHERE user_id = ? AND text_id = ?"
        cursor.execute(search_for_user, (user_id, text_id))
        result = [dict(row) for row in cursor.fetchall()]

        connection.commit()
        connection.close()

        return result

    @staticmethod
    def _retrieve_user_data_2(user_id):
        url = f"https://dbapi.pl/user/byId/{user_id}"
        response = requests.request("GET", url).json()

        return response['data']

    @staticmethod
    def retrieve_user_data_3(user_email, text_id, filename):
        from json import JSONDecodeError
        new_user_data_dict: dict
        url = f"https://dbapi.pl/texts/byEmail/100000/{user_email}"
        try:
            response = requests.request("GET", url).json()
        except JSONDecodeError:
            return {'message': 'User data not found!',
                    'status': 'error'}
        user_id = response['data']['userId']
        for each_text_data in response['data']['texts']:
            if each_text_data['textId'] == text_id:
                new_user_data_dict = {'user_id': user_id,
                                      'image_file': each_text_data['imageFile'],
                                      'image_id': each_text_data['imageId'],
                                      'text_id': each_text_data['textId'],
                                      'text_phrase': each_text_data['phrase'],
                                      }
        '''
        user_data_dict = {'user_id': user_id,
                          'image_file': response['data']['texts'][text_id]['imageFile'],
                          'image_id': response['data']['texts'][text_id]['imageId'],
                          'text_id': response['data']['texts'][text_id]['textId'],
                          'text_phrase': response['data']['texts'][text_id]['phrase'],
                          }
        '''

        return new_user_data_dict

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
