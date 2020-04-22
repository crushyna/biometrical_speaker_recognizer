from flask_restful import Resource, Api, reqparse
from flask import Flask
from verify_func.verify_main import VoiceVerification, VoiceVerificationTest, GetTextPhrase
from upload_array_function.upload_array_main import VoiceArrayUploader
from generate_image_function.generate_image_function import VoiceImageGenerator

app_main = Flask(__name__)
api = Api(app_main)

api.add_resource(VoiceVerificationTest, '/verify_voice_test')
api.add_resource(GetTextPhrase, '/get_text_phrase/<string:user_email>')
# api.add_resource(VoiceVerification, '/verify_voice/<string:user_login>/<string:filename>/<int:text_id>')
# api.add_resource(VoiceArrayUploader, '/array_upload/<int:user_id>/<string:filename>/<int:text_id>')
# api.add_resource(VoiceImageGenerator, '/image_generator/<int:user_id>/<int:text_id>')

app_main.run(port=5500, debug=True)

if __name__ == '__main__':
    app_main.run(port=5000, debug=True)