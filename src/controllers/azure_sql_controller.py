import pyodbc
from pickle import dumps, loads
from numpy import asarray, ndarray

# TODO: this class needs unit tests!
class SQLController:

    def __init__(self):
        self.server = 'neptun04.database.windows.net'
        self.database = 'v_biometrics_database'
        self.username = 'crushyna'
        self.password = 'AllsoP1234administrator'
        # self.driver = '{FreeTDS}'
        self.driver = '{ODBC Driver 17 for SQL Server}'
        # self.driver_version = '7.4'
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
        self.cursor.execute(query_string, values[0], values[1])
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
                # print(each_row)

            row = self.cursor.fetchone()

        return result_list

    @staticmethod
    def test_connection_query():
        query = f"""SELECT TOP 1 id FROM [dbo].[Users]"""
        result = sql_database.execute_select(query)
        print(f"Result: {result}")

        return result

    @staticmethod
    def get_user_login_and_voice_image_id(user_id: int):
        """
        simple function to return users login
        :param user_id: int
        :return: str, int
        """
        query = f"""SELECT [login], [voice_image_id]
                            FROM [dbo].[Users]
                            WHERE [id] = {user_id};"""
        try:
            result = sql_database.execute_query_multiple_rows(query)
            if type(result[0]) is str and type(result[1]) is int:
                return result[0], result[1]
        except IndexError:
            raise IndexError('Error! User does not exist in database!')
        except pyodbc.ProgrammingError:
            raise pyodbc.ProgrammingError('Wrong input data type!')

    @staticmethod
    def get_user_id_and_voice_image_id(user_login: str):
        """
        checks if user exists in database, returns its user ID and voice image ID (int)
        :param user_login:
        :return: object
        """
        query = f"""SELECT id, voice_image_id FROM [dbo].[Users]
                            WHERE login = '{user_login}';"""
        result = sql_database.execute_query_multiple_rows(query)

        try:
            if type(result[0]) and type(result[1]) is int:
                return result[0], result[1]
        except IndexError:
            raise IndexError('Error! User does not exist in database!')
        except pyodbc.ProgrammingError:
            raise pyodbc.ProgrammingError('Wrong input data type!')

    @staticmethod
    def upload_voice_array(user_id: int, voice_ndarray: ndarray):
        query = f"""INSERT INTO [dbo].[Voice_Arrays_List] (user_id, sample_array)
                    VALUES (?, ?);"""
        values = (user_id, dumps(voice_ndarray))
        try:
            sql_database.execute_update_or_insert_with_values(query, values)
            print(f'Added voice array for user ID: {user_id}')
            return 1
        except pyodbc.ProgrammingError:
            raise pyodbc.ProgrammingError("Something went wrong while executing INSERT statement. Maybe inappropriate "
                                          "data types?")

    @staticmethod
    def download_user_voice_arrays(user_id: int):
        """
        input specific user id, and returns and array of ndarrays for further analysis
        :param user_id:
        :return: list
        """
        query = f"""SELECT sample_array FROM [dbo].[Voice_Arrays_List]
                                    WHERE user_id = {user_id};"""
        query_result = sql_database.execute_select(query)

        result_arrays = []
        for each_value in query_result:
            result_arrays.append(loads(each_value))

        return result_arrays

    @staticmethod
    def upload_voice_image(voice_image_id: int, image_filepath):
        """
        upload into database a binary representation of Voice Image
        :param voice_image_id: int
        :param image_filepath:
        :return:
        """
        query = "INSERT INTO [dbo].[Voice_Images] (id, voice_array) VALUES (?, ?)"
        values = (voice_image_id, dumps(image_filepath))

        try:
            sql_database.execute_update_or_insert_with_values(query, values)
            print(f'Added voice image, ID: {voice_image_id}')
            print(f'{len(bytearray(image_filepath))}-byte file written.')
            return 1
        except pyodbc.ProgrammingError:
            raise pyodbc.ProgrammingError("Something went wrong while executing INSERT statement. Maybe inappropriate "
                                          "data types?")

    @staticmethod
    def download_voice_image(voice_id: int):
        """
        retrieve binary voice image by it's own ID
        :param voice_id: int
        :return: bytes
        """
        try:
            query = f"SELECT voice_array FROM [dbo].[Voice_Images] WHERE id = {voice_id}"
            retrieved_bytes = sql_database.execute_select(query)
            print(f'{len(retrieved_bytes)} bytes retrieved and written to memory.')
            return retrieved_bytes[0]
        except IndexError:
            raise IndexError('Error! Specified image does not exist in database!')
        except pyodbc.ProgrammingError:
            raise pyodbc.ProgrammingError('Wrong input data type!')

    @staticmethod
    def __old__check_if_voice_image_exists(users_voice_image_id: int):
        """
        check if voice image already exists in database
        :param users_voice_image_id:
        :return:
        """
        query = f"""SELECT voice_array FROM [dbo].[Voice_Images]
                            WHERE id = {users_voice_image_id};"""

        voice_image_array = sql_database.execute_select(query)
        return voice_image_array

    @staticmethod
    def __old__download_voice_array_list(user_id: int):
        query = f"""SELECT TOP 1 sample_array FROM [dbo].[Voice_Arrays_List]
                            WHERE user_id = {user_id}
                            ORDER BY create_timestamp DESC;"""
        query_result = sql_database.execute_select(query)
        result = query_result[0].strip('[]\",').split()

        result_array = []
        for each_element in result:
            result_array.append(float(each_element.strip(',')))

        return asarray(result_array)

    @staticmethod
    def __old__download_one_voice_array(user_id: int):
        """
        test purposes only
        :param user_id:
        :return: ndarray
        """
        query = f"""SELECT TOP 1 sample_array FROM [dbo].[Voice_Arrays_List]
                        WHERE user_id = {user_id}
                        ORDER BY create_timestamp DESC;"""
        query_result = sql_database.execute_select(query)
        result = query_result[0].strip('[]\",').split()

        result_array = []
        for each_element in result:
            result_array.append(float(each_element.strip(',')))

        return asarray(result_array)


sql_database = SQLController()
