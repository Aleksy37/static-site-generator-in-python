def markdown_to_blocks(markdown):
    splits = markdown.split("\n\n")
    blocks = []
    for block in splits:
        block = block.strip()
        if len(block) == 0:
            continue
        blocks.append(block)
    return blocks

