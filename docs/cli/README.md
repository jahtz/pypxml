# pypxml CLI

Command-line interface for analyzing and modifying PAGE-XML files.

## Installation

```bash
pip install pypxml[cli]
```

## Usage

```bash
pypxml
```

## Global Options

Available for all commands:

- `--help` - Show help message
- `--version` - Show version
- `--logging [ERROR|WARNING|INFO]` - Set logging level (default: ERROR)

## Commands

### get-codec

Extract the character set used in PAGE-XML files.

```bash
pypxml get-codec [OPTIONS] FILES...
```

**Options:**
- `-o, --output PATH` - Save results to CSV file (default: stdout)
- `-s, --source [TextRegion|TextLine|Word|Glyph]` - Element type to extract from (default: TextLine)
- `-i, --index INT` - Only use TextEquiv elements with specified index
- `--plaintext/--unicode` - Use PlainText or Unicode elements (default: unicode)
- `-w, --whitespace` - Include whitespace characters
- `-f, --frequency` - Output character frequencies
- `-n, --normalize [NFC|NFD|NFKC|NFKD]` - Normalize unicode before analysis

**Examples:**

```bash
# Extract character set from text lines
pypxml get-codec document.xml

# Get character frequencies with normalization
pypxml get-codec -f -n NFC document.xml

# Extract from multiple files and save to CSV
pypxml get-codec -o charset.csv *.xml

# Include whitespace in analysis
pypxml get-codec -w -s TextRegion document.xml
```

---

### get-regions

List region types found in PAGE-XML files.

```bash
pypxml get-regions [OPTIONS] FILES...
```

**Options:**
- `-o, --output PATH` - Save results to CSV file (default: stdout)
- `-l, --level [total|directory|file]` - Aggregation level (default: total)
- `-f, --frequency` - Output region frequencies
- `-s, --subtypes` - Include region subtypes

**Examples:**

```bash
# List all region types across files
pypxml get-regions *.xml

# Get region counts per file
pypxml get-regions -l file -f *.xml

# Include subtypes and save to CSV
pypxml get-regions -s -o regions.csv *.xml

# Aggregate by directory
pypxml get-regions -l directory -f documents/**/*.xml
```

---

### get-text

Extract text content from a PAGE-XML file.

```bash
pypxml get-text [OPTIONS] FILE
```

**Options:**
- `-o, --output PATH` - Save text to file (default: stdout)
- `-i, --index INT` - Only use TextEquiv elements with specified index
- `--plaintext/--unicode` - Use PlainText or Unicode elements (default: unicode)
- `-s, --separator TEXT` - Separator between regions (use "" for empty line)

**Examples:**

```bash
# Extract text to stdout
pypxml get-text document.xml

# Save text to file
pypxml get-text -o output.txt document.xml

# Use custom separator between regions
pypxml get-text -s "---" document.xml

# Extract plain text instead of unicode
pypxml get-text --plaintext document.xml
```

---

### prettify

Reformat and standardize PAGE-XML files.

```bash
pypxml prettify [OPTIONS] FILES...
```

**Options:**
- `-o, --output DIR` - Directory for output files (default: overwrite input)
- `-s, --schema [2017|2019]` - PAGE-XML schema version (default: 2019)

**Examples:**

```bash
# Prettify files in place
pypxml prettify *.xml

# Save to output directory with 2019 schema
pypxml prettify -o output/ -s 2019 *.xml
```

---

### regularise-codec

Apply character replacement rules to text in PAGE-XML files.

```bash
pypxml regularise-codec [OPTIONS] -r OLD NEW FILES...
```

**Options:**
- `-o, --output DIR` - Directory for output files (default: overwrite input)
- `-i, --index INT` - Only modify TextEquiv elements with specified index
- `-t, --target [TextRegion|TextLine|Word|Glyph]` - Elements to modify (multiple allowed)
- `-e, --element [PlainText|Unicode]` - Text elements to modify (multiple allowed)
- `-r, --rule OLD NEW` - Replacement rule (multiple allowed, required)

**Examples:**

```bash
# Replace character with another
pypxml regularise-codec -r "ſ" "s" *.xml

# Multiple replacement rules
pypxml regularise-codec -r "ſ" "s" -r "æ" "ae" *.xml

# Remove characters (replace with empty string)
pypxml regularise-codec -r "~" "" *.xml

# Target only text lines
pypxml regularise-codec -t TextLine -r "ſ" "s" *.xml

# Save to output directory
pypxml regularise-codec -o output/ -r "ſ" "s" *.xml
```

---

### regularise-regions

Modify or remove region types in PAGE-XML files.

```bash
pypxml regularise-regions [OPTIONS] -r OLD NEW FILES...
```

**Options:**
- `-o, --output DIR` - Directory for output files (default: overwrite input)
- `-r, --rule OLD NEW` - Region replacement rule (multiple allowed, required)
  - Format: `PageType` or `PageType.subtype`
  - Use `None` as NEW to delete regions

**Examples:**

```bash
# Change region type
pypxml regularise-regions -r "GraphicRegion" "ImageRegion" *.xml

# Change region with subtype
pypxml regularise-regions -r "TextRegion.heading" "TextRegion.header" *.xml

# Delete specific region type
pypxml regularise-regions -r "NoiseRegion" "None" *.xml

# Multiple rules
pypxml regularise-regions \
  -r "GraphicRegion" "ImageRegion" \
  -r "NoiseRegion" "None" \
  *.xml

# Save to output directory
pypxml regularise-regions -o clean/ -r "NoiseRegion" "None" *.xml
```