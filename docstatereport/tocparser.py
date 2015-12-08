import re


class TocParser:
    def __init__(self, tocfile):
        self.lookup = {}
        entry = None
        for indent, name, filename in TocParser._toc_entries(tocfile):
            entry = TocEntry(indent, name, filename, entry)
            self.lookup[entry.filename + '.md'] = entry

    def __getitem__(self, filename):
        return self.lookup[filename]

    def get_area(self, filename, default):
        entry = self.lookup.get(filename, None)
        return str(entry) if entry else default

    @staticmethod
    def _toc_entries(tocfile):
        tocline_template = re.compile(r'^( *)\* \[(.*)\]\((.*)\)')
        for line in tocfile:
            match = tocline_template.match(line)
            if match:
                yield match.groups()


class TocEntry:
    def __init__(self, indent, name, filename, prev_entry):
        self.indent = len(indent)
        self.name = name
        self.filename = filename
        self.parent = TocEntry._find_parent(self.indent, prev_entry)

    def __str__(self):
        if self.parent:
            return str(self.parent) + ":" + self.name
        else:
            return self.name

    @staticmethod
    def _find_parent(indent, prev_entry):
        if prev_entry is not None:
            if prev_entry.indent < indent:
                return prev_entry
            else:
                return TocEntry._find_parent(indent, prev_entry.parent)
        return prev_entry
