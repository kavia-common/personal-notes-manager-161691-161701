import os
from app import create_app

# PUBLIC_INTERFACE
def main():
    """Entrypoint to run the Flask app on port 3001 for preview."""
    app = create_app()
    port = int(os.getenv("PORT", "3001"))
    host = os.getenv("HOST", "0.0.0.0")
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    main()
