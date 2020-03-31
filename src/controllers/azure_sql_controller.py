from pickle import dumps, loads
import pyodbc
from numpy import asarray, ndarray

# errors:
err_no_user = "Error! User does not exist in database!"
err_wrong_input = "Wrong input data type!"
err_wrong_input_insert = "Something went wrong while executing INSERT statement. Maybe inappropriate data types?"


# TODO: this class needs unit tests!
class SQLController:

    def __init__(self):
        self.server = 'neptun04.database.windows.net'
        self.database = 'v_biometrics_database'
        self.username = 'crushyna'
        self.password = 'AllsoP1234administrator'
        self.driver = '{ODBC Driver 17 for SQL Server}'
        '''self.cnxn = pyodbc.connect( 'DRIVER={0};SERVER={1};PORT=1433;DATABASE={2};UID={3};PWD={4};TDS_Version={
        5};'Trusted_Connection=YES';'.format(self.driver, self.server,self.database, self.username,self.password, 
        self.driver_version)) '''
        self.cnxn = pyodbc.connect(
            'DRIVER={0};SERVER={1};PORT=1433;DATABASE={2};UID={3};PWD={4};'.format(
                self.driver, self.server, self.database, self.username, self.password))
        self.cursor = self.cnxn.cursor()

    def execute_update_or_insert(self, query_string: str):
        self.cursor.execute(query_string)
        self.cnxn.commit()

        print("Affected rows = {}".format(self.cursor.rowcount))

    def execute_update_or_insert_with_values(self, query_string: str, values: tuple):
        self.cursor.execute(query_string, [i for i in values])
        self.cnxn.commit()

        print("Affected rows = {}".format(self.cursor.rowcount))

    def execute_select(self, query_string: str):
        self.cursor.execute(query_string)
        row = self.cursor.fetchall()
        result = []
        for each_row in row:
            result.append(each_row[0])

        return result

    def execute_query_multiple_rows(self, query_string: str):
        result_list = []
        self.cursor.execute(query_string)
        row = self.cursor.fetchone()
        while row:
            for each_row in row:
                result_list.append(each_row)

            row = self.cursor.fetchone()

        return result_list

    @staticmethod
    def test_connection_query():
        query = f"""SELECT TOP 1 id FROM [dbo].[Users]"""
        result = default_sql_database.execute_select(query)
        print(f"Result: {result}")

        return result[0]

    @staticmethod
    def get_user_login_and_voice_id(user_id: int):
        """
        simple function to return users login
        :param user_id: int
        :return: str, int
        """
        query = f"""SELECT [login], [voice_id]
                            FROM [dbo].[Users]
                            WHERE [id] = {user_id};"""
        try:
            result = default_sql_database.execute_query_multiple_rows(query)
            if type(result[0]) is str and type(result[1]) is int:
                return result[0], result[1]

        except IndexError:
            raise IndexError(err_no_user)
        except pyodbc.ProgrammingError:
            raise ValueError(err_wrong_input)

    @staticmethod
    def get_user_id_and_voice_id(user_login: str):
        """
        checks if user exists in database, returns its user ID and voice image ID (int)
        :param user_login:
        :return: object
        """
        query = f"""SELECT id, voice_id FROM [dbo].[Users]
                            WHERE login = '{user_login}';"""
        result = default_sql_database.execute_query_multiple_rows(query)

        try:
            if type(result[0]) and type(result[1]) is int:
                return result[0], result[1]
        except IndexError:
            raise IndexError(err_no_user)
        except pyodbc.ProgrammingError:
            raise ValueError(err_wrong_input)

    @staticmethod
    def upload_voice_array(user_id: int, voice_ndarray: ndarray, text_id: int):
        query = f"""INSERT INTO [dbo].[Voice_Arrays_List] (user_id, sample_array, text_id)
                    VALUES (?, ?, ?);"""
        values = (user_id, dumps(voice_ndarray), text_id)
        try:
            default_sql_database.execute_update_or_insert_with_values(query, values)
            print(f'Added voice array for user ID: {user_id}, text ID: {text_id}')
            return 1

        except IndexError:
            raise IndexError(err_no_user)
        except pyodbc.ProgrammingError:
            raise ValueError(err_wrong_input_insert)

    @staticmethod
    def download_user_voice_arrays(user_id: int, text_id: int):
        """
        input specific user id, and returns and array of ndarrays for further analysis
        :param text_id:
        :param user_id:
        :return: list
        """
        query = f"""SELECT sample_array FROM [dbo].[Voice_Arrays_List]
                                    WHERE user_id = {user_id} AND text_id = {text_id};"""
        query_result = default_sql_database.execute_select(query)

        result_arrays = []
        for each_value in query_result:
            result_arrays.append(loads(each_value))

        return result_arrays

    @staticmethod
    def update_voice_image_link(voice_id: int, text_id: int):
        """
        update Voice Image Link
        :param voice_id: int
        :param text_id: int
        :return: voice_image_id int
        """
        query1 = "INSERT INTO [dbo].[Voice_Image_Link] (voice_id, text_id) VALUES (?, ?)"
        values1 = (voice_id, text_id)
        try:
            default_sql_database.execute_update_or_insert_with_values(query1, values1)
            print(f'Updated Voice Image Link, for Voice ID: {voice_id}, Text ID: {text_id}')
        except pyodbc.ProgrammingError as er:
            raise pyodbc.ProgrammingError(er)

        query2 = f"SELECT [image_id] FROM [dbo].[Voice_Image_Link] WHERE [voice_id] = {voice_id} AND [text_id] = {text_id}"
        try:
            voice_image_id = default_sql_database.execute_select(query2)
        except pyodbc.ProgrammingError as er:
            raise pyodbc.ProgrammingError(er)

        return voice_image_id[0]

    @staticmethod
    def upload_voice_image(voice_image_id: int, image_array: ndarray):
        """
        upload into database a binary representation of Voice Image
        :param image_array:
        :param voice_image_id: int
        :return:
        """
        query = "INSERT INTO [dbo].[Voice_Images] (id, voice_array) VALUES (?, ?)"
        values = (voice_image_id, dumps(image_array))

        try:
            default_sql_database.execute_update_or_insert_with_values(query, values)
            print(f'Added voice image, ID: {voice_image_id}')
            print(f'{len(bytearray(image_array))}-byte file written.')
            return 1

        except pyodbc.ProgrammingError:
            raise ValueError(err_wrong_input_insert)
        except pyodbc.IntegrityError:
            raise LookupError("Voice image for this user already exists!")

    @staticmethod
    def get_image_voice_id(voice_id: int, text_id: int):
        query = f"SELECT [image_id] FROM [dbo].[Voice_Image_Link] WHERE [voice_id] = {voice_id} AND [text_id] = {text_id}"
        try:
            voice_image_id = default_sql_database.execute_select(query)
        except pyodbc.ProgrammingError as er:
            raise pyodbc.ProgrammingError(er)

        return voice_image_id[0]

    @staticmethod
    def download_voice_image(voice_id: int):
        """
        retrieve binary voice image by it's own ID
        :param voice_id: int
        :return: bytes
        """
        try:
            query = f"SELECT voice_array FROM [dbo].[Voice_Images] WHERE id = {voice_id}"
            retrieved_bytes = default_sql_database.execute_select(query)

            print(f'{len(retrieved_bytes[0])} bytes retrieved from database, ID = {voice_id}.')
            print(f'Retrieved data: {loads(retrieved_bytes[0])}')

            return loads(retrieved_bytes[0])

        except IndexError:
            raise IndexError("Error! Specified image does not exist in database!")
        except pyodbc.ProgrammingError:
            raise ValueError(err_wrong_input)


default_sql_database = SQLController()
