from flask_restful import Api
from flask import Flask
from functions.frontend_functions.add_user import AddUser
from functions.frontend_functions.login_user import LoginUser
from functions.verify_func.verify_main import VoiceVerification
from functions.upload_array_function.upload_array_main import VoiceArrayUploader
from functions.generate_image_function.generate_image_function import VoiceImageGenerator
from helpers.helpers import VoiceVerificationTest, GetTextPhrase, VoiceFileUpload

app_main = Flask(__name__)
api = Api(app_main)

# REST test endpoint
api.add_resource(VoiceVerificationTest, '/verify_voice_test')

# add new user to database
api.add_resource(AddUser, '/add_new_user/')

# login module: check if user exists in database
api.add_resource(LoginUser, '/user_login/')

# get random text phrase per user email
api.add_resource(GetTextPhrase, '/get_text_phrase/<string:user_email>')

# upload wave file to server
api.add_resource(VoiceFileUpload, '/upload_voicefile/<string:filename>')

# upload from back-end server to database
api.add_resource(VoiceArrayUploader,
                 '/array_upload/<int:merchant_id>/<int:user_id>/<int:text_id>/<string:local_filename>')

# verify voice entry point
api.add_resource(VoiceVerification, '/verify_voice/<string:user_email>/<int:text_id>/<string:filename>')

# generate voice images from arrays on the server
api.add_resource(VoiceImageGenerator, '/image_generator/<string:user_email>/<int:text_id>')

if __name__ == '__main__':
    app_main.run(host='0.0.0.0', port=5500, debug=True)
