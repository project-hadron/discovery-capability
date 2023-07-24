import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc

class DataDiscovery(object):

    @staticmethod
    def data_dictionary(canonical: pa.Table, display_width: int=None, stylise: bool=None):
        """ returns a DataFrame of a data dictionary showing 'Attribute', 'Type', '% Nulls', 'Count',
        'Unique', 'Observations' where attribute is the column names in the df
        Note that the subject_matter, if used, should be in the form:
            { subject_ref, { column_name : text_str}}
        the subject reference will be the header of the column and the text_str put in next to each attribute row

        :param canonical: (optional) the Table to get the dictionary from
        :return: a pandas.DataFrame
        """
        display_width = display_width if isinstance(display_width, int) else 80
        stylise = stylise if isinstance(stylise, bool) else False
        record = []
        labels = [f'Attributes', 'DataType', 'Nulls', 'Dominate', 'Valid', 'Unique', 'Observations']
        for c in canonical.column_names:
            column = canonical.column(c).combine_chunks()
            line = [c,
                    # data type
                    'Category' if pc.starts_with(str(column.type), 'dict').as_py() else str(column.type),
                    # null percentage
                    round(column.null_count / canonical.num_rows * 100, 1)
                    ]
            # dominant percentage
            arr_vc = column.value_counts()
            value = arr_vc.filter(pc.equal(arr_vc.field(1), pc.max(arr_vc.field(1)))).field(1)[0].as_py()
            line.append(round(value / canonical.num_rows * 100, 1))
            # valid
            line.append(pc.sum(column.is_valid()).as_py())
            # unique
            line.append(pc.count(column.unique()).as_py())
            # observations
            vc = column.drop_null().value_counts()
            if pa.types.is_dictionary(column.type):
                t = pa.table([vc.field(1), vc.field(0).dictionary], names=['v', 'n']).sort_by([("v", "descending")])
            else:
                t = pa.table([vc.field(1), vc.field(0)], names=['v', 'n']).sort_by([("v", "descending")])
            s = str(t.column('n').to_pylist())
            if len(s) > display_width:
                s = s[:display_width] + "..."
            line.append(s)
            record.append(line)
        df = pd.DataFrame(record, columns=labels)
        if stylise:
            style = [{'selector': 'th', 'props': [('font-size', "120%"), ("text-align", "center")]},
                     {'selector': '.row_heading, .blank', 'props': [('display', 'none;')]}]
            df_style = df.style.set_table_styles(style)
            _ = df_style.applymap(DataDiscovery._highlight_null_dom, subset=['Nulls', 'Dominate'])
            _ = df_style.applymap(lambda x: 'color: white' if x > 0.98 else 'color: black', subset=['Nulls', 'Dominate'])
            _ = df_style.applymap(DataDiscovery._dtype_color, subset=['DataType'])
            _ = df_style.applymap(DataDiscovery._color_unique, subset=['Unique'])
            _ = df_style.applymap(lambda x: 'color: white' if x < 2 else 'color: black', subset=['Unique'])
            _ = df_style.format({'Nulls': "{:.1%}", 'Dominate': '{:.1%}'})
            _ = df_style.set_caption(f"dataset has {canonical.num_columns} columns")
            _ = df_style.set_properties(subset=['Attributes'],  **{'font-weight': 'bold', 'font-size': "120%"})
            return df_style
        return pa.Table.from_pandas(df)

    @staticmethod
    def _dtype_color(dtype: str):
        """Apply color to types"""
        if str(dtype).startswith('cat'):
            color = '#208a0f'
        elif str(dtype).startswith('int'):
            color = '#0f398a'
        elif str(dtype).startswith('float'):
            color = '#2f0f8a'
        elif str(dtype).startswith('date'):
            color = '#790f8a'
        elif str(dtype).startswith('bool'):
            color = '#08488e'
        elif str(dtype).startswith('str'):
            color = '#761d38'
        else:
            return ''
        return 'color: %s' % color

    @staticmethod
    def _highlight_null_dom(x: str):
        x = float(x)
        if not isinstance(x, float) or x < 0.65:
            return ''
        elif x < 0.85:
            color = '#ffede5'
        elif x < 0.90:
            color = '#fdcdb9'
        elif x < 0.95:
            color = '#fcb499'
        elif x < 0.98:
            color = '#fc9576'
        elif x < 0.99:
            color = '#fb7858'
        elif x < 0.997:
            color = '#f7593f'
        else:
            color = '#ec382b'
        return 'background-color: %s' % color

    @staticmethod
    def _color_unique(x: str):
        x = int(x)
        if not isinstance(x, int):
            return ''
        elif x < 2:
            color = '#ec382b'
        elif x < 3:
            color = '#a1cbe2'
        elif x < 5:
            color = '#84cc83'
        elif x < 10:
            color = '#a4da9e'
        elif x < 20:
            color = '#c1e6ba'
        elif x < 50:
            color = '#e5f5e0'
        elif x < 100:
            color = '#f0f9ed'
        else:
            return ''
        return 'background-color: %s' % color
