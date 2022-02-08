"""
This module contains the bot settings
"""

import os
import MetaTrader5


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

STRATEGY_DIR = os.path.join(ROOT_DIR, 'strategy')

TYPE_FILLING = MetaTrader5.ORDER_FILLING_RETURN
