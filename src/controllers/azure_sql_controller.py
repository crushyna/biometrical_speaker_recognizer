import pyodbc


class SQLController:

    def __init__(self):
        self.server = 'neptun04.database.windows.net'
        self.database = 'v_biometrics_database '
        self.username = 'crushyna'
        self.password = 'AllsoP1234administrator'
        # self.driver = '{FreeTDS}'
        self.driver = '{ODBC Driver 17 for SQL Server}'
        # self.driver_version = '7.4'
        '''
        self.cnxn = pyodbc.connect(
            'DRIVER={0};SERVER={1};PORT=1433;DATABASE={2};UID={3};PWD={4};TDS_Version={5};'.format(self.driver, self.server,
                                                                                  self.database, self.username,
                                                                               self.password, self.driver_version)) '''
        self.cnxn = pyodbc.connect(
            'DRIVER={0};SERVER={1};PORT=1433;DATABASE={2};UID={3};PWD={4};'.format(
                self.driver, self.server, self.database, self.username, self.password))
        self.cursor = self.cnxn.cursor()

    def execute_update_or_insert(self, query_string: str):
        self.cursor.execute(query_string)
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
        query_list = []
        self.cursor.execute(query_string)
        row = self.cursor.fetchone()
        while row:
            for each_row in row:
                query_list.append(each_row)
                # print(each_row)

            row = self.cursor.fetchone()

        return query_list

    @staticmethod
    def test_query():
        query = f"""SELECT id FROM [dbo].[Users]"""
        result = sql_database.execute_select(query)
        print(f"Result: {result}")

        return result

    @staticmethod
    def check_if_user_exist(user_login: str):
        """
        checks if user exists in database, returns its user ID and voice image ID (int)
        :param user_login:
        :return: object
        """
        query = f"""SELECT id, voice_image_id FROM [dbo].[Users]
                            WHERE login = '{user_login}';"""
        result = sql_database.execute_query_multiple_rows(query)
        print(f"User ID: {result[0]}")
        print(f"Voice ID: {result[1]}")

        try:
            if type(result[0]) and type(result[1]) is int:
                return result[0], result[1]
        except IndexError:
            raise IndexError('Error! User does not exist in database!')

    @staticmethod
    def check_if_voice_image_exists(users_voice_image_id: int):
        query = f"""SELECT voice_array FROM [dbo].[Voice_Images]
                            WHERE id = {users_voice_image_id};"""
        voice_image_array = sql_database.execute_select(query)
        print(voice_image_array)
        print(type(voice_image_array))
        return voice_image_array

    @staticmethod
    def upload_voice_array(user_id, voice_ndarray):
        query = f"""INSERT INTO [dbo].[Voice_Arrays_List] (user_id, sample_array)
                    VALUES ({user_id}, '{voice_ndarray}');"""
        try:
            sql_database.execute_update_or_insert(query)
            print(f'Added voice array for user ID: {user_id}')
            return 1
        except pyodbc.ProgrammingError:
            raise pyodbc.ProgrammingError("Something went wrong while executing INSERT statement. Maybe inappropriate "
                                          "data types?")

    @staticmethod
    def download_voice_array(user_id):
        query = f"""SELECT TOP 1 sample_array FROM [dbo].[Voice_Arrays_List]
                        WHERE user_id = {user_id}
                        ORDER BY create_timestamp DESC;"""
        result = sql_database.execute_select(query)

        print(*result)
        print(type(result))
        return result


sql_database = SQLController()
