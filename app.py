from flask import Flask, request, jsonify, make_response
from datetime import datetime
from flask_restful import Resource, Api

# Buat flask instance
app = Flask(__name__)
# API object
api = Api(app)

todos = []
format_data = "%d-%m-%Y %H:%M:%S"

class GetTodos(Resource):
    def get(self):
        if len(todos) == 0:
            return {'Error' : 'Todos Not Found'}, 404

        return {'data':todos}, 200

class AddTodo(Resource):
    def post(self):
        if request.is_json:
            id = len(todos) + 1
            title = request.json['title']
            description = request.json['description']
            created_at = datetime.now().strftime(format_data)

            todo = {'Id': id, 
            'title': title, 
            'description': description,
            'created_at': created_at,
            'updated_at': '',
            'finished_at': '',
            'deleted_at': ''}
            todos.append(todo)

            return make_response({'data': todo,'message': 'Todo successfully created'})

        else:
            return {'error': 'Request must be JSON'}, 400

class GetTodoById(Resource):
    def get(self, id):
        if len(todos) == 0:
            return {'Error': "Todo Not Found"}, 404
        
        index = 0
        while index < len(todos):
            dictionary = todos[index]
            if dictionary['Id'] == id:
                return {'data': dictionary}
            index += 1

        return {'Error': "Todo Not Found"}, 404

class UpdateTodo(Resource):
    def put(self, id):
        if len(todos) == 0:
            return {'Error': "Todo Not Found"}, 404
        
        if request.is_json != True:
            return {'error': 'Request must be JSON'}, 402
        
        index = 0
        index_of_data = 0
        data = []
        while index < len(todos):
            dictionary = todos[index]
            if dictionary['Id'] == id:
                index_of_data = index
                data = dictionary
            index += 1

        if len(data) == 0:
            return {'Error': "Todo Not Found"}, 404

        data['title'] = request.json['title']
        data['description'] = request.json['description']
        data['updated_at'] = datetime.now().strftime(format_data)
        todos[index_of_data] = data

        return {'message': "Todo has been updated"}, 200

class FinishTodo(Resource):
    def post(self,id):
        if len(todos) == 0:
            return {'Error': "Todo Not Found"}, 404
      
        index = 0
        index_of_data = 0
        data = []
        while index < len(todos):
            dictionary = todos[index]
            if dictionary['Id'] == id:
                index_of_data = index
                data = dictionary
            index += 1

        if len(data) == 0:
            return {'Error': "Todo Not Found"}, 404

        data['finished_at'] = datetime.now().strftime(format_data)
        todos[index_of_data] = data

        return {'message': "Todo Finished"}, 200

class DeleteTodo(Resource):
    def delete(self,id):
        if len(todos) == 0:
            return {'Error': "Todo Not Found"}, 404
      
        index = 0
        index_of_data = 0
        data = []
        while index < len(todos):
            dictionary = todos[index]
            if dictionary['Id'] == id:
                index_of_data = index
                data = dictionary
            index += 1

        if len(data) == 0:
            return {'Error': "Todo Not Found"}, 404

        # todos.pop(index_of_data)
        data['deleted_at'] = datetime.now().strftime(format_data)
        todos[index_of_data] = data

        return {'message': "Todo Deleted"}, 200

api.add_resource(GetTodos, '/')
api.add_resource(AddTodo, '/')
api.add_resource(GetTodoById,'/<int:id>')
api.add_resource(UpdateTodo,'/<int:id>')
api.add_resource(FinishTodo,'/<int:id>/finish')
api.add_resource(DeleteTodo,'/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)