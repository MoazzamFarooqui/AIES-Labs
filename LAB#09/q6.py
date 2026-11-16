fs = {
    'C:': ['Documents', 'Pictures', 'Program Files'],
    'Documents': ['Resume.docx', 'Reports'],
    'Reports': ['Q1.pdf', 'Q2.pdf'],
    'Pictures': ['Holiday', 'logo.png'],
    'Holiday': ['beach.jpg', 'hotel.jpg'],
    'Program Files': ['Python', 'notes.txt'],
    'Python': ['python.exe']
}

def walk(node, depth=0):
    kind = "[DIR] " if node in fs else "      "
    print("  " * depth + kind + node)
    for child in fs.get(node, []): 
        walk(child, depth + 1)

walk('C:')

