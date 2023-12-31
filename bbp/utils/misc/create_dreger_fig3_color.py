#!/usr/bin/env python
"""
BSD 3-Clause License

Copyright (c) 2021, University of Southern California
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
from __future__ import division, print_function

# Import Python modules
import os
import sys
import math
import numpy as np
import scipy.stats as st
import matplotlib as mpl
if mpl.get_backend() != 'agg':
    mpl.use('Agg') # Disables use of Tk/X11
import pylab

COLORS2 = ["red", "yellow", "sandybrown", "lime", "darkorange", "khaki",
           "yellowgreen", "violet", "palegreen", "turquoise", "gold",
           "cyan", "dodgerblue", "blueviolet", "magenta",
           "deeppink", "brown", "teal", "wheat", "silver"]
COLORS = ["red", "cyan", "gold", "lime", "blueviolet",
          "cyan", "gold", "lime", "blueviolet", "red",
          "gold", "lime", "blueviolet", "red", "cyan",
          "lime", "blueviolet", "red", "cyan", "gold"]
MARKERS = ["+", "*", "^", "o", "x",
           "+", "*", "^", "o", "x",
           "+", "*", "^", "o", "x",
           "+", "*", "^", "o", "x"]

def read_data(input_file):
    """
    This function reads the input file and loads the data into
    our data structures
    """
    rrup = None
    data = []
    ifile = open(input_file, 'r')
    for line in ifile:
        line = line.strip()
        # Skip empty lines
        if not line:
            continue
        # Skip comments
        if line.startswith("%") or line.startswith("#"):
            continue
        # Skip Average lines
        if line.startswith("Average"):
            continue
        if line.startswith("Mechanism"):
            # Done with this file!
            break
        if line.startswith("Rrup"):
            # Process Rrup line
            pieces = line.split()
            distances = pieces[2]
            pieces = [float(piece) for piece in distances.split("-")]
            rrup = np.mean(pieces)
            continue
        # Real data line, process it!
        pieces = line.split()[1:]
        pieces = [np.nan if piece == "N/A" else piece for piece in pieces]
        pieces = [float(piece) for piece in pieces]
        pieces.insert(0, rrup)
        pieces.append(line.split()[0])
        data.append(pieces)
    ifile.close()

    # All done, return data array
    return data

def summarize_and_plot_data(data, method, output_file):
    """
    Summarized all data into the format we need for plotting
    """
    mean_data = {}
    bins = 4
    titles = ["0.01 to 0.1s",
              "0.1 to 1s",
              "1 to 3s",
              "> 3s"]
    locs = [[0,0], [0,1], [1,0], [1,1]]
    event_names = np.array([piece[-1] for piece in data])

    # Calculate mean_data
    start = 1
    step = 3

    # Create fig
    fig, axs = pylab.plt.subplots(2, 2)
    fig.set_size_inches(17, 8.5)
    fig.suptitle("Method: %s" % (method))
    fig.subplots_adjust(hspace=0.4)
    fig.subplots_adjust(left=0.05)
    fig.subplots_adjust(right=0.98)

    current = start
    for bin in range(0, bins):
        mean_data[bin] = {}
        mean_data[bin]['mean'] = np.array([piece[current] for piece in data])
        mean_data[bin]['n'] = np.array([piece[current+2] for piece in data])
        current = current + step

    # List of distances
    r = np.array([piece[0] for piece in data])
    
    # Process each bin
    for bin in range(0, bins):
        x = np.log(r[~np.isnan(mean_data[bin]['mean'])])
        y = mean_data[bin]['mean'][~np.isnan(mean_data[bin]['mean'])]
        event_data = []
        event_legend = []
        e_labels = event_names[~np.isnan(mean_data[bin]['mean'])]
        e_labels_set = sorted(list(set(e_labels)), key=str.lower)
        # First we create a list events/markers/colors for the legend
        for index, event in enumerate(e_labels_set):
            event_legend.append([event, COLORS[index], MARKERS[index]])
            print("%s - %s - %s" % (event, COLORS[index], MARKERS[index]))
        for index, event in enumerate(e_labels_set):
            event_x = []
            event_y = []
            for label, x_val, y_val in zip(e_labels, x, y):
                if label == event:
                    event_x.append(x_val)
                    event_y.append(y_val)
            if len(event_x):
                event_data.append([event_x, event_y,
                                   COLORS[index], MARKERS[index]])

        ww = mean_data[bin]['n'][~np.isnan(mean_data[bin]['n'])]
        numdata = len(y)

        A = np.array([list(np.ones(len(x))), x])
        A = A.T
        W = np.diag(ww)
        b = np.linalg.lstsq(((A.T).dot(W)).dot(A),
                            ((A.T).dot(W)).dot(np.array(y).T),
                            rcond=-1)[0]
        intercept = b[0]
        slope = b[1]

        degfree = len(x) - 2
        e = y - (intercept + slope * x)
        var = np.sum(e * e) / degfree
        se_y = np.sqrt(var)
        sdev = np.sqrt(var)
        se_b = sdev / np.sqrt(np.sum((x - np.mean(x)) * (x - np.mean(x))))
        se_a = sdev * np.sqrt(1.0 / len(x) + np.mean(x) * np.mean(x) /
                              np.sum((x - np.mean(x)) * (x - np.mean(x))))

        xx = np.linspace(min(x), max(x),
                         num=(int(math.ceil((max(x) - min(x)) / 0.1))))
        yy = slope * xx + intercept

        # Calculate 95% confidence bounds
        t = st.t.ppf(1.0 - 0.05 / 2, degfree)
        b95 = se_b * t
        a95 = se_a * t
        ratio = abs(slope) / b95
        ratio_round = round(ratio * 100) / 100.0
        lower95 = yy - t * se_y * np.sqrt(1.0 /
                                          len(x) + ((xx - np.mean(x)) *
                                                    (xx - np.mean(x))) /
                                          np.sum((xx - np.mean(x)) *
                                                 (xx - np.mean(x))))
        upper95 = yy + t * se_y * np.sqrt(1.0 /
                                          len(x) + ((xx - np.mean(x)) *
                                                    (xx - np.mean(x))) /
                                          np.sum((xx - np.mean(x)) *
                                                 (xx - np.mean(x))))

        # Let's plot it
        p_x = locs[bin][0]
        p_y = locs[bin][1]
        subfig = axs[p_x][p_y]
        subfig.set_title("%s - Ratio: %.2f" % (titles[bin], ratio_round))
        for event in event_data:
            event_x = event[0]
            event_y = event[1]
            event_color = event[2]
            event_marker = event[3]
            subfig.plot(event_x, event_y,
                        event_marker, color=event_color)
        #subfig.plot(x, y, 'k+')
        subfig.plot(xx, yy, color='green', ls='-')
        subfig.plot(xx, lower95, 'r--', xx, upper95, 'r--')
        subfig.set_ylabel('ln(data/model)', size=10)
        subfig.set_xlabel('ln(distance(km))', size=10)
        subfig.set_xlim(0, 6)
        subfig.set_ylim(-1.5, 1.5)
        subfig.grid(True)
        subfig.minorticks_on()

    # All done, save plot!
    fig.savefig(output_file, format='png', transparent=False,
                dpi=300)

def main():
    """
    Main function
    """
    if len(sys.argv) != 2:
        print("Usage: %s input_file" % (sys.argv[0]))
        sys.exit(0)

    # Output filename
    input_file = sys.argv[1]
    output_file = "%s.png" % (os.path.splitext(input_file)[0])
    method = os.path.basename(input_file).split("-")[0].upper()

    # Read input file
    data = read_data(input_file)
    summarize_and_plot_data(data, method, output_file)

if __name__ == "__main__":
    main()
