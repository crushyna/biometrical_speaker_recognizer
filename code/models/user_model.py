class InitialUserModel:

    def __init__(self, image_file: str, image_id: int, text_phrase: str, text_id: int, user_id: int):
        self.user_id = user_id
        self.image_file = image_file
        self.image_id = image_id
        self.text_id = text_id
        self.text_phrase = text_phrase

"""
class FullUserModel(InitialUserModel):

    def __init__(self, us_custom_login: str, us_email: str, us_id: int, us_image_file: str, us_image_id: int,
                 us_text_id: int, image_file: str, image_id: int, text_phrase: str, text_id: int, user_id: int):
        super().__init__(image_file, image_id, text_phrase, text_id, user_id, us_email)
        self.us_custom_login = us_custom_login
        self.us_email = us_email
        self.us_id = us_id
        self.us_image_file = us_image_file
        self.us_image_id = us_image_id
        self.us_text_id = us_text_id
"""
