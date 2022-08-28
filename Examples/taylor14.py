'''
How to create a figure with multiple Taylor diagrams using subplots.

A fourteenth example of how to create a Taylor diagram given five sets of data,
each set composed by the statistics of the observation of five diffetent models, 
and each set referring to a different forecasting time. 

Mock data is used in the example.

Author: Andre D. L. Zanchetta

Created on Aug 12, 2022

@author: adlzanchetta@gmail.com
'''

import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import skill_metrics as sm
import numpy as np
import argparse


# ## DATA ####################################################################### #

LEGEND_SUBPLOT = (1, 2)

SUBPLOTS_DATA = [
    {
        "axis_idx": (0, 0),
        "title": "(a) 1 hour lead time",
        "y_label": True,
        "x_label": False,
        "observed": (29.91, 0.00, 1.00),
        "modeled": {
            "Model \u03B1": (30.28, 16.84, 0.84),
            "Model \u03B2": (28.54,  8.83, 0.96),
            "Model \u03B4": (28.02,  9.02, 0.95),
            "Model \u03B8": (28.51,  8.44, 0.96),
            "Model \u03C1": (28.39,  8.47, 0.96)
        }
    }, {
        "axis_idx": (0, 1),
        "title": "(b) 2 hours lead time",
        "y_label": False,
        "x_label": False,
        "observed": (29.91, 0.00, 1.00),
        "modeled": {
            "Model \u03B1": (25.45, 17.58, 0.81),
            "Model \u03B2": (26.07, 14.69, 0.87),
            "Model \u03B4": (24.57, 16.08, 0.84),
            "Model \u03B8": (26.43, 15.26, 0.86),
            "Model \u03C1": (26.57, 13.61, 0.89)
        }
    }, {
        "axis_idx": (0, 2),
        "title": "(c) 3 hours lead time",
        "y_label": False,
        "x_label": True,
        "observed": (29.91, 0.00, 1.00),
        "modeled": {
            "Model \u03B1": (19.37, 23.33, 0.64),
            "Model \u03B2": (21.98, 21.00, 0.72),
            "Model \u03B4": (20.02, 21.74, 0.70),
            "Model \u03B8": (22.46, 20.37, 0.74),
            "Model \u03C1": (23.32, 19.30, 0.77)
        }
    }, {
        "axis_idx": (1, 0),
        "title": "(d) 4 hours lead time",
        "y_label": True,
        "x_label": True,
        "observed": (29.91, 0.00, 1.00),
        "modeled": {
            "Model \u03B1": (15.46, 27.45, 0.46),
            "Model \u03B2": (16.64, 25.49, 0.56),
            "Model \u03B4": (14.74, 25.94, 0.54),
            "Model \u03B8": (19.71, 25.73, 0.56),
            "Model \u03C1": (19.30, 23.28, 0.66)
        }
    }, {
        "axis_idx": (1, 1),
        "title": "(e) 5 hours lead time",
        "y_label": True,
        "x_label": True,
        "observed": (29.91, 0.00, 1.00),
        "modeled": {
            "Model \u03B1": (10.33, 30.00, 0.28),
            "Model \u03B2": (16.54, 30.09, 0.33),
            "Model \u03B4": (12.03, 28.26, 0.43),
            "Model \u03B8": (15.76, 29.92, 0.34),
            "Model \u03C1": (15.87, 27.06, 0.50)
        }
    }
]

MARKERS = {
    "Observed": {
        "marker": "^",
        "color_edge": "#000000",
        "color_face": "#000000",
        "markersize": 9
    },
    "Model \u03B1": {
        "marker": "o",
        "color_edge": "#000000",
        "color_face": "#777777",
        "markersize": 9
    },
    "Model \u03B2": {
        "marker": "D",
        "color_edge": "#AA0000",
        "color_face": "#DD3333",
        "markersize": 9
    },
    "Model \u03B4": {
        "marker": "v",
        "color_edge": "#00AA00",
        "color_face": "#33DD33",
        "markersize": 9
    },
    "Model \u03B8": {
        "marker": "s",
        "color_edge": "#0000AA",
        "color_face": "#3333DD",
        "markersize": 9
    },
    "Model \u03C1": {
        "marker": "*",
        "color_edge": "#D4AF37",
        "color_face": "#FFD700",
        "markersize": 12
    }
}


# ## PLOT STYLE ################################################################# #

FONT_FAMILY = 'Times New Roman'
FONT_SIZE = 9

# specify some styles for the correlation component
COLS_COR = {
    'grid': '#DDDDDD',
    'tick_labels': '#000000',
    'title': '#000000'
}

# specify some styles for the standard deviation
COLS_STD = {
    'grid': '#DDDDDD',
    'tick_labels': '#000000',
    'ticks': '#DDDDDD',
    'title': '#000000'
}

# specify some styles for the root mean square deviation
STYLES_RMS = {
    'color': '#AAAADD',
    'linestyle': '--'
}


# ## CONSTANTS ################################################################## #

OUTPUT_FILE_PATH = "taylor14.png"


# ## MAIN ####################################################################### #

if __name__ == '__main__':

    # Defines the output file name or path 
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-o", "--output_file", dest='output_file', type=str,
                            default=OUTPUT_FILE_PATH,
                            help="Defines the output file name.")
    arg_parser.add_argument('-noshow', dest='no_show', action='store_true',
                            help="No figure is shown if this flag is present.")
    arg_parser.add_argument('-nosave', dest='no_save', action='store_true',
                            help="No figure is saved if this flag is present.")
    args = arg_parser.parse_args()
    del arg_parser

    # Close any previously open graphics windows
    # ToDo: fails to work within Eclipse
    plt.close('all')

    # update figures global properties
    plt.rcParams.update({'font.size': FONT_SIZE, 'font.family': FONT_FAMILY})

    # create figure with 2 lines and 3 columns
    fig_size = (3*2.8, 2*2.8)
    fig, axs = plt.subplots(2, 3, figsize=fig_size, sharey=True)
    del fig_size

    # build subplot by subplot
    for subplot_data in SUBPLOTS_DATA:
        
        # get subplot object and ensure it will be a square
        # y-axis labels will only appear on leftmost subplot
        ax = axs[subplot_data["axis_idx"][0]][subplot_data["axis_idx"][1]]
        ax.set(adjustable='box', aspect='equal')

        # create the plot with the observed data
        stdev, crmsd, ccoef = subplot_data["observed"]
        sm.taylor_diagram(ax,
                          np.asarray((stdev, stdev)), 
                          np.asarray((crmsd, crmsd)), 
                          np.asarray((ccoef, ccoef)),
                          markercolors = {
                              "face": MARKERS["Observed"]["color_edge"],
                              "edge": MARKERS["Observed"]["color_face"]
                              },
                          markersize = MARKERS["Observed"]["markersize"],
                          markersymbol = MARKERS["Observed"]["marker"],
                          styleOBS = ':',
                          colOBS = MARKERS["Observed"]["color_edge"],
                          alpha = 1.0,
                          titleSTD = 'off',
                          titleRMS = 'off',
                          showlabelsRMS = 'on',
                          tickRMS = [10, 20, 30],
                          colRMS = STYLES_RMS['color'],
                          tickRMSangle = 115,
                          styleRMS = STYLES_RMS['linestyle'],
                          colscor = COLS_COR,
                          colsstd = COLS_STD,
                          styleCOR='-',
                          styleSTD='-',
                          colframe='#DDDDDD',
                          labelweight='normal',
                          titlecorshape='linear')

        # add label below the marker
        ax.text(stdev, -0.5, "Obsv.", verticalalignment="top",
                horizontalalignment="center", 
                fontsize=FONT_SIZE+1, fontweight="bold")
        
        # get rid of variables not to be used anymore
        del stdev, crmsd, ccoef

        # create one overlay for each model marker
        for model_id, (stdev, crmsd, ccoef) in subplot_data["modeled"].items():
            marker = MARKERS[model_id]
            sm.taylor_diagram(ax,
                              np.asarray((stdev, stdev)),
                              np.asarray((crmsd, crmsd)),
                              np.asarray((ccoef, ccoef)),
                              markersymbol = marker["marker"],
                              markercolors = {
                                "face": marker["color_face"],
                                "edge": marker["color_edge"]
                              },
                              markersize = marker["markersize"],
                              alpha = 1.0,
                              overlay = 'on',
                              styleCOR = '-',
                              styleSTD = '-')

            # get rid of variables not to be used anymore
            del model_id, stdev, crmsd, ccoef, marker

        # set titles (upper, left, bottom)
        ax.set_title(subplot_data["title"], loc="left", y=1.1)

        # add y label
        if subplot_data["y_label"]:
            ax.set_ylabel("Standard Deviation", fontfamily=FONT_FAMILY,
                          fontsize=FONT_SIZE+2)

        # add xlabel or hide xticklabels
        if subplot_data["x_label"]:
            ax.set_xlabel("Standard Deviation", fontfamily=FONT_FAMILY,
                          fontsize=FONT_SIZE+2)
        else:
            ax.set_xticklabels(ax.get_xticklabels(), color=ax.get_facecolor())

        # just for the peace of mind...
        del subplot_data, ax

    # create legend in the last subplot
    ax = axs[LEGEND_SUBPLOT[0]][LEGEND_SUBPLOT[1]]
    ax.axis('off')

    # build legend handles    
    legend_handles = []
    legend_handles.append(mlines.Line2D([], [],
                          color=STYLES_RMS['color'],
                          linestyle=STYLES_RMS['linestyle'],
                          label="RMSE"))

    for marker_label, marker_desc in MARKERS.items():
        marker = mlines.Line2D([], [], 
                               marker=marker_desc["marker"],
                               markersize=marker_desc["markersize"],
                               markerfacecolor=marker_desc["color_face"],
                               markeredgecolor=marker_desc["color_edge"],
                               linestyle='None',
                               label=marker_label)
        legend_handles.append(marker)
        del marker_label, marker_desc, marker

    # create legend and free memory
    ax.legend(handles=legend_handles, loc="center")    
    del ax, legend_handles

    # avoid some overlapping
    plt.tight_layout()

    # Write plot to file
    None if args.no_save else plt.savefig(args.output_file, dpi=150, facecolor='w')

    # Show plot and close it
    None if args.no_show else plt.show()
    plt.close()