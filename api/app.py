
import flask
from flask import request, jsonify


from models.like import Like
from models.post import Post 
from models.user import User


app = flask.Flask(__name__)




@app.route('/posts', methods=['GET'])
def get_posts():
    params = request.args
    if 'per_page' in params: 
        posts = Post.get(per_page = params['per_page'])
    else:
        posts = Post.get()
    if len(posts) == 0: 
        return jsonify({'error': 'Posts not found'}), 404 
    return jsonify(posts), 200
    

@app.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    post = Post.get(id = id)
    if post is not None: 
        return jsonify(post), 200
    return jsonify({'error': 'Post not found'}), 404

@app.route('/posts', methods =['POST'])
def create_post():
    data = request.get_json()
    fields = Post.fields 
    for key in data:
        if key not in fields:
            return jsonify({'error': 'Mismatched field'}), 400 
    post = Post.create_post(data)
    if post is None: 
        return jsonify({'error': 'Author not found'}), 400
    if post: 
        return jsonify(post), 201
    return jsonify({'error': 'Error creating post'}), 500 
     

@app.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
    fields = Post.fields
    data = request.get_json()
    for key in data: 
        if key not in fields:
            return jsonify({'error': 'Mismatched field'}), 400
    result = Post.update_post(id, data)
    if result is None: 
        return jsonify({'error': 'Post not found'}, 400)
    if result: 
        return jsonify(result), 200 
    return jsonify({'error': 'Error updating post'}), 500  

@app.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = Post.delete_post(id)
    if post is None: 
        return jsonify({'error': 'Post not found'}), 400
    if post:
        return jsonify(post), 200
    return jsonify({"error":"Error deleting post"}), 500 


   
@app.route('/users', methods=['GET'])
def get_users():
    params = request.args
    users = User.get_users(params)
    if len(users) == 0:
        return jsonify({'error': 'Users not found'}), 404 
    return jsonify(users), 200

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.get_user(id)
    if user is None: 
        return jsonify({'error': 'User not found'}), 404 
    return jsonify(user), 200

@app.route('/users/<int:id>/posts', methods=['GET'])
def get_user_posts(id):
    user = User.get_user(id, show_posts = True)
    if user is None:
        return jsonify({'error': 'User not found'}), 404 
    return jsonify(user), 200

@app.route('/users', methods =['POST'])
def create_user():
    data = request.get_json()
    keys = list(data.keys())
    if 'name' not in keys or 'type' not in keys or 'email' not in keys:
        return jsonify({'error': 'Provide required fields'}), 400

    if data['type'].lower() == 'facebook' and 'phone' not in keys:
        return 'Provide a phone number', 400 
    if data['type'].lower() == 'google' and 'occupation' not in keys:
        return 'Provide user occupation', 400
    result = User.create_user(data)
    
    if isinstance(result, list):
        response = {
            'error': 'User already exists',
            'user': result[0] 
        }
        return jsonify(response), 409
    if result:
        return jsonify(result), 201 
    return jsonify({'error': 'Error creating user'}), 500

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    fields = User.fields
    data = request.get_json()
    for key in data: 
        if key not in fields:
            return 'Mismatched field', 400
    result = User.update_user(id, data)
    if result is None: 
        return jsonify({'error': 'User not found'}), 400
    if result: 
        return jsonify(result), 200 
    return 'Error updating user', 500 


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.delete_user(id)
    if user is None:
        return jsonify({'error': 'User not found'}), 400
    if user:
        return jsonify(user), 200
    return jsonify({"message":"Error deleting user"}), 500

@app.route('/likes', methods=['GET'])
def get_likes():
    params = request.args
    if 'user_id' in params: 
        posts = Like.get_posts_liked_by(params['user_id'])
        if posts is None: 
            return jsonify({'error': 'User not found'}), 400 
        return jsonify(posts), 200
    elif 'post_id' in params: 
        users = Like.get_likes_of_post(params['post_id']) 
        if users is None: 
            return jsonify({'error': 'Post not found'}), 400
        return jsonify(users), 200
    likes = Like.get_all_likes()
    return jsonify(likes), 200 

    

@app.route('/likes', methods=['POST'])
def create_like():
    data = request.get_json()
    fields = list(data.keys()) 
    if 'post_id' not in fields or 'user_id' not in fields:
        return jsonify({'error': 'Missing required field'}), 400 
    like = Like.create_like(data)
    if like is None: 
        return jsonify({'error': 'Post/User not found'}), 400
    if like:
        return jsonify(like), 201
    return jsonify({'error': 'Error creating like'}), 500


@app.route('/likes', methods=['DELETE'])
def delete_like():
    data = request.get_json()
    fields = list(data.keys()) 
    if 'post_id' not in fields or 'user_id' not in fields:
        return jsonify({'error': 'Missing required field'}), 400 
    like = Like.delete_like(data)
    if like is None: 
        return jsonify({'error': 'Post/User not found'}), 400
    if like:
        return jsonify(like), 200
    return jsonify({'error': 'Error deleting like'}), 500 
    
        



if __name__ == '__main__':

    app.run(debug=True)