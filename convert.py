import json
import re
import sys

def py_to_notebook(py_file, ipynb_file):
    with open(py_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern for section headers: three lines of equals with SECTION line in middle
    pattern = re.compile(r'(^# =+\n# SECTION \d+:.*\n# =+\n)', re.MULTILINE)
    
    # Split by pattern, keeping the delimiters
    parts = re.split(pattern, content)
    
    # First part is preamble (before first section)
    preamble = parts[0].strip()
    
    # Initialize notebook structure
    notebook = {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.5"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    # Add initial markdown cell with title and instructions
    title = py_file.replace('.py', '').replace('-', ' ').title()
    notebook["cells"].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            f"# {title}\n",
            "\n",
            "This notebook was converted from a Python script.\n",
            "\n",
            "**How to run**: Press `Shift+Enter` to run each cell.\n"
        ]
    })
    
    # Add preamble as code cell if not empty
    if preamble:
        notebook["cells"].append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": preamble.splitlines()
        })
    
    # Process sections: parts[1] is first header, parts[2] is first section, etc.
    i = 1
    while i < len(parts):
        header = parts[i]
        code = parts[i+1] if i+1 < len(parts) else ""
        i += 2
        
        # Extract section title from header (middle line)
        header_lines = header.strip().splitlines()
        if len(header_lines) >= 3:
            section_title = header_lines[1].strip('# ').strip()
        else:
            section_title = "Section"
        
        # Add markdown cell for section title
        notebook["cells"].append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                f"## {section_title}\n"
            ]
        })
        
        # Add code cell for section content
        if code.strip():
            notebook["cells"].append({
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": code.splitlines()
            })
    
    # Write notebook
    with open(ipynb_file, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1)
    
    print(f"Created {ipynb_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert.py <input.py> <output.ipynb>")
        sys.exit(1)
    py_to_notebook(sys.argv[1], sys.argv[2])
