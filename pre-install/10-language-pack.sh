#!/bin/sh
#
# Runs from /tmp/pre-install-scripts before the PrestaShop installer starts;
# docker_run.sh executes every file in that directory.
#
# Why this is needed: the installer downloads its language packs from
# i18n.prestashop-project.org, and that service currently does not serve the
# pack for the plain `en` iso at all (404) while the packs it does have stall
# mid-transfer. Installs therefore abort with
# `Cannot download language pack "en"`.
#
# Both download steps only run when a file is already missing:
#
#   translations/<iso>.gzip       Install.php:636 - existence check only, the
#                                 content is never read
#   translations/sf-<locale>.zip  Language::installSfLanguagePack() checks that
#                                 the file exists, extracts it and returns true
#                                 without validating what was extracted
#
# Pre-creating both files makes the installer skip the network altogether. The
# locale of the `en` language is `en-US` (install/langs/en/language.xml).
#
# The pack holds a single placeholder file: the English texts ship inside the
# image in translations/default/, which the extractor leaves as is. Point both
# files at a real pack if the upstream translations are wanted.
set -e

LOCALE=en-US
TRANSLATIONS=/var/www/html/translations

mkdir -p "$TRANSLATIONS"
touch "$TRANSLATIONS/en.gzip"

# The installer unpacks the pack with ZipArchive, so let ZipArchive write it:
# a hand-rolled empty zip is rejected by libzip, and an archive without a single
# entry is reported as written successfully while no file appears on disk.
cat > /tmp/make-language-pack.php <<'PHP'
<?php
$zip = new ZipArchive();
$zip->open('/var/www/html/translations/sf-en-US.zip', ZipArchive::CREATE | ZipArchive::OVERWRITE);
$zip->addFromString(
    'placeholder.txt',
    'Placeholder language pack, see pre-install/10-language-pack.sh in the repository.' . PHP_EOL
);
$zip->close();
PHP

php /tmp/make-language-pack.php
