#############
Bitshop
#############

The aim of the module is to provide a basic trading infrastructure for cryprocurrencies
across a predefined list of exchanges.

.. note:: For the time being, the module targets Coinbase as the only exchange, but this will be expanded in the future.

This module is composed of three complementary submodules:

.. list-table:: :header-rows: 1

 * - Submodule
   - Objective
 * - **core**
   - Main component of the module; handles the data fetching, orders handling, and basic portfolio management.
 * - **pipeline**
   - Provides connectivity to different exchanges and data sources.
 * - **analytics**
   - Portfolio analytics and tools (*to be developed*).


The module is designed to work with a proprietary database hosted on AWS - RDS. For the sake of context, the database follows the schema below.

.. image:: https://github.com/fcoibanez/bitshop/raw/master/docs/img/data_schema.png
