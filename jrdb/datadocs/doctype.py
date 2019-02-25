from abc import ABC

import pandas as pd

COLS = ['key', 'label', 'OCC', 'width', 'type', 'startpos', 'comment']


class DocType(ABC):
    name = ''
    items = []

    def __init__(self, filepath):
        self.filepath = filepath

    def _validate(self):
        invalid_idx = [str(i) for i, item in enumerate(self.items) if len(item) != 7]
        if invalid_idx:
            idx_list = ', '.join(invalid_idx)
            raise ValueError(f'invalid item indices: {idx_list}')
        return True

    @property
    def spec(self):
        df = pd.DataFrame(self.items, columns=COLS)
        df.OCC = df.OCC.fillna(1).astype(int)
        df.width = df.width.astype(int)
        df.startpos = df.startpos.astype(int) - 1
        df.comment = df.comment.fillna('')
        df.name = self.name
        return df

    def parse(self):
        self._validate()
        with open(self.filepath, 'rb') as f:
            spec_len = len(self.spec.index)
            rows = []
            cols = []
            for line in f:
                if line == b'\n':
                    continue
                row = []
                for i in range(spec_len):
                    item = self.spec.iloc[i]
                    if item.OCC > 1:
                        for j in range(item.OCC):
                            start = item.startpos + (item.width * j)
                            stop = start + item.width
                            cell = line[start:stop].decode('cp932')
                            row.append(cell)
                            cols.append(f'{item.key}_{j}')
                    else:
                        start = item.startpos
                        stop = start + item.width
                        cell = line[start:stop].decode('cp932')
                        row.append(cell)
                        cols.append(item.key)
                rows.append(row)
        return pd.DataFrame(rows, columns=cols)


def parse_template(path):
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
