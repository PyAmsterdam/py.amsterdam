"""
Extracted from sphinx.writers.text
"""

import math
import re
import textwrap
from itertools import chain, groupby
from typing import cast

from docutils import writers
from docutils.utils import column_width
from .conf import MAXWIDTH


class Cell:
    """Represents a cell in a table.
    It can span on multiple columns or on multiple lines.
    """

    def __init__(self, text="", rowspan=1, colspan=1):
        self.text = text
        self.wrapped = []  # type: List[str]
        self.rowspan = rowspan
        self.colspan = colspan
        self.col = None
        self.row = None

    def __repr__(self):
        return "<Cell {!r} {}v{}/{}>{}>".format(
            self.text, self.row, self.rowspan, self.col, self.colspan
        )

    def __hash__(self):
        return hash((self.col, self.row))

    def wrap(self, width):
        self.wrapped = my_wrap(self.text, width)


class Table:
    """Represents a table, handling cells that can span on multiple lines
    or rows, like::

       +-----------+-----+
       | AAA       | BBB |
       +-----+-----+     |
       |     | XXX |     |
       |     +-----+-----+
       | DDD | CCC       |
       +-----+-----------+

    This class can be used in two ways:

    - Either with absolute positions: call ``table[line, col] = Cell(...)``,
      this overwrite an existing cell if any.

    - Either with relative positions: call the ``add_row()`` and
      ``add_cell(Cell(...))`` as needed.

    Cell spanning on multiple rows or multiple columns (having a
    colspan or rowspan greater than one) are automatically referenced
    by all the table cells they covers. This is a usefull
    representation as we can simply check ``if self[x, y] is self[x,
    y+1]`` to recognize a rowspan.

    Colwidth is not automatically computed, it has to be given, either
    at construction time, either during the table construction.

    Example usage::

       table = Table([6, 6])
       table.add_cell(Cell("foo"))
       table.add_cell(Cell("bar"))
       table.set_separator()
       table.add_row()
       table.add_cell(Cell("FOO"))
       table.add_cell(Cell("BAR"))
       print(table)
       +--------+--------+
       | foo    | bar    |
       |========|========|
       | FOO    | BAR    |
       +--------+--------+

    """

    def __init__(self, colwidth=None):
        self.lines = []  # type: List[List[Cell]]
        self.separator = 0
        self.colwidth = colwidth if colwidth is not None else []  # type: List[int]
        self.current_line = 0
        self.current_col = 0

    def add_row(self):
        """Add a row to the table, to use with ``add_cell()``.  It is not needed
        to call ``add_row()`` before the first ``add_cell()``.
        """
        self.current_line += 1
        self.current_col = 0

    def set_separator(self):
        """Sets the separator below the current line.
        """
        self.separator = len(self.lines)

    def add_cell(self, cell):
        """Add a cell to the current line, to use with ``add_row()``.  To add
        a cell spanning on multiple lines or rows, simply set the
        ``cell.colspan`` or ``cell.rowspan`` BEFORE inserting it to
        the table.
        """
        while self[self.current_line, self.current_col]:
            self.current_col += 1
        self[self.current_line, self.current_col] = cell
        self.current_col += cell.colspan

    def __getitem__(self, pos):
        line, col = pos
        self._ensure_has_line(line + 1)
        self._ensure_has_column(col + 1)
        return self.lines[line][col]

    def __setitem__(self, pos, cell):
        line, col = pos
        self._ensure_has_line(line + cell.rowspan)
        self._ensure_has_column(col + cell.colspan)
        for dline in range(cell.rowspan):
            for dcol in range(cell.colspan):
                self.lines[line + dline][col + dcol] = cell
                cell.row = line
                cell.col = col

    def _ensure_has_line(self, line):
        while len(self.lines) < line:
            self.lines.append([])

    def _ensure_has_column(self, col):
        for line in self.lines:
            while len(line) < col:
                line.append(None)

    def __repr__(self):
        return "\n".join(repr(line) for line in self.lines)

    def cell_width(self, cell, source):
        """Give the cell width, according to the given source (either
        ``self.colwidth`` or ``self.measured_widths``).
        This take into account cells spanning on multiple columns.
        """
        width = 0
        for i in range(self[cell.row, cell.col].colspan):
            width += source[cell.col + i]
        return width + (cell.colspan - 1) * 3

    @property
    def cells(self):
        seen = set()  # type: Set[Cell]
        for lineno, line in enumerate(self.lines):
            for colno, cell in enumerate(line):
                if cell and cell not in seen:
                    yield cell
                    seen.add(cell)

    def rewrap(self):
        """Call ``cell.wrap()`` on all cells, and measure each column width
        after wrapping (result written in ``self.measured_widths``).
        """
        self.measured_widths = self.colwidth[:]
        for cell in self.cells:
            cell.wrap(width=self.cell_width(cell, self.colwidth))
            if not cell.wrapped:
                continue
            width = math.ceil(max(column_width(x) for x in cell.wrapped) / cell.colspan)
            for col in range(cell.col, cell.col + cell.colspan):
                self.measured_widths[col] = max(self.measured_widths[col], width)

    def physical_lines_for_line(self, line):
        """From a given line, compute the number of physical lines it spans
        due to text wrapping.
        """
        physical_lines = 1
        for cell in line:
            physical_lines = max(physical_lines, len(cell.wrapped))
        return physical_lines

    def __str__(self):
        out = []
        self.rewrap()

        def writesep(char="-", lineno=None):
            # type: (str, Optional[int]) -> str
            """Called on the line *before* lineno.
            Called with no *lineno* for the last sep.
            """
            out = []  # type: List[str]
            for colno, width in enumerate(self.measured_widths):
                if (
                    lineno is not None
                    and lineno > 0
                    and self[lineno, colno] is self[lineno - 1, colno]
                ):
                    out.append(" " * (width + 2))
                else:
                    out.append(char * (width + 2))
            head = "+" if out[0][0] == "-" else "|"
            tail = "+" if out[-1][0] == "-" else "|"
            glue = [
                "+" if left[0] == "-" or right[0] == "-" else "|"
                for left, right in zip(out, out[1:])
            ]
            glue.append(tail)
            return head + "".join(chain(*zip(out, glue)))

        for lineno, line in enumerate(self.lines):
            if self.separator and lineno == self.separator:
                out.append(writesep("=", lineno))
            else:
                out.append(writesep("-", lineno))
            for physical_line in range(self.physical_lines_for_line(line)):
                linestr = ["|"]
                for colno, cell in enumerate(line):
                    if cell.col != colno:
                        continue
                    if lineno != cell.row:
                        physical_text = ""
                    elif physical_line >= len(cell.wrapped):
                        physical_text = ""
                    else:
                        physical_text = cell.wrapped[physical_line]
                    adjust_len = len(physical_text) - column_width(physical_text)
                    linestr.append(
                        " "
                        + physical_text.ljust(
                            self.cell_width(cell, self.measured_widths) + 1 + adjust_len
                        )
                        + "|"
                    )
                out.append("".join(linestr))
        out.append(writesep("-"))
        return "\n".join(out)


class TextWrapper(textwrap.TextWrapper):
    """Custom subclass that uses a different word separator regex."""

    wordsep_re = re.compile(
        r"(\s+|"  # any whitespace
        r"(?<=\s)(?::[a-z-]+:)?`\S+|"  # interpreted text start
        r"[^\s\w]*\w+[a-zA-Z]-(?=\w+[a-zA-Z])|"  # hyphenated words
        r"(?<=[\w\!\"\'\&\.\,\?])-{2,}(?=\w))"
    )  # em-dash

    def _wrap_chunks(self, chunks):
        # type: (List[str]) -> List[str]
        """_wrap_chunks(chunks : [string]) -> [string]

        The original _wrap_chunks uses len() to calculate width.
        This method respects wide/fullwidth characters for width adjustment.
        """
        lines = []  # type: List[str]
        if self.width <= 0:
            raise ValueError("invalid width %r (must be > 0)" % self.width)

        chunks.reverse()

        while chunks:
            cur_line = []
            cur_len = 0

            if lines:
                indent = self.subsequent_indent
            else:
                indent = self.initial_indent

            width = self.width - column_width(indent)

            if self.drop_whitespace and chunks[-1].strip() == "" and lines:
                del chunks[-1]

            while chunks:
                l = column_width(chunks[-1])

                if cur_len + l <= width:
                    cur_line.append(chunks.pop())
                    cur_len += l

                else:
                    break

            if chunks and column_width(chunks[-1]) > width:
                self._handle_long_word(chunks, cur_line, cur_len, width)

            if self.drop_whitespace and cur_line and cur_line[-1].strip() == "":
                del cur_line[-1]

            if cur_line:
                lines.append(indent + "".join(cur_line))

        return lines

    def _break_word(self, word, space_left):
        # type: (str, int) -> Tuple[str, str]
        """_break_word(word : string, space_left : int) -> (string, string)

        Break line by unicode width instead of len(word).
        """
        total = 0
        for i, c in enumerate(word):
            total += column_width(c)
            if total > space_left:
                return word[: i - 1], word[i - 1 :]
        return word, ""

    def _split(self, text):
        # type: (str) -> List[str]
        """_split(text : string) -> [string]

        Override original method that only split by 'wordsep_re'.
        This '_split' split wide-characters into chunk by one character.
        """

        def split(t):
            # type: (str) -> List[str]
            return super(TextWrapper, self)._split(t)

        chunks = []  # type: List[str]
        for chunk in split(text):
            for w, g in groupby(chunk, column_width):
                if w == 1:
                    chunks.extend(split("".join(g)))
                else:
                    chunks.extend(list(g))
        return chunks

    def _handle_long_word(self, reversed_chunks, cur_line, cur_len, width):
        # type: (List[str], List[str], int, int) -> None
        """_handle_long_word(chunks : [string],
                             cur_line : [string],
                             cur_len : int, width : int)

        Override original method for using self._break_word() instead of slice.
        """
        space_left = max(width - cur_len, 1)
        if self.break_long_words:
            l, r = self._break_word(reversed_chunks[-1], space_left)
            cur_line.append(l)
            reversed_chunks[-1] = r

        elif not cur_line:
            cur_line.append(reversed_chunks.pop())


def my_wrap(text, width=MAXWIDTH, **kwargs):
    # type: (str, int, Any) -> List[str]
    w = TextWrapper(width=width, **kwargs)
    return w.wrap(text)
