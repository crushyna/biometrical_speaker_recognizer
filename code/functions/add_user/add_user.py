from flask_restful import Resource, reqparse
from models.user_model import UserModel


class AddUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_email',
                        type=str,
                        required=True,
                        help="Missing user_email in request!"
                        )
    parser.add_argument('merchant_id',
                        type=int,
                        required=True,
                        help="Missing merchant_id in request!!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Missing password in request!"
                        )

    def post(self):
        """
        add new user to database
        user data needs to be included in request BODY
        :return:
        """
        data = AddUser.parser.parse_args()
        response = UserModel.retrieve_new_user_data(**data)
        if response.json()['error'] != 0:
            return {'message': response['message'],
                    'status': 'error'}
        else:
            return {'message': response.json(),
                    'status': 'success'}

