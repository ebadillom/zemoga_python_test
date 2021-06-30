import json

from flask import Blueprint, abort, jsonify, request, redirect, render_template

from database import mysql
from twitter_auth import tw_api

# blueprint setup
portfolio = Blueprint('portfolio', __name__, url_prefix='/portfolio')


@portfolio.route('/', methods=['GET'])
def get_all():
    """
    ---
    get:
      description: Get all portfolios.
      produces:
        - "application/json"
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: OutputPortfolioListSchema
      tags:
         - portfolio
    """

    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM portfolio")

    columns = cursor.description
    result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]

    return json.dumps(result)


@portfolio.route('/<int:id>', methods=['GET'])
def get_by_id(id: int):
    """
    ---
    get:
      description: Get portfolio by id.
      parameters:
        - name: "id"
          in: "path"
          description: "ID of portfolio"
          required: true
          type: "integer"
          format: "int64"
      produces:
        - application/json
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: OutputPortfolioSchema
      tags:
         - portfolio
    """

    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM portfolio WHERE idportfolio = %s", (id,))
    rows = cursor.fetchall()

    if len(rows) == 0:
        abort(404)

    columns = cursor.description
    result = [{columns[index][0]: column for index, column in enumerate(value)} for value in rows]

    return json.dumps(result[0])


@portfolio.route('/<int:id>/tweets', methods=['GET'])
def get_tweets(id: int):
    """
    ---
    get:
      description: Get tweets by portfolio id.
      produces:
        - application/json
      parameters:
        - name: "id"
          in: "path"
          description: "ID of portfolio"
          required: true
          type: "integer"
          format: "int64"
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: OutputTweetListSchema
      tags:
          - portfolio
    """

    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM portfolio WHERE idportfolio = %s", (id,))
    rows = cursor.fetchall()

    if len(rows) == 0:
        abort(404)

    tweets = []
    try:
        statuses = tw_api.GetUserTimeline(screen_name=rows[0][3], count=5)
        tweets = [{"text": tweet.text} for tweet in statuses]
    except:
        print("Error getting tweets")

    return jsonify(tweets)


@portfolio.route('/<int:id>', methods=['PUT'])
def put_portfolio(id: int):
    """
    ---
    put:
      description: Update an existing portfolio.
      consumes:
        - application/json
      produces:
        - application/json
      parameters:
        - name: "id"
          in: "path"
          description: "ID of portfolio that needs to be updated"
          required: true
          type: "integer"
          format: "int64"
      requestBody:
        required: true
        content:
            application/json:
                schema: InputPortfolioSchema
      responses:
        '200':
          description: call successful
          content:
            application/json:
              schema: OutputPortfolioSchema
      tags:
          - portfolio
    """

    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM portfolio WHERE idportfolio = %s", (id,))
    rows = cursor.fetchall()

    if len(rows) == 0:
        abort(404)

    if not request.json:
        abort(400, description='Payload is mandatory')

    sql = "UPDATE portfolio SET " \
          "description = %s, " \
          "image_url = %s, " \
          "twitter_user_name = %s, " \
          "title = %s, " \
          "user_id = %s, " \
          "experience_summary = %s, " \
          "last_names = %s, " \
          "names = %s, " \
          "twitter_user_id = %s " \
          "WHERE idportfolio = %s"

    val = (request.json['description'],
           request.json['image_url'],
           request.json['twitter_user_name'],
           request.json['title'],
           request.json['user_id'],
           request.json['experience_summary'],
           request.json['last_names'],
           request.json['names'],
           request.json['twitter_user_id'],
           id)

    cursor = mysql.get_db().cursor()
    cursor.execute(sql, val)
    mysql.get_db().commit()

    return redirect("/portfolio/{}".format(id))


@portfolio.route('/<int:id>/profile', methods=['GET'])
def profile(id: int):
    """
    ---
    get:
      description: Get profile page by portfolio id.
      produces:
        - text/html
      parameters:
        - name: "id"
          in: "path"
          description: "ID of portfolio"
          required: true
          type: "integer"
          format: "int64"
      responses:
        '200':
          description: call successful
      tags:
          - portfolio
    """

    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM portfolio WHERE idportfolio = %s", (id,))
    rows = cursor.fetchall()

    columns = cursor.description
    result = [{columns[index][0]: column for index, column in enumerate(value)} for value in rows][0]

    tweets = []
    try:
        statuses = tw_api.GetUserTimeline(screen_name=result['twitter_user_name'], count=5)
        tweets = [{"text": tweet.text} for tweet in statuses]
    except:
        print("Error getting tweets")

    result['tweets'] = tweets

    return render_template('profile.html', profile=result)
