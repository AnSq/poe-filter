#!/usr/bin/env python3

import requests
import json
import re
import time


user_agent = "AnSq/poe-filter/1.0"

ses = requests.Session()
ses.headers.update({"user-agent" : user_agent})


def get_current_league():
    r = ses.get("https://poe.ninja")
    m = re.search(r'window\.economyLeagues = \[\{"name":"(\w+)","url":"challenge",', r.text)
    return m.group(1)


def poe_ninja_item_overview(league, type_):
    r = ses.get("https://poe.ninja/api/data/ItemOverview?league={}&type={}&language=en".format(league, type_))
    return json.loads(r.text)["lines"]


def get_cards(league):
    cards = []
    for card in poe_ninja_item_overview(league, "DivinationCard"):
        #cards[card["name"]] = card["chaosValue"]
        cards.append((card["name"], card["chaosValue"]))
    cards.sort(key=lambda x: (-x[1], x[0]))
    return cards


def interpolate(start, end, steps):
    diff = end - start
    step_size = float(diff) / (steps - 1)
    return [int(round(start+step*step_size)) for step in range(steps)]


def interpolate_colors(start, end, steps):
    diff = [x[0]-x[1] for x in zip(end, start)]
    step_sizes = [float(x)/(steps-1) for x in diff]
    return [[int(round(x[0]+step*x[1])) for x in zip(start, step_sizes)] for step in range(steps)]


def format_filter(border0, border1, text0, text1, back0, back1, size0, size1, volume0, volume1, steps, sounds, members, thresholds, invert=None):
    border = interpolate_colors(border0, border1, steps)
    text   = interpolate_colors(text0,   text1, steps)
    back   = interpolate_colors(back0,   back1, steps)
    size   = interpolate(size0,   size1, steps)
    volume = interpolate(volume0, volume1, steps)

    highs = tuple(reversed(thresholds))
    lows  = tuple(reversed(thresholds))[1:] + (0,)

    if invert is not None:
        tmp = back[invert]
        back[invert] = text[invert]
        text[invert] = tmp
        border[invert] = tmp

    result = ""
    for i in range(steps):
        result += \
        "Show #tier{tier} ({low}-{high}]\n"\
        "    Class Card\n"\
        "    BaseType {members}\n"\
        "    SetBorderColor     {border[0]} {border[1]} {border[2]}\n"\
        "    SetTextColor       {text[0]} {text[1]} {text[2]}\n"\
        "    SetBackgroundColor {back[0]} {back[1]} {back[2]} 250\n"\
        "    SetFontSize {size}\n"\
        "    PlayAlertSound {sound} {volume}\n" \
        .format(tier=i+1, low=lows[i], high=highs[i], members=members[i], border=border[i], text=text[i], back=back[i], size=size[i], sound=sounds[i], volume=min(volume[i],300))
    return result


def main(outfile):
    league = get_current_league()
    cards = get_cards(league)
    for c in cards:
        print(c)

    thresholds = (1, 2.4, 6, 15, 40, 100, 250, float("+inf"))
    tiers = [list() for x in range(len(thresholds))]

    for c in cards:
        for i,t in enumerate(thresholds):
            if t >= c[1]:
                tiers[i].append(c[0])
                break
    tiers.reverse()
    print(list(len(t) for t in tiers))

    members = ['"'+'" "'.join(x)+'"' for x in tiers]
    steps = len(members)
    border0 = (14, 186, 255)
    border1 = (70, 156, 191)
    text0 = (14, 186, 255)
    text1 = (70, 156, 191)
    back0 = (3, 46, 64)
    back1 = (0, 0, 0)
    size0 = 45
    size1 = 22
    volume0 = 350
    volume1 = 50

    num_top = 2
    sounds = [1]*num_top + [4]*(steps - num_top)

    output = "#updated {} ({} league)\n".format(time.strftime("%Y-%m-%d", time.gmtime()), league)
    output += format_filter(border0, border1, text0, text1, back0, back1, size0, size1, volume0, volume1, steps, sounds, members, thresholds, invert=0)

    with open(outfile, "w") as w:
        w.write(output)


if __name__ == "__main__":
    main("filterparts/divcards.filterpart")
