from flask.ext.wtf import Form
from wtforms.fields import SubmitField, SelectField, RadioField
from wtforms.validators import Required

class SurveyForm(Form):
    time_drop = SelectField("When")
    swb_radio = RadioField("Choose")
    submit = SubmitField("Send")
