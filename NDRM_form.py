from wtforms import Form, StringField, SelectField


class ResearchSearchForm(Form):
    choices = [('Topic', 'Topic'),
               ('Author', 'Author')]
    select = SelectField('Search for Research:', choices=choices)
    search = StringField('')