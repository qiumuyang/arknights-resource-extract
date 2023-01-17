from typing import List

_align = {
    'l': '<',
    'r': '>',
    'c': '^'
}


class Table:
    """ A simple table class for printing data in tabular format.

    +---------------------------------+
    |             Title               |
    +---------------------------------+
    | Header1      Header2     ...    |
    |=================================|
    | Cell(1,1)    Cell(1,2)   ...    |
    | Cell(2,1)    Cell(2,2)   ...    |
    | ...           ...        ...    |
    +---------------------------------+

    Attributes:
        title (str): Title of the table.
        headers (List[str]): Column headers.
        rows (List[List[Any]]): Table rows.
        align (str): Alignment of each column. 'l' for left, 'r' for right, 'c' for center. Default: 'l' * len(headers)
        col_spacing (int): Spacing between columns.
        margin (int): Margin between table and left/right border.
        unit (List[str]): Unit of each column. Default: [''] * len(headers)

    .. note::
        Multi-line cells are not supported.
    """

    def __init__(self, title: str, headers: List[str], align: str = '',
                 col_spacing: int = 5, margin: int = 1, unit: List[str] = None):
        self.title = title
        self.headers = headers
        self.rows = []
        self.align = (align or 'l' * len(headers)).lower()
        self.col_spacing = col_spacing
        self.margin = margin
        self.unit = unit or [''] * len(headers)
        assert set(self.align) <= {'l', 'r', 'c'}
        assert len(self.align) == len(self.headers)
        assert len(self.unit) == len(self.headers)

    def add_row(self, row: List[str]):
        assert len(row) == len(self.headers)
        self.rows.append(row)

    def print(self, file=None):
        if file is None:
            print(str(self))
        else:
            print(str(self), file=file)

    def __str__(self):
        headers = self.headers or ['[Empty Table]']
        rows = self.rows or [[''] * len(headers)]
        units = self.unit or [''] * len(headers)
        aligns = [_align[a] for a in self.align] or ['^']

        col_sp = ' ' * self.col_spacing
        max_widths = [len(h) for h in headers]
        for row in self.rows:
            for i, cell in enumerate(row):
                max_widths[i] = max(max_widths[i], len(str(cell) + units[i]))

        full_width = sum(max_widths) + self.col_spacing * (len(headers) - 1)
        assert len(self.title) <= full_width, f'title is too long: {self.title}'

        lb = '|' + ' ' * self.margin  # left border
        rb = ' ' * self.margin + '|'  # right border
        tbb = '+' + '-' * (full_width + 2 * self.margin) + '+'  # top and bottom border
        sep = '|' + '=' * (full_width + 2 * self.margin) + '|'  # separator between header and table

        t_rows = []
        for row in [headers] + rows:
            header = row is headers  # do not add unit to header
            t_rows.append(
                lb + col_sp.join(f'{str(cell) + ("" if header else unit):{align}{width}}'
                                 for cell, width, align, unit in zip(row, max_widths, aligns, units)) + rb)

        title = lb + self.title.center(full_width) + rb

        return '\n'.join([tbb, title, tbb, t_rows[0], sep] + t_rows[1:] + [tbb])

    def __repr__(self):
        return f'<Table {self.title}>'

    def __len__(self):
        return len(self.rows)


__all__ = ['Table']

if __name__ == '__main__':
    tbl = Table('Test Table', ['Header1', 'Header2', 'Header3'], align='lcr')
    tbl.add_row(['Cell(1,1)', 'Cell(1,2)', 'Cell(1,3)'])
    tbl.add_row(['Cell(2,1)', 'Cell(2,2)', 'Cell(2,3)'])
    tbl.add_row(['...', '', ''])
    tbl.print()
