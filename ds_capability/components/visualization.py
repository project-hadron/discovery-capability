import math
import random
import pyarrow as pa
import pyarrow.compute as pc
import pandas as pd
import numpy as np
from matplotlib.colors import LogNorm

from ds_capability.components.commons import Commons
from scipy import stats
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
import seaborn as sns


class Visualisation(object):
    """ a set of data components methods to Visualise pandas.Dataframe"""

    @staticmethod
    def show_chi_square(canonical: pa.Table, target: str, capped_at: int=None, seed: int=None):
        """ Chi-square is one of the most widely used supervised feature selection methods. It selects each feature
         independently in accordance with their scores against a target or label then ranks them by their importance.
         This score should be used to evaluate categorical variables in a classification task.

        :param canonical: The canonical to apply
        :param target: the str header that constitute a binary target.
        :param capped_at: a cap on the size of elements (columns x rows) to process. default at 5,000,000
        :param seed: a seed value
        :return: plt 2d graph
        """
        if target not in canonical.column_names():
            raise ValueError(f"The target '{target}' can't be found in the canonical")
        if pc.count(pc.unique(canonical.column(target))).as_py() != 2:
            raise ValueError(f"The target '{target}' must only be two unique values")
        cap = capped_at if isinstance(capped_at, int) else 5_000_000
        if canonical.num_rows*canonical.num_columns > cap > 0:
            sample = random.sample(range(canonical.num_rows), k=int(cap/canonical.num_columns))
            canonical = canonical.take(sample)
        control = canonical.to_pandas()
        # separate train and test sets
        X_train, X_test, y_train, y_test = train_test_split(control.drop(target, axis=1), control[target],
                                                            test_size=0.3, random_state=seed)
        chi_ls = []
        for feature in X_train.columns:
            # create contingency table
            c = pd.crosstab(y_train, X_train[feature])
            # chi_test
            p_value = stats.chi2_contingency(c)[1]
            chi_ls.append(p_value)
        pd.Series(chi_ls, index=X_train.columns).sort_values(ascending=True).plot.bar(rot=45)
        plt.ylabel('p value')
        plt.title('Feature importance based on chi-square test', fontdict={'size': 20})
        plt.tight_layout()
        plt.show()
        plt.clf()

    @staticmethod
    def show_missing(canonical: pa.Table, headers: [str, list]=None, d_types: [str, list]=None,
                     regex: [str, list]=None, drop: bool=None, capped_at: int=None, **kwargs):
        """ A heatmap of missing data. Each column shows missing values and where in the column the missing data is.

        :param canonical: a canonical to apply
        :param headers: (optional) a filter on headers from the canonical
        :param d_types: (optional) a filter on data type for the canonical. example [pa.int64(), pa.string()]
        :param regex: (optional) a regular expression to search the headers.
        :param drop: (optional) to drop or not drop the resulting headers.
        :param capped_at: (optional) a cap on the size of elements (columns x rows) to process. default at 5,000,000
        :param kwargs: passed to the seaborn heatmap
        :return: pa.Table
        """
        cap = capped_at if isinstance(capped_at, int) else 5_000_000
        if canonical.num_rows*canonical.num_columns > cap > 0:
            sample = random.sample(range(canonical.num_rows), k=int(cap/canonical.num_columns))
            canonical = canonical.take(sample)
        canonical = Commons.filter_columns(canonical, headers=headers, d_types=d_types, regex=regex, drop=drop)
        control = canonical.to_pandas()
        sns.heatmap(control.isnull(), yticklabels=False, cbar=False, cmap='viridis', **kwargs)
        plt.title('missing data', fontdict={'size': 20})
        plt.tight_layout()
        plt.show()
        plt.clf()

    @staticmethod
    def show_correlated(canonical: pa.Table, headers: [str, list]=None, d_types: [str, list]=None,
                        regex: [str, list]=None, drop: bool=None, capped_at: int=None, **kwargs):
        """ shows correlation as a grid of values for each column pair where correlation is represented by a value
        moving towards 100. This only applies to int and float.

        :param canonical: a canonical to apply
        :param headers: (optional) a filter on headers from the canonical
        :param d_types: (optional) a filter on data type for the canonical. example [pa.int64(), pa.string()]
        :param regex: (optional) a regular expression to search the headers.
        :param drop: (optional) to drop or not drop the resulting headers.
        :param capped_at: (optional) a cap on the size of elements (columns x rows) to process. default at 5,000,000
        :param kwargs: passed to the seaborn heatmap
        :return: pa.Table
        """
        cap = capped_at if isinstance(capped_at, int) else 5_000_000
        if canonical.num_rows*canonical.num_columns > cap > 0:
            sample = random.sample(range(canonical.num_rows), k=int(cap/canonical.num_columns))
            canonical = canonical.take(sample)
        canonical = Commons.filter_columns(canonical, headers=headers, d_types=d_types, regex=regex, drop=drop)
        canonical = Commons.filter_columns(canonical, d_types=[pa.int64(),pa.int32(),pa.int16(),pa.int8(),
                                                               pa.float64(),pa.float32(),pa.float16()])
        control = canonical.to_pandas()
        sns.heatmap(control.corr(), annot=True, cmap='BuGn', robust=True, **kwargs)
        plt.title('correlated data', fontdict={'size': 20})
        plt.tight_layout()
        plt.show()
        plt.clf()

    @staticmethod
    def show_cat_time_index(canonical: pa.Table, target: str, headers: [str, list]=None, d_types: [str, list]=None,
                        regex: [str, list]=None, drop: bool=None, capped_at: int=None, filename=None,
                            logscale=False, subplot_h=2, subplot_w=15, param_scale=8, rotation=360, hspace=0.35):
        """"""
        cap = capped_at if isinstance(capped_at, int) else 5_000_000
        if canonical.num_rows*canonical.num_columns > cap > 0:
            sample = random.sample(range(canonical.num_rows), k=int(cap/canonical.num_columns))
            canonical = canonical.take(sample)
        canonical = Commons.filter_columns(canonical, headers=headers, d_types=d_types, regex=regex, drop=drop)
        canonical = Commons.filter_columns(canonical, d_types=[pa.string()])
        col_names = canonical.column_names
        control = canonical.to_pandas()

        dates = pd.date_range(start=control[target].min(), end=control[target].max())
        n_categories = len(col_names)
        cbar_kws = {'orientation': 'horizontal', 'shrink': 0.5}
        n_subplot_rows = np.ceil(control[target].nunique(dropna=True).divide(param_scale))
        n_subplot_rows[-1] += 1
        n_rows = int(n_subplot_rows.sum())
        grid_weights = {'height_ratios': n_subplot_rows.values}
        cmap = 'rocket_r'
        # cmap = sns.cm.rocket_r
        fig, axes = plt.subplots(n_categories, 1, gridspec_kw=grid_weights, sharex='col',
                                 figsize=(subplot_w, n_rows * subplot_h))
        if n_categories == 1:
            axes = [axes]
        for ii in range(n_categories):
            cc = col_names[ii]
            df_single_cat = control[[col_names, cc]]
            df_single_cat = df_single_cat.loc[df_single_cat[target].notnull(), ]
            df_single_cat['Index'] = df_single_cat[target].dt.date
            df_pivot = df_single_cat.pivot_table(index='Index', columns=cc, aggfunc=len, dropna=True)
            df_pivot.index = pd.to_datetime(df_pivot.index)
            toplot = df_pivot.reindex(dates.date).T

            v_min = toplot.min().min()
            v_max = toplot.max().max()
            toplot.reset_index(level=0, drop=True, inplace=True)
            if logscale:
                cbar_ticks = [math.pow(10, i) for i in range(int(math.floor(math.log10(v_min))),
                                                             int(1 + math.ceil(math.log10(v_max))))]
                log_norm = LogNorm(vmin=v_min, vmax=v_max)
            else:
                cbar_ticks = list(range(int(v_min), int(v_max + 1)))
                if len(cbar_ticks) > 5:
                    v_step = int(math.ceil((v_max - v_min) / 4))
                    cbar_ticks = list(range(int(v_min), int(v_max + 1), v_step))
                log_norm = None
            cbar_kws['ticks'] = cbar_ticks
            if ii < (n_categories - 1):
                cbar_kws['pad'] = 0.05
            else:
                cbar_kws['pad'] = 0.25
            sns.heatmap(toplot, cmap=cmap, ax=axes[ii], norm=log_norm, cbar_kws=cbar_kws, yticklabels=True)
            axes[ii].set_ylabel('')
            axes[ii].set_xlabel('')
            axes[ii].set_title(cc)
            axes[ii].set_yticklabels(axes[ii].get_yticklabels(), rotation=rotation)
            for _, spine in axes[ii].spines.items():
                spine.set_visible(True)
        axes[-1].set_xlabel(target)
        plt.subplots_adjust(bottom=0.05, hspace=hspace)
        if filename is None:
            plt.show()
        else:
            fig.savefig(filename)
        plt.clf()
        return
