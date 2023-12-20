import random
import pyarrow as pa
import pyarrow.compute as pc
import pandas as pd
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
    def show_missing(canonical: pa.Table, capped_at: int=None, **kwargs):
        cap = capped_at if isinstance(capped_at, int) else 5_000_000
        if canonical.num_rows*canonical.num_columns > cap > 0:
            sample = random.sample(range(canonical.num_rows), k=int(cap/canonical.num_columns))
            canonical = canonical.take(sample)
        control = canonical.to_pandas()
        sns.heatmap(control.isnull(), yticklabels=False, cbar=False, cmap='viridis', **kwargs)
        plt.title('missing_data', fontdict={'size': 20})
        plt.tight_layout()
        plt.show()
        plt.clf()
