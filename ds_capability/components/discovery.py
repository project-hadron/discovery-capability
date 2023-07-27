import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
from ds_capability.components.commons import Commons


# noinspection PyArgumentList
class DataDiscovery(object):

    @staticmethod
    def data_quality(canonical: pa.Table, nulls_threshold: float=None, dom_threshold: float=None,
                     cat_threshold: int=None, stylise: bool=None):
        """ Analyses a dataset, passed as a DataFrame and returns a quality summary

        :param canonical: The dataset, as a DataFrame.
        :param cat_threshold: The threshold for the max number of unique categories. Default is 60
        :param dom_threshold: The threshold limit of a dominant value. Default 0.98
        :param nulls_threshold: The threshold limit of a nulls value. Default 0.9
        :param stylise: if the output is stylised for jupyter display
        :return: pd.DataFrame
        """
        # defaults
        cat_threshold = cat_threshold if isinstance(cat_threshold, int) else 60
        dom_threshold = dom_threshold if isinstance(dom_threshold, float) and 0 <= dom_threshold <= 1 else 0.98
        nulls_threshold = nulls_threshold if isinstance(nulls_threshold, float) and 0 <= nulls_threshold <= 1 else 0.95
        stylise = stylise if isinstance(stylise, bool) else False
        # cast the values
        tbl = Commons.table_cast(canonical, cat_max=cat_threshold)
        # dictionary
        _null_columns = 0
        _dom_columns = 0
        _date_columns = 0
        _bool_columns = 0
        _cat_columns = 0
        _num_columns = 0
        _int_columns = 0
        _str_columns = 0
        _nest_columns = 0
        _other_columns = 0
        _key_columns = 0
        for n in tbl.column_names:
            c = tbl.column(n).combine_chunks()
            if pa.types.is_nested(c.type):
                _nest_columns += 1
                continue
            if not pa.types.is_dictionary(c.type):
                if pc.count(c).as_py() == 0 or c.null_count/pc.count(c).as_py() > nulls_threshold:
                    _null_columns += 1
                elif pc.count_distinct(c.drop_null()).as_py() == pc.count(c).as_py():
                    _key_columns += 1
                elif 1-(pc.count_distinct(c.drop_null()).as_py()/pc.count(c).as_py()) > dom_threshold:
                    _dom_columns += 1
                elif pc.count_distinct(c.drop_null()).as_py() == pc.count(c).as_py():
                    _key_columns += 1
            if pa.types.is_dictionary(c.type):
                _cat_columns += 1
            elif pa.types.is_string(c.type):
                _str_columns += 1
            elif pa.types.is_integer(c.type):
                _int_columns += 1
            elif pa.types.is_floating(c.type):
                _num_columns += 1
            elif pa.types.is_boolean(c.type):
                _bool_columns += 1
            elif pa.types.is_timestamp(c.type) or pa.types.is_time(c.type):
                _date_columns += 1
            else:
                _other_columns += 1
        # dictionary
        _usable_columns = _date_columns + _bool_columns + _cat_columns + _num_columns + _int_columns + _str_columns
        _null_avg = _null_columns / canonical.num_columns
        _dom_avg = _dom_columns / canonical.num_columns
        _quality_avg = int(round(100 - (((_null_avg + _dom_avg) / 2) * 100), 0))
        _usable = int(round((_usable_columns / canonical.num_columns) * 100, 2))
        _dt_today = pd.to_datetime('today')
        mem_usage = canonical.get_total_buffer_size()
        _tbl_mem = f"{mem_usage >> 20} Mb" if mem_usage >> 20 > 0 else f"{mem_usage} bytes"
        mem_usage = pa.total_allocated_bytes()
        _tot_mem = f"{mem_usage >> 20} Mb" if mem_usage >> 20 > 0 else f"{mem_usage} bytes"
        report = {
            'timestamp': {'readable': _dt_today.strftime('%d %B %Y %I:%M %p'),
                          'semantic': _dt_today.strftime('%Y-%m-%d %H:%M:%S')},
            'score': {'quality_avg': f"{_quality_avg}%", 'usability_avg': f"{_usable}%"},
            'data_shape': {'rows': canonical.num_rows, 'columns': canonical.num_columns,
                         'tbl_memory': _tbl_mem, 'total_allocated': _tot_mem},
            'data_type': {'floating': _num_columns, 'integer': _int_columns,
                          'category': _cat_columns, 'datetime': _date_columns,
                          'bool': _bool_columns,'string': _str_columns,
                          'nested': _nest_columns, 'others': _other_columns},
            'usability': {'mostly_null': _null_columns,
                        'predominance': _dom_columns,
                        'candidate_keys': _key_columns}
        }
        # convert to multi-index DataFrame
        result = pd.DataFrame.from_dict(report, orient="index").stack().to_frame()
        result = pd.DataFrame(result[0].values.tolist(), index=result.index, columns=['summary'])
        result['summary'] = result['summary'].apply(str).str.replace('.0', '', regex=False)
        result = result.reset_index(names=['sections', 'elements'])
        if stylise:
            return Commons.report(result, index_header='sections', bold=['elements'])
        return pa.Table.from_pandas(result)


    @staticmethod
    def data_dictionary(canonical: pa.Table, table_cast: bool=None, display_width: int=None, stylise: bool=None):
        """ The data dictionary for a given canonical

        :param canonical: The canonical to interpret
        :param table_cast: attempt to cast columns to the content
        :param display_width: the width of the display
        :param stylise: if the output is stylised for jupyter display
        :return: a pa.Table or stylised pandas
        """
        display_width = display_width if isinstance(display_width, int) else 50
        stylise = stylise if isinstance(stylise, bool) else False
        record = []
        labels = [f'Attributes', 'DataType', 'Nulls', 'Dominate', 'Valid', 'Unique', 'Observations']
        # attempt cast
        if isinstance(table_cast, bool) and table_cast:
            canonical = Commons.table_cast(canonical)
        for c in canonical.column_names:
            column = canonical.column(c).combine_chunks()
            if pa.types.is_nested(column.type):
                s = str(column.slice(0,20).to_pylist())
                if len(s) > display_width:
                    s = s[:display_width] + "..."
                record.append([c,'nested',0,0,1,1,s])
                continue
            # data type
            line = [c,
                    'category' if pc.starts_with(str(column.type), 'dict').as_py() else str(column.type),
                    # null percentage
                    round(column.null_count / canonical.num_rows, 3)]
            # dominant percentage
            arr_vc = column.value_counts()
            value = arr_vc.filter(pc.equal(arr_vc.field(1), pc.max(arr_vc.field(1)))).field(1)[0].as_py()
            line.append(round(value / canonical.num_rows, 3))
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
