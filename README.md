<!--
SPDX-FileCopyrightText: 2022 KUNBUS GmbH

SPDX-License-Identifier: MIT
-->

# Revolution Pi Benchmark

## About
Simple benchmark application to provide insights about performance related to hardware or software changes.
See the related [Confluence Page](https://kunbus-gmbh.atlassian.net/wiki/spaces/EN/pages/2575663126/Benchmark) to learn more.

Currently this repository only contains some scripts to perform iterative tests of CPU and RAM, and create CVS formatted data which has to be processed later on.
A simple example of such an analysis inside a spreadsheet is also contained.

## To Do

  * automatically generate data for stuff like
    * RAM access
    * CPU performance
    * persistant memory access (EMMC)
    * system environment (e.g. RevPi versions of Hw and Sw)
    * stress testing temperatures
    * you name it
  * process data and generate comprehensible reports
  * export report into a database for reproducibility and better comparison
  * graphical reports could gain insights more intuitively
