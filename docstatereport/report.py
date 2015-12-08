import contextlib
import os
import re
from collections import namedtuple
from subprocess import check_output, STDOUT

from .tocparser import TocParser

FileInfo = namedtuple(
    'FileInfo', ['type', 'area', 'file_name', 'change_author', 'change_date'])


class DocReport(object):
    def __init__(self, repo, revision):
        self.repo = repo
        self.revision = revision

    def __iter__(self):
        for file in self.list_revision_files():
            if self.is_documentation_file(file):
                change_date_author = self.get_change_date_author(file)
                yield FileInfo(self.type,
                               self.area(file),
                               file,
                               change_date_author[0],
                               change_date_author[1])

    def list_revision_files(self):
        return run_hg(self.repo, 'manifest', '-r', self.revision)

    def get_change_date_author(self, file):
        return run_hg(self.repo, 'parent', '-r', self.revision, file,
                      '-T', '{author}\n{date|shortdate}\n')

    def __str__(self):
        return "{} ({})".format(self.type, self.revision)


class ScriptRefReport(DocReport):
    type = 'Script Reference'

    @staticmethod
    def is_documentation_file(file):
        return re.search(r'\.mem\.xml$', file)

    def area(self, file):
        path_components = file.split(os.sep)
        return ":".join(path_components[1:-1])


class ManualReport(DocReport):
    type = 'Manual'

    def __init__(self, repo, revision):
        super(ManualReport, self).__init__(repo, revision)
        self.toc = TocParser(run_hg(self.repo,
                                    'cat', 'content/md/TableOfContents.md',
                                    '-r', self.revision))

    @staticmethod
    def is_documentation_file(file):
        return re.search(r'\.md$', file)

    def area(self, file):
        return self.toc.get_area(os.path.basename(file), 'Unknown')


def run_hg(path, *args):
    with working_directory(path):
        out = check_output(['hg'] + list(args),
                           stderr=STDOUT, universal_newlines=True)
        return out.split('\n')


@contextlib.contextmanager
def working_directory(path):
    """A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit.

    """
    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)
