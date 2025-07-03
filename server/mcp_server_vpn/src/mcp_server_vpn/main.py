import argparse
import logging
import signal
import sys
import threading

from mcp_server_vpn.server import mcp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the VPN MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport protocol to use",
    )
    args = parser.parse_args()

    logger.info("Starting VPN MCP Server with %s transport", args.transport)

    stop_event = threading.Event()

    def run_server() -> None:
        try:
            mcp.run(transport=args.transport)
        finally:
            stop_event.set()

    def handle_signal(signum, frame) -> None:  # noqa: D401
        """Handle termination signals and shut down the server."""
        logger.info("Received signal %s, shutting down gracefully", signum)
        shutdown = getattr(mcp, "shutdown", None)
        if callable(shutdown):
            try:
                shutdown()
            except Exception as exc:  # pragma: no cover - best effort
                logger.error("Error during shutdown: %s", exc)
        stop_event.set()

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    thread = threading.Thread(target=run_server, name="mcp-server")
    thread.start()

    stop_event.wait()
    logger.info("Server shutdown complete")
    sys.exit(0)


if __name__ == "__main__":
    main()
