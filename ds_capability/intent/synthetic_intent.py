import inspect
import string
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
from typing import Any

from ds_capability.components.commons import Commons
from ds_capability.intent.wrangle_intent import WrangleIntentModel
from ds_capability.managers.synthetic_property_manager import SyntheticPropertyManager
from ds_capability.sample.sample_data import Sample


class SyntheticIntentModel(WrangleIntentModel):

    """Synthetic data is representative data that, depending on its application, holds statistical and
    distributive characteristics of its real world counterpart. This component provides a set of actions
    that focuses on building a synthetic data through knowledge and statistical analysis"""
    
    def __init__(self, property_manager: SyntheticPropertyManager, default_save_intent: bool=None,
                 default_intent_level: [str, int, float]=None, order_next_available: bool=None,
                 default_replace_intent: bool=None):
        """initialisation of the Intent class.

        :param property_manager: the property manager class that references the intent contract.
        :param default_save_intent: (optional) The default action for saving intent in the property manager
        :param default_intent_level: (optional) the default level intent should be saved at
        :param order_next_available: (optional) if the default behaviour for the order should be next available order
        :param default_replace_intent: (optional) the default replace existing intent behaviour
        """
        super().__init__(property_manager=property_manager, default_save_intent=default_save_intent,
                         default_intent_level=default_intent_level, order_next_available=order_next_available,
                         default_replace_intent=default_replace_intent)

    def get_number(self, start: [int, float, str]=None, stop: [int, float, str]=None, relative_freq: list=None,
                   precision: int=None, ordered: str=None, at_most: int=None, size: int=None, quantity: float=None,
                   seed: int=None, save_intent: bool=None, intent_order: int=None, column_name: [int, str]=None,
                   replace_intent: bool=None, remove_duplicates: bool=None) -> pa.Array:
        """ returns a number in the range from_value to to_value. if only to_value given from_value is zero

        :param start: optional (signed) integer or float to start from. See below for str
        :param stop: (signed) integer or float the number sequence goes to but not include. See below
        :param relative_freq: a weighting pattern or probability that does not have to add to 1
        :param precision: the precision of the returned number. if None then assumes int value else float
        :param ordered: order the data ascending 'asc' or descending 'dec', values accepted 'asc' or 'des'
        :param at_most: the most times a selection should be chosen
        :param size: the size of the sample
        :param quantity: a number between 0 and 1 representing data that isn't null
        :param seed: a seed value for the random function: default to None
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param column_name: (optional) the column name that groups intent to create a column
        :param intent_order: (optional) the order in which each intent should run.
                    - If None: default's to -1
                    - if -1: added to a level above any current instance of the intent section, level 0 if not found
                    - if int: added to the level specified, overwriting any that already exist
                    
        :param replace_intent: (optional) if the intent method exists at the level, or default level
                    - True - replaces the current intent method with the new
                    - False - leaves it untouched, disregarding the new intent
                    
        :param remove_duplicates: (optional) removes any duplicate intent in any level that is identical
        :return: a random number

        The values can be represented by an environment variable with the format '${NAME}' where NAME is the
        environment variable name
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   column_name=column_name, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        params = locals()
        [params.pop(k) for k in self._INTENT_PARAMS + ['quantity']]
        # set the seed and call the method
        seed = self._seed(seed=seed)
        rtn_list = self._get_number(seed=seed, **params)
        rtn_list = self._set_quantity(rtn_list, quantity=self._quantity(quantity), seed=seed)
        rtn_arr = pa.NumericArray.from_pandas(rtn_list)
        if rtn_arr.type.equals('double'):
            try:
                rtn_arr = pa.array(rtn_arr, pa.int64())
            except pa.lib.ArrowInvalid:
                pass
        return rtn_arr

    def get_category(self, selection: list, size: int, relative_freq: list=None, quantity: float=None, seed: int=None,
                     save_intent: bool=None, column_name: [int, str]=None, intent_order: int=None,
                     replace_intent: bool=None, remove_duplicates: bool=None) -> pa.Array:
        """ returns a category from a list. Of particular not is the at_least parameter that allows you to
        control the number of times a selection can be chosen.

        :param selection: a list of items to select from
        :param size: size of the return
        :param relative_freq: a weighting pattern that does not have to add to 1
        :param quantity: a number between 0 and 1 representing the percentage quantity of the data
        :param seed: a seed value for the random function: default to None
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param column_name: (optional) the column name that groups intent to create a column
        :param intent_order: (optional) the order in which each intent should run.
                    - If None: default's to -1
                    - if -1: added to a level above any current instance of the intent section, level 0 if not found
                    - if int: added to the level specified, overwriting any that already exist

        :param replace_intent: (optional) if the intent method exists at the level, or default level
                    - True - replaces the current intent method with the new
                    - False - leaves it untouched, disregarding the new intent

        :param remove_duplicates: (optional) removes any duplicate intent in any level that is identical
        :return: an item or list of items chosen from the list
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   column_name=column_name, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        params = locals()
        [params.pop(k) for k in self._INTENT_PARAMS + ['quantity']]
        # set the seed and call the method
        seed = self._seed(seed=seed)
        rtn_list = self._get_category(seed=seed, **params)
        rtn_list = self._set_quantity(rtn_list, quantity=self._quantity(quantity), seed=seed)
        return pa.DictionaryArray.from_pandas(rtn_list).dictionary_encode()

    def get_boolean(self, size: int, probability: float=None, quantity: float=None, seed: int=None,
                    save_intent: bool=None, column_name: [int, str]=None, intent_order: int=None,
                    replace_intent: bool=None, remove_duplicates: bool=None) -> pa.Array:
        """A boolean discrete random distribution

        :param size: the size of the sample
        :param probability: a float between 0 and 1 of the probability of success. Default = 0.5
        :param quantity: a number between 0 and 1 representing data that isn't null
        :param seed: a seed value for the random function: default to None
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param column_name: (optional) the column name that groups intent to create a column
        :param intent_order: (optional) the order in which each intent should run.
                    - If None: default's to -1
                    - if -1: added to a level above any current instance of the intent section, level 0 if not found
                    - if int: added to the level specified, overwriting any that already exist

        :param replace_intent: (optional) if the intent method exists at the level, or default level
                    - True - replaces the current intent method with the new
                    - False - leaves it untouched, disregarding the new intent

        :param remove_duplicates: (optional) removes any duplicate intent in any level that is identical
        :return: a random number
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   column_name=column_name, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        prob = probability if isinstance(probability, int) and 0 < probability < 1 else 0.5
        seed = self._seed(seed=seed)
        rtn_list = self._get_category(selection=[True,False], relative_freq=[prob, 1-prob], size=size, seed=seed)
        rtn_list = self._set_quantity(rtn_list, quantity=self._quantity(quantity), seed=seed)
        return pa.BooleanArray.from_pandas(rtn_list)

    def get_datetime(self, start: Any, until: Any,  relative_freq: list=None, at_most: int=None, ordered: str=None,
                     date_format: str=None,  as_num: bool=None, ignore_time: bool=None, ignore_seconds: bool=None,
                     size: int=None, quantity: float=None, seed: int=None, day_first: bool=None, year_first: bool=None,
                     save_intent: bool=None, column_name: [int, str]=None, intent_order: int=None,
                     replace_intent: bool=None, remove_duplicates: bool=None) -> pa.Array:
        """ returns a random date between two date and/or times. weighted patterns can be applied to the overall date
        range. if a signed 'int' type is passed to the start and/or until dates, the inferred date will be the current
        date time with the integer being the offset from the current date time in 'days'.

        Note: If no patterns are set this will return a linearly random number between the range boundaries.

        :param start: the start boundary of the date range can be str, datetime, pd.datetime, pd.Timestamp or int
        :param until: up until boundary of the date range can be str, datetime, pd.datetime, pd.Timestamp or int
        :param quantity: the quantity of values that are not null. Number between 0 and 1
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
                    - If True parses dates with the year first, e.g. 10/11/12 is parsed as 2010-11-12.
                    - If both dayfirst and yearfirst are True, yearfirst is preceded (same as dateutil).

        :param day_first: specifies if to parse with the day first
                    - If True, parses dates with the day first, eg %d-%m-%Y.
                    - If False default to a preferred preference, normally %m-%d-%Y (but not strict)

        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param column_name: (optional) the column name that groups intent to create a column
        :param intent_order: (optional) the order in which each intent should run.
                    - If None: default's to -1
                    - if -1: added to a level above any current instance of the intent section, level 0 if not found
                    - if int: added to the level specified, overwriting any that already exist

        :param replace_intent: (optional) if the intent method exists at the level, or default level
                    - True - replaces the current intent method with the new
                    - False - leaves it untouched, disregarding the new intent

        :param remove_duplicates: (optional) removes any duplicate intent in any level that is identical
        :return: a date or size of dates in the format given.
         """
        # pre check
        if start is None or until is None:
            raise ValueError("The start or until parameters cannot be of NoneType")
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   column_name=column_name, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        params = locals()
        [params.pop(k) for k in self._INTENT_PARAMS + ['quantity']]
        # set the seed and call the method
        seed = self._seed(seed=seed)
        rtn_list = self._get_datetime(seed=seed, **params)
        rtn_list = self._set_quantity(rtn_list, quantity=self._quantity(quantity), seed=seed)
        return pa.TimestampArray.from_pandas(rtn_list)

    def get_intervals(self, intervals: list, relative_freq: list=None, precision: int=None, size: int=None,
                      quantity: float=None, seed: int=None, save_intent: bool=None, column_name: [int, str]=None,
                      intent_order: int=None, replace_intent: bool=None, remove_duplicates: bool=None) -> pa.Array:
        """ returns a number based on a list selection of tuple(lower, upper) interval

       :param intervals: a list of unique tuple pairs representing the interval lower and upper boundaries
        :param relative_freq: a weighting pattern or probability that does not have to add to 1
        :param precision: the precision of the returned number. if None then assumes int value else float
        :param size: the size of the sample
        :param quantity: a number between 0 and 1 representing data that isn't null
        :param seed: a seed value for the random function: default to None
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param column_name: (optional) the column name that groups intent to create a column
        :param intent_order: (optional) the order in which each intent should run.
                    - If None: default's to -1
                    - if -1: added to a level above any current instance of the intent section, level 0 if not found
                    - if int: added to the level specified, overwriting any that already exist

        :param replace_intent: (optional) if the intent method exists at the level, or default level
                    - True - replaces the current intent method with the new
                    - False - leaves it untouched, disregarding the new intent

        :param remove_duplicates: (optional) removes any duplicate intent in any level that is identical
        :return: a random number
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   column_name=column_name, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        params = locals()
        [params.pop(k) for k in self._INTENT_PARAMS + ['quantity']]
        # set the seed and call the method
        seed = self._seed(seed=seed)
        rtn_list = self._get_intervals(seed=seed, **params)
        rtn_list = self._set_quantity(rtn_list, quantity=self._quantity(quantity), seed=seed)
        return pa.StringArray.from_pandas(rtn_list)

    def get_dist_normal(self, mean: float, std: float, precision: int=None, size: int=None, quantity: float=None,
                        seed: int=None, save_intent: bool=None, column_name: [int, str]=None, intent_order: int=None,
                        replace_intent: bool=None, remove_duplicates: bool=None) -> pa.Array:
        """A normal (Gaussian) continuous random distribution.

        :param mean: The mean (“centre”) of the distribution.
        :param std: The standard deviation (jitter or “width”) of the distribution. Must be >= 0
        :param precision: The number of decimal points. The default is 3
        :param size: the size of the sample. if a tuple of intervals, size must match the tuple
        :param quantity: a number between 0 and 1 representing data that isn't null
        :param seed: a seed value for the random function: default to None
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param column_name: (optional) the column name that groups intent to create a column
        :param intent_order: (optional) the order in which each intent should run.
                    - If None: default's to -1
                    - if -1: added to a level above any current instance of the intent section, level 0 if not found
                    - if int: added to the level specified, overwriting any that already exist

        :param replace_intent: (optional) if the intent method exists at the level, or default level
                    - True - replaces the current intent method with the new
                    - False - leaves it untouched, disregarding the new intent

        :param remove_duplicates: (optional) removes any duplicate intent in any level that is identical
        :return: a random number
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   column_name=column_name, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        params = locals()
        [params.pop(k) for k in self._INTENT_PARAMS + ['quantity']]
        # set the seed and call the method
        seed = self._seed(seed=seed)
        rtn_list = self._get_dist_normal(seed=seed, **params)
        rtn_list = self._set_quantity(rtn_list, quantity=self._quantity(quantity), seed=seed)
        return pa.NumericArray.from_pandas(rtn_list)

    def get_dist_choice(self, number: [int, str, float], size: int=None, quantity: float=None, seed: int=None,
                        save_intent: bool=None, column_name: [int, str]=None, intent_order: int=None,
                        replace_intent: bool=None, remove_duplicates: bool=None) -> pa.Array:
        """Creates a list of latent values of 0 or 1 where 1 is randomly selected both upon the number given. The
        ``number`` parameter can be a direct reference to the canonical column header or to an environment variable.
        If the environment variable is used ``number`` should be set to ``"${<<YOUR_ENVIRON>>}"`` where
        <<YOUR_ENVIRON>> is the environment variable name

        :param number: The number of true (1) values to randomly chose from the canonical. see below
        :param size: the size of the sample. if a tuple of intervals, size must match the tuple
        :param quantity: a number between 0 and 1 representing data that isn't null
        :param seed: a seed value for the random function: default to None
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param column_name: (optional) the column name that groups intent to create a column
        :param intent_order: (optional) the order in which each intent should run.
                       If None: default's to -1
                       if -1: added to a level above any current instance of the intent section, level 0 if not found
                       if int: added to the level specified, overwriting any that already exist
        :param replace_intent: (optional) if the intent method exists at the level, or default level
                       True - replaces the current intent method with the new
                       False - leaves it untouched, disregarding the new intent
        :param remove_duplicates: (optional) removes any duplicate intent in any level that is identical
        :return: a list of 1 or 0

        as choice is a fixed value, number can be represented by an environment variable with the format '${NAME}'
        where NAME is the environment variable name
       """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   column_name=column_name, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        params = locals()
        [params.pop(k) for k in self._INTENT_PARAMS + ['quantity']]
        # set the seed and call the method
        seed = self._seed(seed=seed)
        rtn_list = self._get_dist_choice(seed=seed, **params)
        rtn_list = self._set_quantity(rtn_list, quantity=self._quantity(quantity), seed=seed)
        return pa.NumericArray.from_pandas(rtn_list)

    def get_dist_bernoulli(self, probability: float, size: int=None, quantity: float=None, seed: int=None,
                           save_intent: bool=None, column_name: [int, str]=None, intent_order: int=None,
                           replace_intent: bool=None, remove_duplicates: bool=None) -> pa.Array:
        """A Bernoulli discrete random distribution using scipy

        :param probability: the probability occurrence
        :param size: the size of the sample
        :param quantity: a number between 0 and 1 representing data that isn't null
        :param seed: a seed value for the random function: default to None
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param column_name: (optional) the column name that groups intent to create a column
        :param intent_order: (optional) the order in which each intent should run.
                    - If None: default's to -1
                    - if -1: added to a level above any current instance of the intent section, level 0 if not found
                    - if int: added to the level specified, overwriting any that already exist

        :param replace_intent: (optional) if the intent method exists at the level, or default level
                    - True - replaces the current intent method with the new
                    - False - leaves it untouched, disregarding the new intent

        :param remove_duplicates: (optional) removes any duplicate intent in any level that is identical
        :return: a random number
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   column_name=column_name, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        params = locals()
        [params.pop(k) for k in self._INTENT_PARAMS + ['quantity']]
        # set the seed and call the method
        seed = self._seed(seed=seed)
        rtn_list = self._get_dist_bernoulli(seed=seed, **params)
        rtn_list = self._set_quantity(rtn_list, quantity=self._quantity(quantity), seed=seed)
        return pa.NumericArray.from_pandas(rtn_list)

    def get_dist_bounded_normal(self, mean: float, std: float, lower: float, upper: float, precision: int=None,
                                size: int=None, quantity: float=None, seed: int=None, save_intent: bool=None,
                                column_name: [int, str]=None, intent_order: int=None, replace_intent: bool=None,
                                remove_duplicates: bool=None) -> pa.Array:
        """A bounded normal continuous random distribution.

        :param mean: the mean of the distribution
        :param std: the standard deviation
        :param lower: the lower limit of the distribution
        :param upper: the upper limit of the distribution
        :param precision: the precision of the returned number. if None then assumes int value else float
        :param size: the size of the sample
        :param quantity: a number between 0 and 1 representing data that isn't null
        :param seed: a seed value for the random function: default to None
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param column_name: (optional) the column name that groups intent to create a column
        :param intent_order: (optional) the order in which each intent should run.
                    - If None: default's to -1
                    - if -1: added to a level above any current instance of the intent section, level 0 if not found
                    - if int: added to the level specified, overwriting any that already exist

        :param replace_intent: (optional) if the intent method exists at the level, or default level
                    - True - replaces the current intent method with the new
                    - False - leaves it untouched, disregarding the new intent

        :param remove_duplicates: (optional) removes any duplicate intent in any level that is identical
        :return: a random number
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   column_name=column_name, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        params = locals()
        [params.pop(k) for k in self._INTENT_PARAMS + ['quantity']]
        # set the seed and call the method
        seed = self._seed(seed=seed)
        rtn_list = self._get_dist_bounded_normal(seed=seed, **params)
        rtn_list = self._set_quantity(rtn_list, quantity=self._quantity(quantity), seed=seed)
        return pa.NumericArray.from_pandas(rtn_list)

    def get_distribution(self, distribution: str, is_stats: bool=None, precision: int=None, size: int=None,
                         quantity: float=None, seed: int=None, save_intent: bool=None, column_name: [int, str]=None,
                         intent_order: int=None, replace_intent: bool=None, remove_duplicates: bool=None,
                         **kwargs) -> pa.Array:
        """returns a number based the distribution type.

        :param distribution: The string name of the distribution function from numpy random Generator class
        :param is_stats: (optional) if the generator is from the stats package and not numpy
        :param precision: (optional) the precision of the returned number
        :param size: (optional) the size of the sample
        :param quantity: (optional) a number between 0 and 1 representing data that isn't null
        :param seed: (optional) a seed value for the random function: default to None
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param column_name: (optional) the column name that groups intent to create a column
        :param intent_order: (optional) the order in which each intent should run.
                    - If None: default's to -1
                    - if -1: added to a level above any current instance of the intent section, level 0 if not found
                    - if int: added to the level specified, overwriting any that already exist

        :param replace_intent: (optional) if the intent method exists at the level, or default level
                    - True - replaces the current intent method with the new
                    - False - leaves it untouched, disregarding the new intent

        :param remove_duplicates: (optional) removes any duplicate intent in any level that is identical
        :param kwargs: the parameters of the method
        :return: a random number
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   column_name=column_name, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        params = locals()
        [params.pop(k) for k in self._INTENT_PARAMS + ['quantity']]
        params.update(params.pop('kwargs', {}))
        # set the seed and call the method
        seed = self._seed(seed=seed)
        rtn_list = self._get_distribution(seed=seed, **params)
        rtn_list = self._set_quantity(rtn_list, quantity=self._quantity(quantity), seed=seed)
        return pa.NumericArray.from_pandas(rtn_list)

    def get_string_pattern(self, pattern: str, choices: dict=None, as_binary: bool=None, quantity: [float, int]=None,
                           size: int=None, choice_only: bool=None, seed: int=None, save_intent: bool=None,
                           column_name: [int, str]=None, intent_order: int=None, replace_intent: bool=None,
                           remove_duplicates: bool=None) -> pa.Array:
        """ Returns a random string based on the pattern given. The pattern is made up from the choices passed but
        by default is as follows:
                - c = random char [a-z][A-Z]
                - d = digit [0-9]
                - l = lower case char [a-z]
                - U = upper case char [A-Z]
                - p = all punctuation
                - s = space

        you can also use punctuation in the pattern that will be retained
        A pattern example might be

        .. code:: text

                uuddsduu => BA12 2NE or dl-{uu} => 4g-{FY}

        to create your own choices pass a dictionary with a reference char key with a list of choices as a value

        :param pattern: the pattern to create the string from
        :param choices: (optional) an optional dictionary of list of choices to replace the default.
        :param as_binary: (optional) if the return string is prefixed with a b
        :param quantity: (optional) a number between 0 and 1 representing the percentage quantity of the data
        :param size: (optional) the size of the return list. if None returns a single value
        :param choice_only: (optional) if to only use the choices given or to take not found characters as is
        :param seed: (optional) a seed value for the random function: default to None
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param column_name: (optional) the column name that groups intent to create a column
        :param intent_order: (optional) the order in which each intent should run.
                    - If None: default's to -1
                    - if -1: added to a level above any current instance of the intent section, level 0 if not found
                    - if int: added to the level specified, overwriting any that already exist

        :param replace_intent: (optional) if the intent method exists at the level, or default level
                    - True - replaces the current intent method with the new
                    - False - leaves it untouched, disregarding the new intent

        :param remove_duplicates: (optional) removes any duplicate intent in any level that is identical
        :return: a string based on the pattern
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   column_name=column_name, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # Code block for intent
        choice_only = False if choice_only is None or not isinstance(choice_only, bool) else choice_only
        as_binary = as_binary if isinstance(as_binary, bool) else False
        quantity = self._quantity(quantity)
        size = size if isinstance(size, int) and size > 0 else 1
        seed = self._seed(seed=seed)
        if choices is None or not isinstance(choices, dict):
            choices = {'c': list(string.ascii_letters),
                       'd': list(string.digits),
                       'l': list(string.ascii_lowercase),
                       'U': list(string.ascii_uppercase),
                       'p': list(string.punctuation),
                       's': [' '],
                       }
            choices.update({p: [p] for p in list(string.punctuation)})
        else:
            for k, v in choices.items():
                if not isinstance(v, list):
                    raise ValueError(
                        "The key '{}' must contain a 'list' of replacements options. '{}' found".format(k, type(v)))

        generator = np.random.default_rng(seed=seed)
        rtn_list = pd.Series(dtype=str)
        for c in list(pattern):
            if c in choices.keys():
                result = generator.choice(choices[c], size=size)
            elif not choice_only:
                result = [c]*size
            else:
                continue
            s_result = pd.Series(result)
            if rtn_list.empty:
                rtn_list = s_result
            else:
                rtn_list += s_result
        if as_binary:
            rtn_list = rtn_list.str.encode(encoding='raw_unicode_escape')
        rtn_list = self._set_quantity(rtn_list.to_list(), quantity=self._quantity(quantity), seed=seed)
        return pa.StringArray.from_pandas(rtn_list)

    def get_sample(self, sample_name: str, sample_size: int=None, shuffle: bool=None, size: int=None,
                   quantity: float=None, seed: int=None, save_intent: bool=None, column_name: [int, str]=None,
                   intent_order: int=None, replace_intent: bool=None, remove_duplicates: bool=None) -> pa.Array:
        """ returns a sample set based on sector and name
        To see the sample sets available use the Sample class __dir__() method:

            > from ds_capability.sample.sample_data import Sample
            > Sample().__dir__()

        :param sample_name: The name of the Sample method to be used.
        :param sample_size: (optional) the size of the sample to take from the reference file
        :param shuffle: (optional) if the selection should be shuffled before selection. Default is true
        :param quantity: (optional) a number between 0 and 1 representing the percentage quantity of the data
        :param size: (optional) size of the return. default to 1
        :param seed: (optional) a seed value for the random function: default to None
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param column_name: (optional) the column name that groups intent to create a column
        :param intent_order: (optional) the order in which each intent should run.
                    - If None: default's to -1
                    - if -1: added to a level above any current instance of the intent section, level 0 if not found
                    - if int: added to the level specified, overwriting any that already exist

        :param replace_intent: (optional) if the intent method exists at the level, or default level
                    - True - replaces the current intent method with the new
                    - False - leaves it untouched, disregarding the new intent

        :param remove_duplicates: (optional) removes any duplicate intent in any level that is identical
        :return: a sample list
        """
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   column_name=column_name, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # Code block for intent
        size = 1 if size is None else size
        sample_size = sample_name if isinstance(sample_size, int) else size
        quantity = self._quantity(quantity)
        _seed = self._seed(seed=seed)
        shuffle = shuffle if isinstance(shuffle, bool) else True
        selection = eval(f"Sample.{sample_name}(size={size}, shuffle={shuffle}, seed={_seed})")
        rtn_list = self._set_quantity(selection, quantity=quantity, seed=_seed)
        return pa.Array.from_pandas(rtn_list)

    def correlate_number(self, canonical: pa.Array, choice: [int, float, str]=None, choice_header: str=None,
                         precision: int=None, jitter: [int, float, str]=None, offset: [int, float, str]=None,
                         code_str: Any=None, lower: [int, float]=None, upper: [int, float]=None, keep_zero: bool=None,
                         seed: int=None, save_intent: bool=None, column_name: [int, str]=None, intent_order: int=None,
                         replace_intent: bool=None, remove_duplicates: bool=None) -> list:
        """ correlate a list of continuous values adjusting those values, or a subset of those values, with a
        normalised jitter (std from the value) along with a value offset. ``choice``, ``jitter`` and ``offset``
        can accept environment variable string names starting with ``${`` and ending with ``}``.

        If the choice is an int, it represents the number of rows to choose. If the choice is a float it must be
        between 1 and 0 and represent a percentage of rows to choose.

        :param canonical:
        :param choice: (optional) The number of values to choose to apply the change to. Can be an environment variable.
        :param choice_header: (optional) those not chosen are given the values of the given header
        :param precision: (optional) to what precision the return values should be
        :param offset: (optional) a fixed value to offset or if str an operation to perform using @ as the header value.
        :param code_str: (optional) passing a str lambda function. e.g. 'lambda x: (x - 3) / 2''
        :param jitter: (optional) a perturbation of the value where the jitter is a random normally distributed std
        :param precision: (optional) how many decimal places. default to 3
        :param seed: (optional) the random seed. defaults to current datetime
        :param keep_zero: (optional) if True then zeros passed remain zero despite a change, Default is False
        :param lower: a minimum value not to go below
        :param upper: a max value not to go above
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param column_name: (optional) the column name that groups intent to create a column
        :param intent_order: (optional) the order in which each intent should run.
                    - If None: default's to -1
                    - if -1: added to a level above any current instance of the intent section, level 0 if not found
                    - if int: added to the level specified, overwriting any that already exist

        :param replace_intent: (optional) if the intent method exists at the level, or default level
                    - True - replaces the current intent method with the new
                    - False - leaves it untouched, disregarding the new intent

        :param remove_duplicates: (optional) removes any duplicate intent in any level that is identical
        :return: an equal length list of correlated values
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   column_name=column_name, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        params = locals()
        [params.pop(k) for k in self._INTENT_PARAMS]
        # set the seed and call the method
        seed = self._seed(seed=seed)
        rtn_list = self._correlate_number(seed=seed, **params)
        rtn_arr = pa.NumericArray.from_pandas(rtn_list)
        if rtn_arr.type.equals('double'):
            try:
                rtn_arr = pa.array(rtn_arr, pa.int64())
            except pa.lib.ArrowInvalid:
                pass
        return rtn_arr

    def model_analysis(self, size: int, other: [str, pa.Table], category_limit: int=None,
                       seed: int=None, save_intent: bool=None, column_name: [int, str]=None, intent_order: int=None,
                       replace_intent: bool=None, remove_duplicates: bool=None) -> pa.Table:
        """ builds a set of columns based on another (see analyse_association)
        if a reference DataFrame is passed then as the analysis is run if the column already exists the row
        value will be taken as the reference to the sub category and not the random value. This allows already
        constructed association to be used as reference for a sub category.

        :param size: The number of rows
        :param other: a direct or generated pd.DataFrame. see context notes below
        :param category_limit: (optional) a global cap on categories captured. zero value returns no limits
        :param seed: seed: (optional) a seed value for the random function: default to None
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param column_name: (optional) the column name that groups intent to create a column
        :param intent_order: (optional) the order in which each intent should run. In
                    - If None: default's to -1
                    - if -1: added to a level above any current instance of the intent section, level 0 if not found
                    - if int: added to the level specified, overwriting any that already exist

        :param replace_intent: (optional) if the intent method exists at the level, or default level
                    - True - replaces the current intent method with the new
                    - False - leaves it untouched, disregarding the new intent

        :param remove_duplicates: (optional) removes any duplicate intent in any level that is identical
        :return: a pa.Table
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   column_name=column_name, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # Code block for intent
        other = self._get_canonical(other)
        rtn_tbl = None
        for c in other.column_names:
            column = other.column(c).combine_chunks()
            if pa.types.is_dictionary(column.type):
                selection = column.dictionary.to_pylist()
                frequency = column.value_counts().field(1).to_pylist()
                result = self.get_category(selection=selection, relative_freq=frequency, size=size, save_intent=False)
            elif pa.types.is_integer(column.type) or pa.types.is_floating(column.type):
                precision = 0 if pa.types.is_integer(column.type) else 5
                std = pc.round(pc.multiply(pc.stddev(column), 0.6), 5).as_py()
                rtn_col = pa.table([self.correlate_number(column, jitter=std, precision=precision, save_intent=False)],
                                   names=['num'])
                while rtn_col.num_rows < size:
                    _ = pa.table([self.correlate_number(column, jitter=std, precision=precision, save_intent=False)],
                                 names=['num'])
                    rtn_col = pa.concat_tables([rtn_col, _])
                result = rtn_col.slice(0, size).column('num')
            elif pa.types.is_boolean(column.type):
                frequency = dict(zip(column.value_counts().field(0).to_pylist(),
                                     column.value_counts().field(1).to_pylist())).get(True)

            else:
                continue
            if isinstance(rtn_tbl, pa.Table):
                rtn_tbl = rtn_tbl.append_column(c, result)
            else:
                rtn_tbl = pa.table([result], names=[c])
        return rtn_tbl



    def model_synthetic_data_types(self, size: int, inc_nulls: bool=None, p_nulls: float=None, seed: int=None,
                                   save_intent: bool=None, column_name: [int, str]=None, intent_order: int=None,
                                   replace_intent: bool=None, remove_duplicates: bool=None) -> pa.Table:
        """ A dataset with example data types

        :param size:
        :param inc_nulls: include values with nulls
        :param p_nulls: a value between 0 an 1 of the percentage of nulls in the *_nulls column. Default is 0.02
        :param seed: a seed value for the random function: default to None
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param column_name: (optional) the column name that groups intent to create a column
        :param intent_order: (optional) the order in which each intent should run.
                    - If None: default's to -1
                    - if -1: added to a level above any current instance of the intent section, level 0 if not found
                    - if int: added to the level specified, overwriting any that already exist

        :param replace_intent: (optional) if the intent method exists at the level, or default level
                    - True - replaces the current intent method with the new
                    - False - leaves it untouched, disregarding the new intent

        :param remove_duplicates: (optional) removes any duplicate intent in any level that is identical
        :return: pandas DataSet
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   column_name=column_name, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        seed = self._seed(seed=seed)
        p_nulls = p_nulls if isinstance(p_nulls, float) and 0 < p_nulls < 1 else 0.02
        # cat
        _ = self.get_category(selection=['SUSPENDED', 'ACTIVE', 'PENDING', 'INACTIVE'], size=size, seed=seed,
                              relative_freq=[1, 99, 10, 40],  save_intent=False)
        canonical = pa.table([_], names=['cat'])
        # num
        _ = self.get_dist_normal(mean=4, std=1, size=size, seed=seed, save_intent=False)
        canonical = canonical.append_column('num', _)
        # int
        _ = self.get_number(start=-1000, stop=1000, size=size, seed=seed, save_intent=False)
        canonical = canonical.append_column('int', _)
        # bool
        _ = self.get_boolean(size=size, probability=0.7, seed=seed, save_intent=False)
        canonical = canonical.append_column('bool', _)
        # date
        _ = self.get_datetime(start='2022-12-01', until='2023-03-31', ordered=True, size=size, seed=seed,
                              save_intent=False)
        canonical = canonical.append_column('date', _)
        # string
        _ = self.get_sample(sample_name='us_street_names', size=size, seed=seed,  save_intent=False)
        canonical = canonical.append_column('string', _)
        # binary
        _ = self.get_string_pattern(pattern='cccccccc', as_binary=True, size=size, seed=seed, save_intent=False)
        canonical = canonical.append_column('binary', _)

        if isinstance(inc_nulls, bool) and inc_nulls:
            # cat_null
            _ = self.get_category(selection=['M', 'F', 'U'], relative_freq=[9,8,4], quantity=1 - p_nulls, size=size, seed=seed,
                                  save_intent=False)
            canonical = canonical.append_column('cat_null', _)
            # num_null
            _ = self.get_number(column_name='num_null', start=-1.0, stop=1.0, relative_freq=[1, 1, 2, 3, 5, 8, 13, 21],
                                size=size, quantity=1 - p_nulls, seed=seed, save_intent=False)
            canonical = canonical.append_column('num_null', _)
            # int_null
            _ = self.get_number(start=-1000, stop=1000, size=size, quantity=1 - p_nulls, seed=seed, save_intent=False)
            canonical = canonical.append_column('int_null', _)
            # bool_null
            _ = self.get_boolean(size=size, probability=0.4, seed=seed, quantity=1 - p_nulls, save_intent=False)
            canonical = canonical.append_column('bool_null', _)
            # date_null
            _ = self.get_datetime(start='2022-12-01', until='2023-03-31', ordered=True, size=size, quantity=1 - p_nulls,
                                  seed=seed, save_intent=False)
            canonical = canonical.append_column('date_null', _)
            # string_null
            _ = self.get_sample(sample_name='us_street_names', size=size, quantity=1 - p_nulls, seed=seed, save_intent=False)
            canonical = canonical.append_column('string_null', _)

        return canonical

    def model_noise(self, size: int,  num_columns: int, seed: int = None,
                    save_intent: bool = None, column_name: [int, str] = None, intent_order: int = None,
                    replace_intent: bool = None, remove_duplicates: bool = None) -> pd.DataFrame:
        """ Generates multiple columns of noise in your dataset

        :param size: The number of rows
        :param num_columns: the number of columns of noise
        :param seed: seed: (optional) a seed value for the random function: default to None
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param column_name: (optional) the column name that groups intent to create a column
        :param intent_order: (optional) the order in which each intent should run.
                    - If None: default's to -1
                    - if -1: added to a level above any current instance of the intent section, level 0 if not found
                    - if int: added to the level specified, overwriting any that already exist

        :param replace_intent: (optional) if the intent method exists at the level, or default level
                    - True - replaces the current intent method with the new
                    - False - leaves it untouched, disregarding the new intent

        :param remove_duplicates: (optional) removes any duplicate intent in any level that is identical
        :return: a DataFrame
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   column_name=column_name, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # Code block for intent
        _seed = self._seed(seed=seed)
        num_columns = num_columns if isinstance(num_columns, int) else 1
        label_gen = Commons.label_gen()
        tbl = None
        generator = np.random.default_rng(seed=_seed)
        for _ in range(num_columns):
            _seed = self._seed(seed=_seed, increment=True)
            a = generator.choice(range(1, 6))
            b = generator.choice(range(1, 6))
            arr = self.get_distribution(distribution='beta', a=a, b=b, precision=6, size=size, seed=_seed,
                                                      save_intent=False)
            if isinstance(tbl, pa.Table):
                tbl = tbl.append_column(next(label_gen), arr)
            else:
                tbl = pa.table([arr], next(label_gen))
        return tbl

    @property
    def sample_lists(self) -> list:
        """A list of sample options"""
        return Sample().__dir__()


    """
        PRIVATE METHODS SECTION
    """

    def _get_canonical(self, data: [pa.Table, str],  size: int=None) -> pa.Table:
        """ Used to return or generate a PyArrow Table from a number of different types.

        The following can be passed and their returns
        - pa.Table -> a PyArrow Table that is directly returned
        - str -> instantiates a connector handler with the connector_name and loads the Table from the connection

        :param data: a dataframe or action event to generate a dataframe
        :param size: (optional) a size parameter for @empty of @generate
        :return: a pa.Table
        """
        if isinstance(data, pa.Table):
            return data
        elif isinstance(data, str):
            if self._pm.has_connector(connector_name=data):
                handler = self._pm.get_connector_handler(data)
                return handler.load_canonical()
            raise ValueError(f"The data connector name '{data}' is not in the connectors catalog")
        raise ValueError(f"The canonical format is not a recognised pc.Field or str type, '{type(data)}' type passed")

    def _set_quantity(self, selection, quantity, seed=None):
        """Returns the quantity percent of good values in selection with the rest fill"""
        quantity = self._quantity(quantity)
        if quantity == 1:
            return selection
        if quantity == 0:
            return [np.nan] * len(selection)
        seed = self._seed(seed=seed)
        quantity = 1 - quantity
        generator = np.random.default_rng(seed)
        length = len(selection)
        size = int(length * quantity)
        nulls_idx = generator.choice(length, size=size, replace=False)
        result = pd.Series(selection)
        result.iloc[nulls_idx] = np.nan
        return result.to_list()

    @staticmethod
    def _quantity(quantity: [float, int]) -> float:
        """normalises quantity to a percentage float between 0 and 1.0"""
        if not isinstance(quantity, (int, float)) or not 0 <= quantity <= 100:
            return 1.0
        if quantity > 1:
            return round(quantity / 100, 2)
        return float(quantity)
