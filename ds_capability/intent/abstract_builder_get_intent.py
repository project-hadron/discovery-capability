from abc import abstractmethod
from typing import Any
import numpy as np
import pandas as pd
import pyarrow as pa
from scipy import stats
from ds_capability.components.commons import Commons
from ds_capability.intent.abstract_common_intent import AbstractCommonsIntentModel


class AbstractBuilderGetIntent(AbstractCommonsIntentModel):

    @abstractmethod
    def run_intent_pipeline(self, *args, **kwargs) -> [None, tuple]:
        """ Collectively runs all parameterised intent taken from the property manager against the code base as
        defined by the intent_contract.
        """

    def _get_number(self, start: Any=None, stop: Any=None, relative_freq: list=None, precision: int=None,
                    ordered: str=None, at_most: int=None, size: int=None, seed: int=None) -> list:
        """ returns a number in the range from_value to to_value. if only one number given from_value is zero
    
        :param start: optional, (signed) integer or float to start from. See below
        :param stop: (signed) integer or float the number sequence goes to but not include. See below
        :param relative_freq: a weighting pattern or probability that does not have to add to 1
        :param precision: the precision of the returned number. if None then assumes int value else float
        :param ordered: order the data ascending 'asc' or descending 'dec', values accepted 'asc' or 'des'
        :param at_most: the most times a selection should be chosen
        :param size: the size of the sample
        :param seed: a seed value for the random function: default to None
    
        The values can be represented by an environment variable with the format '${NAME}' where NAME is the
        environment variable name
        """
        start = self._extract_value(start)
        stop = self._extract_value(stop)
        if not isinstance(size, int):
            raise ValueError("size not set. Size must be an int greater than zero")
        if not isinstance(start, (int, float)) and not isinstance(stop, (int, float)):
            raise ValueError(f"either a 'from_value' or a 'from_value' and 'to_value' must be provided")
        if not isinstance(start, (float, int)):
            start = 0
        if not isinstance(stop, (float, int)):
            (start, stop) = (0, start)
        if stop <= start:
            raise ValueError("The number range must be a positive difference, where to_value <= from_value")
        at_most = 0 if not isinstance(at_most, int) else at_most
#        size = size if isinstance(size, int) else 1
        _seed = self._seed() if seed is None else seed
        precision = 3 if not isinstance(precision, int) else precision
        if precision == 0:
            start = int(round(start, 0))
            stop = int(round(stop, 0))
        is_int = True if (isinstance(stop, int) and isinstance(start, int)) else False
        if is_int:
            precision = 0
        # build the distribution sizes
        if isinstance(relative_freq, list) and len(relative_freq) > 1 and sum(relative_freq) > 1:
            freq_dist_size = self._freq_dist_size(relative_freq=relative_freq, size=size, seed=_seed)
        else:
            freq_dist_size = [size]
        # generate the numbers
        rtn_list = []
        generator = np.random.default_rng(seed=_seed)
        d_type = int if is_int else float
        bins = np.linspace(start, stop, len(freq_dist_size) + 1, dtype=d_type)
        for idx in np.arange(1, len(bins)):
            low = bins[idx - 1]
            high = bins[idx]
            if low >= high:
                continue
            elif at_most > 0:
                sample = []
                for _ in np.arange(at_most, dtype=d_type):
                    count_size = freq_dist_size[idx - 1] * generator.integers(2, 4, size=1)[0]
                    sample += list(set(np.linspace(bins[idx - 1], bins[idx], num=count_size, dtype=d_type,
                                                   endpoint=False)))
                if len(sample) < freq_dist_size[idx - 1]:
                    raise ValueError(f"The value range has insufficient samples to choose from when using at_most."
                                     f"Try increasing the range of values to sample.")
                rtn_list += list(generator.choice(sample, size=freq_dist_size[idx - 1], replace=False))
            else:
                if d_type == int:
                    rtn_list += generator.integers(low=low, high=high, size=freq_dist_size[idx - 1]).tolist()
                else:
                    choice = generator.random(size=freq_dist_size[idx - 1], dtype=float)
                    choice = np.round(choice * (high - low) + low, precision).tolist()
                    # make sure the precision
                    choice = [high - 10 ** (-precision) if x >= high else x for x in choice]
                    rtn_list += choice
        # order or shuffle the return list
        if isinstance(ordered, str) and ordered.lower() in ['asc', 'des']:
            rtn_list.sort(reverse=True if ordered.lower() == 'asc' else False)
        else:
            generator.shuffle(rtn_list)
        return rtn_list

    def _get_category(self, selection: list, size: int, relative_freq: list=None,
                      seed: int=None) -> list:
        """ returns a category from a list. Of particular not is the at_least parameter that allows you to
        control the number of times a selection can be chosen.
    
        :param selection: a list of items to select from
        :param size: size of the return
        :param relative_freq: a weighting pattern that does not have to add to 1
        :param seed: a seed value for the random function: default to None
        :return: an item or list of items chosen from the list
        """
        if len(selection) < 1:
            return [None] * size
        seed = self._seed() if seed is None else seed
        relative_freq = relative_freq if isinstance(relative_freq, list) else [1]*len(selection)
        select_index = self._freq_dist_size(relative_freq=relative_freq, size=size, dist_length=len(selection),
                                                  dist_on='right', seed=seed)
        rtn_list = []
        for idx in range(len(select_index)):
            rtn_list += [selection[idx]]*select_index[idx]
        gen = np.random.default_rng(seed)
        gen.shuffle(rtn_list)
        return rtn_list
    
    def _get_datetime(self, start: Any, until: Any, relative_freq: list=None, at_most: int=None, ordered: str=None,
                      date_format: str=None, as_num: bool=None, ignore_time: bool=None, ignore_seconds: bool=None,
                      size: int=None, seed: int=None, day_first: bool=None, year_first: bool=None) -> list:
        """ returns a random date between two date and/or times. weighted patterns can be applied to the overall date
        range.
        if a signed 'int' type is passed to the start and/or until dates, the inferred date will be the current date
        time with the integer being the offset from the current date time in 'days'.
        if a dictionary of time delta name values is passed this is treated as a time delta from the start time.
        for example if start = 0, until = {days=1, hours=3} the date range will be between now and 1 days and 3 hours
    
        Note: If no patterns are set this will return a linearly random number between the range boundaries.
    
        :param start: the start boundary of the date range can be str, datetime, pd.datetime, pd.Timestamp or int
        :param until: up until boundary of the date range can be str, datetime, pd.datetime, pd.Timestamp, pd.delta, int
        :param relative_freq: (optional) A pattern across the whole date range.
        :param at_most: the most times a selection should be chosen
        :param ordered: order the data ascending 'asc' or descending 'dec', values accepted 'asc' or 'des'
        :param ignore_time: ignore time elements and only select from Year, Month, Day elements. Default is False
        :param ignore_seconds: ignore second elements and only select from Year to minute elements. Default is False
        :param date_format: the string format of the date to be returned. if not set then pd.Timestamp returned
        :param as_num: returns a list of Matplotlib date values as a float. Default is False
        :param size: the size of the sample to return. Default to 1
        :param seed: a seed value for the random function: default to None
        :param year_first: specifies if to parse with the year first
                If True parses dates with the year first, eg 10/11/12 is parsed as 2010-11-12.
                If both dayfirst and yearfirst are True, yearfirst is preceded (same as dateutil).
        :param day_first: specifies if to parse with the day first
                If True, parses dates with the day first, eg %d-%m-%Y.
                If False default to the a preferred preference, normally %m-%d-%Y (but not strict)
        :return: a date or size of dates in the format given.
         """
        # pre check
        if not isinstance(size, int):
            raise ValueError("size not set. Size must be an int greater than zero")
        if start is None or until is None:
            raise ValueError("The start or until parameters cannot be of NoneType")
        # Code block for intent
        as_num = as_num if isinstance(as_num, bool) else False
        ignore_seconds = ignore_seconds if isinstance(ignore_seconds, bool) else False
        ignore_time = ignore_time if isinstance(ignore_time, bool) else False
        size = 1 if size is None else size
        _seed = self._seed() if seed is None else seed
        # start = start.to_pydatetime() if isinstance(start, pd.Timestamp) else start
        # until = until.to_pydatetime() if isinstance(until, pd.Timestamp) else until
        if isinstance(start, int):
            start = (pd.Timestamp.now() + pd.Timedelta(days=start))
        start = pd.to_datetime(start, errors='coerce', dayfirst=day_first,
                               yearfirst=year_first)
        if isinstance(until, int):
            until = (pd.Timestamp.now() + pd.Timedelta(days=until))
        elif isinstance(until, dict):
            until = (start + pd.Timedelta(**until))
        until = pd.to_datetime(until, errors='coerce', dayfirst=day_first,
                               yearfirst=year_first)
        if start == until:
            rtn_list = pd.Series([start] * size)
        else:
            dt_tz = pd.Series(start).dt.tz
            _dt_start = Commons.date2value(start, day_first=day_first, year_first=year_first)[0]
            _dt_until = Commons.date2value(until, day_first=day_first, year_first=year_first)[0]
            precision = 15
            rtn_list = self._get_number(start=_dt_start, stop=_dt_until, relative_freq=relative_freq,
                                        at_most=at_most, ordered=ordered, precision=precision, size=size, seed=seed)
            rtn_list = pd.Series(Commons.value2date(rtn_list, dt_tz=dt_tz))
        if ignore_time:
            rtn_list = pd.Series(pd.DatetimeIndex(rtn_list).normalize())
        if ignore_seconds:
            rtn_list = rtn_list.apply(lambda t: t.replace(second=0, microsecond=0, nanosecond=0))
        if as_num:
            return Commons.date2value(rtn_list)
        if isinstance(date_format, str) and len(rtn_list) > 0:
            rtn_list = rtn_list.dt.strftime(date_format)
        return rtn_list.to_list()
    
    
    def _get_intervals(self, intervals: list, relative_freq: list=None, precision: int=None, size: int=None,
                       seed: int=None) -> list:
        """ returns a number based on a list selection of tuple(lower, upper) interval
    
        :param intervals: a list of unique tuple pairs representing the interval lower and upper boundaries
        :param relative_freq: a weighting pattern or probability that does not have to add to 1
        :param precision: the precision of the returned number. if None then assumes float
        :param size: the size of the sample
        :param seed: a seed value for the random function: default to None
        :return: a random number
        """
        # Code block for intent
        if not isinstance(size, int):
            raise ValueError("size not set. Size must be an int greater than zero")
        precision = precision if isinstance(precision, (float, int)) else 3
        _seed = self._seed() if seed is None else seed
        if not all(isinstance(value, tuple) for value in intervals):
            raise ValueError("The intervals list must be a list of tuples")
        interval_list = self._get_category(selection=intervals, relative_freq=relative_freq, size=size, seed=_seed)
        interval_counts = pd.Series(interval_list, dtype='object').value_counts()
        rtn_list = []
        for index in interval_counts.index:
            size = interval_counts[index]
            if size == 0:
                continue
            if len(index) == 2:
                (lower, upper) = index
                if index == 0:
                    closed = 'both'
                else:
                    closed = 'right'
            else:
                (lower, upper, closed) = index
            if lower == upper:
                rtn_list += [round(lower, precision)] * size
                continue
            if precision == 0:
                margin = 1
            else:
                margin = 10 ** (((-1) * precision) - 1)
            if str.lower(closed) == 'neither':
                lower += margin
                upper -= margin
            elif str.lower(closed) == 'right':
                lower += margin
            elif str.lower(closed) == 'both':
                upper += margin
            # correct adjustments
            if lower >= upper:
                upper = lower + margin
            rtn_list += self._get_number(lower, upper, precision=precision, size=size, seed=_seed)
        np.random.default_rng(seed=_seed).shuffle(rtn_list)
        return rtn_list
    
    
    def _get_dist_normal(self, mean: float, std: float, precision: int=None, size: int=None, seed: int=None) -> list:
        """A normal (Gaussian) continuous random distribution.
    
        :param mean: The mean (“centre”) of the distribution.
        :param std: The standard deviation (jitter or “width”) of the distribution. Must be >= 0
        :param precision: The number of decimal points. The default is 3
        :param size: the size of the sample. if a tuple of intervals, size must match the tuple
        :param seed: a seed value for the random function: default to None
        :return: a random number
        """
        if not isinstance(size, int):
            raise ValueError("size not set. Size must be an int greater than zero")
        _seed = self._seed() if seed is None else seed
        precision = precision if isinstance(precision, int) else 3
        generator = np.random.default_rng(seed=_seed)
        rtn_list = list(generator.normal(loc=mean, scale=std, size=size))
        return list(np.around(rtn_list, precision))
    
    def _get_dist_choice(self, number: [int, str, float], size: int=None, seed: int=None) -> list:
        """Creates a list of latent values of 0 or 1 where 1 is randomly selected both upon the number given.
    
       :param number: The number of true (1) values to randomly chose from the canonical. see below
       :param size: the size of the sample. if a tuple of intervals, size must match the tuple
       :param seed: a seed value for the random function: default to None
       :return: a list of 1 or 0
    
        As choice is a fixed value, number can be represented by an environment variable with the format '${NAME}'
        where NAME is the environment variable name
    
        If number is an int then that number of 1's are chosen. If number is a float between 0 and 1 it is taken as
        a fraction of the total variable count
        """
        if not isinstance(size, int):
            raise ValueError("size not set. Size must be an int greater than zero")
        _seed = self._seed() if seed is None else seed
        number = self._extract_value(number)
        number = int(number * size) if isinstance(number, float) and 0 <= number <= 1 else int(number)
        number = number if 0 <= number < size else size
        if isinstance(number, int) and 0 <= number <= size:
            rtn_list = pd.Series(data=[0] * size)
            choice_idx = self._get_number(stop=size, size=number, at_most=1, precision=0, ordered='asc', seed=_seed)
            rtn_list.iloc[choice_idx] = [1] * number
            return rtn_list.reset_index(drop=True).to_list()
        return pd.Series(data=[0] * size).to_list()
    
    def _get_dist_bernoulli(self, probability: float, size: int=None, seed: int=None) -> list:
        """A Bernoulli process is a discrete random distribution. Bernoulli trial is a random experiment with exactly
        two possible outcomes, "success" and "failure", in which the probability of success is the same every time
        the experiment is conducted.
    
        The mathematical formalisation of the Bernoulli trial, this distribution,  is known as the Bernoulli process.
        A Bernoulli process is a finite or infinite sequence of binary random variables. Prosaically, a Bernoulli
        process is a repeated coin flipping, possibly with an unfair coin (but with consistent unfairness).

        As probability is a fixed value, probability can be represented by an environment variable with the
        format '${NAME}' where NAME is the environment variable name
    
        :param probability: the probability occurrence of getting a 1 or 0
        :param size: the size of the sample
        :param seed: a seed value for the random function: default to None
        :return: a random number
        """
        if not isinstance(size, int):
            raise ValueError("size not set. Size must be an int greater than zero")
        _seed = self._seed() if seed is None else seed
        probability = self._extract_value(probability)
        rtn_list = list(stats.bernoulli.rvs(p=probability, size=size, random_state=_seed))
        return rtn_list

    def _get_dist_bounded_normal(self, mean: float, std: float, lower: float, upper: float, precision: int=None,
                                 size: int=None, seed: int=None) -> list:
        """A bounded normal continuous random distribution.
    
        :param mean: the mean of the distribution
        :param std: the standard deviation
        :param lower: the lower limit of the distribution
        :param upper: the upper limit of the distribution
        :param precision: the precision of the returned number. if None then assumes int value else float
        :param size: the size of the sample
        :param seed: a seed value for the random function: default to None
        :return: a random number
        """
        if not isinstance(size, int):
            raise ValueError("size not set. Size must be an int greater than zero")
        precision = precision if isinstance(precision, int) else 3
        seed = self._seed() if seed is None else seed
        rtn_list = stats.truncnorm((lower - mean) / std, (upper - mean) / std, loc=mean, scale=std)
        rtn_list = rtn_list.rvs(size, random_state=seed).round(precision)
        return rtn_list

    def _get_distribution(self, distribution: str, is_stats: bool=None, precision: int=None, size: int=None,
                          seed: int=None, **kwargs) -> list:
        """returns a number based the distribution type.
    
        :param distribution: The string name of the distribution function from numpy random Generator class
        :param is_stats: (optional) if the generator is from the stats package and not numpy
        :param precision: (optional) the precision of the returned number
        :param size: (optional) the size of the sample
        :param seed: (optional) a seed value for the random function: default to None
        :return: a random number
        """
        if not isinstance(size, int):
            raise ValueError("size not set. Size must be an int greater than zero")
        _seed = self._seed() if seed is None else seed
        precision = 3 if precision is None else precision
        is_stats = is_stats if isinstance(is_stats, bool) else False
        if is_stats:
            rtn_list = eval(f"stats.{distribution}.rvs(size=size, random_state=_seed, **kwargs)", globals(), locals())
        else:
            generator = np.random.default_rng(seed=_seed)
            rtn_list = eval(f"generator.{distribution}(size=size, **kwargs)", globals(), locals())
        return list(np.around(rtn_list, precision))

    def _correlate_number(self, canonical: pa.Array, choice: [int, float, str ] =None, choice_header: str =None,
                          jitter: [int, float, str ] =None, offset: [int, float, str ] =None, code_str: str =None,
                          lower: [int, float ] =None, upper: [int, float ] =None, precision: int =None, keep_zero: bool =None,
                          seed: int =None):
        """ correlate a list of continuous values adjusting those values, or a subset of those values, with a
        normalised jitter (std from the value) along with a value offset. ``choice``, ``jitter`` and ``offset``
        can accept environment variable string names starting with ``${`` and ending with ``}``.

        If the choice is an int, it represents the number of rows to choose. If the choice is a float it must be
        between 1 and 0 and represent a percentage of rows to choose.

        :param canonical: a pd.DataFrame as the reference dataframe
        :param choice: (optional) The number of values or percentage between 0 and 1 to choose.
        :param choice_header: (optional) those not chosen are given the values of the given header
        :param precision: (optional) to what precision the return values should be
        :param offset: (optional) a fixed value or an environment variable where the name is wrapped with '${' and '}'
        :param code_str: (optional) passing a str lambda function. e.g. 'lambda x: (x - 3) / 2''
        :param jitter: (optional) a perturbation of the value where the jitter is a random normally distributed std
        :param precision: (optional) how many decimal places. default to 3
        :param seed: (optional) the random seed. defaults to current datetime
        :param keep_zero: (optional) if True then zeros passed remain zero despite a change, Default is False
        :param lower: a minimum value not to go below
        :param upper: a max value not to go above
        :return: list
        """
        s_values = canonical.to_pandas()
        s_others = s_values.copy()
        other_size = s_others.size
        seed = self._seed() if seed is None else seed
        offset = self._extract_value(offset)
        keep_zero = keep_zero if isinstance(keep_zero, bool) else False
        precision = precision if isinstance(precision, int) else 3
        lower = lower if isinstance(lower, (int, float)) else float('-inf')
        upper = upper if isinstance(upper, (int, float)) else float('inf')
        # mark the zeros and nulls
        null_idx = s_values[s_values.isna()].index
        zero_idx = s_values.where(s_values == 0).dropna().index if keep_zero else []
        # choose the items to jitter
        if isinstance(choice, (str, int, float)):
            size = s_values.size
            choice = self._extract_value(choice)
            choice = int(choice * size) if isinstance(choice, float) and 0 <= choice <= 1 else int(choice)
            choice = choice if 0 <= choice < size else size
            gen = np.random.default_rng(seed=seed)
            choice_idx = gen.choice(s_values.index, size=choice, replace=False)
            choice_idx = [choice_idx] if isinstance(choice_idx, int) else choice_idx
            s_values = s_values.iloc[choice_idx]
        if isinstance(jitter, (str, int, float)) and s_values.size > 0:
            jitter = self._extract_value(jitter)
            size = s_values.size
            gen = np.random.default_rng(seed)
            results = gen.normal(loc=0, scale=jitter, size=size)
            s_values = s_values.add(results)
        # set code_str
        if isinstance(code_str, str) and s_values.size > 0:
            if code_str.startswith('lambda'):
                s_values = s_values.transform(eval(code_str))
            else:
                code_str = code_str.replace("@", 'x')
                s_values = s_values.transform(lambda x: eval(code_str))
        # set offset for all values
        if isinstance(offset, (int, float)) and offset != 0 and s_values.size > 0:
            s_values = s_values.add(offset)
        # set the changed values
        if other_size == s_values.size:
            s_others = s_values
        else:
            s_others.iloc[s_values.index] = s_values
        # max and min caps
        s_others = pd.Series([upper if x > upper else x for x in s_others])
        s_others = pd.Series([lower if x < lower else x for x in s_others])
        if isinstance(keep_zero, bool) and keep_zero:
            if other_size == zero_idx.size:
                s_others = 0 * zero_idx.size
            else:
                s_others.iloc[zero_idx] = 0
        if other_size == null_idx.size:
            s_others = np.nan * null_idx.size
        else:
            s_others.iloc[null_idx] = np.nan
        s_others = s_others.round(precision)
        if precision == 0 and not s_others.isnull().any():
            s_others = s_others.astype(int)
        return s_others.to_list()

