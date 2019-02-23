from collections import namedtuple

TEMPLATE_ROW = namedtuple('TEMPLATE_ROW', 'key label OCC width type startpos comment')


def read_doc(path):
    """
    Helper function for developer to extract template rows from data doc files
    and print them as lists

    Exported rows may contain missing information (OCC field, comments)
    and incorrectly parsed comment strings
    """
    with open(path, 'rb') as f:
        nonnull_fields = []
        for line in f:
            fields = line.decode('cp932').strip().split()
            if fields and len(fields) > 1:
                nonnull_fields.append(fields)

        startpos = None
        for i, line in enumerate(nonnull_fields):
            if line[0] == '項目名':
                startpos = i + 1
                break

        endpos = None
        for i, line in enumerate(nonnull_fields[startpos:], startpos):
            if '**' in line[0]:
                endpos = i
                break

        template_fields = [field for field in nonnull_fields[startpos:endpos] if len(field) > 3]
        for field in template_fields:
            print(field)
