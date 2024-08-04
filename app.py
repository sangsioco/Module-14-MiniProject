from flask import Flask
from flask_graphql import GraphQLView
import graphene
from mutations.main import Mutation
from querries.main import Query
from database import db

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    db.init_app(app)

    schema = graphene.Schema(query=Query, mutation=Mutation)

    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
    )

    with app.app_context():
        # db.drop_all()
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app('DevelopmentConfig')
    app.run(debug=True)
