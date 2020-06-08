from flask_restful import Resource, reqparse
from models.user_model import UserModel


class LoginUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('merchant_id',
                        type=int,
                        required=True,
                        help="Missing merchant_id in request!"
                        )
    parser.add_argument('user_email',
                        type=str,
                        required=True,
                        help="Missing user_email in request!!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Missing password in request!!"
                        )

    def post(self):
        """
        check is user has an account in application (check if user / password is correct)
        user data needs to be included in request BODY
        :return: message, status and status code
        """
        data = LoginUser.parser.parse_args()
        response = UserModel.retrieve_logging_user_data(**data)

        if response:
            return {
                       "message": "Authorized",
                       "status": "success"
                   }, 200
        else:
            return {
                       "message": "Unauthorized!",
                       "error": response,
                       "status": "error"
                   }, 401
