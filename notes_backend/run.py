import os
import logging
from app import create_app

# Configure basic logging for startup diagnostics
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

# PUBLIC_INTERFACE
def main():
    """Entrypoint to run the Flask app on port 3001 for preview.

    Binds to 0.0.0.0:3001 by default so the orchestrator can reach it.
    Disables the Flask reloader to avoid double-start and port binding issues in CI/containers.
    Environment variables:
      - PORT: override listening port (default 3001)
      - HOST: override host interface (default 0.0.0.0)
      - FLASK_DEBUG: set "1" to enable debug mode (reloader stays disabled)
    """
    app = create_app()
    port = int(os.getenv("PORT", "3001"))
    host = os.getenv("HOST", "0.0.0.0")
    debug = os.getenv("FLASK_DEBUG", "0") == "1"

    logger.info("Starting Notes Backend on %s:%s (debug=%s, reloader=%s)", host, port, debug, False)
    # Use threaded=True to allow concurrent requests in preview; disable reloader to prevent double bind
    app.run(host=host, port=port, debug=debug, use_reloader=False, threaded=True)


if __name__ == "__main__":
    main()
