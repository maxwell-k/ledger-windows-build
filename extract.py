import docutils.core

INPUT = "README.rst"


if __name__ == "__main__":
    with open(INPUT) as file_:
        document = docutils.core.publish_doctree(file_.read())
    detail = document.traverse(
        lambda i: i.tagname == "section" and i.attributes["ids"] == ["detail"]
    )[0]
    blocks = detail.traverse(lambda i: i.tagname == "literal_block")
    source_code = [block.astext() for block in blocks]
    for i in source_code:
        print(i)
