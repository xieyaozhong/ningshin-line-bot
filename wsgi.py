from main import app
from threads_insights import threads_bp

app.register_blueprint(threads_bp)
