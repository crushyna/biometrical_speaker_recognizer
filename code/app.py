from flask_restful import Api
from flask import Flask
from functions.verify_func.verify_main import VoiceVerificationTest, GetTextPhrase, VoiceVerification

app_main = Flask(__name__)
api = Api(app_main)

api.add_resource(VoiceVerificationTest, '/verify_voice_test')
api.add_resource(GetTextPhrase, '/get_text_phrase/<string:user_email>')
api.add_resource(VoiceVerification, '/verify_voice/<int:user_id>/<int:text_id>')

# api.add_resource(VoiceVerification, '/_old_verify_voice/<string:user_email>/<string:filename>/<int:text_id>')
# api.add_resource(VoiceArrayUploader, '/array_upload/<int:user_id>/<string:filename>/<int:text_id>')
# api.add_resource(VoiceImageGenerator, '/image_generator/<int:user_id>/<int:text_id>')

if __name__ == '__main__':
    app_main.run(port=5500, debug=True)