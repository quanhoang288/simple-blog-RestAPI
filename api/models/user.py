from models.model import Model

class User(Model):
    fields = Model.describe(Model.db_handler, 'users')

    
    def get_users(params=None):
        condition = '1=1 AND'
        values = []
        if params is not None and 'name' in params:
            condition += ' name = %s AND'
            values.append(params['name'])
        if params is not None and 'occupation' in params: 
            condition += ' occupation = %s AND'
            values.append(params['occupation'])

        condition = condition[:-3]

        query = 'SELECT * FROM users WHERE ' + condition
        results = Model.db_handler.execute(query, tuple(values)) 
        return results
    
    def get_user(id, show_posts = False):
        query = 'SELECT * FROM users WHERE id = %s'
        results = Model.db_handler.execute(query, (id, ))
        if len(results) == 0: 
            return None 
        user = results[0]

        if show_posts: 
            result = {'user': user}
            user_id = id 
            post_query = 'SELECT * FROM posts WHERE author_id = %s' 
            posts = Model.db_handler.execute(post_query, (user_id, ))
            result['posts'] = posts
            return result 
        return user
                
                


         
    def create_user(data):
        name = data['name']
        acc_type =  data['type'].lower()
        email = data['email']
        phone = data['phone'] if acc_type == 'facebook' or 'phone' in data else None  
        occupation = data['occupation'] if acc_type == 'google' or 'occupation' in data else None 
        values = [name] 
        insert_fields = ['name']
        if phone: 
            insert_fields.append('phone')
            values.append(phone)
        if occupation:
            insert_fields.append('occupation')
            values.append(occupation)
        insert_fields.extend(['type', 'email'])
        values.extend([acc_type, email])
        user_query = 'SELECT * FROM users WHERE email = %s'
        user = Model.db_handler.execute(user_query, (email,))
        if len(user) > 0: 

            return user
        query = 'INSERT INTO users (' 
        for field in insert_fields:
            query += field + ',' 
        query = query[:-1] + ') VALUES ('
        for _ in range(len(insert_fields)):
            query += '%s,'
        query = query[:-1] + ')'

        result =  Model.db_handler.execute(query, tuple(values), commit=True)
        if result: 
            user_query = 'SELECT * FROM users WHERE email = %s'
            users = Model.db_handler.execute(user_query, (email,))
            return users[0]
        return False 
            
         
    def update_user(id, data):
        user_query = 'SELECT * FROM users WHERE id = %s'
        users = Model.db_handler.execute(user_query, (id, ))
        if len(users) == 0:
            return None 
        update = ''
        values = []  
        user = users[0]
        for key, value in data.items():
            update += key + '= %s,'
            values.append(value) 
            user[key] = value
        values.append(id)
        update = update[:-1]
        query = 'UPDATE users SET ' + update + ' WHERE id = %s'
        result =  Model.db_handler.execute(query, values, commit=True) 
        if result: 
            return user
        return False
            
            
        
    def delete_user(id):
        user_query = 'SELECT * FROM users WHERE id = %s'
        result = Model.db_handler.execute(user_query, (id,))
        if len(result) == 0:
            return None
        user = result[0]
        query = 'DELETE FROM users WHERE id = %s'
        result = Model.db_handler.execute(query, (id,), commit=True) 
        if result:
            return user 
        return False