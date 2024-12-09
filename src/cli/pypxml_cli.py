import click

from .regularize_cli import regularize_cli


@click.group()
@click.help_option('--help')
@click.version_option('2.1.1', '--version',
                      prog_name='pypxml',
                      message='%(prog)s v%(version)s - Developed at Centre for Philology and Digitality (ZPD), '
                              'University of Würzburg')
def cli():
    """
    PyPXML command line interface entry point.
    """
    pass


cli.add_command(regularize_cli)
