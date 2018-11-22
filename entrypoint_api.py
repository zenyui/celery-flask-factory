from server import create_app
import argparse

def cli():
    p = argparse.ArgumentParser()
    p.add_argument('--host', dest='host', default='0.0.0.0')
    p.add_argument('--port', dest='port', type=int, default=8080)
    p.add_argument('--debug', dest='debug', action='store_true')
    args = p.parse_args()
    app = create_app()
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    cli()
