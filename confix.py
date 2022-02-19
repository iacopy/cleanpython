"""
sphinx-quickstart creates conf.py and index.rst files.

They need to be edited before launching the build.
"""


def fix_docs_conf_py():
    """
    Lines to be edited in docs/conf.py:

        # import os
        # import sys
        # sys.path.insert(0, os.path.abspath('.'))

    to:

        import os
        import sys
        sys.path.insert(0, os.path.abspath('../src'))
    """
    with open('docs/conf.py', 'r', encoding='utf-8') as file_obj:
        lines = file_obj.readlines()
    with open('docs/conf.py', 'w', encoding='utf-8') as file_obj:
        for line in lines:
            if line.startswith('# import os'):
                line = 'import os\n'
            if line.startswith('# import sys'):
                line = 'import sys\n'
            if line.startswith('# sys.path.insert'):
                line = '\nsys.path.insert(0, os.path.abspath(\'../src\'))\n'
            file_obj.write(line)


def fix_docs_index_rst():
    """
    In docs/index.rst, the string "modules" must be added 2 lines below ":caption: Contents:".

    .. toctree::
       :maxdepth: 2
       :caption: Contents:

       modules
    """
    towrite = []
    with open('docs/index.rst', 'r', encoding='utf-8') as file_obj:
        lines = file_obj.readlines()
    for line in lines:
        # Add "modules" to the toctree
        # raise an error if the string "modules" is already in the file
        if line.startswith('   :caption: Contents:'):
            towrite.append('   :caption: Contents:\n')
            towrite.append('\n')
            towrite.append('   modules\n')
        else:
            towrite.append(line)

        if line.strip() == 'modules':
            raise Exception('"modules" is already in docs/index.rst')

    with open('docs/index.rst', 'w', encoding='utf-8') as file_obj:
        file_obj.write(''.join(towrite))


if __name__ == '__main__':
    fix_docs_conf_py()
    fix_docs_index_rst()
