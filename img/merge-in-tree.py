def insert_tree_to_markdown(tree_file: str, markdown_file: str):
    # Open the tree file in read mode and markdown file in append mode
    with open(tree_file, 'r') as tree, open(markdown_file, 'a') as md:
        # Read the tree file content
        tree_content = tree.read()

        # Prepare the markdown-formatted tree content
        md_tree_content = '```text\n' + tree_content + '\n```'

        # Write the tree content to the markdown file
        md.write(md_tree_content)

insert_tree_to_markdown('tree2.txt', 'Automation.md')