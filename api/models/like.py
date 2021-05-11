from models.model import Model 


class Like(Model):
    def __init__(self):
        super().__init__()


    def get_all_likes():
        query = 'SELECT * FROM likes'
        likes = Model.db_handler.execute(query)
        return likes 
    def get_posts_liked_by(user_id):
        user_query = 'SELECT id FROM users WHERE id = %s' 
        users = Model.db_handler.execute(user_query, (user_id,))
        if len(users) == 0:
            return None
        query = 'SELECT * FROM posts WHERE id IN (SELECT post_id FROM likes WHERE user_id = %s)'
        posts = Model.db_handler.execute(query, (user_id, ))
        return posts  
    def get_likes_of_post(post_id):
        post_query = 'SELECT id FROM users WHERE id = %s' 
        posts = Model.db_handler.execute(post_query, (post_id,))
        if len(posts) == 0:
            return None
        query = 'SELECT * FROM users WHERE id IN (SELECT user_id FROM likes WHERE post_id = %s)' 
        users = Model.db_handler.execute(query, (post_id, ))
        return users  
    
    def create_like(data):
        user_query = 'SELECT id FROM users WHERE id = %s'
        users = Model.db_handler.execute(user_query, (data['user_id'], ))
        post_query = 'SELECT id FROM posts WHERE id = %s'
        posts = Model.db_handler.execute(post_query, (data['post_id'], ))
        if len(users) == 0 or len(posts) == 0: 
            return None 
        query = 'INSERT INTO likes (user_id, post_id) VALUES (%(user_id)s, %(post_id)s)'
        result =  Model.db_handler.execute(query, data,  commit=True) 
        if result:
            return data 
        return False 

    def delete_like(data):
        user_query = 'SELECT id FROM users WHERE id = %s'
        users = Model.db_handler.execute(user_query, (data['user_id'], ))

        post_query = 'SELECT id FROM posts WHERE id = %s'
        posts = Model.db_handler.execute(post_query, (data['post_id'], ))
        if len(users) == 0 or len(posts) == 0: 
            return None 
        query = 'DELETE FROM likes WHERE user_id = %(user_id)s AND post_id = %(post_id)s'
        result = Model.db_handler.execute(query, data, commit=True) 
        if result: 
            return data
        return False
    