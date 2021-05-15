def text_from_tag(tag, tree):
    texts = text_list_from_tag(tag, tree)
    if not texts:
        return None
    assert len(texts) == 1, f"More than one {tag} tag: {texts}"
    text = texts[0]
    return text


def text_list_from_tag(tag, tree):
    nodes = tree.iterfind(tag)
    texts = [text_from_node(node) for node in nodes]
    return texts


def text_from_node(node):
    text = " ".join(node.itertext())
    text = text.strip()
    return text
