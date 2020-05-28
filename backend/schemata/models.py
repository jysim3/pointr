from app import api

authModel = api.parser().add_argument('Authorization', help="Authorization Token in the form '<AUTH_TOKEN>'",location='headers', required=True)

offsetModel = api.parser()
offsetModel.add_argument('days', help='Number of days to search', default="0")
offsetModel.add_argument('offset', help='Start day. today=0.')