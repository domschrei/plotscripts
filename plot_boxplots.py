#!/usr/bin/env python3

"""
The box extends from the first quartile (Q1) to the third quartile (Q3) of the data, with a line at the median. The whiskers extend from the box by 1.5x the inter-quartile range (IQR). Flier points are those past the end of the whiskers. See https://en.wikipedia.org/wiki/Box_plot for reference.

     Q1-1.5IQR   Q1   median  Q3   Q3+1.5IQR
                  |-----:-----|
  o      |--------|     :     |--------|    o  o
                  |-----:-----|
flier             <----------->            fliers
                       IQR
"""


import sys

infiles = []
labels = []
xlabel = ""
ylabel = ""
ymax = None
sansfont = False
timesfont = False
grid = False
yticks = None
ytickslabels = None
rotatetext = 90
title = None
spacing = 0.6
width = 0.4
sizex = 3
sizey = 3

hlines = []

for arg in sys.argv[1:]:
    if arg.startswith("-l="):
        labels += [arg[len("-l="):]]
    elif arg.startswith("-xlabel="):
        xlabel = arg[len("-xlabel="):]
    elif arg.startswith("-ylabel="):
        ylabel = arg[len("-ylabel="):]
    elif arg.startswith("-ymax="):
        ymax = float(arg[len("-ymax="):])
    elif arg.startswith("-hline="):
        hlines += [float(arg[len("-hline="):])]
    elif arg.startswith("-sansfont"):
        sansfont = True
    elif arg.startswith("-grid"):
        grid = True
    elif arg.startswith("-yticks="):
        yticks = arg[len("-yticks="):].split(",")
    elif arg.startswith("-ytickslabels="):
        ytickslabels = arg[len("-ytickslabels="):].split(",")
    elif arg.startswith("-rotatelabels="):
        rotatetext = int(arg[len("-rotatelabels="):])
    elif arg.startswith("-title="):
        title = arg[len("-title="):]
    elif arg.startswith("-sizex="):
        sizex = float(arg[len("-sizex="):])
    elif arg.startswith("-sizey="):
        sizey = float(arg[len("-sizey="):])
    elif arg.startswith("-spacing="):
        spacing = float(arg[len("-spacing="):])
    elif arg.startswith("-width="):
        width = float(arg[len("-width="):])
    else:
        infiles += [arg]
outfile = infiles[-1]
del infiles[-1]

import matplotlib
if outfile:
    matplotlib.use('pdf')
matplotlib.rcParams['hatch.linewidth'] = 0.5  # previous pdf hatch linewidth
import matplotlib.pyplot as plt
from matplotlib import rc

rc('text', usetex=True)
if sansfont:
    matplotlib.rcParams['text.latex.preamble'] += r'\usepackage[cm]{sfmath}'
    #matplotlib.rcParams['font.family'] = 'sans-serif'
    #matplotlib.rcParams['font.sans-serif'] = 'cm'
    rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
    #\renewcommand\familydefault{\sfdefault} 
else:
    rc('font', family='serif')
    if timesfont:
        rc('font', serif=['Times'])

datas = []
positions = []
calcymax = 0
for (i, f) in enumerate(infiles):
    data = []
    for line in open(f, 'r').readlines():
        words = line.rstrip().split(" ")
        data += [float(words[0])]
        if ymax is None:
            calcymax = max(calcymax, data[-1])
    datas += [data]
    positions += [0.5+spacing*i]

if ymax is None:
    ymax = calcymax

plt.figure(figsize=(sizex, sizey))
xmin = positions[0]-0.5*width-0.1
xmax = positions[-1]+0.5*width+0.1
plt.xlim(xmin, xmax)
if ymax:
    plt.ylim(0, ymax)
plt.boxplot(datas, labels=labels, positions=positions, widths=[0.4 for x in datas], sym='.', flierprops={"markersize":2, "alpha":0.5})
for (i, data) in enumerate(datas):
    asterisk = "^*" if max(data) > ymax else ""
    plt.text(positions[i], ymax, f"(${len(data)}{asterisk}$)", ha='center', va='bottom', fontsize=8)

for y in hlines:
    plt.plot([xmin, xmax], [y, y], linestyle="--", color="gray", lw=0.7)
    plt.text(xmin-0.1, y, str(y), ha='right', va='center', color="gray")

plt.xticks(rotation=rotatetext)

if grid:
    plt.grid(axis='y', color='#dddddd')

if xlabel:
    plt.xlabel(xlabel)
if ylabel:
    plt.ylabel(ylabel)

if title:
    plt.title(title, pad=16)

plt.tight_layout()

if yticks:
    ax = plt.gca()
    ax.set_yticklabels(ytickslabels if ytickslabels else yticks)
    ax.set_yticks([float(x) for x in yticks])

# remove "zero" from y ticks
"""
(ylocs, ylabels) = plt.yticks()
new_ylocs = []
new_ylabels = []
for i in range(len(ylocs)):
    if ylocs[i] <= 0:
        continue
    if ylocs[i] > ymax:
        continue
    new_ylocs += [ylocs[i]]
    new_ylabels += [ylabels[i]]
plt.yticks(new_ylocs, new_ylabels)
"""

plt.savefig(outfile)
