
xquery version "3.1";

module namespace pm-config="http://www.tei-c.org/tei-simple/pm-config";

import module namespace pm-hubp-web="http://www.tei-c.org/pm/models/hubp/web/module" at "../transform/hubp-web-module.xql";
import module namespace pm-hubp-print="http://www.tei-c.org/pm/models/hubp/print/module" at "../transform/hubp-print-module.xql";
import module namespace pm-hubp-latex="http://www.tei-c.org/pm/models/hubp/latex/module" at "../transform/hubp-latex-module.xql";
import module namespace pm-hubp-epub="http://www.tei-c.org/pm/models/hubp/epub/module" at "../transform/hubp-epub-module.xql";
import module namespace pm-hubp-fo="http://www.tei-c.org/pm/models/hubp/fo/module" at "../transform/hubp-fo-module.xql";
import module namespace pm-docx-tei="http://www.tei-c.org/pm/models/docx/tei/module" at "../transform/docx-tei-module.xql";

declare variable $pm-config:web-transform := function($xml as node()*, $parameters as map(*)?, $odd as xs:string?) {
    switch ($odd)
    case "hubp.odd" return pm-hubp-web:transform($xml, $parameters)
    default return pm-hubp-web:transform($xml, $parameters)
            
    
};
            


declare variable $pm-config:print-transform := function($xml as node()*, $parameters as map(*)?, $odd as xs:string?) {
    switch ($odd)
    case "hubp.odd" return pm-hubp-print:transform($xml, $parameters)
    default return pm-hubp-print:transform($xml, $parameters)
            
    
};
            


declare variable $pm-config:latex-transform := function($xml as node()*, $parameters as map(*)?, $odd as xs:string?) {
    switch ($odd)
    case "hubp.odd" return pm-hubp-latex:transform($xml, $parameters)
    default return pm-hubp-latex:transform($xml, $parameters)
            
    
};
            


declare variable $pm-config:epub-transform := function($xml as node()*, $parameters as map(*)?, $odd as xs:string?) {
    switch ($odd)
    case "hubp.odd" return pm-hubp-epub:transform($xml, $parameters)
    default return pm-hubp-epub:transform($xml, $parameters)
            
    
};
            


declare variable $pm-config:fo-transform := function($xml as node()*, $parameters as map(*)?, $odd as xs:string?) {
    switch ($odd)
    case "hubp.odd" return pm-hubp-fo:transform($xml, $parameters)
    default return pm-hubp-fo:transform($xml, $parameters)
            
    
};
            


declare variable $pm-config:tei-transform := function($xml as node()*, $parameters as map(*)?, $odd as xs:string?) {
    switch ($odd)
    case "docx.odd" return pm-docx-tei:transform($xml, $parameters)
    default return error(QName("http://www.tei-c.org/tei-simple/pm-config", "error"), "No default ODD found for output mode tei")
            
    
};
            
    