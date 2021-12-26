import numpy as np
from dateutil.parser import parse
import unicodedata

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.text as text

import matplotlib.dates as mdates
import matplotlib.cbook as cbook

import datetime as dt


################################################################################
def read_file(filename):
    data = np.loadtxt(filename, skiprows=1, delimiter=',', dtype=bytes)

    return data


################################################################################
def is_date(x):
    try:
        a = parse(x)
        return a
    except ValueError:
        return False


################################################################################
# From here
# http://pythoncentral.io/how-to-check-if-a-string-is-a-number-in-python-including-unicode/
################################################################################
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


################################################################################


def gantt_chart(activities, colors, verbose=False):
    fig1 = plt.gcf()  # plt.figure(figsize=(12,8))
    # ax = fig1.add_subplot(111, aspect='equal')
    ax = fig1.add_subplot(1, 1, 1)

    ymax = 10000

    datemin = dt.datetime(3000, 1, 1)
    datemax = dt.datetime(1, 1, 1)

    ###########################################################
    # Validate
    ###########################################################
    for i, key in enumerate(activities.keys()):
        activity = activities[key]
        akeys = activity.keys()
        if 'start' not in akeys:
            # print("Activity %s does not have a start date/dependence!" % (key))
            # exit()
            break

        if 'duration' in akeys and 'end' in akeys:
            deltat = is_date(activity['end']) - is_date(activity['start'])
            if deltat.days != activity['duration']:
                # print("Activity %s has both a duration and an end date, but they don't match up!" % (key))
                # print("Duration: %.2f" % (activity['duration']))
                # print("End-Start: %.2f" % (deltat.days))
                break

    for i, key in enumerate(activities.keys()):

        activity = activities[key]
        start = is_date(activity["start"])
        if verbose:
            print("activity")
            print(activity)
            print("start: ", start)
            print(key, activity["start"], start)
        if start == False:
            idx = activity["start"]
            # start = is_date(activities[idx]["start"]) + dt.timedelta(days = activities[idx]["duration"])
            if verbose:
                print("here")
                print(activities[idx]["start"], activities[idx]["duration"])
            start = activities[idx]["start"] + dt.timedelta(days=activities[idx]["duration"])
            # activities[key]['start'] = start
        # print(type(start))
        # else:
        if verbose:
            print(start)
        activities[key]['start'] = start  # Save it as a datetime object

        duration = activity["duration"]
        end = start + dt.timedelta(days=duration)

        if 1:
            if verbose:
                print("end: ", end, datemax)
            if start < datemin:
                datemin = start
            if end > datemax:
                datemax = end
            # color = colors[event["type_of_work"]]
            # print(activity['type_of_work'])
            # print(colors)
            color = colors[activity['type_of_work']]
            # color = colors[activity['type_of_work']]

            ax.barh(-i, duration, 0.5, start, align='center', alpha=1.0, color=color)

    # fig1.autofmt_xdate()
    xfmt = mdates.DateFormatter('%m-%d-%Y')
    ax.xaxis.set_major_formatter(xfmt)

    plt.xticks(fontsize=14)  # , rotation=90)

    datemin -= dt.timedelta(days=60)
    datemax += dt.timedelta(days=60)

    timespan = (datemax - datemin).days
    if verbose:
        print("timespan: ", timespan)

    label_start = datemin - dt.timedelta(days=0.3 * timespan)

    #######################################
    # Generate month grids by hand
    yearmin = datemin.year
    monthmin = datemin.month
    yearmax = datemax.year
    monthmax = datemax.month

    xticks = []

    nmonths = 12 * (yearmax - yearmin + 1)
    y0 = -len(activities)
    y1 = 1

    year = yearmin

    nticks = nmonths / 4

    while year <= yearmax + 1:
        month = 1
        while month <= 12:
            x = dt.datetime(year, month, 1)
            if month % 4 == 1:
                xticks.append(x)
            # rint(x,y0,y1)
            plt.plot([x, x], [y0, y1], 'k--', alpha=0.2)
            month += 1
        year += 1

    ax.set_xticks(xticks)

    # DRAW TODAY
    x = dt.datetime.today()
    plt.plot([x, x], [y0, y1], 'r-', alpha=1.0, label='Today')
    ###################################################

    # '''
    ############### Add the labels ##################################3
    # Put the names
    for i, key in enumerate(activities.keys()):
        activity = activities[key]
        # print(activity)
        name = activity["name"]

        y = -i
        # x = datemin + dt.timedelta(days=0.1)
        x = label_start
        # print("TEXT: ",name,(x,y))

        plt.text(x, y, name, backgroundcolor='white', bbox=(dict(facecolor='lightgray', alpha=1.0)), fontsize=18)
    # '''

    ##### LEGEND #######
    label_colors = []
    for key in colors.keys():
        label_colors.append(colors[key])

    label_colors.append('r')  # For the "Today" line
    # colors = ['r', 'g', 'b']
    # labels = ['foo', 'bar', 'baz']
    dummies = [ax.plot([], [], ls='-', lw=10, c=c)[0] for c in label_colors[:-1]]
    dummies += [ax.plot([], [], ls='-', lw=2, c=c)[0] for c in label_colors[-1]]  # The today line

    labels = list(colors.keys())
    labels.append('Today')
    # print(labels)
    # print(dummies)
    ax.legend(dummies, labels, loc='upper right', fontsize=18)
    #######################

    if verbose:
        print(datemin)
        print(datemax)

    ax.set_xlim(label_start, datemax)
    ax.set_ylim(-len(activities), 1)
    ax.yaxis.label.set_visible(False)

    ax.set_yticklabels([])
    # ax.set_yticks([])

    # ax.grid(axis='y')

    plt.tight_layout()
    plt.savefig("chart.jpg")

    return ax