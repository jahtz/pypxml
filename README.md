# PyPXML

A python library for parsing, creating and modifying PageXML files.

## Setup

>[!NOTE]
>Python version `>=3.11`

### Install from PyPI

```shell
pip install pypxml
```

### Install upstream from source

1. Clone repository: `git clone https://github.com/jahtz/pypxml`
2. Install package: `cd pypxml && pip install .`

## API

PyPXML provides a feature rich Python API for working with PageXML files.

Full [documentation](docs/DOCUMENTATION.md)

## CLI

```txt
$ pypxml --help
Usage: pypxml [OPTIONS] COMMAND [ARGS]...

  A python library for parsing, converting and modifying PageXML files.

Options:
  --help     Show this message and exit.
  --version  Show the version and exit.

Commands:
  get-codec           Extract the character set from PageXML files.
  get-custom          List all custom region attributes in PageXML files.
  get-regions         List all regions in PageXML files.
  get-text            Extract text from PageXML files.
  regularize-codec    Regularize character encodings in PageXML files.
  regularize-regions  Regularize region types in PageXML files.
```

### analytics

#### get-codec

```txt
$ pypxml get-codec --help
Usage: pypxml get-codec [OPTIONS] FILES...

  This tool analyzes the text content of PageXML files and extracts the set of
  characters used.

  It can optionally normalize unicode, remove whitespace, and output character
  frequencies. Results are printed to the console or saved as a CSV file.

  FILES: List of PageXML file paths to process. Accepts individual files, glob
  wildcards, or directories.

Options:
  -o, --output FILE               Path to a CSV file to save the results. If
                                  omitted, results are printed to stdout. If a
                                  directory is given, the file 'codec.csv'
                                  will be created inside it.
  -l, --level [TextRegion|TextLine|Word|Glyph]
                                  PageXML level from which to extract text.
                                  [default: TextLine]
  -i, --index INTEGER             Only consider TextEquiv elements with the
                                  specified index.
  -w, --remove-whitespace         Remove all whitespace characters before
                                  analyzing text.
  -f, --frequencies               Also output character frequencies.
  -n, --normalize [NFC|NFD|NFKC|NFKD]
                                  Normalize unicode before analyzing text.
```

#### get-regions

```txt
$ pypxml get-regions --help
Usage: pypxml get-regions [OPTIONS] FILES...

  Analyzes PageXML files and lists the region types found.

  Optionally includes subtypes, outputs frequencies, and group by file,
  directory, or globally.

  FILES: List of PageXML file paths to process. Accepts individual files, glob
  wildcards, or directories.

Options:
  -o, --output PATH               CSV file or directory where the results are
                                  saved. If a directory is given, the file
                                  'regions.csv' will be created inside it. If
                                  omitted, results are printed to stdout.
  -l, --level [total|directory|file]
                                  Set the aggregation level for the output.
                                  'total' combines all files, 'directory'
                                  aggregates by parent directory, and 'file'
                                  lists results per individual file.
                                  [default: total]
  -f, --frequencies               Also output the frequency (count) of each
                                  region type.
  -t, --types                     Include subtypes by printing them as
                                  'PageType.type' if available.
```

#### get-custom

```txt
$ pypxml get-custom --help
Usage: pypxml get-custom [OPTIONS] FILES...

  Analyzes PageXML files and lists the custom region types found.

  Optionally outputs frequencies and group by file, directory, or globally.

  FILES: List of PageXML file paths to process. Accepts individual files, glob
  wildcards, or directories.

Options:
  -o, --output PATH               CSV file or directory where the results are
                                  saved. If a directory is given, the file
                                  'customs.csv' will be created inside it. If
                                  omitted, results are printed to stdout.
  -l, --level [total|directory|file]
                                  Set the aggregation level for the output.
                                  'total' combines all files, 'directory'
                                  aggregates by parent directory, and 'file'
                                  lists results per individual file.
                                  [default: total]
  -f, --frequencies               Also output the frequency (count) of each
                                  custom attribute.
```

#### get-text

```txt
$ pypxml get-text --help
Usage: pypxml get-text [OPTIONS] FILES...

  Extract text from PageXML files at the TextLine level.

  Outputs to individual text files, a single file, or prints to the console,
  with optional separators between regions and pages.

  FILES: List of PageXML file paths to process. Accepts individual files, glob
  wildcards, or directories.

Options:
  -o, --output PATH            Output destination. If a directory is
                               specified, a separate text file is created for
                               each PageXML file, ignoring the page separator.
                               If a file is specified, the text from all files
                               is concatenated into that file. If omitted, the
                               text is printed to stdout.
  -i, --index INTEGER          Use only the text from TextEquiv elements at
                               the given index.
  -r, --region-separator TEXT  Separator string inserted between regions. Use
                               "" for an empty line, "\n" for two empty lines,
                               ...
  -p, --page-separator TEXT    Separator string inserted between pages when
                               outputting to a single file or stdout. Ignored
                               when outputting multiple files. Use "" for an
                               empty line, "\n" for two empty lines, ...
```

### regularize

#### regularize-codec

```txt
$ pypxml regularize-codec --help
Usage: pypxml regularize-codec [OPTIONS] FILES...

  Apply character replacement rules to text elements in PageXML files.

  Supports selecting PlainText or Unicode elements and limiting replacements
  to specific element levels.

  FILES: List of PageXML file paths to process. Accepts individual files, glob
  wildcards, or directories.

Options:
  -o, --output DIRECTORY          Directory to save the modified PageXML
                                  files. If omitted, input files will be
                                  overwritten.
  -i, --index INTEGER             Use only TextEquiv elements with the
                                  specified index. Defaults to all TextEquiv
                                  elements if not set.
  -l, --level [TextRegion|TextLine|Word|Glyph]
                                  PageXML element level to process.  [default:
                                  TextLine]
  --plaintext / --unicode         Select the text element to use.Choose from
                                  PlainText (without formatting) or Unicode
                                  (formatted).  [default: unicode]
  -r, --rule TEXT...              Define substring replacement rules. Each
                                  rule is a pair of strings: '--rule SOURCE
                                  TARGET'. Multiple rules can be specified by
                                  repeating the option.  [required]
```

#### regularize-regions

```txt
$ pypxml regularize-regions --help
Usage: pypxml regularize-regions [OPTIONS] FILES...

  This tool processes PageXML files and updates or removes regions based on
  specified rules.

  Regions are matched by their PageType and optional subtype. Regions matching
  the source specification are either updated to a new type or deleted if
  target is set to 'None'.

  FILES: List of PageXML file paths to process. Accepts individual files, glob
  wildcards, or directories.

Options:
  -o, --output DIRECTORY  Directory to save the modified PageXML files. If
                          omitted, input files will be overwritten.
  -r, --rule TEXT...      Define rules for region regularization. Format:
                          --rule SOURCE TARGET where SOURCE is the original
                          region type (e.g., TextRegion.paragraph,
                          ImageRegion), and TARGET is the new region type. Use
                          an 'None' TARGET to delete the region. Only region
                          PageTypes are allowed. Multiple rules can be
                          specified by repeating this option.  [required]
```

## ZPD

Developed at Centre for [Philology and Digitality](https://www.uni-wuerzburg.de/en/zpd/) (ZPD), [University of Würzburg](https://www.uni-wuerzburg.de/en/).
