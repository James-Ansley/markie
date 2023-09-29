from pprint import pformat

from approvaltests import verify

from markie import Doc

SIMPLE_DOC = """
---
tag1: Hello
tag2: 5
---

# A Heading

Some text

## Subsection

Text in a subsection
""".strip()

DOC_WITH_SINGLE_H1 = """
---
tag1: Goodbye
tag3:
  - 1
  - 2
---

New Preamble

# An H1 Tag

H1 Preamble
""".strip()

DOC_WITH_SUBHEADINGS = """
---
tag1: Hello
tag2: 5
---

Original Preamble

## Subheading 1

Subheading 1 Text

## Subheading 2

Subheading 2 Text
""".strip()

DOC_WITH_SUBSUBHEADINGS = """
---
tag1: Hello
tag2: 5
---

### An H3

Some H3 content

## An H2

Some H2 content

# An H1

Some H1 content
""".strip()


def test_doc_parsing():
    doc = Doc.from_md(SIMPLE_DOC)
    assert doc.metadata == {"tag1": "Hello", "tag2": 5}
    assert doc.sections[0].title == "A Heading"
    verify(pformat(doc, width=120))


def test_doc_rendering():
    doc = Doc.from_md(SIMPLE_DOC)
    verify(doc.render())


def test_basic_prepend():
    doc = Doc.from_md(DOC_WITH_SUBHEADINGS)
    doc.prepend(DOC_WITH_SINGLE_H1)
    assert doc.metadata == {"tag1": "Hello", "tag2": 5}
    assert len(doc.sections) == 1
    assert doc.sections[0].title == "An H1 Tag"
    assert doc.sections[0].level == 1
    verify(pformat(doc, width=120))


def test_nesting_prepend():
    doc = Doc.from_md(DOC_WITH_SUBSUBHEADINGS)
    doc.prepend(SIMPLE_DOC)
    assert doc.metadata == {"tag1": "Hello", "tag2": 5}
    assert len(doc.sections) == 2
    assert doc.sections[0].title == "A Heading"
    assert doc.sections[0].level == 1
    verify(pformat(doc, width=120))
