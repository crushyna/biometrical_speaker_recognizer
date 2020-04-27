import os
from flask_restful import Api
from flask import Flask
from functions.verify_func.verify_main import VoiceVerification, VoiceFileUpload
from helpers.helpers import VoiceVerificationTest, GetTextPhrase
from models.user_model import UserModel

app_main = Flask(__name__)
api = Api(app_main)
'''
UPLOAD_DIRECTORY = 'code/functions/verify_func/temp_voicefiles'
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)
'''

api.add_resource(VoiceVerificationTest, '/verify_voice_test')
api.add_resource(GetTextPhrase, '/get_text_phrase/<string:user_email>')
api.add_resource(VoiceFileUpload, '/upload_voicefile/<string:filename>')
api.add_resource(VoiceVerification, '/verify_voice/<int:user_id>/<int:text_id>/<string:filename>')


# api.add_resource(VoiceVerification, '/_old_verify_voice/<string:user_email>/<string:filename>/<int:text_id>')
# api.add_resource(VoiceArrayUploader, '/array_upload/<int:user_id>/<string:filename>/<int:text_id>')
# api.add_resource(VoiceImageGenerator, '/image_generator/<int:user_id>/<int:text_id>')

if __name__ == '__main__':
    # UserModel.create_table_for_users()
    app_main.run(host='0.0.0.0', port=5500, debug=True)