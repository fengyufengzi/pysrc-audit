'''
Created on 1 Sep 2011

@author: Francis
'''

from Auditer.pathutils import walkfiles
from optparse import OptionParser
import os
import sys

def countLines(filename):
    fname = os.path.realpath(filename)
    fp = open(fname, "r")
    try:
        lines = fp.readlines()
    finally:
        fp.close()
    count = 0
    blankLines = 0
    commentLines = 0
    docstringLines = 0
    ignore = False
    for line in lines:
        line = line.strip()
        if len(line)>0:
            #    Ignore comments:
            if line.startswith("#") is True:
                commentLines += 1
                continue
            #    Ignore docstrings:
            elif line.startswith("'''") is True or line.startswith('"""') is True:
                if ignore is True:
                    #    Currently ignoring docstrings - this is the end of the docstring!
                    ignore = False
                else:
                    #    This is the start if the docstring
                    ignore = True
            elif line.startswith("r'''") is True or line.startswith('r"""') is True:
                #    Start of the docstring for-sure!
                ignore = True
            if ignore is True:
                docstringLines += 1
            else:
                count += 1
        else:
            blankLines += 1
    _str = "%(F)s - [%(C)s, %(B)s, %(O)s, %(D)s]"%{"F":filename, "C":count, "D":docstringLines, "B":blankLines, "O":commentLines}
    return (_str, (count, blankLines, commentLines, docstringLines, len(lines)))

def linecount(paths, quiet=True, supportedTypes=[".py"], ignoreDirs=["ezPyCrypto", "rpyc", "pymysql"], dump=False):
    r"""
    @summary: Count the number of source-code lines in the code-base!
    """
    assert paths
    results = []
    failedCount = 0
    for path in paths:
        for filename in walkfiles(path, ignoreDirs=ignoreDirs, hiddenDirs=False):
            (_name, ext) = os.path.splitext(filename)
            if ext in supportedTypes:
                try:
                    results.append(countLines(filename))
                except:
                    failedCount += 1
    totalCount = 0
    absoluteTotal = 0
    totalDocstringLines = 0
    totalCommentLines = 0
    totalBlankLines = 0
    for result in results:
        (_str, (count, blankLines, commentLines, docstringLines, totalLines)) = result
        totalCount += count
        totalDocstringLines += docstringLines
        totalCommentLines += commentLines
        totalBlankLines += blankLines
        absoluteTotal += totalLines
        if quiet is False:
            print _str
    percentage = 0
    try:
        percentage = int((float(totalCount)/float(absoluteTotal))*100)
    except:
        percentage = "N/A"
    s = [""]
    s.append("Audited the code-base for line counts...")
    s.append("")
    s.append("Statistics:")
    s.append("Comment lines: %(N)s"%{"N":totalCommentLines})
    s.append("Docstring lines: %(N)s"%{"N":totalDocstringLines})
    s.append("Blank lines: %(N)s"%{"N":totalBlankLines})
    s.append("")
    s.append("Total: **%(T)s** from %(ABS)s - %(P)s%%"%{"T":totalCount, "ABS":absoluteTotal, "P":percentage})
    print "\r\n".join(s)
    return (totalCount, (absoluteTotal, percentage), (totalCommentLines, totalDocstringLines, totalBlankLines))

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-p", "--path", action="append", dest="path", 
        default=[os.path.dirname(sys.argv[0])], help="alternative path to recursively query.", metavar="PATH")
    parser.add_option("-q", "--quiet", action="store_true", dest="quiet", 
        default=False, help="quiet output (except the actual line-count!)", metavar="QUIET")
    parser.add_option("-l", "--loud", action="store_false", dest="quiet", 
        default=False, help="non-quiet output", metavar="LOUD")
    opts, _args = parser.parse_args()
    linecount(opts.path, opts.quiet, dump=True)
