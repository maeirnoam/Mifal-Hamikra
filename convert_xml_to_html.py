import xml.etree.ElementTree as ET

# Load the provided XML file
xml_file_path = 'Apparatus III Encoding 2.xml'

def create_html_entry(entry):
    lemma_info = entry.find('LemmaInfo')
    chapter = lemma_info.find('Chapter').text if lemma_info.find('Chapter') is not None else ''
    verses = lemma_info.find('Verses')
    verse = verses.text if verses is not None and verses.text else ''
    verse_from = verses.find('From').text if verses is not None and verses.find('From') is not None else ''
    verse_to = verses.find('To').text if verses is not None and verses.find('To') is not None else ''
    entry_number = entry.get('Number')

    lemmas = lemma_info.find('Lemmas') if lemma_info is not None else None
    lemma_texts = []
    lemma_numbers = []
    lemma_ks = []
    lemma_qs = []
    if lemmas:
        for lemma in lemmas.findall('Lemma'):
            text = lemma.find('Text').text if lemma.find('Text') is not None else ''
            k_value = lemma.find('K').text if lemma.find('K') is not None else ''
            q_value = lemma.find('Q').text if lemma.find('Q') is not None else ''
            number = lemma.find('Number').text if lemma.find('Number') is not None else ''
            lemma_texts.append(text.strip())
            if k_value:
                lemma_ks.append((text.strip(), k_value.strip()))
            if q_value:
                lemma_qs.append((text.strip(), q_value.strip()))
            if number:
                lemma_numbers.append(number.strip())

    from_lemmas = lemma_info.find('./Lemmas/From') if lemma_info.find('./Lemmas/From') is not None else None
    to_lemmas = lemma_info.find('./Lemmas/To') if lemma_info.find('./Lemmas/To') is not None else None

    from_lemma_texts = [lemma.find('Text').text if lemma.find('Text') is not None else '' for lemma in from_lemmas] if from_lemmas is not None else []
    to_lemma_texts = [lemma.find('Text').text if lemma.find('Text') is not None else '' for lemma in to_lemmas] if to_lemmas is not None else []

    html = f'''
    <div class="apparatus" data-entry-number="{entry_number}">
        <h2>Apparatus Entry Number {entry_number}</h2>
    '''

    def add_field(label, value, field_class):
        return f'''
        <div class="field">
            <label>{label}:</label>
            <input type="text" value="{value}" class="{field_class}-input" data-title="{label}" data-status="original" readonly dir="rtl">
            <button type="button" onclick="enableEdit(this)">Edit</button>
            <button type="button" onclick="markDeleted(this)">Mark for Deletion</button>
            <div class="additional-cells">
                <button type="button" onclick="addCell(this)">Add Cell</button>
            </div>
        </div>
        '''

    if chapter:
        html += add_field("Chapter", chapter, "chapter")

    if verse:
        html += add_field("Verse", verse, "verse")

    if verse_from:
        html += add_field("Verse From", verse_from, "verse-from")

    if verse_to:
        html += add_field("Verse To", verse_to, "verse-to")

    full_entry = entry.find('Entry').text if entry.find('Entry') is not None else ''
    if full_entry:
        html += add_field("Entry", full_entry, "entry")

    if lemma_texts:
        html += add_field("Lemma", ", ".join(lemma_texts), "lemma")

    if lemma_numbers:
        html += add_field("Lemma Numbers", ", ".join(lemma_numbers), "lemma-numbers")

    if from_lemma_texts:
        html += add_field("From Lemma", ", ".join(from_lemma_texts), "from-lemma")

    if to_lemma_texts:
        html += add_field("To Lemma", ", ".join(to_lemma_texts), "to-lemma")

    if lemma_ks:
        html += f'''
        <div class="field">
            <label>Lemma K:</label>
            <input type="text" value="{", ".join([f'{text}' for text, k in lemma_ks])}" class="lemma-k-input" data-title="lemma_k">
            <button type="button" onclick="enableEdit(this)">Edit</button>
            <button type="button" onclick="markDeleted(this)">Mark for Deletion</button>
            <div class="additional-cells">
                <button onclick="addCell(this)">Add Cell</button>
            </div>
        </div>
        '''

    if lemma_qs:
        html += f'''
        <div class="field">
            <label>Lemma Q:</label>
            <input type="text" value="{", ".join([f'{text}' for text, q in lemma_qs])}" class="lemma-q-input" data-title="lemma_q">
            <button type="button" onclick="enableEdit(this)">Edit</button>
            <button type="button" onclick="markDeleted(this)">Mark for Deletion</button>
            <div class="additional-cells">
                <button onclick="addCell(this)">Add Cell</button>
            </div>
        </div>
        '''

    for decoded_entry in entry.findall('DecodedEntry'):
        type_ = decoded_entry.find('Type').text if decoded_entry.find('Type') is not None else ''
        details = decoded_entry.find('Details')
        witnesses = details.find('Witnesses') if details is not None else None
        readings = details.find('Rdg') if details is not None else None
        general_comments = readings.find('GeneralComment') if readings is not None else None
        sigla = readings.find('Sigla').text if readings is not None and readings.find('Sigla') is not None else ''
        reading_text = readings.find('Reading').text if readings is not None and readings.find('Reading') is not None else ''

        cross_references = details.find('CrossReferences') if details is not None else None
        references = [ref.text if ref is not None else '' for ref in cross_references.findall('Reference')] if cross_references is not None else []

        witness_texts = [
            {
                'Collection': witness.find('Collection').text if witness.find('Collection') is not None else '',
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

        if type_:
            html += add_field("Type", type_, "type")

        if reading_text:
            html += add_field("Reading", reading_text, "reading")

        if sigla:
            html += add_field("Sigla", sigla, "sigla")

        if witness_texts:
            html += '<div class="field"><label>Witnesses:</label>'
            for witness in witness_texts:
                html += '<div class="witness">'
                if 'Collection' in witness:
                    html += add_field("Collection", witness["Collection"], "witness-collection")
                if 'Manuscript' in witness:
                    html += add_field("Manuscript", witness["Manuscript"], "witness-manuscript")
                if 'Comment' in witness:
                    html += add_field("Comment", witness["Comment"], "witness-comment")
                html += '</div>'
            html += '</div>'

        if references:
            html += add_field("References", ", ".join(references), "references")

        general_comment_text = general_comments.text if general_comments is not None else ''
        if general_comment_text:
            html += f'''
            <div class="field">
                <label>General Comment:</label>
                <textarea class="general-comment-input" data-title="General Comment" data-status="original" readonly>{general_comment_text}</textarea>
                <button type="button" onclick="enableEdit(this)">Edit</button>
                <button type="button" onclick="markDeleted(this)">Mark for Deletion</button>
                <div class="additional-cells">
                    <button type="button" onclick="addCell(this)">Add Cell</button>
                </div>
            </div>
            '''
        html += '</div>'

    html += '''
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
            .field { margin-left: 20px; }
            .field label { display: block; font-weight: bold; margin-bottom: 5px; }
            .field input, .field textarea { width: 100%; }
            .comment-section { margin-top: 10px; }
            .deleted { text-decoration: line-through; }
            .readonly { background-color: #f0f0f0; border: none; }
        </style>
    </head>
    <body>
        <h1>TEI Document</h1>
    '''

    for entry in root.findall('.//entry'):
        html_content += create_html_entry(entry)
#<button onclick="midwaySave()">Midway Save</button>
    html_content += '''
        <button onclick="saveChanges()">Save Changes</button>
        
        <script>
            function enableEdit(button) {
                const input = button.parentNode.querySelector('input, textarea');
                input.removeAttribute('readonly');
                input.classList.add('edited');
                input.dataset.status = 'edited';
                input.focus();
            }


            function markDeleted(button) {
                const input = button.parentNode.querySelector('input, textarea');
                input.dataset.status = 'deleted';
                input.classList.add('deleted');
                input.style.textDecoration = 'line-through';
            }


            function addCell(button) {
                const container = button.parentNode;
                const cell = document.createElement('div');
                cell.className = 'additional-cell';
                cell.innerHTML = `
                    <input type="text" placeholder="New Cell" class="additional-title">
                    <input type="text" placeholder="New Value" class="additional-value" data-status="added">
                    <button type="button" onclick="removeCell(this)">Remove</button>
                `;
                container.insertBefore(cell, button);
            }

            function removeCell(button) {
                const cell = button.parentNode;
                cell.remove();
            }

            function collectData() {
                const entries = document.querySelectorAll('.apparatus');
                return Array.from(entries).map(entry => {
                    const entryNumber = entry.getAttribute('data-entry-number'); // Capture the entry number
            
                    const additionalCells = Array.from(entry.querySelectorAll('.additional-cell')).map(cell => {
                        return {
                            title: cell.querySelector('.additional-title') ? cell.querySelector('.additional-title').value : '',
                            value: cell.querySelector('.additional-value') ? cell.querySelector('.additional-value').value : '',
                            status: cell.querySelector('.additional-value').dataset.status || 'original'
                        };
                    });
                    
                    const fields = Array.from(entry.querySelectorAll('.field input, .field textarea')).map(field => {
                        if (field.dataset.title) {
                            return {
                                title: field.dataset.title,
                                value: field.value,
                                status: field.dataset.status || 'original'
                            };
                        }
                    }).filter(Boolean);
                    
                    const variants = Array.from(entry.querySelectorAll('.variant')).map(variant => {
                        const witnesses = Array.from(variant.querySelectorAll('.witness')).map(witness => {
                            return {
                                Collection: witness.querySelector('.witness-collection-input') ? witness.querySelector('.witness-collection-input').value : '',
                                Manuscript: witness.querySelector('.witness-manuscript-input') ? witness.querySelector('.witness-manuscript-input').value : '',
                                Comment: witness.querySelector('.witness-comment-input') ? witness.querySelector('.witness-comment-input').value : '',
                                status: witness.querySelector('.witness-collection-input') && witness.querySelector('.witness-collection-input').dataset.status ? witness.querySelector('.witness-collection-input').dataset.status : 'original'
                            };
                        });
                        return {
                            type: {
                                text: variant.querySelector('.type-input') ? variant.querySelector('.type-input').value : '',
                                status: variant.querySelector('.type-input') && variant.querySelector('.type-input').dataset.status ? variant.querySelector('.type-input').dataset.status : 'original'
                            },
                            reading: {
                                text: variant.querySelector('.reading-input') ? variant.querySelector('.reading-input').value : '',
                                status: variant.querySelector('.reading-input') && variant.querySelector('.reading-input').dataset.status ? variant.querySelector('.reading-input').dataset.status : 'original'
                            },
                            sigla: {
                                text: variant.querySelector('.sigla-input') ? variant.querySelector('.sigla-input').value : '',
                                status: variant.querySelector('.sigla-input') && variant.querySelector('.sigla-input').dataset.status ? variant.querySelector('.sigla-input').dataset.status : 'original'
                            },
                            witnesses: witnesses,
                            references: {
                                text: variant.querySelector('.references-input') ? variant.querySelector('.references-input').value : '',
                                status: variant.querySelector('.references-input') && variant.querySelector('.references-input').dataset.status ? variant.querySelector('.references-input').dataset.status : 'original'
                            },
                            general_comment: {
                                text: variant.querySelector('.general-comment-input') ? variant.querySelector('.general-comment-input').value : '',
                                status: variant.querySelector('.general-comment-input') && variant.querySelector('.general-comment-input').dataset.status ? variant.querySelector('.general-comment-input').dataset.status : 'original'
                            },
                            status: variant.classList.contains('edited') ? 'edited' : 'original'
                        };
                    });
                    
                    const result = {
                        entry_number: entryNumber, // Add entry number to the result
                        entry: {
                            text: entry.querySelector('.entry-input') ? entry.querySelector('.entry-input').value : '',
                            status: entry.querySelector('.entry-input') && entry.querySelector('.entry-input').dataset.status ? entry.querySelector('.entry-input').dataset.status : 'original'
                        },
                        chapter: {
                            text: entry.querySelector('.chapter-input') ? entry.querySelector('.chapter-input').value : '',
                            status: entry.querySelector('.chapter-input') && entry.querySelector('.chapter-input').dataset.status ? entry.querySelector('.chapter-input').dataset.status : 'original'
                        },
                        verse: {
                            text: entry.querySelector('.verse-input') ? entry.querySelector('.verse-input').value : '',
                            status: entry.querySelector('.verse-input') && entry.querySelector('.verse-input').dataset.status ? entry.querySelector('.verse-input').dataset.status : 'original'
                        },
                        verse_from: {
                            text: entry.querySelector('.verse-from-input') ? entry.querySelector('.verse-from-input').value : '',
                            status: entry.querySelector('.verse-from-input') && entry.querySelector('.verse-from-input').dataset.status ? entry.querySelector('.verse-from-input').dataset.status : 'original'
                        },
                        verse_to: {
                            text: entry.querySelector('.verse-to-input') ? entry.querySelector('.verse-to-input').value : '',
                            status: entry.querySelector('.verse-to-input') && entry.querySelector('.verse-to-input').dataset.status ? entry.querySelector('.verse-to-input').dataset.status : 'original'
                        },
                        number: {
                            text: entry.querySelector('.number-input') ? entry.querySelector('.number-input').value : '',
                            status: entry.querySelector('.number-input') && entry.querySelector('.number-input').dataset.status ? entry.querySelector('.number-input').dataset.status : 'original'
                        },
                        lemma: {
                            text: entry.querySelector('.lemma-input') ? entry.querySelector('.lemma-input').value : '',
                            status: entry.querySelector('.lemma-input') && entry.querySelector('.lemma-input').dataset.status ? entry.querySelector('.lemma-input').dataset.status : 'original'
                        },
                        lemma_numbers: {
                            text: entry.querySelector('.lemma-numbers-input') ? entry.querySelector('.lemma-numbers-input').value : '',
                            status: entry.querySelector('.lemma-numbers-input') && entry.querySelector('.lemma-numbers-input').dataset.status ? entry.querySelector('.lemma-numbers-input').dataset.status : 'original'
                        },
                        from_lemma: {
                            text: entry.querySelector('.from-lemma-input') ? entry.querySelector('.from-lemma-input').value : '',
                            status: entry.querySelector('.from-lemma-input') && entry.querySelector('.from-lemma-input').dataset.status ? entry.querySelector('.from-lemma-input').dataset.status : 'original'
                        },
                        to_lemma: {
                            text: entry.querySelector('.to-lemma-input') ? entry.querySelector('.to-lemma-input').value : '',
                            status: entry.querySelector('.to-lemma-input') && entry.querySelector('.to-lemma-input').dataset.status ? entry.querySelector('.to-lemma-input').dataset.status : 'original'
                        },
                        variants: variants,
                        additionalCells: additionalCells,
                        general_comment: {
                            text: entry.querySelector('.general-comment-input') ? entry.querySelector('.general-comment-input').value : '',
                            status: entry.querySelector('.general-comment-input') && entry.querySelector('.general-comment-input').dataset.status ? entry.querySelector('.general-comment-input').dataset.status : 'original'
                        },
                        status: entry.dataset.status || 'original'
                    };
                    // Add fields to the result
                    fields.forEach(field => {
                        if (field) {
                            result[field.title.toLowerCase().replace(/\s+/g, '_')] = {
                                text: field.value,
                                status: field.status
                            };
                        }
                    });
                    return result;
                });
            }

            
            function saveChanges() {
                const data = collectData();
                const json = JSON.stringify(data, null, 2);
                console.log(json);  // Log the JSON to the console for debugging
                const blob = new Blob([json], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'comments_and_edits.json';
                a.click();
            }


    
            function midwaySave() {
                const data = collectData();
                localStorage.setItem('teiDocumentState', JSON.stringify(data));
                alert('Progress saved!');
            }
    
            function loadSavedState() {
                const savedData = localStorage.getItem('teiDocumentState');
                if (savedData) {
                    const data = JSON.parse(savedData);
                    data.forEach((entry, index) => {
                        const entryElement = document.querySelector(`.apparatus[data-entry-number="${entry.entry.text}"]`);
                        if (entryElement) {
                            Object.keys(entry).forEach(key => {
                                const field = entry[key];
                                if (key !== 'variants' && key !== 'additionalCells' && key !== 'status') {
                                    const input = entryElement.querySelector(`.${key}-input`);
                                    if (input) {
                                        input.value = field.text;
                                        input.dataset.status = field.status;
                                        if (field.status === 'deleted') {
                                            input.classList.add('deleted');
                                            input.style.textDecoration = 'line-through';
                                        } else if (field.status === 'edited') {
                                            input.classList.add('edited');
                                        }
                                    }
                                } else if (key === 'variants') {
                                    entry.variants.forEach((variant, variantIndex) => {
                                        const variantElement = entryElement.querySelectorAll('.variant')[variantIndex];
                                        if (variantElement) {
                                            Object.keys(variant).forEach(variantKey => {
                                                const variantField = variant[variantKey];
                                                const variantInput = variantElement.querySelector(`.${variantKey}-input`);
                                                if (variantInput) {
                                                    variantInput.value = variantField.text;
                                                    variantInput.dataset.status = variantField.status;
                                                    if (variantField.status === 'deleted') {
                                                        variantInput.classList.add('deleted');
                                                        variantInput.style.textDecoration = 'line-through';
                                                    } else if (variantField.status === 'edited') {
                                                        variantInput.classList.add('edited');
                                                    }
                                                }
                                            });
                                        }
                                    });
                                } else if (key === 'additionalCells') {
                                    entry.additionalCells.forEach(cell => {
                                        const additionalCell = document.createElement('div');
                                        additionalCell.className = 'additional-cell';
                                        additionalCell.innerHTML = `
                                            <input type="text" value="${cell.title}" class="additional-title">
                                            <input type="text" value="${cell.value}" class="additional-value" data-status="${cell.status}">
                                            <button type="button" onclick="removeCell(this)">Remove</button>
                                        `;
                                        entryElement.querySelector('.additional-cells').insertBefore(additionalCell, entryElement.querySelector('.additional-cells button'));
                                    });
                                }
                            });
                        }
                    });
                    alert('Progress loaded!');
                }
            }

            window.onload = loadSavedState;

        </script>
    </body>
    </html>
    '''

    return html_content

# Generate HTML content from the provided XML file
html_output = convert_xml_to_html(xml_file_path)
html_output_path = 'editable_teidocument.html'

# Save the HTML content to a file
with open(html_output_path, 'w', encoding='utf-8') as f:
    f.write(html_output)

print(f'HTML file generated at: {html_output_path}')
