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
        if target not in canonical.column_names:
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
    def show_distributions(canonical: pa.Table, target: str, capped_at: int=None):
        """"""
        cap = capped_at if isinstance(capped_at, int) else 5_000_000
        if canonical.num_rows*canonical.num_columns > cap > 0:
            sample = random.sample(range(canonical.num_rows), k=int(cap/canonical.num_columns))
            canonical = canonical.take(sample)
        canonical = Commons.filter_columns(canonical, d_types=[pa.int64(),pa.int32(),pa.int16(),pa.int8(),
                                                               pa.float64(),pa.float32(),pa.float16()])
        control = canonical.to_pandas()
        # Define figure size.
        _ = plt.suptitle('Show Distribution', fontdict={'size': 20})
        # histogram
        plt.subplot(1, 3, 1)
        sns.histplot(control[target], bins=30)
        plt.title('Histogram')
        # Q-Q plot
        plt.subplot(1, 3, 2)
        stats.probplot(control[target], dist="norm", plot=plt)
        plt.ylabel('RM quantiles')
        # boxplot
        plt.subplot(1, 3, 3)
        sns.boxplot(y=control[target])
        plt.title('Boxplot')
        plt.tight_layout()
        plt.show()
        plt.clf()
