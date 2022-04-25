from flask import Response, request
from flask_restful import Resource
from models import Post, db, Following
from views import get_authorized_user_ids

import json

def get_path():
    return request.host_url + 'api/posts/'

class PostListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user


    def get(self):  #HTTP GET
        args = request.args 
        print(args)
        # Goal: limit to only user #12 (current_user)'s network
        #   - oneself
        #   - ppl #12 are following

        #1. Query the following table to get the user_ids that #12 is following:
        # user_ids_tuples = (
        #     db.session
        #         .query(Following.following_id)
        #         .filter(Following.user_id == self.current_user.id)
        #         .order_by(Following.following_id)
        #         .all()
        #     )
        # print(user_ids_tuples)
        # user_ids = [id for (id,) in user_ids_tuples]
        # print(user_ids)
        # user_ids.append(self.current_user.id)
        user_ids = get_authorized_user_ids(self.current_user)

        limit = args.get('limit') or 10 # 10 is the default
        #posts = Post.query.limit(limit).all()
        posts = Post.query.filter(Post.user_id.in_(user_ids)).limit(limit).all()
        posts_json = [post.to_dict() for post in posts]
        return Response(json.dumps(posts_json), mimetype="application/json", status=200)

    def post(self):   #HTTP POST
        # create a new post based on the data posted in the body 
        body = request.get_json()
        print(body)  
        return Response(json.dumps({}), mimetype="application/json", status=201)
        
class PostDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
        

    def patch(self, id):
        # update post based on the data posted in the body 
        body = request.get_json()
        print(body)       
        return Response(json.dumps({}), mimetype="application/json", status=200)


    def delete(self, id):
        # delete post where "id"=id
        return Response(json.dumps({}), mimetype="application/json", status=200)


    def get(self, id):
        # get the post based on the id
        print(id)
        return Response(json.dumps({"id": id}), mimetype="application/json", status=200)

def initialize_routes(api):
    api.add_resource(
        PostListEndpoint, 
        '/api/posts', '/api/posts/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
    api.add_resource(
        PostDetailEndpoint, 
        '/api/posts/<int:id>', '/api/posts/<int:id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )