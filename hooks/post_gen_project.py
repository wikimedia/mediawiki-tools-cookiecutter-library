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

import datetime
import json
import os
import pathlib
import re
import shutil
import string
import subprocess

_TEMPLATE_ROOT = pathlib.Path('{{ cookiecutter._repo_dir }}')
with open(_TEMPLATE_ROOT / 'composer.json') as f:
    DEPENDENCIES = json.load(f)['require-dev']
LICENSES = 'licenses'


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


def replace_variable(fname, find, replace):
    with open(fname, 'r') as f:
        text = f.read()

    text = text.replace('!!%s!!' % find, replace)

    with open(fname, 'w') as f:
        f.write(text)


def main():
    for fname in ['composer.json', 'README.md']:
        replace_variable(
            fname,
            'COMPOSER_NAME',
            'wikimedia/' + composerify_name('{{ cookiecutter.library_name }}')
        )

    for dep, version in DEPENDENCIES.items():
        subprocess.call([
            'composer', 'require', '%s:%s' % (dep, version),
            '--dev', '--no-update'
        ])

    license = '{{ cookiecutter.license }}'
    license_fname = 'LICENSE'
    if license in ['Apache-2.0', 'MIT']:
        license_file = license + '.txt'
    elif license.startswith('GPL-2.0'):
        license_file = 'GPL-2.0.txt'
        license_fname = 'COPYING'
    elif license.startswith('GPL-3.0'):
        license_file = 'GPL-3.0.txt'
        license_fname = 'COPYING'
    else:
        license_file = 'placeholder.txt'

    # Copy the correct license to COPYING/LICENSE
    shutil.copy(os.path.join(LICENSES, license_file), license_fname)
    # Then delete the rest of the stock licenses
    shutil.rmtree(LICENSES)
    # Replace copyright variables in license
    replace_variable(license_fname,
                     'AUTHOR_NAME', '{{ cookiecutter.author_name }}')
    replace_variable(license_fname,
                     'AUTHOR_EMAIL', '{{ cookiecutter.author_email }}')
    replace_variable(license_fname, 'YEAR', str(datetime.date.today().year))


if __name__ == '__main__':
    main()
