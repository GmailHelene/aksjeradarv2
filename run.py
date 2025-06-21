import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Only use debug mode and custom port in development
    debug = os.environ.get('FLASK_ENV') != 'production'
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=debug)
