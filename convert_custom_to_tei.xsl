<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tei="http://www.tei-c.org/ns/1.0">

    <!-- Output TEI XML format -->
    <xsl:output method="xml" indent="yes"/>

    <xsl:template match="/">
        <TEI xmlns="http://www.tei-c.org/ns/1.0">
            <teiHeader>
                <fileDesc>
                    <titleStmt>
                        <title>Converted TEI Document</title>
                    </titleStmt>
                    <publicationStmt>
                        <p>Generated from custom XML</p>
                    </publicationStmt>
                    <sourceDesc>
                        <p>Converted from custom format</p>
                    </sourceDesc>
                </fileDesc>
            </teiHeader>
            <text>
                <body>
                    <listApp>
                        <xsl:apply-templates select="processed_entries/entry"/>
                    </listApp>
                </body>
            </text>
        </TEI>
    </xsl:template>

    <xsl:template match="entry">
        <app>
            <xsl:attribute name="xml:id">
                <xsl:text>app-</xsl:text>
                <xsl:value-of select="LemmaInfo/Chapter"/>
                <xsl-text>-</xsl-text>
                <xsl:value-of select="@Number"/>
            </xsl:attribute>
            
            <xsl:if test="LemmaInfo/Verses">
                <xsl:attribute name="loc">
                    <xsl:value-of select="LemmaInfo/Verses"/>
                </xsl:attribute>
            </xsl:if>
            
            <xsl:if test="DecodedEntry/Rdg/from">
                <xsl:attribute name="from">
                    <xsl:value-of select="DecodedEntry/Rdg/from"/>
                </xsl:attribute>
            </xsl:if>
            
            <xsl:if test="DecodedEntry/Rdg/to">
                <xsl:attribute name="to">
                    <xsl:value-of select="DecodedEntry/Rdg/to"/>
                </xsl:attribute>
            </xsl:if>
            
            <!-- Lemma Handling -->
            <xsl:if test="LemmaInfo/Lemmas/Lemma">
                <lem>
                    <xsl:apply-templates select="LemmaInfo/Lemmas/Lemma/Text"/>
                </lem>
            </xsl:if>

            <!-- Readings -->
            <rdgGrp>
                <xsl:apply-templates select="DecodedEntry"/>
            </rdgGrp>
        </app>
    </xsl:template>

    <xsl:template match="LemmaInfo/Lemmas/Lemma/Text">
        <w><xsl:value-of select="."/></w>
    </xsl:template>

    <xsl:template match="DecodedEntry">
        <rdg>
            <xsl:if test="Details/Witnesses/Witness/Manuscript">
                <xsl:attribute name="wit">
                    <xsl:for-each select="Details/Witnesses/Witness/Manuscript">
                        <xsl:value-of select="."/>
                        <xsl:if test="position() != last()"> </xsl:if>
                    </xsl:for-each>
                </xsl:attribute>
            </xsl:if>
            
            <xsl:if test="Details/Rdg/Reading">
                <seg><xsl:value-of select="Details/Rdg/Reading"/></seg>
            </xsl:if>
        </rdg>
    </xsl:template>

</xsl:stylesheet>