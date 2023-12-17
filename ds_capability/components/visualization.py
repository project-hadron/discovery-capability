import random
import pyarrow as pa
import pandas as pd
from scipy import stats
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt


class Visualisation(object):
    """ a set of data components methods to Visualise pandas.Dataframe"""

    @staticmethod
    def show_chi_square(canonical: pa.Table, target: [str, list], capped_at: int=None, seed: int=None):
        """Chi-square is one of the most widely used supervised feature selection methods. It selects each feature
         independently in accordance with their scores against a target or label then ranks them by their importance.
         This score should be used to evaluate categorical variables in a classification task."""
        cap = capped_at if isinstance(capped_at, int) else 10
        if canonical.num_rows > cap > 0:
            sample = random.sample(range(canonical.num_rows), k=cap)
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

