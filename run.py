from apps import create_app
app = create_app('development')
app.run(host='0.0.0.0')
