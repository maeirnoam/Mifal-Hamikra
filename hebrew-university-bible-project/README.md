# Hebrew University Bible Project

This repository holds the code and assets required to publish the prototype for the Hebrew University Bible Project on eXist-db platform.
This app has been initially generated with TEI Publisher.

## Demo

[dh-lab](https://dh-lab.teipublisher.com/exist/apps/hubp)

## Local installation

1. Clone or pull the most recent version of this repository
1. Build xar package with Ant
1. Deploy to eXist-db (v. 6.2.0 or later) via Dashboard > Package Manager

### Troubleshooting

If there's a problem with resolving links and API calls on the server, the context-path setting in `modules/config.xqm` may need adjustment. NB commented out parts.

```xquery
declare variable $config:context-path :=
(:    let $prop := util:system-property("teipublisher.context-path"):)
(:    return:)
(:        if (exists($prop)) then:)
(:            if ($prop = "auto") then:)
(:                request:get-context-path() || substring-after($config:app-root, "/db") :)
(:            else:)
(:                $prop:)
(:        else if (exists(request:get-header("X-Forwarded-Host"))):)
(:            then "":)
(:        else:)
       request:get-context-path() || substring-after($config:app-root, "/db")
;

```

## Support

Use the [issue tracker](https://gitlab.existsolutions.com/hebrew-university/hebrew-university-bible-project/-/issues) to register bugs, problems and feature requests.

## Roadmap

Some of the features considered for the future include:

* coverage of other apparatus layers (I, II, IV, V, VI)
* presentation of verse and chapter information
* TOC and intra-document navigation
* UI/UX redesign of user interactions (perhaps dynamic layout)
* interactive elements (tooltips for witnessess and cross-referenced sections), switch/toggle features like original/stripped spelling
* visual theme
* responsiveness and accessibility
* factoring out data collection into separate app and data organization
* formal schema for validation and constraint checks

## Authors and acknowledgment

This app has been developed primarily by Magdalena Turska, based on the TEI Publisher frameworks, authored primarily by Wolfgang Meier.
Data samples were provided by Noam Meir.

## License

This project is licensed under the GNU Affero General Public License v3.0. See [more](https://www.gnu.org/licenses/agpl-3.0.txt). In short this means you can use and publish it as you like, including any modifications, but you MUST:

* prominently attribute this work and authors
* make a prominent note of the date and scope of any of the modifications
* release your results to the public under the same license.

## Project status

As of March 2025 the first iteration of the project comes to an end. Further work may be carried as additional funding is granted.

## Localization

Basic localization is available for numerous languages through default TEI Publisher localization. Hebrew localization might be contributed via https://crowdin.com/project/tei-publisher.

Localization of custom labels has not been realized. It might be added based on `{language-code}.json`, e.g. `en.json` localization files in JSON format, available in `resources/i18n/app` subcollection of this repository. Structure of this files would need to corresponds to `key` values of `<pb-i18n>` custom web components used in this app's HTML templates.

Cf. TEI Publisher documentation for general principles and typical solutions regarding i18n for TEI Publisher projects.

## HTML layout templates and styling 

For document view this app uses custom template, stored in `templates/pages/hubp.html`. No significant consideration has been given into user interface and experience design. **No** consideration at all has been given to visual identification of the project and aesthetics.

Only a small bunch of ODD-related CSS classes has been defined, in `resources/odd/hubp.css`.