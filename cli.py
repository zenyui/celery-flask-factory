from server import create_app
import argparse

def run():
    app = create_app()
    port = app.config['FLASK_PORT']
    app.run(host='0.0.0.0', port=port, debug=True)

if __name__ == "__main__":
    run()
