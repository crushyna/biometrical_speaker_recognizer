from flask_restful import Api
from flask import Flask
from functions.verify_func.verify_main import VoiceVerification, VoiceFileUpload
from functions.upload_array_function.upload_array_main import VoiceArrayUploader
from helpers.helpers import VoiceVerificationTest, GetTextPhrase
from models.user_model import UserModel

app_main = Flask(__name__)
api = Api(app_main)

api.add_resource(VoiceVerificationTest, '/verify_voice_test')
api.add_resource(GetTextPhrase, '/get_text_phrase/<string:user_email>')
api.add_resource(VoiceFileUpload, '/upload_voicefile/<string:filename>')
api.add_resource(VoiceArrayUploader, '/array_upload/<int:merchant_id>/<int:user_id>/<int:text_id>/<string:filename>')
api.add_resource(VoiceVerification, '/verify_voice/<string:user_email>/<int:text_id>/<string:filename>')


# api.add_resource(VoiceVerification, '/_old_verify_voice/<string:user_email>/<string:filename>/<int:text_id>')

# api.add_resource(VoiceImageGenerator, '/image_generator/<int:user_id>/<int:text_id>')

if __name__ == '__main__':
    app_main.run(host='0.0.0.0', port=5500, debug=True)