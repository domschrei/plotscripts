#!/usr/bin/env python3
 
import math
import sys
import re
import argparse

# Moves all unqualified "named" arguments to the front of the program args.
# This allows to use the script with constructs like 
# "datafile1 -l=Label1 datafile2 -l=Label2 ..."
def move_unqualified_args_to_front():
    print(f"Args before: {sys.argv}")
    optargs = []
    namedargs = [sys.argv[0]]
    next_is_value = False
    for arg in sys.argv[1:]:
        if re.match(r'-[A-Za-z0-9_-]+=.+', arg):
            # argument with "="
            optargs += [arg]
        elif re.match(r'-[A-Za-z0-9_-]+', arg):
            # option
            next_is_value = True
            optargs += [arg]
        elif next_is_value:
            # value
            next_is_value = False
            optargs += [arg]
        else:
            # unqualified "named" argument!
            namedargs += [arg]
    sys.argv = namedargs + optargs
    print(f"Args after: {sys.argv}")

def unpack_comma_separated_options(argvalue):
    if not argvalue:
        return
    argvalue = argvalue.split(',')
    print(argvalue)

parser = argparse.ArgumentParser(description='Plot a number of curves.')

parser.add_argument('-logx', '--logx', '-log-x', '--log-x', action="store_true", 
                    help='Enable logarithmic scale for x axis')
parser.add_argument('-logy', '--logy', '-log-y', '--log-y', action="store_true", 
                    help='Enable logarithmic scale for y axis')
parser.add_argument('-y2', '--y2', action="store_true", 
                    help='Enable 2nd y axis on the right')
parser.add_argument('-nomarkers', '--nomarkers', '-no-markers', '--no-markers', 
                    action="store_true", help='Disable markers')
parser.add_argument('-nolinestyles', '--nolinestyles', '-no-linestyles', '--no-linestyles', 
                    action="store_true", help='Disable line styles')
parser.add_argument('-nolines', '--nolines', '-no-lines', '--no-lines', 
                    action="store_true", help='Disable lines')
parser.add_argument('-nolegend', '--nolegend', '-no-legend', '--no-legend', 
                    action="store_true", help='Disable legend')
parser.add_argument('-confidence', '--confidence',
                    action="store_true", help='Add confidence area')
parser.add_argument('-legendright', '--legendright', '-legend-right', '--legend-right',
                    action="store_true", help='Move legend to the right outside of the plot')
parser.add_argument('-rect', '--rect',
                    action="store_true", help='Plot connecting lines between points in a rectangular fashion')
parser.add_argument('-extend-to-right', '--extend-to-right',
                    action="store_true", help='Extend lines after the final data point to the right until -max-x value')
parser.add_argument('-sansfont', '--sans-font',
                    action="store_true", help='Use LaTeX sans serif font')
parser.add_argument('-timesfont', '--times-font',
                    action="store_true", help='Use Times New Roman like font')
parser.add_argument('-gridx', '--gridx', '-grid-x', '--grid-x',
                    action="store_true", help='Draw grid along x direction')
parser.add_argument('-gridy', '--gridy', '-grid-y', '--grid-y',
                    action="store_true", help='Draw grid along y direction')
parser.add_argument('-grid', '--grid',
                    action="store_true", help='Draw grid along both directions')
parser.add_argument('-xyc', '--xyc',
                    action="store_true", help='Expect x coordinate, y coordinate, and color value for each data point')
parser.add_argument('-xy', '--xy',
                    action="store_true", help='Expect x coordinate and y coordinate for each data point')

parser.add_argument('-legend-spacing', '--legend-spacing', type=float, default=0.5, help='Vertical spacing between legend items')
parser.add_argument('-lloc', '--lloc', '-legend-location', '--legend-location', type=int, default=0,
                    help='(PyPlot) location of legend')
parser.add_argument('-sizex', '--sizex', '-size-x', '--size-x', type=float, default=4, help='Plot width')
parser.add_argument('-sizey', '--sizey', '-size-y', '--size-y', type=float, default=4, help='Plot height')
parser.add_argument('-size', '--size', type=float, help='Plot size (width and height)')
parser.add_argument('-lw', '--lw', '-linewidth', '--linewidth', type=float, default=1, help='Line width')
parser.add_argument('-markersize', '--markersize', '-marker-size', '--marker-size', type=float, help='Marker size')

parser.add_argument('datafile', type=str, help='Add data file with whitespace-separated values', action='append', nargs='*')
parser.add_argument('-y2data', '--y2data', '-y2-data', '--y2-data', action='append', nargs='*',
                    type=str, help='Add data file, mapped to 2nd y axis, with whitespace-separated values')
parser.add_argument('-l', '--label', help='Add curve label', action='append', nargs=1, default=[])

parser.add_argument('-minx', '--minx', '-min-x', '--min-x', type=float, help='Minimum x value')
parser.add_argument('-maxx', '--maxx', '-max-x', '--max-x', type=float, help='Maximum x value')
parser.add_argument('-miny', '--miny', '-min-y', '--min-y', type=float, help='Minimum y value')
parser.add_argument('-maxy', '--maxy', '-max-y', '--max-y', type=float, help='Maximum y value')
parser.add_argument('-miny2', '--miny2', '-min-y2', '--min-y2', type=float, help='Minimum 2nd y value')
parser.add_argument('-maxy2', '--maxy2', '-max-y2', '--max-y2', type=float, help='Maximum 2nd y value')
parser.add_argument('-labelx', '--labelx', '-label-x', '--label-x', type=str, help='Label of x axis')
parser.add_argument('-labely', '--labely', '-label-y', '--label-y', type=str, help='Label of y axis')
parser.add_argument('-labely2', '--labely2', '-label-y2', '--label-y2', type=str, help='Label of 2nd y axis')
parser.add_argument('-title', '--title', type=str, help='Title text above the plot')
parser.add_argument('-o', '--o', '--output', type=str, help='Output file')

parser.add_argument('-colors', '--colors', type=str, help='Comma-separated (Pythonic) color values to cycle through',
                    default='#377eb8,#ff7f00,#e41a1c,#f781bf,#a65628,#4daf4a,#984ea3,#999999,#dede00,#377eb8')
parser.add_argument('-markers', '--markers', type=str, help='Comma-separated (Pythonic) marker symbols to cycle through',
                    default='^,s,o,+,x,*')
parser.add_argument('-linestyles', '--linestyles', type=str, help='Comma-separated (Pythonic) linestyle symbols to cycle through',
                    default='-.,:,--,-')
parser.add_argument('-linewidths', '--linewidths', '-line-widths', '--line-widths', type=str, default='',
                    help='Comma-separated line widths to cycle through')
parser.add_argument('-ticksx', '--ticksx', '-ticks-x', '--ticks-x', type=str, default='',
                    help='Comma-separated tick values for x axis')
parser.add_argument('-ticksy', '--ticksy', '-ticks-y', '--ticks-y', type=str, default='',
                    help='Comma-separated tick values for y axis')
parser.add_argument('-ticksy2', '--ticksy2', '-ticks-y2', '--ticks-y2', type=str, default='',
                    help='Comma-separated tick values for 2nd y axis')

move_unqualified_args_to_front()
args = parser.parse_args()
args.colorslist = args.colors.split(',') if args.colors else []
args.markerslist = args.markers.split(',') if args.markers else []
args.linestyleslist = args.linestyles.split(',') if args.linestyles else []
args.linewidthslist = args.linewidths.split(',') if args.linewidths else []
args.ticksxlist = args.ticksx.split(',') if args.ticksx else []
args.ticksylist = args.ticksy.split(',') if args.ticksy else []
args.ticksy2list = args.ticksy2.split(',') if args.ticksy2 else []
args.labellist = [l for labels in args.label for l in labels]

print(args)

import matplotlib
if args.o:
    matplotlib.use('pdf')
matplotlib.rcParams['hatch.linewidth'] = 0.5  # previous pdf hatch linewidth
import matplotlib.pyplot as plt
from matplotlib import rc

rc('text', usetex=True)
if args.sans_font:
    matplotlib.rcParams['text.latex.preamble'] = [r'\usepackage[cm]{sfmath}']
    matplotlib.rcParams['font.family'] = 'sans-serif'
    matplotlib.rcParams['font.sans-serif'] = 'cm'
    #\renewcommand\familydefault{\sfdefault} 
else:
    rc('font', family='serif')
    if args.times_font:
        rc('font', serif=['Times'])

def process_line(line, X, Y, C, lc):
    
    words = line.rstrip().split(" ")
    
    # check validity
    for word in words:
        try:
            x = float(word)
        except:
            return
    
    num_ys = len(words)
    if args.xyc:
        num_ys -= 1
    
    if not Y:
        if args.xy or args.xyc:
            for i in range(1, num_ys):
                Y += [[]]
        else:
            for i in range(num_ys):
                Y += [[]]
        
    # X value
    if args.rect and len(X) > 0:
        x = float(words[0])-0.0001
        X += [x]
    if args.xy or args.xyc:
        x = float(words[0])
        X += [x]
        words = words[1:]
        if args.xyc:
            C += [int(words[-1])]
            words = words[0:-1]
    else:
        X += [lc]
        
    # Y values
    for i in range(len(words)):
        y = float(words[i])
        if args.rect and len(Y[i]) > 0:
            Y[i] += [Y[i][-1]]
        Y[i] += [y]

data = []
datanames = []
is_data_on_y2 = []

if not args.datafile or args.datafile == [[]]:
    # Read from stdin
    X = []
    Y = []
    C = []
    lc = 0
    for line in sys.stdin:
        process_line(line, X, Y, C, lc)
        lc += 1
        
    print("stdin:",str(len(X)),"vals")
    for vals in Y:
        data += [[X, vals, C]]
        is_data_on_y2 += [False]
    
else:
    print("Files specified")
    files_y1 = [(f, False) for arg in args.datafile for f in arg]
    files_y2 = []
    if args.y2data:
        files_y2 = [(f, True) for arg in args.y2data for f in arg]
    print(files_y1)
    print(files_y2)
    files = files_y1 + files_y2
    print(files)
    
    for (arg, y2) in files:
        X = []
        Y = []
        C = []
        lc = 0
        for line in open(arg, 'r').readlines():
            process_line(line, X, Y, C, lc)
            lc += 1
        if args.extend_to_right and args.maxx and X[-1] < args.maxx:
            if len(C) == len(X):
                C += [C[-1]]
            X += [args.maxx+(args.maxx-args.minx)]
            for Ys in Y:
                Ys += [Ys[-1]]
            
        print(arg,":",str(len(X)),"vals")
        for vals in Y:
            data += [[X, vals, C]]
            datanames += [arg]
            is_data_on_y2 += [y2]

fig, ax = plt.subplots(1, 1, figsize=(args.sizex, args.sizey))

ax.set_axisbelow(True)
if args.gridx and args.gridy:
    plt.grid(axis='both', color='#dddddd')
elif args.gridx:
    plt.grid(axis='x', color='#dddddd')
elif args.gridy:
    plt.grid(axis='y', color='#dddddd')

if args.confidence:
    plt.fill_between(data[1][0], data[1][1], data[2][1], color='#ccccff')

if args.y2:
    ax = plt.gca()
    ax2 = ax.twinx()

i = 0
for d in data:
    print(i)
    
    kwargs = dict()
    
    if i < len(args.labellist):
        kwargs['label'] = args.labellist[i]
    else:
        kwargs['label'] = datanames[i].replace('_', '-')
    
    if args.xyc:
        kwargs['color'] = [args.colorslist[x%len(args.colorslist)] for x in d[2]]
    else:
        kwargs['color'] = args.colorslist[i%len(args.colorslist)]

    if not args.nomarkers and args.markers:
        kwargs['marker'] = args.markerslist[i%len(args.markerslist)]
        if kwargs['marker'] in ['+', 'x']:
            kwargs['markerfacecolor'] = kwargs['color']
        else:
            kwargs['markerfacecolor'] = 'none'
    
    if not args.nolinestyles:
        kwargs['linestyle'] = args.linestyleslist[i%len(args.linestyleslist)]
    
    if args.linewidthslist:
        kwargs['lw'] = args.linewidthslist[i%len(args.linewidthslist)]
    elif args.nolines:
        kwargs['lw'] = 0
    elif args.lw:
        kwargs['lw'] = args.lw
    
    if args.markersize:
        kwargs['markersize'] = args.markersize
    
    if is_data_on_y2[i]:
        ax2.plot(d[0], d[1], **kwargs)
    else:
        ax.plot(d[0], d[1], **kwargs)
    i += 1

if args.title:
    plt.title(args.title)
if args.logx:
    plt.xscale("log")
if args.logy:
    plt.yscale("log")
if args.y2:
    ax.set_xlabel(args.labelx)
    ax.set_ylim(args.miny, args.maxy)
    ax.set_ylabel(args.labely)
    ax2.set_ylim(args.miny2, args.maxy2)
    ax2.set_ylabel(args.labely2)
else:
    if args.labelx:
        plt.xlabel(args.labelx)
    if args.labely:
        plt.ylabel(args.labely)
    plt.ylim(args.miny, args.maxy)
    plt.xlim(args.minx, args.maxx)

if not args.nolegend:
    if args.legendright:
        plt.legend(bbox_to_anchor=(1.05, 0.5), loc='center left', edgecolor="black", labelspacing=args.legend_spacing)
    else:
        plt.legend(loc=args.lloc, labelspacing=args.legend_spacing)

if args.ticksxlist:
    print("xticks")
    ax.set_xticklabels(args.ticksxlist)
    ax.set_xticks([float(x) for x in args.ticksxlist])
    plt.minorticks_off()
if args.ticksylist:
    print("yticks")
    ax.set_yticklabels(args.ticksylist)
    ax.set_yticks([float(x) for x in args.ticksylist])
    plt.minorticks_off()
if args.ticksy2list:
    print("y2ticks")
    ax2.set_yticklabels(args.ticksy2list)
    ax2.set_yticks([float(x) for x in args.ticksy2list])
    plt.minorticks_off()

plt.tight_layout()
if args.o:
    plt.savefig(args.o) #, dpi=600, format='eps')
else:
    plt.show()
