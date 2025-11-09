# Mifal HaMikra - Hosea Critical Edition TEI Encoding Project

## Overview

This project is part of the Hebrew University Bible Project (HUBP) "Mifal HaMikra" initiative, focusing on the digital critical edition of the Book of Hosea (הושע). The project converts traditional critical apparatus formats into TEI (Text Encoding Initiative) XML format, enabling modern digital humanities scholarship and text analysis.

## Project Description

The Mifal HaMikra project aims to create a comprehensive digital critical edition of biblical texts using TEI standards. This repository specifically handles:

- **Main Hebrew Text (Nosah Panim)**: The base text of Hosea with detailed word-level encoding
- **Critical Apparatus I-IV**: Multiple apparatus types documenting textual variants from various witnesses
- **Masoretic Notes**: Apparatus MG (Masorah Gedolah) and MK (Masorah Ketanah)
- **Textual Witnesses**: Documentation of manuscript and versional evidence

## Repository Structure

### Source Documents
- **`הושע נוסח פנים.txt`**: Hebrew base text of Hosea
- **`Hosea.App.1/`**: Apparatus I source files (chapters 1-14)
- **`01 Hosea App III - מתוקן.txt`**: Apparatus III source data
- **`00 מס''ק כל הספרים עם למות - מעודכן העתק שמש 13.5.24.txt`**: Masoretic notes
- **`טעמי המקרא.txt`**: Cantillation marks reference
- **`list_of_witnesses.txt`**: Textual witnesses reference

### Python Notebooks (Parsers)
- **`Parser Apparatus I FULL.ipynb`**: Parses Word documents (Apparatus I) and extracts footnotes
- **`Parser Apparatus II.ipynb`**: Processes Apparatus II
- **`Parser Apparatus III.ipynb`**: Handles Apparatus III textual variants
- **`Parser Apparatus IV.ipynb`**: Processes Apparatus IV
- **`Parser Apparatus MG.ipynb`**: Masoretic Gedolah parser
- **`Parser Apparatus MK.ipynb`**: Masoretic Ketanah parser
- **`TEI Rendering of inner NOSAH.ipynb`**: Converts Hebrew base text to TEI XML
- **`TEI Parser Apparatus I.ipynb`**: TEI encoding for Apparatus I
- **`TEI Parser Apparatus III.ipynb`**: TEI encoding for Apparatus III
- **`TEI Parser Apparatus IV.ipynb`**: TEI encoding for Apparatus IV
- **`XML-2-TEI Converter.ipynb`**: General XML to TEI conversion utilities

### TEI Output Files
- **`APPI_CH_01.xml`**: TEI Apparatus I, Chapter 1
- **`APPII_CH_01.xml`**: TEI Apparatus II, Chapter 1
- **`APPIII_CH_01.xml`**: TEI Apparatus III encoding (under development)
- **`APPIV_CH_01.xml`**: TEI Apparatus IV, Chapter 1
- **`APPMG_CH_01.xml`**: TEI Masoretic Gedolah
- **`APPMK_CH_01.xml`**: TEI Masoretic Ketanah
- **`Hosea_Inner_Text.xml`**: TEI-encoded base text
- **`output_hosea_fixed_v8.tei.xml`**: Latest comprehensive TEI output
- **`final_output_tei.xml`**: Final combined TEI document

### Transformation Files
- **`convert_custom_to_tei.xsl`**: XSLT for custom XML to TEI conversion
- **`tei_to_html.xsl`**: XSLT for rendering TEI as HTML
- **`convert_xml_to_html.py`**: Python script for XML to HTML conversion

### Data Files
- **`App.1.FULL.json`**: JSON representation of Apparatus I
- **`processed_df.csv`**: Processed dataframe of textual data
- **`comments_and_edits.json`**: Editorial comments and revision notes

## Technical Stack

### Dependencies
- **Python 3.x**
- **lxml**: XML/XSLT processing
- **pandas**: Data manipulation and CSV handling
- **python-docx**: Word document processing
- **pywin32**: Windows COM interface for Word automation
- **xml.etree.ElementTree**: XML parsing
- **unicodedata**: Hebrew text normalization

### Installation

```bash
pip install lxml pandas python-docx pywin32
```

## Workflow

### 1. Extract Source Data
The parsers read Word documents and text files containing the critical apparatus and base text.

### 2. Process and Structure
- Extract footnotes from Word documents
- Parse Hebrew text with diacritics and punctuation
- Identify textual witnesses and variants
- Structure data according to chapter and verse divisions

### 3. TEI Encoding
- Convert parsed data to TEI P5 XML format
- Create `<app>` (apparatus) entries with `<lem>` (lemma) and `<rdg>` (reading) elements
- Encode witnesses with proper `@wit` attributes
- Generate `<listWit>` for witness descriptions
- Preserve Hebrew text encoding with proper Unicode normalization

### 4. Validation and Output
- Validate against TEI schema
- Generate HTML representations for review
- Export final TEI XML for scholarly use

## TEI Structure

### Main Text Encoding
```xml
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>...</teiHeader>
  <text>
    <body>
      <div type="chapter" n="1">
        <div type="verse" n="1">
          <w xml:id="hos_1_1_w1">דְּבַר־</w>
          ...
        </div>
      </div>
    </body>
  </text>
</TEI>
```

### Apparatus Encoding
```xml
<listApp>
  <app xml:id="hos_1_2" n="1:2">
    <lem wit="#MT">בְּהוֹשֵׁעַ</lem>
    <rdg wit="#LXX">πρός</rdg>
    <rdg wit="#Peshitta">ܕܗܘܐ ܥܠ</rdg>
  </app>
</listApp>
```

## Features

- **Multi-layered apparatus**: Supports multiple types of critical apparatus
- **Witness tracking**: Maintains relationships between witnesses and readings
- **Hebrew text support**: Full Unicode Hebrew with cantillation and vowel marks
- **Word-level granularity**: Individual word encoding with morphological details
- **Masoretic integration**: Includes traditional Masoretic notes
- **Flexible export**: TEI XML, HTML, JSON formats

## Usage

### Running the Parsers
Open any of the Jupyter notebooks in VS Code or Jupyter Lab:

```bash
jupyter notebook "Parser Apparatus I FULL.ipynb"
```

### Converting to TEI
Run the TEI Parser notebooks to generate standardized TEI output:

```bash
jupyter notebook "TEI Parser Apparatus III.ipynb"
```

### Generating HTML Preview
Use the XSLT transformations or Python scripts:

```python
python convert_xml_to_html.py
```

## Project Goals

1. **Digitization**: Convert traditional printed apparatus to digital format
2. **Standardization**: Use TEI P5 for interoperability
3. **Accessibility**: Make critical edition data available for computational analysis
4. **Preservation**: Create archival-quality digital representations
5. **Scholarship**: Enable new forms of textual research and comparison

## Current Status

- ✅ Apparatus I: Chapters 1-14 parsed and TEI-encoded
- ✅ Base text (Nosah): Full TEI encoding with word-level detail
- 🚧 Apparatus III: In progress
- 🚧 Apparatus IV: In progress
- 🚧 Masoretic apparatus: Ongoing development
- 📋 Validation and schema refinement

## Contributing

This is an academic research project under the Hebrew University Bible Project. For questions or collaboration inquiries, please refer to the project documentation.

## Related Resources

- [TEI Guidelines](https://tei-c.org/release/doc/tei-p5-doc/en/html/)
- [Hebrew University Bible Project (HUBP)](https://www.hubp.huji.ac.il/)
- [Digital Humanities and Biblical Studies](https://dhhuji.github.io/)

## License

Academic research project - refer to institutional guidelines for usage terms.

## Acknowledgments

This work is part of the Hebrew University Bible Project's ongoing efforts to create comprehensive critical editions of biblical texts using modern digital humanities methodologies.

---

**Project maintained by the Digital Humanities team at Hebrew University of Jerusalem**
