from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import (
    ValidationError,
    DataRequired,
    URL,
    Regexp,
    Length,
)
from app.models import Site


class AddSiteForm(FlaskForm):
    url = StringField(
        "url",
        validators=[
            URL(message="Please enter a valid URL (https://example.com)"),
            DataRequired(),
        ],
    )
    alias = StringField(
        "alias",
        validators=[
            DataRequired(),
            Regexp(
                "^[a-zA-Z0123456789\\-_.~]*$", message="Invalid characters"
            ),
            Length(min=1, max=200),
        ],
    )
    submit = SubmitField("Add Alias")

    def validate_alias(self, alias):
        site = Site.query.filter(Site.alias.ilike(self.alias.data)).first()
        if self.alias.data.lower() == "add" or site is not None:
            raise ValidationError("Please use a different alias.")
