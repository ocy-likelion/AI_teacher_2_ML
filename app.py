import os
from flask import Flask
from route.math_explain import math_explain_bp

app = Flask(__name__)

app.register_blueprint(math_explain_bp)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
