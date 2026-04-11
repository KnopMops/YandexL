from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, Email


class DepartmentForm(FlaskForm):
    title = StringField("Title of department", validators=[DataRequired()])
    chief_id = IntegerField("Chief id", validators=[DataRequired()])
    members = StringField("Members (comma separated)", validators=[DataRequired()])
    email = StringField("Department Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Submit")
