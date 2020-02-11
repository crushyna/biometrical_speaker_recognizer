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

    def execute_update(self, query_string: str):
        self.cursor.execute(query_string)
        self.cnxn.commit()

        print("Affected rows = {}".format(self.cursor.rowcount))

    def execute_select(self, query_string: str):
        self.cursor.execute(query_string)
        row = self.cursor.fetchall()
        result = []
        for each_row in row:
            result.append(each_row[0])

        # result = self.cursor.fetchone()
        return result

    def execute_query_multiple_rows(self, query_string: str):
        query_list = []
        self.cursor.execute(query_string)
        row = self.cursor.fetchone()
        while row:
            for each_row in row:
                query_list.append(each_row)
                print(each_row)

            row = self.cursor.fetchone()

        return query_list

    @staticmethod
    def test_query():
        query = f"""SELECT id FROM [dbo].[Users]"""
        result = sql_database.execute_select(query)
        print(f"Result: {result}")

        return result

    @staticmethod
    def switch_user_status(card_id: int, card_text: str):
        current_status = f"""SELECT [IsPresent]
                            FROM [dbo].[Persons]
                            WHERE [RfidCardId] = {card_id}
                            AND [RfidCardText] = '{card_text}';"""

        status = sql_database.execute_select(current_status)

        if status:
            query1 = f"""UPDATE [dbo].[Persons]
                        SET [IsPresent] = 'False'
                        WHERE [RfidCardId] = {card_id}
                        AND [RfidCardText] = '{card_text}';"""

            sql_database.execute_update(query1)
            print(f"{card_id}, {card_text}: IsPresent = False")

        else:
            query2 = f"""UPDATE [dbo].[Persons]
                        SET [IsPresent] = 'True'
                        WHERE [RfidCardId] = {card_id}
                        AND [RfidCardText] = '{card_text}';"""

            sql_database.execute_update(query2)
            print(f"{card_id}, {card_text}: IsPresent = True")

    @staticmethod
    def check_user_access(card_id: int, card_text: str):
        query = f"""SELECT [HasAccess] 
                    FROM [dbo].[Persons]
                    WHERE [RfidCardId] = {card_id}
                    AND [RfidCardText] = '{card_text}'"""

        result = sql_database.execute_select(query)
        print(f"HasAccess: {result}")

        return result

    # 329308361597
    # test1
    # sql_database.check_user_access(329308361597, 'test1')
    # sql_database.switch_user_status(329308361597, 'test1')


sql_database = SQLController()
# sql_database.switch_user_status(329308361597, 'test1')