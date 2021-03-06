from flask_restful import Api
from flask import Flask
from functions.frontend_functions.add_user import AddUser
from functions.frontend_functions.login_user import LoginUser
from functions.verify_func.verify_main import VoiceVerification
from functions.upload_array_function.upload_array_main import VoiceArrayUploader
from functions.generate_image_function.generate_image_function import VoiceImageGenerator
from helpers.helpers import ConnectionTest, GetTextPhrase, WaveFileUpload, CheckIfUserExists, WorkingFolders
from helpers.front_registration import GetSamplesInfoByUserId

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = WorkingFolders.upload_folder
app.config['ARRAYS_FOLDER'] = WorkingFolders.arrays_folder
app.config['IMAGES_FOLDER'] = WorkingFolders.images_folder
api = Api(app)

# REST test endpoint
api.add_resource(ConnectionTest, '/connection_test')

# add new user to database
api.add_resource(AddUser, '/add_new_user/')

# login module: check if user exists in database and create it's model
api.add_resource(LoginUser, '/user_login/')

# ONLY check, if user exists (for registration purposes)
api.add_resource(CheckIfUserExists, '/check_if_user_exists/<int:merchant_id>/<string:user_email>')

# get random text phrase per user email
api.add_resource(GetTextPhrase, '/get_text_phrase/<int:merchant_id>/<string:user_email>')

# upload wave file to server
api.add_resource(WaveFileUpload, '/upload_wavefile/<string:filename>')

# upload from back-end server to database
api.add_resource(VoiceArrayUploader,
                 '/array_upload/<int:merchant_id>/<int:user_id>/<int:text_id>/<string:local_filename>/<string:remote_filename>')

# generate voice images from arrays on the server
api.add_resource(VoiceImageGenerator, '/image_generator/<int:merchant_id>/<int:user_id>/<int:text_id>')

# verify voice entry point
api.add_resource(VoiceVerification,
                 '/verify_voice/<int:merchant_id>/<string:user_email>/<int:text_id>/<string:filename>')

### STRICTLY FOR FRONT-END REGISTRATION ###
api.add_resource(GetSamplesInfoByUserId, '/samples/info/byUserId/<int:merchant_id>/<int:user_id>')

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=80, debug=True)
    app.run(host='0.0.0.0', port=80)
