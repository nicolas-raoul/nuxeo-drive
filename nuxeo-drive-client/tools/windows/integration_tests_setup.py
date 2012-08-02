r"""Setup the windows machine for Continuous Integration on the MSI package

This will:

    - download the latest nightly build of Nuxeo from Jenkins
    - deploy the server side package of nuxeo-drive (TODO)
    - start the server
    - setup test environment variables
    - download http://code.google.com/p/lessmsi if not already there
    - extract the MSI archive in a local, non system folder with lessmsi
    - launch the ``ndrive test`` command to run the integration tests
    - stop the server and collect the logs

Get the help on running this with::

    C:\Python27\python tools\windows\integration_tests_setup.py --help

"""

import urllib2
import argparse
import re

DEFAULT_MSI = r"dist\nuxeo-drive-0.1.0-win32.msi"
DEFAULT_NUXEO_ARCHIVE_URL=("http://qa.nuxeo.org/jenkins/job/IT-nuxeo-master-build/"
                           "lastSuccessfulBuild/artifact/archives/")
DEFAULT_LESSMSI_URL="http://lessmsi.googlecode.com/files/lessmsi-v1.0.8.zip"
DEFAULT_ARCHIVE_PATTERN=r"nuxeo-cap-\d\.\d-I\d+_\d+-tomcat\.zip"


def parse_args(args=None):
    parser = argparse.ArgumentParser(
        description="Launch integration tests on Windows")

    parser.add_argument("--msi", default=DEFAULT_MSI)
    parser.add_argument("--nuxeo-archive-url",
                        default=DEFAULT_NUXEO_ARCHIVE_URL)
    parser.add_argument("--lessmsi-url", default=DEFAULT_LESSMSI_URL)

    return parser.parse_args(args)


def setup_nuxeo(nuxeo_archive_url):
    print "Finding latest nuxeo ZIP archive at: " + nuxeo_archive_url
    index_html = urllib2.urlopen(nuxeo_archive_url).read()
    filenames = re.compile(DEFAULT_ARCHIVE_PATTERN).findall(index_html)
    if not filenames:
        raise ValueError("Could not find ZIP archives on " + nuxeo_archive_url)
    filenames.sort()
    filename = filenames[0]
    file_url = nuxeo_archive_url + filename
    print "Downloading: " + file_url
    reader = urllib2.urlopen(file_url)
    with open(filename, 'wb') as f:
        while True:
            b = reader.read(1000 ** 2)
            if b == '':
                break
            f.write(b)

    # TODO: skip wizard


if __name__ == "__main__":
    options = parse_args()
    setup_nuxeo(options.nuxeo_archive_url)