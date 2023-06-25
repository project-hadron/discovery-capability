import time
from abc import abstractmethod
import numpy as np
import pandas as pd
import pyarrow as pa
from aistac.handlers.abstract_handlers import ConnectorContract, HandlerFactory
from aistac.intent.abstract_intent import AbstractIntentModel

__author__ = 'Darryl Oatridge'


class AbstractCommonsIntentModel(AbstractIntentModel):

    @classmethod
    def __dir__(cls):
        """returns the list of available methods associated with the parameterized intent"""
        rtn_list = []
        for m in dir(cls):
            if not m.startswith('_'):
                rtn_list.append(m)
        return rtn_list

    @abstractmethod
    def run_intent_pipeline(self, *args, **kwargs) -> [None, tuple]:
        """ Collectively runs all parameterised intent taken from the property manager against the code base as
        defined by the intent_contract.
        """

    """
        PRIVATE METHODS SECTION
    """
    def _get_canonical(self, data: [pa.Table, pa.Array, pd.DataFrame, pd.Series, list, dict, str],
                       header: str=None) -> pa.Table:
        """
        :param data: a dataframe or action event to generate a dataframe
        :param header: (optional) header for pd.Series or list
        :return: a pd.Dataframe
        """
        if isinstance(data, pa.Table):
            return data
        if isinstance(data, pd.DataFrame):
            return pa.Table.from_pandas(df=data)
        if isinstance(data, pd.Series):
            header = header if isinstance(header, str) else 'default'
            arr = pa.Array.from_pandas(data)
            return pa.table([arr], names=[header])
        elif isinstance(data, str):
            if not self._pm.has_connector(connector_name=data):
                raise ValueError(f"The data connector name '{data}' is not in the connectors catalog")
            handler = self._pm.get_connector_handler(data)
            canonical = handler.load_canonical()
            return canonical
        raise ValueError(f"The canonical format is not recognised, pd.DataFrame, pd.Series, "
                         f"str, list or dict expected, {type(data)} passed")

    @staticmethod
    def _extract_value(value: [str, int, float]):
        if isinstance(value, str):
            if value.startswith('${') and value.endswith('}'):
                value = ConnectorContract.parse_environ(value)
                if value.isnumeric():
                    return int(value)
                elif value.replace('.', '', 1).isnumeric():
                    return float(value)
                else:
                    return str(value)
            else:
                return str(value)
        return value

    @staticmethod
    def _seed(seed: int=None, increment: bool=False):
        if not isinstance(seed, int):
            return int(time.time() * np.random.default_rng().random())
        if increment:
            seed += 1
            if seed > 2 ** 31:
                seed = int(time.time() * np.random.default_rng(seed=seed-1).random())
        return seed

    """
        UTILITY METHODS SECTION
    """

    @staticmethod
    def _freq_dist_size(relative_freq: list, size: int, dist_length: int=None, dist_on: str=None, seed: int=None):
        """ utility method taking a list of relative frequencies and based on size returns the size distribution
        of element based on the frequency. The distribution is based upon binomial distributions.

        :param relative_freq: a list of int or float values representing a relative distribution frequency
        :param size: the size of the values to be distributed
        :param dist_length: (optional) the expected length of the element's in relative_freq
        :param dist_on: (optional) if element length differs. distribute on 'left', 'right' or 'center'. Default 'right'
        :param seed: (optional) a seed value for the random function: default to None
        :return: an integer list of the distribution that sum to the size
        """
        if not isinstance(relative_freq, list) or not all(isinstance(x, (int, float)) for x in relative_freq):
            raise ValueError("The weighted pattern must be an list of numbers")
        dist_length = dist_length if isinstance(dist_length, int) else len(relative_freq)
        dist_on = dist_on if dist_on in ['right', 'left'] else 'both'
        seed = seed if isinstance(seed, int) else int(time.time() * np.random.random())
        # sort the width
        if len(relative_freq) > dist_length:
            a = np.array(relative_freq)
            trim = dist_length - a.size
            if dist_on.startswith('right'):
                relative_freq = a[:trim]
            elif dist_on.startswith('left'):
                relative_freq = a[abs(trim):]
            else:
                l_size = int(trim/2)
                r_size = a.size + l_size - dist_length
                relative_freq = a[r_size:l_size].tolist()
        if len(relative_freq) < dist_length:
            a = np.array(relative_freq)
            rvalue = a[-1:]
            lvalue = a[:1]
            if dist_on.startswith('left'):
                r_dist = []
                l_dist = np.tile(lvalue, dist_length - a.size)
            elif dist_on.startswith('right'):
                r_dist = np.tile(rvalue, dist_length - a.size)
                l_dist = []
            else:
                l_size = int((dist_length - a.size) / 2)
                r_dist = np.tile(rvalue, l_size)
                l_dist = np.tile(lvalue, dist_length - l_size - a.size)
            relative_freq = np.hstack([l_dist, a, r_dist]).tolist()
        # turn it to percentage
        if sum(relative_freq) != 1:
            relative_freq = np.round(relative_freq / np.sum(relative_freq), 5)
        generator = np.random.default_rng(seed=seed)
        result = list(generator.binomial(n=size, p=relative_freq, size=len(relative_freq)))
        diff = size - sum(result)
        adjust = [0] * len(relative_freq)
        # There is a possibility the required size is not fulfilled, therefore add or remove elements based on freq
        if diff != 0:
            unit = diff / sum(relative_freq)
            for idx in range(len(relative_freq)):
                adjust[idx] = int(round(relative_freq[idx] * unit, 0))
        result = [a + b for (a, b) in zip(result, adjust)]
        # rounding can still make us out by 1
        if sum(result) > size or sum(result) < size:
            gap = sum(result) - size
            result[result.index(max(result))] -= gap
        return result
