import xml.etree.ElementTree as ET

# Load the provided XML file
xml_file_path = 'Apparatus III Encoding.xml'


def create_html_entry(entry):
    lemma_info = entry.find('LemmaInfo')
    chapter = lemma_info.find('Chapter').text if lemma_info.find('Chapter') is not None else ''
    verse = lemma_info.find('Verses').text if lemma_info.find('Verses') is not None else ''
    lemmas = lemma_info.find('Lemmas') if lemma_info is not None else None
    lemma_texts = [lemma.find('Text').text if lemma.find('Text') is not None else '' for lemma in
                   lemmas] if lemmas is not None else []
    lemma_numbers = [lemma.find('Number').text if lemma.find('Number') is not None else '' for lemma in
                     lemmas] if lemmas is not None else []

    decoded_entry = entry.find('DecodedEntry')
    details = decoded_entry.find('Details') if decoded_entry is not None else None
    witnesses = details.find('Witnesses') if details is not None else None
    readings = details.find('Rdg') if details is not None else None
    comments = readings.find('Comment') if readings is not None else None
    sigla = readings.find('Sigla') if readings is not None else None

    cross_references = details.find('CrossReferences') if details is not None else None
    references = [ref.text if ref is not None else '' for ref in
                  cross_references.findall('Reference')] if cross_references is not None else []

    witness_texts = [
        {
            'Manuscript': witness.find('Manuscript').text if witness.find('Manuscript') is not None else '',
            'Comment': witness.find('Comment').text if witness.find('Comment') is not None else ''
        }
        for witness in witnesses
    ] if witnesses is not None else []

    # Ensure that witness_texts contains no None values and exclude empty entries
    witness_texts = [
        {k: v for k, v in witness.items() if v}
        for witness in witness_texts if any(witness.values())
    ]

    html = f'''
    <div class="apparatus">
        <h2>Apparatus Entry Number {entry.get('Number')}</h2>
    '''

    if chapter:
        html += f'<p class="chapter">Chapter: <input type="text" value="{chapter}" class="chapter-input"></p>'

    if verse:
        html += f'<p class="verse">Verse: <input type="text" value="{verse}" class="verse-input"></p>'

    full_entry = entry.find('Entry').text if entry.find('Entry') is not None else ''
    if full_entry:
        html += f'<p class="full-entry">Entry: <input type="text" value="{full_entry}" class="entry-input"></p>'

    lemma_combined = [f'{text} {num}' for text, num in zip(lemma_texts, lemma_numbers)]
    if lemma_combined:
        html += f'<p class="lemma">Lemma: <input type="text" value="{", ".join(lemma_combined)}" class="lemma-input"></p>'

    reading_text = readings.find('Reading').text if readings is not None and readings.find(
        'Reading') is not None else ''
    if reading_text:
        html += f'<p class="reading">Reading: <input type="text" value="{reading_text}" class="reading-input"></p>'

    sigla_text = sigla.text if sigla is not None else ''
    if sigla_text:
        html += f'<p class="sigla">Sigla: <input type="text" value="{sigla_text}" class="sigla-input"></p>'

    if witness_texts:
        html += '<p class="witnesses">Witnesses:</p>'
        for witness in witness_texts:
            html += '<div class="witness">'
            if 'Manuscript' in witness:
                html += f'<p>Manuscript: <input type="text" value="{witness["Manuscript"]}" class="witness-manuscript-input"></p>'
            if 'Comment' in witness:
                html += f'<p>Comment: <input type="text" value="{witness["Comment"]}" class="witness-comment-input"></p>'
            html += '</div>'

    if references:
        html += f'<p class="references">References: <input type="text" value="{", ".join(references)}" class="references-input"></p>'

    comment_text = comments.text if comments is not None else ''
    if comment_text:
        html += f'<div class="comment-section"><label for="comment">Comment:</label><textarea class="comment-input">{comment_text}</textarea></div>'

    html += '''
        <div class="additional-cells">
            <button onclick="addCell(this)">Add Cell</button>
        </div>
    </div>
    '''
    return html


def convert_xml_to_html(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>TEI Document</title>
        <style>
            body { font-family: Arial, sans-serif; }
            .apparatus { margin: 20px; padding: 10px; border: 1px solid #ddd; }
            .apparatus h2 { margin-top: 0; }
            .chapter, .verse, .full-entry, .lemma, .reading, .sigla, .witness, .references, .comment-section { margin-left: 20px; }
            .lemma { font-weight: bold; }
            textarea, input { width: 100%; }
            .comment-section { margin-top: 10px; }
        </style>
    </head>
    <body>
        <h1>TEI Document</h1>
    '''

    for entry in root.findall('.//entry'):
        html_content += create_html_entry(entry)

    html_content += '''
        <button onclick="saveChanges()">Save Changes</button>
        <script>
            function saveChanges() {
                const entries = document.querySelectorAll('.apparatus');
                const data = Array.from(entries).map(entry => {
                    const additionalCells = Array.from(entry.querySelectorAll('.additional-cell')).map(cell => {
                        return {
                            title: cell.querySelector('.additional-title').value,
                            value: cell.querySelector('.additional-value').value
                        };
                    });
                    const witnesses = Array.from(entry.querySelectorAll('.witness')).map(witness => {
                        return {
                            Manuscript: witness.querySelector('.witness-manuscript-input').value,
                            Comment: witness.querySelector('.witness-comment-input').value
                        };
                    });
                    return {
                        entry: entry.querySelector('.entry-input').value,
                        chapter: entry.querySelector('.chapter-input').value,
                        verse: entry.querySelector('.verse-input').value,
                        lemma: entry.querySelector('.lemma-input').value,
                        reading: entry.querySelector('.reading-input').value,
                        sigla: entry.querySelector('.sigla-input').value,
                        witnesses: witnesses,
                        references: entry.querySelector('.references-input').value,
                        comment: entry.querySelector('.comment-input').value,
                        additionalCells: additionalCells
                    };
                });
                const json = JSON.stringify(data, null, 2);
                const blob = new Blob([json], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'comments_and_edits.json';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            }

            function addCell(button) {
                const container = button.parentNode;
                const cell = document.createElement('div');
                cell.className = 'additional-cell';
                cell.innerHTML = `
                    <input type="text" placeholder="Title" class="additional-title">
                    <input type="text" placeholder="Value" class="additional-value">
                    <button onclick="removeCell(this)">Remove</button>
                `;
                container.insertBefore(cell, button);
            }

            function removeCell(button) {
                const cell = button.parentNode;
                cell.remove();
            }
        </script>
    </body>
    </html>
    '''

    return html_content


# Generate HTML content from the provided XML file
html_output = convert_xml_to_html(xml_file_path)
html_output_path = 'editable_teidocument_2.html'

# Save the HTML content to a file
with open(html_output_path, 'w', encoding='utf-8') as f:
    f.write(html_output)

print(f'HTML file generated at: {html_output_path}')
