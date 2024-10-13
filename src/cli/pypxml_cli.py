import click


@click.group()
@click.help_option('--help')
@click.version_option('1.0', '--version',
                      prog_name='PyPXML',
                      message='%(prog)s v%(version)s - Developed at Centre for Philology and Digitality (ZPD), '
                              'University of Würzburg')
def cli():
    """
    PyPXML command line interface entry point.
    """
    pass

