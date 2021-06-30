from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields

# Create an APISpec
spec = APISpec(
    title="My App",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)


# Define schemas
class InputPortfolioSchema(Schema):
    description = fields.String(description="description")
    image_url = fields.String(description="image_url")
    twitter_user_name = fields.String(description="twitter_user_name")
    title = fields.String(description="title")
    user_id = fields.String(description="user_id")
    experience_summary = fields.String(description="experience_summary")
    last_names = fields.String(description="last_names")
    names = fields.String(description="names")
    twitter_user_id = fields.String(description="twitter_user_id")


class OutputPortfolioSchema(Schema):
    idportfolio = fields.Int(description="idportfolio")
    description = fields.String(description="description")
    image_url = fields.String(description="image_url")
    twitter_user_name = fields.String(description="twitter_user_name")
    title = fields.String(description="title")
    user_id = fields.String(description="user_id")
    experience_summary = fields.String(description="experience_summary")
    last_names = fields.String(description="last_names")
    names = fields.String(description="names")
    twitter_user_id = fields.String(description="twitter_user_id")


class OutputPortfolioListSchema(Schema):
    content = fields.List(fields.Nested(OutputPortfolioSchema))


class OutputTweetSchema(Schema):
    text = fields.String(description="Tweet text")


class OutputTweetListSchema(Schema):
    content = fields.List(fields.Nested(OutputTweetSchema))


# register schemas with spec
spec.components.schema("OutputPortfolioSchema", schema=OutputPortfolioSchema)
spec.components.schema("OutputPortfolioListSchema", schema=OutputPortfolioListSchema)
spec.components.schema("OutputTweetListSchema", schema=OutputTweetListSchema)
spec.components.schema("InputPortfolioSchema", schema=InputPortfolioSchema)

# add swagger tags that are used for endpoint annotation
tags = [
    {'name': 'portfolio',
     'description': 'Portfolio services endpoints'
     },
]

for tag in tags:
    spec.tag(tag)
