from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument(
    "team_leader", required=True, type=int, help="Team leader id is required"
)
parser.add_argument("job", required=True, help="Job description is required")
parser.add_argument(
    "work_size", required=True, type=int, help="Work size (hours) is required"
)
parser.add_argument(
    "collaborators", required=True, help="Collaborators list is required"
)
parser.add_argument(
    "is_finished", required=True, type=bool, help="is_finished flag is required"
)
