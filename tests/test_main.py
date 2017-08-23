from child_support_tables import __main__ as main

from pytest import fail


EXPECTED_HELP = \
'''usage: Justice Canada child support tables extractor [-h] [input]

positional arguments:
  input       Name of XML-formatted family law document

optional arguments:
  -h, --help  show this help message and exit
'''


def test_help(capsys):
    main.argument_parser.print_help()
    out, err = capsys.readouterr()
    assert out == EXPECTED_HELP
    assert not err


def test_argument_parser(capsys):
    from sys import stdin
    assert main.argument_parser.parse_args(['foo.html']).input == 'foo.html'
    assert main.argument_parser.parse_args(['http://laws-lois.justice.gc.ca/eng/XML/SOR-97-175.xml']) \
                               .input == 'http://laws-lois.justice.gc.ca/eng/XML/SOR-97-175.xml'
    assert main.argument_parser.parse_args([]).input == stdin


def test_main():
    fail('Not testable/refactored yet')
