from json import JSONEncoder
from pyexpat import model
from flask import Flask, json, jsonify, request
from model.post import Post

posts = []

app = Flask(__name__)
my_storage = model.storage.Storage()
API_ROOT = '/api/blog'

#json_encoder
class CustomsJSONEncoder(json, JSONEncoder):
    def default(self,obj):
        if isinstance(obj,Post):
            return{'body': obj.body, 'user': obj.user}
        else:
            return super().default(obj)
        
app.json_encoder = CustomsJSONEncoder

@app.route('/ping')
def ping():
    return jsonify({'response': "pong"})

#создание поста
@app.route('/post', methods = ['POST'])
def publish_post():
    '''{'body': "Hello, man", 'author': '@full_master'}
    '''
    post_json = request.get_json()
    post = Post(post_json['body'],post_json['author'])
    posts.append(post)
    return jsonify({'status':'success'})

#чтение поста    
@app.route('/post', methods = ['GET'])
def read_post():
    return jsonify({'posts':'posts'})

#редактирование поста
@app.route(API_ROOT + '/post/<post_id>/', methods=['PUT']) 
def edit_post(post_id: str):
    try:
        post_json = request.get_json()
        post = Post(post_json['text'], post_json['author'])
        my_storage.edit_post(post_id, post)
        return jsonify({'status': 'success', 'message': f'id {post.id} edited'})
    except Exception as ex:
        return f'{ex}'

#удаление поста
@app.route(API_ROOT + '/post/<post_id>/', methods=['DELETE']) 
def delete_post(post_id: str):
    try:
        my_storage.delete_post(post_id)
        return jsonify({'status': 'success', 'message': f'id {post_id} deleted'})
    except Exception as ex:
        return f'{ex}'




if __name__ == '__main__':
    app.run(debug=True)