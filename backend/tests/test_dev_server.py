from backend.dev_server import build_parser


def test_dev_server_parser_defaults():
    args = build_parser().parse_args([])

    assert args.host == "127.0.0.1"
    assert args.port == 8000
    assert args.reload is False


def test_dev_server_parser_accepts_overrides():
    args = build_parser().parse_args(["--host", "0.0.0.0", "--port", "9000", "--reload"])

    assert args.host == "0.0.0.0"
    assert args.port == 9000
    assert args.reload is True
