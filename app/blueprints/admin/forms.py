from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    IntegerField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp


class ProjectForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=128)])
    slug = StringField(
        "Slug",
        validators=[
            DataRequired(),
            Length(max=128),
            Regexp(
                r"^[a-z0-9-]+$",
                message="Slug may only contain lowercase letters, numbers, and hyphens.",
            ),
        ],
    )
    description = TextAreaField("Description", validators=[DataRequired()])
    tags = StringField(
        "Tags",
        validators=[Optional(), Length(max=256)],
        description="Comma-separated, e.g. Python, Flask, Bootstrap",
    )
    icon = StringField(
        "Icon class",
        validators=[Optional(), Length(max=64)],
        description="Bootstrap Icons class name, e.g. bi-code-square",
    )
    url = StringField(
        "Live URL",
        validators=[Optional(), URL(message="Enter a valid URL or leave blank.")],
    )
    repo_url = StringField(
        "Repo URL",
        validators=[Optional(), URL(message="Enter a valid URL or leave blank.")],
    )
    order = IntegerField(
        "Display order",
        default=0,
        validators=[Optional()],
        description="Lower numbers appear first.",
    )
    status = SelectField(
        "Status",
        choices=[
            ("planning",       "Planning"),
            ("in_development", "In Development"),
            ("live",           "Live"),
            ("parked",         "Parked"),
            ("archived",       "Archived"),
        ],
        default="in_development",
    )
    is_visible = BooleanField("Visible on portfolio", default=True)
    submit = SubmitField("Save Project")


class ProjectSectionForm(FlaskForm):
    heading = StringField(
        "Heading",
        validators=[Optional(), Length(max=128)],
        description="Optional title shown above this section.",
    )
    section_type = SelectField(
        "Type",
        choices=[
            ("text",     "Text / paragraph"),
            ("features", "Feature list"),
            ("image",    "Image"),
            ("code",     "Code snippet"),
        ],
    )
    body = TextAreaField(
        "Body",
        validators=[DataRequired()],
        description=(
            "Text: Markdown content. "
            "Feature list: one item per line. "
            "Image: the full image URL. "
            "Code: the code to display."
        ),
    )
    extra = StringField(
        "Language / Caption",
        validators=[Optional(), Length(max=128)],
        description="Code: language hint (e.g. python, javascript). Image: caption text.",
    )
    submit = SubmitField("Save Section")


class SettingsForm(FlaskForm):
    display_name = StringField(
        "Display name",
        validators=[DataRequired(), Length(max=128)],
        description="Your name as shown in the hero section.",
    )
    tagline = StringField(
        "Tagline",
        validators=[DataRequired(), Length(max=256)],
        description="One sentence shown beneath your name in the hero. Keep it punchy.",
    )
    bio = TextAreaField(
        "About / Bio",
        validators=[DataRequired()],
        description="Full bio shown in the About section. Separate paragraphs with a blank line.",
    )
    github_url = StringField(
        "GitHub URL",
        validators=[Optional(), URL(message="Enter a valid URL or leave blank.")],
    )
    linkedin_url = StringField(
        "LinkedIn URL",
        validators=[Optional(), URL(message="Enter a valid URL or leave blank.")],
    )
    twitter_url = StringField(
        "Twitter / X URL",
        validators=[Optional(), URL(message="Enter a valid URL or leave blank.")],
    )
    submit = SubmitField("Save Settings")
