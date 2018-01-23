#!/usr/bin/env python3
"""
Runs after cookiecutter has created the basic files
Copyright (C) 2017 Kunal Mehta <legoktm@member.fsf.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import re
import string
import subprocess

DEPENDENCIES = {
    # Would be nice if we didnt need to hardcode these...
    'jakub-onderka/php-parallel-lint': '0.9.2',
    'jakub-onderka/php-console-highlighter': '0.3.2',
    'mediawiki/mediawiki-codesniffer': '15.0.0',
    'mediawiki/minus-x': '0.2.1',
    'phpunit/phpunit': '4.8.36',
}

for dep, version in DEPENDENCIES.items():
    subprocess.call([
        'composer', 'require', '%s:%s' % (dep, version),
        '--dev', '--no-update'
    ])


# Set composer_name properly
library_name = '{{ cookiecutter.library_name }}'


def composerify_name(name):
    sp = re.split('([%s])' % string.ascii_uppercase, name)
    new = ''
    for part in sp:
        if part == '':
            continue
        if part.isupper():
            if new != '':
                new += '-'
            new += part.lower()
        else:
            new += part

    return new


with open('composer.json', 'r') as f:
    text = f.read()

text = text.replace(
    '!!COMPOSER_NAME!!',
    'wikimedia/' + composerify_name(library_name)
)

with open('composer.json', 'w') as f:
    f.write(text)
