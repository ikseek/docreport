from __future__ import absolute_import, print_function

from argparse import ArgumentParser, FileType
from itertools import chain
from subprocess import CalledProcessError
import os
import sys

from .formats import produce_csv, produce_html
from .report import ScriptRefReport, ManualReport

REPORT_FORMATS = {'csv': produce_csv, 'html': produce_html}


def script_ref_report(params_str):
    params = params_str.split(':')
    return ScriptRefReport(params[0], params[1])


def manual_report(params_str):
    params = params_str.split(':')
    return ManualReport(params[0], params[1])


def get_args():
    parser = ArgumentParser(description='Produce documentation state report')
    parser.add_argument('--scriptref', type=script_ref_report,
                        metavar="PATH:REV",
                        help='generate ScriptRef report for REV in REPO_PATH')
    parser.add_argument('--manual', type=manual_report, metavar="PATH:REV",
                        help='generate Manual report for REV in REPO_PATH')
    parser.add_argument('--format', choices=REPORT_FORMATS.keys(),
                        default='html', help='report format')
    parser.add_argument('OUTFILE', nargs='?', type=FileType('w'),
                        default=sys.stdout, help='output file name')
    args = parser.parse_args()
    if not args.scriptref and not args.manual:
        parser.error("Must request at least one report")
    return args


def main():
    args = get_args()
    try:
        reports = [r for r in (args.scriptref, args.manual) if r is not None]
        description = ", ".join(str(r) for r in reports)
        all_reports = chain(*reports)
        report_format = REPORT_FORMATS[args.format]
        for line in report_format(description, all_reports):
            print(line, file=args.OUTFILE)
        return os.EX_OK
    except CalledProcessError as e:
        print(e, e.output)
        return os.EX_SOFTWARE
