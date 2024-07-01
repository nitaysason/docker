from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a simple model for blog posts
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Post {self.id}: {self.title}>'

# Create the SQLite database and add initial data
with app.app_context():
    db.create_all()

    # Add initial data
    post1 = Post(title='First Post', content='This is the content of the first post.')
    post2 = Post(title='Second Post', content='This is the content of the second post.')
    
    db.session.add(post1)
    db.session.add(post2)
    
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        print(str(e))

# Routes
@app.route('/posts', methods=['GET'])
def get_posts():
    try:
        posts = Post.query.all()
        return jsonify([{'id': post.id, 'title': post.title, 'content': post.content} for post in posts])
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        return jsonify({'id': post.id, 'title': post.title, 'content': post.content})
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

@app.route('/posts', methods=['POST'])
def create_post():
    try:
        data = request.get_json()
        new_post = Post(title=data['title'], content=data['content'])
        db.session.add(new_post)
        db.session.commit()
        return jsonify({'message': 'Post created successfully'}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing key: {str(e)}'}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        data = request.get_json()
        post.title = data['title']
        post.content = data['content']
        db.session.commit()
        return jsonify({'message': 'Post updated successfully'})
    except KeyError as e:
        return jsonify({'error': f'Missing key: {str(e)}'}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': 'Post deleted successfully'})
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
