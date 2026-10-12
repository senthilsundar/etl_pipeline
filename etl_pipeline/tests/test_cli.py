from etl_pipeline.cli import build_parser


def test_cli_parser_defaults():
    args = build_parser().parse_args([])
    assert args.limit == 1000
    assert args.output_dir == "data"
    assert args.source_file is None
