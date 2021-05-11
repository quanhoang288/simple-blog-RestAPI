
from flask.json import jsonify
from models.model import Model



class Post(Model):
    fields = Model.describe(Model.db_handler, 'posts')
    
    def get(id=None, per_page=None):
        
        if id: 
            query = 'SELECT * FROM posts WHERE id = %s'
            results = Model.db_handler.execute(query, (id, )) 
        elif per_page: 
            query = 'SELECT * FROM posts ORDER BY time_created DESC LIMIT %s'
            results = Model.db_handler.execute(query, (int(per_page), ))
            print(results)
        else:
            query = 'SELECT * FROM posts ORDER BY time_created DESC'
            results = Model.db_handler.execute(query)
        posts = []
        for post in results: 
            
            post_id = post['id']
            author_id = post['author_id']
            author_query = 'SELECT name FROM users WHERE id = %s'
            author = Model.db_handler.execute(author_query, (author_id, ))[0]
            like_query = 'SELECT name FROM users WHERE id IN (SELECT user_id FROM likes WHERE post_id = %s)'
            result = Model.db_handler.execute(like_query, (post_id,))
            post['num_likes'] = len(result)
            users = result[:2]
            user_names = []
            for user in users: 
                user_names.append(user['name'])
            post_detail = {}
            for key, value in post.items():
                post_detail[key] = value 
            post_detail['author_name'] = author['name']
            post_detail['first_two_likes'] = user_names 
            posts.append(post_detail)
            # posts.append(Post(post_id, post['title'], post['body'], post['time_created'], author_id, author['name'], num_likes['num_likes'], user_names, post['last_modified']).to_dict())
        if id is not None: 
            return posts[0] if len(posts) > 0 else None 
        return posts  




         
    def create_post(data):
        author_id = data['author_id']
        author_query = 'SELECT * FROM users WHERE id = %s'
        result = Model.db_handler.execute(author_query, (author_id, ))
        if len(result) == 0:
            return None   
        # author = result[0]
        query = 'INSERT INTO posts (title , body, author_id, time_created) VALUES (%(title)s, %(body)s, %(author_id)s, %(time_created)s)'
        
        result = Model.db_handler.execute(query, data, commit=True)
        if result: 
            post_id = Model.db_handler.get_lastrowid()
            post_query = 'SELECT * FROM posts WHERE id=%s'
            post = Model.db_handler.execute(post_query, (post_id,))[0]
            return post 
        else: 
            return False 
         
    def update_post(id, data):
        post_query = 'SELECT * FROM posts WHERE id = %s'
        result = Model.db_handler.execute(post_query, (id, ))
        if len(result) == 0:
            return None
        post = result[0]
        update = ''
        values = []
        for key, value in data.items():
            update += key + '= %s,'
            values.append(value)      
            post[key] = value  
        values.append(id)
        update = update[:-1]
        query = 'UPDATE posts SET ' + update + ' WHERE id = %s'
        result = Model.db_handler.execute(query, values, commit=True) 
        if result: 
            post_query = 'SELECT * FROM posts WHERE id = %s'
            post = Model.db_handler.execute(post_query, (id,))[0]
            return post 
        return False 
            

    def delete_post(id):
        # query = 'DELETE FROM posts WHERE id = %s'
        # Model.db_handle.execute(query, (id, )) 
        post_query = 'SELECT * FROM posts WHERE id = %s'
        result = Model.db_handler.execute(post_query, (id,))
        if len(result) == 0:
            return None
        post = result[0]
        query = 'DELETE FROM posts WHERE id = %s'
        result = Model.db_handler.execute(query, (id,), commit=True) 
        if result:
            return post  
        return False
    