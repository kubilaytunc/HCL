import json
import uuid
from flask import Flask, render_template, request, redirect, url_for
from models import db, JsonData

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('json_file')
        if file and file.filename.endswith('.json'):
            try:
                data = json.load(file)
                unique_id = str(uuid.uuid4())
                db.session.add(JsonData(id=unique_id, content=json.dumps(data)))
                db.session.commit()
                return redirect(url_for('view_json', json_id=unique_id))
            except Exception as e:
                return f"JSON yüklenemedi: {e}", 400
    return render_template('index.html')

@app.route('/view/<json_id>')
def view_json(json_id):
    json_entry = JsonData.query.get_or_404(json_id)
    try:
        data = json.loads(json_entry.content)
    except json.JSONDecodeError:
        return "JSON verisi hatalı.", 500
    return render_template('view.html', data=data, json_id=json_id)

@app.route('/list', methods=['GET'])
def list_jsons():
    search_query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 10

    query = JsonData.query

    if search_query:
        query = query.filter(JsonData.content.like(f'%{search_query}%'))

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    results = pagination.items

    def extract_title(json_text):
        try:
            data = json.loads(json_text)
            if isinstance(data, dict):
                return next(iter(data.keys()), 'Başlıksız JSON')
            return 'JSON Listesi'
        except:
            return 'Hatalı JSON'

    return render_template(
        'list.html',
        results=results,
        extract_title=extract_title,
        query=search_query,
        pagination=pagination
    )


if __name__ == '__main__':
    app.run(debug=True)

