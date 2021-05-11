from database.db import DatabaseAdapter 


class Model:
    db_handler = DatabaseAdapter()
        
    def describe(db_handler, table):
        query = 'DESCRIBE ' + table  
        results = db_handler.execute(query)
        fields = []
        for field in results:
            fields.append(field['Field'])
        return fields
        

