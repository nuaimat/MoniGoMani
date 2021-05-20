# --- Do not remove these libs ----------------------------------------------------------------------
from MoniGoManiHyperStrategy import MoniGoManiHyperStrategy as MGMStrategy
from freqtrade.strategy \
    import IStrategy, CategoricalParameter, IntParameter, RealParameter, merge_informative_pair, timeframe_to_minutes
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))


# Function to initialize the parameters values without manual overriding
def init_vars(parameter_dictionary, parameter_name, parameter_default_value, parameter_max_value,
              parameter_threshold, precision):
    parameter_value = parameter_dictionary.get(parameter_name)

    if parameter_value is None:
        min_value = 0
        max_value = parameter_max_value
    else:
        min_value = 0 if parameter_value <= (0 + parameter_threshold) else \
            parameter_value - parameter_threshold
        max_value = parameter_max_value if parameter_value >= (parameter_max_value - parameter_threshold) else \
            parameter_value + parameter_threshold

    if parameter_value is None:
        default_value = parameter_default_value
    elif max_value == parameter_max_value:
        default_value = parameter_max_value
    elif min_value == 0:
        default_value = 0
    else:
        default_value = parameter_value

    return_vars_dictionary = {
        "min_value": min_value * precision,
        "max_value": max_value * precision,
        "default_value": default_value * precision,
        "opt_and_Load": False if parameter_value is not None and (
                min_value == 0 or max_value == parameter_max_value) else True
    }

    return return_vars_dictionary


#################################################################################
#     *** THIS IS A CHILD STRATEGY, REQUIRES IMPORT OF PARENT STRATEGY ***      #
#################################################################################
class MoniGoManiConfiguration(MGMStrategy):
    ####################################################################################################################
    # Global parameters you want to override
    ####################################################################################################################
    timeframe = '1h'
    precision = 1

    # Search space threshold: to reduce the search space with min / max around the first value found
    search_threshold = 10

    # Maximum value for weighted indicators
    max_weight_value = 100
    # Maximum value for trend lookback indicators
    max_trend_lookback_value = int(360 / timeframe_to_minutes(timeframe))

    # Number of weighted signals:
    # Fill in the total number of different weighted signals in use in the weighted tables
    # 'buy/sell__downwards/sideways/upwards_trend_total_signal_needed' settings will be multiplied with this value
    # so their search spaces will be larger, resulting in more equally divided weighted signal scores when hyperopting
    number_of_weighted_signals = 9

    # ROI Table StepSize:
    # Size of the steps in minutes to be used when calculating the long continuous ROI table
    # MGM generates a custom really long table so it will have less gaps in it and be more continuous in it's decrease
    roi_table_step_size = 5

    ####################################################################################################################
    #                                    START OF HYPEROPT RESULTS COPY-PASTE SECTION                                  #
    # ##################################################################################################################
    # ### COPY/PASTE hyperopt results after 1st iteration below #####
    # Buy hyperspace params:
    buy_params = {
    }

    # Sell hyperspace params:
    sell_params = {
    }

    # ROI table:

    # Stoploss:

    # Trailing stop:

    # #####################################################################
    # ###              DO NOT REMOVE / MODIFY THESE LINES             #####
    buy_param_final = buy_params
    sell_param_final = sell_params
    # ####################################################################

    # ####################################################################
    # ### COPY/PASTE hyperopt result of 2nd (or more) iteration below #####
    # ##################################################################################################################

    # #################################   END OF HYPEROPT RESULTS COPY-PASTE SECTION   #################################
    # ##################################################################################################################

    # ##################################################################################################################
    # ### DO NOT REMOVE / MODIFY THESE LINES --- CONCATENATION OF 1st AND 2nd result #####
    buy_param_final.update(buy_params)
    sell_param_final.update(sell_params)

    buy_params = buy_param_final
    sell_params = sell_param_final
    ####################################################################################################################

    ####################################################################################################################
    #                                             START OF OVERRIDES SECTION                                           #
    ####################################################################################################################

    # ################ 1st run --- initial overrides ###################
    # ---------------------------------------------------------------- #
    #                  Buy HyperOpt Space Parameters                   #
    # ---------------------------------------------------------------- #
    # React to Buy Signals when certain trends are detected (False would disable trading in said trend)
    buy___trades_when_downwards = \
        CategoricalParameter([True, False], default=True, space='buy', optimize=False, load=False)
    buy___trades_when_sideways = \
        CategoricalParameter([True, False], default=False, space='buy', optimize=False, load=False)
    buy___trades_when_upwards = \
        CategoricalParameter([True, False], default=True, space='buy', optimize=False, load=False)

    # ---------------------------------------------------------------- #
    #                  Sell HyperOpt Space Parameters                  #
    # ---------------------------------------------------------------- #
    # React to Sell Signals when certain trends are detected (False would disable trading in said trend)
    sell___trades_when_downwards = \
        CategoricalParameter([True, False], default=True, space='sell', optimize=False, load=False)
    sell___trades_when_sideways = \
        CategoricalParameter([True, False], default=False, space='sell', optimize=False, load=False)
    sell___trades_when_upwards = \
        CategoricalParameter([True, False], default=True, space='sell', optimize=False, load=False)

    # ---------------------------------------------------------------- #
    #             Sell Unclogger HyperOpt Space Parameters             #
    # ---------------------------------------------------------------- #
    sell___unclogger_enabled = \
        CategoricalParameter([True, False], default=True, space='sell', optimize=False, load=False)
    sell___unclogger_trend_lookback_window_uses_downwards_candles = \
        CategoricalParameter([True, False], default=True, space='sell', optimize=False, load=False)
    sell___unclogger_trend_lookback_window_uses_sideways_candles = \
        CategoricalParameter([True, False], default=True, space='sell', optimize=False, load=False)
    sell___unclogger_trend_lookback_window_uses_upwards_candles = \
        CategoricalParameter([True, False], default=False, space='sell', optimize=False, load=False)

    # ################# 2nd run --- addtional overrides #################
    #
    #   !!!!!!!!!! Before going further make sure have set "optimize=False" for the parameters of section 1 !!!!!!!!!
    #

    # HyperOpt Settings Override
    # --------------------------
    # When the Parameters in below HyperOpt Space Parameters sections are altered as following examples then they can be
    # used as overrides while hyperopting / backtesting / dry/live-running (only truly useful when hyperopting though!)
    # Meaning you can use this to set individual buy_params/sell_params to a fixed value when hyperopting!
    # WARNING: Always double check that when doing a fresh hyperopt or doing a dry/live-run that all overrides are
    # turned off!
    #
    # Override Examples:
    # Override to False:    CategoricalParameter([True, False], default=False, space='buy', optimize=False, load=False)
    # Override to 0:        IntParameter(0, int(100*precision), default=0, space='sell', optimize=False, load=False)
    #
    # default=           The value used when overriding
    # optimize=False     Exclude from hyperopting (Make static)
    # load=False         Don't load from above HYPEROPT RESULTS COPY-PASTE SECTION

    # ---------------------------------------------------------------- #
    #                  Buy HyperOpt Space Parameters                   #
    # ---------------------------------------------------------------- #

    # Trend Detecting Buy Signal Weight Influence Tables
    # -------------------------------------------------------
    # The idea is to let hyperopt find out which signals are more important over other signals by allocating weights to
    # them while also finding the "perfect" weight division between each-other.
    # These Signal Weight Influence Tables will be allocated to signals when their respective trend is detected
    # (Signals can be turned off by allocating 0 or turned into an override by setting them equal to or higher then
    # total_buy_signal_needed)

    # Downwards Trend Buy
    # -------------------

    # Total Buy Signal Percentage needed for a signal to be positive
    param = init_vars(buy_params, "buy__downwards_trend_total_signal_needed", 30, int(100 * number_of_weighted_signals),
                      search_threshold, precision)
    buy__downwards_trend_total_signal_needed = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy__downwards_trend_total_signal_needed_candles_lookback_window", 1,
                      max_trend_lookback_value, search_threshold, precision)
    buy__downwards_trend_total_signal_needed_candles_lookback_window = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    # Buy Signal Weight Influence Table
    param = \
        init_vars(buy_params, "buy_downwards_trend_adx_strong_up_weight", 0, max_weight_value, search_threshold,
                  precision)
    buy_downwards_trend_adx_strong_up_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_downwards_trend_bollinger_bands_weight", 0, max_weight_value, search_threshold,
                      precision)
    buy_downwards_trend_bollinger_bands_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_downwards_trend_ema_long_golden_cross_weight", 0, max_weight_value,
                      search_threshold, precision)
    buy_downwards_trend_ema_long_golden_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_downwards_trend_ema_short_golden_cross_weight", 0, max_weight_value,
                      search_threshold, precision)
    buy_downwards_trend_ema_short_golden_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_downwards_trend_macd_weight", 0, max_weight_value, search_threshold, precision)
    buy_downwards_trend_macd_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_downwards_trend_rsi_weight", 0, max_weight_value, search_threshold, precision)
    buy_downwards_trend_rsi_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_downwards_trend_sma_long_golden_cross_weight", 0, max_weight_value,
                      search_threshold, precision)
    buy_downwards_trend_sma_long_golden_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_downwards_trend_sma_short_golden_cross_weight", 0, max_weight_value,
                      search_threshold, precision)
    buy_downwards_trend_sma_short_golden_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_downwards_trend_vwap_cross_weight", 0, max_weight_value, search_threshold,
                      precision)
    buy_downwards_trend_vwap_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    # Sideways Trend Buy
    # ------------------

    # Total Buy Signal Percentage needed for a signal to be positive
    param = init_vars(buy_params, "buy__sideways_trend_total_signal_needed", 30, int(100 * number_of_weighted_signals),
                      search_threshold, precision)
    buy__sideways_trend_total_signal_needed = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy__sideways_trend_total_signal_needed_candles_lookback_window", 1,
                      max_trend_lookback_value, search_threshold, precision)
    buy__sideways_trend_total_signal_needed_candles_lookback_window = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    # Buy Signal Weight Influence Table
    param = init_vars(buy_params, "buy_sideways_trend_adx_strong_up_weight", 0, max_weight_value, search_threshold,
                      precision)
    buy_sideways_trend_adx_strong_up_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_sideways_trend_bollinger_bands_weight", 0, max_weight_value, search_threshold,
                      precision)
    buy_sideways_trend_bollinger_bands_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_sideways_trend_ema_long_golden_cross_weight", 0, max_weight_value,
                      search_threshold, precision)
    buy_sideways_trend_ema_long_golden_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_sideways_trend_ema_short_golden_cross_weight", 0, max_weight_value,
                      search_threshold, precision)
    buy_sideways_trend_ema_short_golden_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_sideways_trend_macd_weight", 0, max_weight_value, search_threshold, precision)
    buy_sideways_trend_macd_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_sideways_trend_rsi_weight", 0, max_weight_value, search_threshold, precision)
    buy_sideways_trend_rsi_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_sideways_trend_sma_long_golden_cross_weight", 0, max_weight_value,
                      search_threshold, precision)
    buy_sideways_trend_sma_long_golden_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_sideways_trend_sma_short_golden_cross_weight", 0, max_weight_value,
                      search_threshold, precision)
    buy_sideways_trend_sma_short_golden_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_sideways_trend_vwap_cross_weight", 0, max_weight_value, search_threshold,
                      precision)
    buy_sideways_trend_vwap_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    # Upwards Trend Buy
    # -----------------

    # Total Buy Signal Percentage needed for a signal to be positive
    param = init_vars(buy_params, "buy__upwards_trend_total_signal_needed", 30, int(100 * number_of_weighted_signals),
                      search_threshold, precision)
    buy__upwards_trend_total_signal_needed = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy__upwards_trend_total_signal_needed_candles_lookback_window", 1,
                      max_trend_lookback_value, search_threshold, precision)
    buy__upwards_trend_total_signal_needed_candles_lookback_window = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    # Buy Signal Weight Influence Table
    param = init_vars(buy_params, "buy_upwards_trend_adx_strong_up_weight", 0, max_weight_value, search_threshold,
                      precision)
    buy_upwards_trend_adx_strong_up_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_upwards_trend_bollinger_bands_weight", 0, max_weight_value, search_threshold,
                      precision)
    buy_upwards_trend_bollinger_bands_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_upwards_trend_ema_short_golden_cross_weight", 0, max_weight_value,
                      search_threshold, precision)
    buy_upwards_trend_ema_short_golden_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_upwards_trend_ema_long_golden_cross_weight", 0, max_weight_value,
                      search_threshold, precision)
    buy_upwards_trend_ema_long_golden_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_upwards_trend_macd_weight", 0, max_weight_value, search_threshold, precision)
    buy_upwards_trend_macd_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_upwards_trend_rsi_weight", 0, max_weight_value, search_threshold, precision)
    buy_upwards_trend_rsi_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_upwards_trend_sma_long_golden_cross_weight", 0, max_weight_value,
                      search_threshold, precision)
    buy_upwards_trend_sma_long_golden_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_upwards_trend_sma_short_golden_cross_weight", 0, max_weight_value,
                      search_threshold, precision)
    buy_upwards_trend_sma_short_golden_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(buy_params, "buy_upwards_trend_vwap_cross_weight", 0, max_weight_value, search_threshold,
                      precision)
    buy_upwards_trend_vwap_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='buy', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    # ---------------------------------------------------------------- #
    #                  Sell HyperOpt Space Parameters                  #
    # ---------------------------------------------------------------- #

    # Trend Detecting Buy Signal Weight Influence Tables
    # -------------------------------------------------------
    # The idea is to let hyperopt find out which signals are more important over other signals by allocating weights to
    # them while also finding the "perfect" weight division between each-other.
    # These Signal Weight Influence Tables will be allocated to signals when their respective trend is detected
    # (Signals can be turned off by allocating 0 or turned into an override by setting them equal to or higher then
    # total_buy_signal_needed)

    # Downwards Trend Sell
    # --------------------

    # Total Sell Signal Percentage needed for a signal to be positive
    param = init_vars(sell_params, "sell__downwards_trend_total_signal_needed", 30,
                      int(100 * number_of_weighted_signals), search_threshold, precision)
    sell__downwards_trend_total_signal_needed = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell__downwards_trend_total_signal_needed_candles_lookback_window", 1,
                      max_trend_lookback_value, search_threshold, precision)
    sell__downwards_trend_total_signal_needed_candles_lookback_window = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    # Sell Signal Weight Influence Table
    param = init_vars(sell_params, "sell_downwards_trend_adx_strong_down_weight", 0, max_weight_value, search_threshold,
                      precision)
    sell_downwards_trend_adx_strong_down_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_downwards_trend_bollinger_bands_weight", 0, max_weight_value, search_threshold,
                      precision)
    sell_downwards_trend_bollinger_bands_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_downwards_trend_ema_long_death_cross_weight", 0, max_weight_value,
                      search_threshold, precision)
    sell_downwards_trend_ema_long_death_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_downwards_trend_ema_short_death_cross_weight", 0, max_weight_value,
                      search_threshold, precision)
    sell_downwards_trend_ema_short_death_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_downwards_trend_macd_weight", 0, max_weight_value, search_threshold, precision)
    sell_downwards_trend_macd_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_downwards_trend_rsi_weight", 0, max_weight_value, search_threshold, precision)
    sell_downwards_trend_rsi_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_downwards_trend_sma_long_death_cross_weight", 0, max_weight_value,
                      search_threshold, precision)
    sell_downwards_trend_sma_long_death_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_downwards_trend_sma_short_death_cross_weight", 0, max_weight_value,
                      search_threshold, precision)
    sell_downwards_trend_sma_short_death_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_downwards_trend_vwap_cross_weight", 0, max_weight_value, search_threshold,
                      precision)
    sell_downwards_trend_vwap_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    # Sideways Trend Sell
    # -------------------

    # Total Sell Signal Percentage needed for a signal to be positive
    param = init_vars(sell_params, "sell__sideways_trend_total_signal_needed", 30,
                      int(100 * number_of_weighted_signals), search_threshold, precision)
    sell__sideways_trend_total_signal_needed = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell__sideways_trend_total_signal_needed_candles_lookback_window", 1,
                      max_trend_lookback_value, search_threshold, precision)
    sell__sideways_trend_total_signal_needed_candles_lookback_window = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    # Sell Signal Weight Influence Table
    param = init_vars(sell_params, "sell_sideways_trend_adx_strong_down_weight", 0, max_weight_value, search_threshold,
                      precision)
    sell_sideways_trend_adx_strong_down_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_sideways_trend_bollinger_bands_weight", 0, max_weight_value, search_threshold,
                      precision)
    sell_sideways_trend_bollinger_bands_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_sideways_trend_ema_long_death_cross_weight", 0, max_weight_value,
                      search_threshold, precision)
    sell_sideways_trend_ema_long_death_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_sideways_trend_ema_short_death_cross_weight", 0, max_weight_value,
                      search_threshold, precision)
    sell_sideways_trend_ema_short_death_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_sideways_trend_macd_weight", 0, max_weight_value, search_threshold, precision)
    sell_sideways_trend_macd_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_sideways_trend_rsi_weight", 0, max_weight_value, search_threshold, precision)
    sell_sideways_trend_rsi_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_sideways_trend_sma_long_death_cross_weight", 0, max_weight_value,
                      search_threshold, precision)
    sell_sideways_trend_sma_long_death_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_sideways_trend_sma_short_death_cross_weight", 0, max_weight_value,
                      search_threshold, precision)
    sell_sideways_trend_sma_short_death_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_sideways_trend_vwap_cross_weight", 0, max_weight_value, search_threshold,
                      precision)
    sell_sideways_trend_vwap_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    # Upwards Trend Sell
    # ------------------

    # Total Sell Signal Percentage needed for a signal to be positive
    param = init_vars(sell_params, "sell__upwards_trend_total_signal_needed", 30, int(100 * number_of_weighted_signals),
                      search_threshold, precision)
    sell__upwards_trend_total_signal_needed = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell__upwards_trend_total_signal_needed_candles_lookback_window", 1,
                      max_trend_lookback_value, search_threshold, precision)
    sell__upwards_trend_total_signal_needed_candles_lookback_window = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    # Sell Signal Weight Influence Table
    param = init_vars(sell_params, "sell_upwards_trend_adx_strong_down_weight", 0, max_weight_value, search_threshold,
                      precision)
    sell_upwards_trend_adx_strong_down_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_upwards_trend_bollinger_bands_weight", 0, max_weight_value, search_threshold,
                      precision)
    sell_upwards_trend_bollinger_bands_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_upwards_trend_ema_long_death_cross_weight", 0, max_weight_value,
                      search_threshold, precision)
    sell_upwards_trend_ema_long_death_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_upwards_trend_ema_short_death_cross_weight", 0, max_weight_value,
                      search_threshold, precision)
    sell_upwards_trend_ema_short_death_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_upwards_trend_macd_weight", 0, max_weight_value, search_threshold, precision)
    sell_upwards_trend_macd_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_upwards_trend_rsi_weight", 0, max_weight_value, search_threshold, precision)
    sell_upwards_trend_rsi_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_upwards_trend_sma_long_death_cross_weight", 0, max_weight_value,
                      search_threshold, precision)
    sell_upwards_trend_sma_long_death_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_upwards_trend_sma_short_death_cross_weight", 0, max_weight_value,
                      search_threshold, precision)
    sell_upwards_trend_sma_short_death_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    param = init_vars(sell_params, "sell_upwards_trend_vwap_cross_weight", 0, max_weight_value, search_threshold,
                      precision)
    sell_upwards_trend_vwap_cross_weight = \
        IntParameter(param["min_value"], param["max_value"], default=param["default_value"],
                     space='sell', optimize=param["opt_and_Load"], load=param["opt_and_Load"])

    # ---------------------------------------------------------------- #
    #             Sell Unclogger HyperOpt Space Parameters             #
    # ---------------------------------------------------------------- #
    sell___unclogger_minimal_losing_trade_duration_minutes = \
        IntParameter(int(15 * precision), int(60 * precision), default=int(15 * precision),
                     space='sell', optimize=True, load=True)
    sell___unclogger_minimal_losing_trades_open = \
        IntParameter(int(1 * precision), int(5 * precision), default=int(1 * precision),
                     space='sell', optimize=True, load=True)
    sell___unclogger_open_trades_losing_percentage_needed = \
        IntParameter(int(1 * precision), int(60 * precision), default=int(1 * precision),
                     space='sell', optimize=True, load=True)
    sell___unclogger_trend_lookback_candles_window = \
        IntParameter(int(10 * precision), int(60 * precision), default=int(10 * precision),
                     space='sell', optimize=True, load=True)
    sell___unclogger_trend_lookback_candles_window_percentage_needed = \
        IntParameter(int(10 * precision), int(40 * precision), default=int(10 * precision),
                     space='sell', optimize=True, load=True)

    ####################################################################################################################
    #                                              END OF OVERRIDES SECTION                                            #
    ####################################################################################################################
