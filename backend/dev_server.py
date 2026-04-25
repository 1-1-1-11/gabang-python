from argparse import ArgumentParser, Namespace

import uvicorn


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Run the gobang-python FastAPI development server.")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface to bind.")
    parser.add_argument("--port", default=8000, type=int, help="Port to bind.")
    parser.add_argument("--reload", action="store_true", help="Reload the server when Python files change.")
    return parser


def run_server(args: Namespace) -> None:
    uvicorn.run("backend.app.main:app", host=args.host, port=args.port, reload=args.reload)


def main() -> None:
    run_server(build_parser().parse_args())


if __name__ == "__main__":
    main()
