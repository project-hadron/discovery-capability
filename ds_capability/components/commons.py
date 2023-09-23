from typing import Any
import pandas as pd
import pyarrow as pa
from ds_core.components.core_commons import CoreCommons


class Commons(CoreCommons):

    @staticmethod
    def date2value(dates: Any, day_first: bool=True, year_first: bool=False) -> list:
        """ converts a date to a number represented by to number of microseconds to the epoch"""
        values = pd.Series(pd.to_datetime(dates, errors='coerce', dayfirst=day_first, yearfirst=year_first))
        v_native = values.dt.tz_convert(None) if values.dt.tz else values
        null_idx = values[values.isna()].index
        values.iloc[null_idx] = pd.to_datetime(0)
        result =  ((v_native - pd.Timestamp("1970-01-01")) / pd.Timedelta(microseconds=1)).astype(int).to_list()
        values.iloc[null_idx] = None
        return result

    @staticmethod
    def value2date(values: Any, dt_tz: Any=None, date_format: str=None) -> list:
        """ converts an integer into a datetime. The integer should represent time in microseconds since the epoch"""
        if dt_tz:
            dates = pd.Series(pd.to_datetime(values, unit='us', utc=True)).map(lambda x: x.tz_convert(dt_tz))
        else:
            dates = pd.Series(pd.to_datetime(values, unit='us'))
        if isinstance(date_format, str):
            dates = dates.dt.strftime(date_format)
        return dates.to_list()

    @staticmethod
    def report(canonical: pd.DataFrame, index_header: [str, list]=None, bold: [str, list]=None,
               large_font: [str, list]=None):
        """ generates a stylised report

        :param canonical: the DataFrame to report on
        :param index_header: the header to index on
        :param bold: any columns to make bold
        :param large_font: any columns to enlarge
        :return: stylised report DataFrame
        """
        index_header = Commons.list_formatter(index_header)
        pd.set_option('max_colwidth', 200)
        pd.set_option('expand_frame_repr', True)
        bold = Commons.list_formatter(bold)
        bold += index_header
        large_font = Commons.list_formatter(large_font)
        large_font += index_header
        style = [{'selector': 'th', 'props': [('font-size', "120%"), ("text-align", "center")]},
                 {'selector': '.row_heading, .blank', 'props': [('display', 'none;')]}]
        for header in index_header:
            prev = ''
            for idx in range(len(canonical[header])):
                if canonical[header].iloc[idx] == prev:
                    canonical[header].iloc[idx] = ''
                else:
                    prev = canonical[header].iloc[idx]
        canonical = canonical.reset_index(drop=True)
        df_style = canonical.style.set_table_styles(style)
        _ = df_style.set_properties(**{'text-align': 'left'})
        if len(bold) > 0:
            _ = df_style.set_properties(subset=bold, **{'font-weight': 'bold'})
        if len(large_font) > 0:
            _ = df_style.set_properties(subset=large_font, **{'font-size': "120%"})
        return df_style

    @staticmethod
    def table_report(t: pa.Table, index_header: [str, list]=None, bold: [str, list]=None,
                     large_font: [str, list]=None):
        """ generates a stylised version of the pyarrow table """
        df = pd.DataFrame(Commons.table_nest(t))
        return Commons.report(df, index_header=index_header, bold=bold, large_font=large_font)


# class Condition(object):
#
#     def __init__(self, compare: [str, int, float, list, pa.Array, pa.Scalar], operator: str,
#                  logic: str = None, mask_null: str = None):
#         self.compare = compare
#         self.operator = operator
#         self.logic = logic if isinstance(logic, str) else 'or_'
#         self.mask_null = mask_null if isinstance(mask_null, str) else False
#
#     @classmethod
#     def from_dict(cls, condition: dict):
#         c = condition.get('compare')
#         o = condition.get('operator')
#         l = condition.get('logic', 'or_')
#         m = condition.get('mask_null', False)
#         return cls(compare=c, operator=o, logic=l, mask_null=m)
#
#     @classmethod
#     def from_tuple(cls, condition: tuple):
#         if len(condition) == 4:
#             (c, o, l, m) = condition
#             return cls(compare=c, operator=o, logic=l, mask_null=m)
#         if len(condition) == 3 and isinstance(condition[3], bool):
#             (c, o, m) = condition
#             return cls(compare=c, operator=o, logic='or_', mask_null=m)
#         if len(condition) == 3:
#             (c, o, l) = condition
#             return cls(compare=c, operator=o, logic=l, mask_null=False)
#         if len(condition) == 3:
#             (c, o) = condition
#             return cls(compare=c, operator=o, logic='or_', mask_null=False)
#         raise ValueError("The tuple must be between two and four elements")
#
#     def condition(self) -> tuple:
#         return self.compare, self.operator, self.logic
#
#     def to_dict(self):
#         if isinstance(self.compare, pa.Array):
#             compare = self.compare.to_pylist()
#         elif isinstance(self.compare, pa.Scalar):
#             compare = self.compare.as_py()
#         else:
#             compare = self.compare
#         return {'compare': compare, 'operator': self.operator, 'logic': self.logic, 'mask_null': self.mask_null}
#
#     def __repr__(self):
#         return f"<class 'Condition({type(self.compare)}, {type(self.operator)}, {type(self.logic)}, " \
#                f"{type(self.mask_null)})'>"
#
#     def __str__(self):
#         compare = self.compare if isinstance(self.compare, (str, int, float, pa.Scalar)) else type(self.compare)
#         return f"Selection:\n\tcompare = {compare}\n\toperator = {self.operator}\n\tlogic = {self.logic}" \
#                f"\n\tmask_null = {self.mask_null}"
#
#
# class Selection(Condition):
#
#     def __init__(self, header: str, compare: [str, int, float, list, pa.Array, pa.Scalar], operator: str,
#                  logic: str = None, mask_null: str = None):
#         super().__init__(compare=compare, operator=operator, logic=logic, mask_null=mask_null)
#         self.header = header
#
#     def to_dict(self):
#         if isinstance(self.compare, pa.Array):
#             compare = self.compare.to_pylist()
#         elif isinstance(self.compare, pa.Scalar):
#             compare = self.compare.as_py()
#         else:
#             compare = self.compare
#         return {'header': self.header, 'compare': compare, 'operator': self.operator, 'logic': self.logic,
#                 'mask_null': self.mask_null}
#
#     def __repr__(self):
#         return f"<class 'Condition({type(self.header)}, {type(self.compare)}, {type(self.operator)}, {type(self.logic)}, {type(self.mask_null)})'>"
#
#     def __str__(self):
#         compare = self.compare if isinstance(self.compare, (str, int, float, pa.Scalar)) else type(self.compare)
#         return f"Selection:\n\theader = {self.header}\n\tcompare = {compare}\n\toperator = {self.operator}\n\tlogic = {self.logic}\n\tmask_null = {self.mask_null}"
