import requests
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
        response = UserModel.add_new_user(**data)

        if response.status_code in (200, 201):
            return {'message': response.json(),
                    'status': 'success'}
        else:
            return {'message': 'Database or connection error!',
                    'status': 'error'}
