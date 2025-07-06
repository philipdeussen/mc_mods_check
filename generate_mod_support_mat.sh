#!/usr/bin/env bash


CSV_FILENAME="tmp.csv"
PLOT_FILENAME="mods_support_matrix_plot.png"

python3 get_mod_info.py ${CSV_FILENAME}
python3 plot_support_matrix.py ${CSV_FILENAME} ${PLOT_FILENAME}

rm ${CSV_FILENAME}