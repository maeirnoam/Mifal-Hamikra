<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0">
    
    <xsl:output method="html" indent="yes" encoding="UTF-8"/>
    
    <xsl:template match="/">
        <html>
            <head>
                <title>TEI Document</title>
                <style>
                    body { font-family: Arial, sans-serif; }
                    .apparatus { margin: 20px; padding: 10px; border: 1px solid #ddd; }
                    .apparatus h2 { margin-top: 0; }
                    .lemma, .reading, .witness, .note, .reference, .sigla {
                        margin-left: 20px;
                    }
                    .lemma { font-weight: bold; }
                </style>
            </head>
            <body>
                <h1>TEI Document</h1>
                <xsl:apply-templates/>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="tei:app">
        <div class="apparatus">
            <h2>Apparatus Entry</h2>
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <xsl:template match="tei:lem">
        <p class="lemma">Lemma: <xsl:value-of select="."/></p>
    </xsl:template>

    <xsl:template match="tei:rdg">
        <p class="reading">Reading: <xsl:value-of select="."/></p>
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="tei:wit">
        <p class="witness">Witness: <xsl:value-of select="."/></p>
    </xsl:template>

    <xsl:template match="tei:note">
        <p class="note">Note: <xsl:value-of select="."/></p>
    </xsl:template>

    <xsl:template match="tei:ref">
        <p class="reference">Reference: <xsl:value-of select="."/></p>
    </xsl:template>

    <xsl:template match="tei:seg[@type='sigla']">
        <p class="sigla">Sigla: <xsl:value-of select="."/></p>
    </xsl:template>
    
</xsl:stylesheet>
