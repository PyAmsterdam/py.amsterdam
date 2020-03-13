"""
Modified sphinx.translator.TextTranslator

"""
import os
from typing import List, Tuple, Union, cast, Iterable

from docutils import nodes
from docutils.utils import column_width
from .conf import MAXWIDTH, STDINDENT
from .elements import Cell, Table, my_wrap


# from sphinx import addnodes
# from sphinx.deprecation import RemovedInSphinx30Warning
# from sphinx.locale import admonitionlabels
# import warnings


class TextTranslator(nodes.NodeVisitor):
    def __init__(self, document):
        """
        Translator from docutils docutils.nodes.document to formatted plain text.


        Parameters
        ----------
        document
            docutils

        """
        # type: # (nodes.document, TextBuilder) -> None
        super().__init__(document)
        self.compact_p = None

        newlines = "unix"
        if newlines == "windows":
            self.nl = "\r\n"
        elif newlines == "native":
            self.nl = os.linesep
        else:
            self.nl = "\n"

        # # with overline, for parts
        # * with overline, for chapters
        # =, for sections
        # -, for Sec 1sections
        # ^, for Sec 1Sec 1sections
        # ", for paragraphs

        self.sectionchars = "-~.+*^\"'`"
        # self.sectionchars = " "
        # self.sectionchars = '=-~+"*`'
        self.add_secnumbers = True
        self.secnumber_suffix = ". "

        # states hold the resulting text in form List[(indent, ['line', 'line'])]
        self.states = [[]]  # type: List[List[Tuple[int, Union[str, List[str]]]]]

        self.stateindent = [0]
        self.list_counter = []  # type: List[int]
        self.sectionlevel = 0
        self.lineblocklevel = 0
        self.table = None  # type: Table
        self.body = []
        self.list_links = False  # my lame implementation of .. :target-notes:
        self.external_links = [(0, ['Links', f'-----', ''])]

        self.docinfo = []

    def visit_docinfo(self, node: nodes.Element) -> List or None:
        raise nodes.SkipNode

    def depart_docinfo(self, node: nodes.Element) -> None:
        # self.end_state()
        pass

    def visit_docinfo_item(self, node):

        pass

    def depart_docinfo_item(self, node):
        pass

    def visit_date(self, node: nodes.Element) -> None:
        # print("date", node.astext())
        pass
        # self.add_text(f"DATE: {node.astext()}")

    def depart_date(self, node: nodes.Element) -> None:
        pass

    def add_text(self, text):
        # type: (str) -> None
        self.states[-1].append((-1, text))

    def new_state(self, indent=STDINDENT):
        # type: (int) -> None
        self.states.append([])
        self.stateindent.append(indent)

    def end_state(self, wrap=True, end=[""], first=None):
        # type: (bool, List[str], str) -> None
        content = self.states.pop()
        maxindent = sum(self.stateindent)
        indent = self.stateindent.pop()
        result = []  # type: List[Tuple[int, List[str]]]
        toformat = []  # type: List[str]

        def do_format():
            # type: () -> None
            if not toformat:
                return
            if wrap:
                res = my_wrap("".join(toformat), width=MAXWIDTH - maxindent)
            else:
                res = "".join(toformat).splitlines()
            if end:
                res += end
            result.append((indent, res))

        for itemindent, item in content:
            if itemindent == -1:
                toformat.append(item)  # type: ignore
            else:
                do_format()
                result.append((indent + itemindent, item))  # type: ignore
                toformat = []
        do_format()
        if first is not None and result:
            itemindent, item = result[0]
            result_rest, result = result[1:], []
            if item:
                toformat = [first + " ".join(item)]
                do_format()  # re-create `result` from `toformat`
                _dummy, new_item = result[0]
                result.insert(0, (itemindent - indent, [new_item[0]]))
                result[1] = (itemindent, new_item[1:])
                result.extend(result_rest)
        self.states[-1].extend(result)

    def visit_document(self, node: nodes.Element) -> None:
        self.new_state(0)

    def depart_document(self, node: nodes.Element) -> None:
        self.end_state()

        if self.list_links and len(self.external_links) > 1:
            self.external_links[-1][1].append('')
            self.states[0].extend(self.external_links)

        self.body = self.nl.join(
            line and (" " * indent + line)
            for indent, lines in self.states[0]
            for line in lines
        )

    def visit_section(self, node: nodes.Element) -> None:
        self._title_char = self.sectionchars[self.sectionlevel]
        self.sectionlevel += 1

    def depart_section(self, node: nodes.Element) -> None:
        self.sectionlevel -= 1

    def visit_topic(self, node: nodes.Element) -> None:
        self.new_state(0)

    def depart_topic(self, node: nodes.Element) -> None:
        self.end_state()

    visit_sidebar = visit_topic
    depart_sidebar = depart_topic

    def visit_rubric(self, node: nodes.Element) -> None:
        self.new_state(0)
        self.add_text("-[ ")

    def depart_rubric(self, node: nodes.Element) -> None:
        self.add_text(" ]-")
        self.end_state()

    def visit_compound(self, node: nodes.Element) -> None:
        pass

    def depart_compound(self, node: nodes.Element) -> None:
        pass

    def visit_glossary(self, node: nodes.Element) -> None:
        pass

    def depart_glossary(self, node: nodes.Element) -> None:
        pass

    def visit_title(self, node: nodes.Element) -> None:
        if isinstance(node.parent, nodes.Admonition):
            self.add_text(node.astext() + ": ")
            raise nodes.SkipNode
        self.new_state(0)

    # def get_section_number_string(self, node: nodes.Element) -> None:
    #     """This does not work due to builder."""
    #     # type: (nodes.Element) -> str
    #     if isinstance(node.parent, nodes.section):
    #         anchorname = "#" + node.parent["ids"][0]
    #         numbers = self.builder.secnumbers.get(anchorname)
    #         if numbers is None:
    #             numbers = self.builder.secnumbers.get("")
    #         if numbers is not None:
    #             return ".".join(map(str, numbers)) + self.secnumber_suffix
    #     return ""

    def depart_title(self, node: nodes.Element) -> None:
        pass
        if isinstance(node.parent, nodes.section):
            char = self._title_char
        else:
            char = "="
        text = ""
        text = "".join(x[1] for x in self.states.pop() if x[0] == -1)  # type: ignore
        # if self.add_secnumbers:
        #     text = self.get_section_number_string(node) + text
        self.stateindent.pop()
        title = ["", text, "%s" % (char * column_width(text)), ""]
        if len(self.states) == 2 and len(self.states[-1]) == 0:
            # remove an empty line before title if it is first section title in the document
            title.pop(0)
        self.states[-1].append((0, title))

    def visit_subtitle(self, node: nodes.Element) -> None:
        pass

    def depart_subtitle(self, node: nodes.Element) -> None:
        pass

    def visit_attribution(self, node: nodes.Element) -> None:
        self.add_text("-- ")

    def depart_attribution(self, node: nodes.Element) -> None:
        pass

    def visit_desc(self, node: nodes.Element) -> None:
        pass

    def depart_desc(self, node: nodes.Element) -> None:
        pass

    def visit_desc_signature(self, node: nodes.Element) -> None:
        self.new_state(0)

    def depart_desc_signature(self, node: nodes.Element) -> None:
        # XXX: wrap signatures in a way that makes sense
        self.end_state(wrap=False, end=None)

    def visit_desc_signature_line(self, node: nodes.Element) -> None:
        pass

    def depart_desc_signature_line(self, node: nodes.Element) -> None:
        self.add_text("\n")

    def visit_desc_name(self, node: nodes.Element) -> None:
        pass

    def depart_desc_name(self, node: nodes.Element) -> None:
        pass

    def visit_desc_addname(self, node: nodes.Element) -> None:
        pass

    def depart_desc_addname(self, node: nodes.Element) -> None:
        pass

    def visit_desc_type(self, node: nodes.Element) -> None:
        pass

    def depart_desc_type(self, node: nodes.Element) -> None:
        pass

    def visit_desc_returns(self, node: nodes.Element) -> None:
        self.add_text(" -> ")

    def depart_desc_returns(self, node: nodes.Element) -> None:
        pass

    def visit_desc_parameterlist(self, node: nodes.Element) -> None:
        self.add_text("(")
        self.first_param = 1

    def depart_desc_parameterlist(self, node: nodes.Element) -> None:
        self.add_text(")")

    def visit_desc_parameter(self, node: nodes.Element) -> None:
        if not self.first_param:
            self.add_text(", ")
        else:
            self.first_param = 0
        self.add_text(node.astext())
        raise nodes.SkipNode

    def visit_desc_optional(self, node: nodes.Element) -> None:
        self.add_text("[")

    def depart_desc_optional(self, node: nodes.Element) -> None:
        self.add_text("]")

    def visit_desc_annotation(self, node: nodes.Element) -> None:
        pass

    def depart_desc_annotation(self, node: nodes.Element) -> None:
        pass

    def visit_desc_content(self, node: nodes.Element) -> None:
        self.new_state()
        self.add_text(self.nl)

    def depart_desc_content(self, node: nodes.Element) -> None:
        self.end_state()

    def visit_figure(self, node: nodes.Element) -> None:
        self.new_state()

    def depart_figure(self, node: nodes.Element) -> None:
        self.end_state()

    def visit_caption(self, node: nodes.Element) -> None:
        pass

    def depart_caption(self, node: nodes.Element) -> None:
        pass

    def visit_productionlist(self, node: nodes.Element) -> None:

        # self.new_state()
        # names = []
        # productionlist = cast(Iterable[addnodes.production], node)
        # for production in productionlist:
        #     names.append(production["tokenname"])
        # maxlen = max(len(name) for name in names)
        # lastname = None
        # for production in productionlist:
        #     if production["tokenname"]:
        #         self.add_text(production["tokenname"].ljust(maxlen) + " ::=")
        #         lastname = production["tokenname"]
        #     elif lastname is not None:
        #         self.add_text("%s    " % (" " * len(lastname)))
        #     self.add_text(production.astext() + self.nl)
        # self.end_state(wrap=False)
        raise nodes.SkipNode

    def visit_footnote(self, node: nodes.Element) -> None:
        n0 = node[0]
        label = cast(nodes.label, node[0])
        ft = label.astext().strip()
        self._footnote = label.astext().strip()
        self.new_state(len(self._footnote) + 3)

    def depart_footnote(self, node: nodes.Element) -> None:
        self.end_state(first="[%s] " % self._footnote)

    def visit_citation(self, node: nodes.Element) -> None:
        if len(node) and isinstance(node[0], nodes.label):
            self._citlabel = node[0].astext()
        else:
            self._citlabel = ""
        self.new_state(len(self._citlabel) + 3)

    def depart_citation(self, node: nodes.Element) -> None:
        self.end_state(first="[%s] " % self._citlabel)

    def visit_label(self, node: nodes.Element) -> None:
        raise nodes.SkipNode

    def visit_legend(self, node: nodes.Element) -> None:
        pass

    def depart_legend(self, node: nodes.Element) -> None:
        pass

    # XXX: option list could use some better styling

    def visit_option_list(self, node: nodes.Element) -> None:
        pass

    def depart_option_list(self, node: nodes.Element) -> None:
        pass

    def visit_option_list_item(self, node: nodes.Element) -> None:
        self.new_state(0)

    def depart_option_list_item(self, node: nodes.Element) -> None:
        self.end_state()

    def visit_option_group(self, node: nodes.Element) -> None:
        self._firstoption = True

    def depart_option_group(self, node: nodes.Element) -> None:
        self.add_text("     ")

    def visit_option(self, node: nodes.Element) -> None:
        if self._firstoption:
            self._firstoption = False
        else:
            self.add_text(", ")

    def depart_option(self, node: nodes.Element) -> None:
        pass

    def visit_option_string(self, node: nodes.Element) -> None:
        pass

    def depart_option_string(self, node: nodes.Element) -> None:
        pass

    def visit_option_argument(self, node: nodes.Element) -> None:
        self.add_text(node["delimiter"])

    def depart_option_argument(self, node: nodes.Element) -> None:
        pass

    def visit_description(self, node: nodes.Element) -> None:
        pass

    def depart_description(self, node: nodes.Element) -> None:
        pass

    def visit_tabular_col_spec(self, node: nodes.Element) -> None:
        raise nodes.SkipNode

    def visit_colspec(self, node: nodes.Element) -> None:
        self.table.colwidth.append(node["colwidth"])
        raise nodes.SkipNode

    def visit_tgroup(self, node: nodes.Element) -> None:
        pass

    def depart_tgroup(self, node: nodes.Element) -> None:
        pass

    def visit_thead(self, node: nodes.Element) -> None:
        pass

    def depart_thead(self, node: nodes.Element) -> None:
        pass

    def visit_tbody(self, node: nodes.Element) -> None:
        self.table.set_separator()

    def depart_tbody(self, node: nodes.Element) -> None:
        pass

    def visit_row(self, node: nodes.Element) -> None:
        if self.table.lines:
            self.table.add_row()

    def depart_row(self, node: nodes.Element) -> None:
        pass

    def visit_entry(self, node: nodes.Element) -> None:
        self.entry = Cell(
            rowspan=node.get("morerows", 0) + 1, colspan=node.get("morecols", 0) + 1
        )
        self.new_state(0)

    def depart_entry(self, node: nodes.Element) -> None:
        text = self.nl.join(self.nl.join(x[1]) for x in self.states.pop())
        self.stateindent.pop()
        self.entry.text = text
        self.table.add_cell(self.entry)
        self.entry = None

    def visit_table(self, node: nodes.Element) -> None:
        if self.table:
            raise NotImplementedError("Nested tables are not supported.")
        self.new_state(0)
        self.table = Table()

    def depart_table(self, node: nodes.Element) -> None:
        self.add_text(str(self.table))
        self.table = None
        self.end_state(wrap=False)

    def visit_acks(self, node: nodes.Element) -> None:
        bullet_list = cast(nodes.bullet_list, node[0])
        list_items = cast(Iterable[nodes.list_item], bullet_list)
        self.new_state(0)
        self.add_text(", ".join(n.astext() for n in list_items) + ".")
        self.end_state()
        raise nodes.SkipNode

    def visit_image(self, node: nodes.Element) -> None:
        if "alt" in node.attributes:
            self.add_text("[image: %s]" % node["alt"])
        self.add_text("[image]")
        raise nodes.SkipNode

    def visit_transition(self, node: nodes.Element) -> None:
        indent = sum(self.stateindent)
        self.new_state(0)
        self.add_text("=" * (MAXWIDTH - indent))
        self.end_state()
        raise nodes.SkipNode

    def visit_bullet_list(self, node: nodes.Element) -> None:
        self.list_counter.append(-1)

    def depart_bullet_list(self, node: nodes.Element) -> None:
        self.list_counter.pop()

    def visit_enumerated_list(self, node: nodes.Element) -> None:
        self.list_counter.append(node.get("start", 1) - 1)

    def depart_enumerated_list(self, node: nodes.Element) -> None:
        self.list_counter.pop()

    def visit_definition_list(self, node: nodes.Element) -> None:
        self.list_counter.append(-2)

    def depart_definition_list(self, node: nodes.Element) -> None:
        self.list_counter.pop()

    def visit_list_item(self, node: nodes.Element) -> None:
        if self.list_counter[-1] == -1:
            # bullet list
            self.new_state(2)
        elif self.list_counter[-1] == -2:
            # definition list
            pass
        else:
            # enumerated list
            self.list_counter[-1] += 1
            self.new_state(len(str(self.list_counter[-1])) + 2)

    def depart_list_item(self, node: nodes.Element) -> None:
        if self.list_counter[-1] == -1:
            self.end_state(first="* ")
        elif self.list_counter[-1] == -2:
            pass
        else:
            self.end_state(first="%s. " % self.list_counter[-1])

    def visit_definition_list_item(self, node: nodes.Element) -> None:
        self._classifier_count_in_li = len(node.traverse(nodes.classifier))

    def depart_definition_list_item(self, node: nodes.Element) -> None:
        pass

    def visit_term(self, node: nodes.Element) -> None:
        self.new_state(0)

    def depart_term(self, node: nodes.Element) -> None:
        if not self._classifier_count_in_li:
            self.end_state(end=None)

    def visit_classifier(self, node: nodes.Element) -> None:
        self.add_text(" : ")

    def depart_classifier(self, node: nodes.Element) -> None:
        self._classifier_count_in_li -= 1
        if not self._classifier_count_in_li:
            self.end_state(end=None)

    def visit_definition(self, node: nodes.Element) -> None:
        self.new_state()

    def depart_definition(self, node: nodes.Element) -> None:
        self.end_state()

    def visit_field_list(self, node: nodes.Element) -> None:
        print("Visit field list", node.astext())
        pass

    def depart_field_list(self, node: nodes.Element) -> None:
        pass

    def visit_field(self, node: nodes.Element) -> None:
        print("Visit field", node.astext())
        pass

    def depart_field(self, node: nodes.Element) -> None:
        pass

    def visit_field_name(self, node: nodes.Element) -> None:
        print("Visit field name", node.astext())
        self.new_state(0)

    def depart_field_name(self, node: nodes.Element) -> None:
        self.add_text(":")
        self.end_state(end=None)

    def visit_field_body(self, node: nodes.Element) -> None:
        self.new_state()

    def depart_field_body(self, node: nodes.Element) -> None:
        self.end_state()

    def visit_centered(self, node: nodes.Element) -> None:
        pass

    def depart_centered(self, node: nodes.Element) -> None:
        pass

    def visit_hlist(self, node: nodes.Element) -> None:
        pass

    def depart_hlist(self, node: nodes.Element) -> None:
        pass

    def visit_hlistcol(self, node: nodes.Element) -> None:
        pass

    def depart_hlistcol(self, node: nodes.Element) -> None:
        pass

    def visit_admonition(self, node: nodes.Element) -> None:
        self.new_state(0)

    def depart_admonition(self, node: nodes.Element) -> None:
        self.end_state()

    def _visit_admonition(self, node: nodes.Element) -> None:
        self.new_state(2)

        if isinstance(node.children[0], nodes.Sequential):
            self.add_text(self.nl)

    def _depart_admonition(self, node: nodes.Element) -> None:
        # label = admonitionlabels[node.tagname]
        label = node.tagname
        self.end_state(first=label + ": ")

    visit_attention = _visit_admonition
    depart_attention = _depart_admonition
    visit_caution = _visit_admonition
    depart_caution = _depart_admonition
    visit_danger = _visit_admonition
    depart_danger = _depart_admonition
    visit_error = _visit_admonition
    depart_error = _depart_admonition
    visit_hint = _visit_admonition
    depart_hint = _depart_admonition
    visit_important = _visit_admonition
    depart_important = _depart_admonition
    visit_note = _visit_admonition
    depart_note = _depart_admonition
    visit_tip = _visit_admonition
    depart_tip = _depart_admonition
    visit_warning = _visit_admonition
    depart_warning = _depart_admonition
    visit_seealso = _visit_admonition
    depart_seealso = _depart_admonition

    def visit_versionmodified(self, node: nodes.Element) -> None:
        self.new_state(0)

    def depart_versionmodified(self, node: nodes.Element) -> None:
        self.end_state()

    def visit_literal_block(self, node: nodes.Element) -> None:
        self.new_state()

    def depart_literal_block(self, node: nodes.Element) -> None:
        self.end_state(wrap=False)

    def visit_doctest_block(self, node: nodes.Element) -> None:
        self.new_state(0)

    def depart_doctest_block(self, node: nodes.Element) -> None:
        self.end_state(wrap=False)

    def visit_line_block(self, node: nodes.Element) -> None:
        self.new_state()
        self.lineblocklevel += 1

    def depart_line_block(self, node: nodes.Element) -> None:
        self.lineblocklevel -= 1
        self.end_state(wrap=False, end=None)
        if not self.lineblocklevel:
            self.add_text("\n")

    def visit_line(self, node: nodes.Element) -> None:
        pass

    def depart_line(self, node: nodes.Element) -> None:
        self.add_text("\n")

    def visit_block_quote(self, node: nodes.Element) -> None:
        self.new_state()

    def depart_block_quote(self, node: nodes.Element) -> None:
        self.end_state()

    def visit_compact_paragraph(self, node: nodes.Element) -> None:
        pass

    def depart_compact_paragraph(self, node: nodes.Element) -> None:
        pass

    def visit_paragraph(self, node: nodes.Element) -> None:
        self.new_state(0)
        # if not isinstance(node.parent, nodes.Admonition) or isinstance(
        #     node.parent, addnodes.seealso
        # ):
        #     self.new_state(0)

    def depart_paragraph(self, node: nodes.Element) -> None:
        self.end_state()
        # if not isinstance(node.parent, nodes.Admonition) or isinstance(
        #     node.parent, addnodes.seealso
        # ):
        #     self.end_state()

    def visit_target(self, node: nodes.Element) -> None:
        """External link target"""

        if self.list_links and 'refuri' in node:
            uri = node.attributes['refuri']
            name = ' '.join(node.attributes['names'])
            self.external_links.append((0, [f"* {name}: {uri}"]))

        raise nodes.SkipNode

    def visit_index(self, node: nodes.Element) -> None:
        raise nodes.SkipNode

    def visit_toctree(self, node: nodes.Element) -> None:
        raise nodes.SkipNode

    def visit_pending_xref(self, node: nodes.Element) -> None:
        pass

    def depart_pending_xref(self, node: nodes.Element) -> None:
        pass

    def visit_reference(self, node: nodes.Element) -> None:
        if self.add_secnumbers:
            numbers = node.get("secnumber")
            if numbers is not None:
                self.add_text('.'.join(map(str, numbers)) + self.secnumber_suffix)
        # label = cast(nodes.label, node[0])
        # "[%s]" % node.astext()
        # self.add_text(f"{node.astext()}[1]")

        # self._ref = label.astext().strip()
        # self.new_state(len(self._ref) + 3)

        # self.add_text("[%s]" % node.astext())
        # raise nodes.SkipNode

        # if self.add_secnumbers:
        #     numbers = node.get("secnumber")
        #     if numbers is not None:
        #         self.add_text(".".join(map(str, numbers)) + self.secnumber_suffix)

    def depart_reference(self, node: nodes.Element) -> None:
        # self.end_state(first="[%s] " % self._ref)
        pass

    def visit_number_reference(self, node: nodes.Element) -> None:
        text = nodes.Text(node.get("title", "#"))
        self.visit_Text(text)
        raise nodes.SkipNode

    def visit_download_reference(self, node: nodes.Element) -> None:
        pass

    def depart_download_reference(self, node: nodes.Element) -> None:
        pass

    def visit_emphasis(self, node: nodes.Element) -> None:
        self.add_text("*")

    def depart_emphasis(self, node: nodes.Element) -> None:
        self.add_text("*")

    def visit_literal_emphasis(self, node: nodes.Element) -> None:
        self.add_text("*")

    def depart_literal_emphasis(self, node: nodes.Element) -> None:
        self.add_text("*")

    def visit_strong(self, node: nodes.Element) -> None:
        self.add_text("**")

    def depart_strong(self, node: nodes.Element) -> None:
        self.add_text("**")

    def visit_literal_strong(self, node: nodes.Element) -> None:
        self.add_text("**")

    def depart_literal_strong(self, node: nodes.Element) -> None:
        self.add_text("**")

    def visit_abbreviation(self, node: nodes.Element) -> None:
        self.add_text("")

    def depart_abbreviation(self, node: nodes.Element) -> None:
        if node.hasattr("explanation"):
            self.add_text(" (%s)" % node["explanation"])

    def visit_manpage(self, node: nodes.Element) -> None:
        return self.visit_literal_emphasis(node)

    def depart_manpage(self, node: nodes.Element) -> None:
        return self.depart_literal_emphasis(node)

    def visit_title_reference(self, node: nodes.Element) -> None:
        self.add_text("*")

    def depart_title_reference(self, node: nodes.Element) -> None:
        self.add_text("*")

    def visit_literal(self, node: nodes.Element) -> None:
        self.add_text('"')

    def depart_literal(self, node: nodes.Element) -> None:
        self.add_text('"')

    def visit_subscript(self, node: nodes.Element) -> None:
        self.add_text("_")

    def depart_subscript(self, node: nodes.Element) -> None:
        pass

    def visit_superscript(self, node: nodes.Element) -> None:
        self.add_text("^")

    def depart_superscript(self, node: nodes.Element) -> None:
        pass

    def visit_footnote_reference(self, node: nodes.Element) -> None:
        self.add_text("[%s]" % node.astext())
        raise nodes.SkipNode

    def visit_citation_reference(self, node: nodes.Element) -> None:
        self.add_text("[%s]" % node.astext())
        raise nodes.SkipNode

    def visit_Text(self, node: nodes.Element) -> None:
        self.add_text(node.astext())

    def depart_Text(self, node: nodes.Element) -> None:
        pass

    def visit_generated(self, node: nodes.Element) -> None:
        pass

    def depart_generated(self, node: nodes.Element) -> None:
        pass

    def visit_inline(self, node: nodes.Element) -> None:
        if "xref" in node["classes"] or "term" in node["classes"]:
            self.add_text("*")

    def depart_inline(self, node: nodes.Element) -> None:
        if "xref" in node["classes"] or "term" in node["classes"]:
            self.add_text("*")

    def visit_container(self, node: nodes.Element) -> None:
        pass

    def depart_container(self, node: nodes.Element) -> None:
        pass

    def visit_problematic(self, node: nodes.Element) -> None:
        self.add_text(">>")

    def depart_problematic(self, node: nodes.Element) -> None:
        self.add_text("<<")

    def visit_system_message(self, node: nodes.Element) -> None:
        self.new_state(0)
        self.add_text("<SYSTEM MESSAGE: %s>" % node.astext())
        self.end_state()
        raise nodes.SkipNode

    def visit_comment(self, node: nodes.Element) -> None:
        raise nodes.SkipNode

    def visit_meta(self, node: nodes.Element) -> None:
        # only valid for HTML
        raise nodes.SkipNode

    def visit_raw(self, node: nodes.Element) -> None:
        if "text" in node.get("format", "").split():
            self.new_state(0)
            self.add_text(node.astext())
            self.end_state(wrap=False)
        raise nodes.SkipNode

    def visit_math(self, node: nodes.Element) -> None:
        pass

    def depart_math(self, node: nodes.Element) -> None:
        pass

    def visit_math_block(self, node: nodes.Element) -> None:
        self.new_state()

    def depart_math_block(self, node: nodes.Element) -> None:
        self.end_state()

    def unknown_visit(self, node: nodes.Element) -> None:
        pass
        # raise NotImplementedError('Unknown node: ' + node.__class__.__name__)

    # def _make_depart_admonition(name):  # type: ignore
    #     # type: (str) -> Callable[[TextTranslator, nodes.Element], None]
    #     # warnings.warn(
    #     #     "TextTranslator._make_depart_admonition() is deprecated.",
    #     #     RemovedInSphinx30Warning,
    #     # )
    #
    #     def depart_admonition(self, node: nodes.Element) -> None:
    #         self.end_state(first=admonitionlabels[name] + ": ")
    #
    #     return depart_admonition
