#!/usr/bin/env python3

from typing import Sequence
import os
import requests
import json
import urllib.parse
import time
import textwrap


user_agent = "AnSq/poe-filter/1.0"

ses = requests.Session()
ses.headers.update({"user-agent" : user_agent})


def get_current_league():
    r = ses.get("https://poe.ninja/api/data/getindexstate")
    return json.loads(r.text)["economyLeagues"][0]["name"]


def poe_ninja_item_overview(league, type_):
    r = ses.get(f"https://poe.ninja/api/data/ItemOverview?league={urllib.parse.quote_plus(league)}&type={type_}&language=en")
    return json.loads(r.text)["lines"]


def get_cards(league):
    cards = []
    for card in poe_ninja_item_overview(league, "DivinationCard"):
        #cards[card["name"]] = card["chaosValue"]
        cards.append((card["name"], card["chaosValue"]))
    cards.sort(key=lambda x: (-x[1], x[0]))
    return cards


def interpolate(start:int, end:int, steps:int) -> list[int]:
    diff = end - start
    step_size = float(diff) / (steps - 1)
    return [int(round(start+step*step_size)) for step in range(steps)]


def interpolate_colors(start:Sequence[int], end:Sequence[int], steps:int) -> list[list[int]]:
    diff = [x[0]-x[1] for x in zip(end, start)]
    step_sizes = [float(x)/(steps-1) for x in diff]
    return [[int(round(x[0]+step*x[1])) for x in zip(start, step_sizes)] for step in range(steps)]


def format_divcards_filter(border0, border1, text0, text1, back0, back1, size0, size1, volume0, volume1, steps, iconsize, sounds, members, thresholds, invert=None):
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
        "    BaseType == {members}\n"\
        "    SetBorderColor     {border[0]} {border[1]} {border[2]}\n"\
        "    SetTextColor       {text[0]} {text[1]} {text[2]}\n"\
        "    SetBackgroundColor {back[0]} {back[1]} {back[2]} 250\n"\
        "    MinimapIcon {iconsize} Blue Square\n"\
        "    SetFontSize {size}\n"\
        "    PlayAlertSound {sound} {volume}\n" \
        .format(tier=i+1, low=lows[i], high=highs[i], members=members[i], border=border[i], text=text[i], back=back[i], iconsize=iconsize[i], size=size[i], sound=sounds[i], volume=min(volume[i],300))
    return result


def format_levelingflasks_filter(flask_sizes, flask_levels, font_sizes):
    filter_rule = textwrap.dedent("""\
        Show
            Class Flask
            BaseType {size}
            Rarity Normal Magic
            Quality 0
            AreaLevel >= {min_level}
            AreaLevel < {max_level}
            SetFontSize {font_size}
            """)

    result = ""

    for i,size in enumerate(flask_sizes):
        for j,font_size in enumerate(font_sizes):
            result += filter_rule.format(
                size      = size,
                min_level = (1 if j == 0 else flask_levels[i+j]),
                max_level = flask_levels[i+j+1],
                font_size = font_size
            )

    return result


def make_divcards(outfile):
    league = get_current_league()
    print(f"{league} league")

    cards = get_cards(league)

    thresholds = (1, 2.4, 6, 15, 40, 100, 250, float("+inf"))
    iconsize = tuple(reversed((2, 2, 1, 1, 0, 0, 0, 0)))

    tiers = [list() for x in range(len(thresholds))]

    for c in cards:
        for i,t in enumerate(thresholds):
            if t >= c[1]:
                tiers[i].append(c[0])
                break
    tiers.reverse()
    print("Cards per tier:", list(len(t) for t in tiers))

    members = ['"'+'" "'.join(x)+'"' for x in tiers]
    steps = len(members)
    border0 = (14, 186, 255)
    border1 = (70, 156, 191)
    text0 = (14, 186, 255)
    text1 = (70, 156, 191)
    back0 = (3, 46, 64)
    back1 = (0, 0, 0)
    size0 = 45
    size1 = 24
    volume0 = 350
    volume1 = 50

    num_top = 2
    sounds = [1]*num_top + [4]*(steps - num_top)

    output = "# Updated {} ({} league)\n".format(time.strftime("%Y-%m-%d", time.gmtime()), league)
    output += format_divcards_filter(border0, border1, text0, text1, back0, back1, size0, size1, volume0, volume1, steps, iconsize, sounds, members, thresholds, invert=0)

    with open(outfile, "w") as f:
        f.write(output)


def make_levelingflasks(outfile):
    output  = "# levelingflasks is automatically generated {\n\n"

    flask_sizes   = ('"Small Hybrid"', '"Medium Hybrid"', '"Large Hybrid"', '"Colossal Hybrid"', '"Sacred Hybrid"', '"Hallowed Hybrid"')
    flask_levels  = (10, 20, 30, 40, 50, 60)
    flask_levels += (68, 72)
    font_sizes    = (28, 18)
    output += f"# Hybrid Flasks - top {len(font_sizes)} for leveling\n"
    output += format_levelingflasks_filter(flask_sizes, flask_levels, font_sizes)

    flask_sizes   = ("Small", "Medium", "Large", "Greater", "Grand", "Giant", "Colossal", "Sacred", "Hallowed", "Sanctified", "Divine", "Eternal")
    flask_levels  = (1, 3, 6, 12, 18, 24, 30, 36, 42, 50, 60, 65)
    flask_levels += (68, 70, 72)
    font_sizes    = (30, 24, 18)
    output += f"\n# Life and Mana Flasks - top {len(font_sizes)} for leveling\n"
    output += format_levelingflasks_filter(flask_sizes, flask_levels, font_sizes)

    output += "# } end levelingflasks\n"

    with open(outfile, "w") as f:
        f.write(output)


def make_regularcurrency(outfile):
    output = ""

    tiers = [
        ["Orb of Transmutation", "Armourer's Scrap", "Blacksmith's Whetstone"],
        ["Jeweller's Orb", "Orb of Binding", "Orb of Augmentation", "Engineer's Orb", "Orb of Chance"],
        ["Orb of Alteration", "Orb of Alchemy", "Chromatic Orb", "Orb of Fusing"],
        ["Cartographer's Chisel", "Glassblower's Bauble", "Orb of Horizons", "Instilling Orb", "Enkindling Orb"],
        ["Blessed Orb", "Orb of Scouring", "Orb of Regret"],
        ["Chaos Orb", "Regal Orb", "Exalted Shard", "Vaal Orb", "Gemcutter's Prism", "Orb of Unmaking", "Annulment Shard", "Harbinger's Orb"],
        ["Stacked Deck", "Awakened Sextant", "Orb of Annulment"],
        ["Exalted Orb", "Ancient Orb", "Sacred Orb", "Fracturing Shard", "Elevated Sextant"],
        ["Divine Orb", "Veiled Orb", "Reflecting Mist", "Fracturing Orb", "Hinekora's Lock", "Mirror Shard", "Mirror of Kalandra"]
    ]
    start_color = (170, 158, 130)
    end_color = (255, 192, 45)

    colors = interpolate_colors(start_color, end_color, len(tiers) - 1)
    colors.append(colors[-1])

    sizes = interpolate(26, 45, len(tiers) - 1) + [45]
    volumes = [10, 25, 50, 100, 150, 250, 275, 300, 300]
    icon_sizes = [None, None, 2, 2, 2, 1, 1, 0, 0]
    effect = [None, None, 1, 1, 0, 0, 0, 0, 0]

    for i in range(len(tiers)):
        members = '"' + '" "'.join(tiers[i]) + '"'
        color = " ".join(str(x) for x in colors[i])
        border_color = color
        sound = 3
        icon_color = "Yellow"

        if i == len(tiers) - 2:
            background_color = "50 40 0 240"
        elif i == len(tiers) - 1:
            background_color = color + " 240"
            color = "74 10 60"
            border_color = "240 0 160"
            sound = 1
            icon_color = "Pink"
        else:
            background_color = "10 10 0 240"

        output += textwrap.dedent(f"""\
            Show
                Class Currency
                BaseType == {members}
                SetBorderColor {border_color}
                SetTextColor {color}
                SetBackgroundColor {background_color}
                SetFontSize {sizes[i]}
                PlayAlertSound {sound} {volumes[i]}
                """)

        if icon_sizes[i] is not None:
            output += f"    MinimapIcon {icon_sizes[i]} {icon_color} Star\n"

        if effect[i] is not None:
            output += f"    PlayEffect {icon_color}{' Temp' if effect[i] else ''}\n"

    with open(outfile, "w") as f:
        f.write(output)


def make_currencyshards(outfile):
    output = ""

    tiers = [
        ["Scroll Fragment"],
        ["Transmutation Shard"],
        ["Binding Shard", "Engineer's Shard"],
        ["Alteration Shard", "Alchemy Shard"],
        ["Horizon Shard"],
        ["Regal Shard", "Chaos Shard", "Harbinger's Shard"],
        ["Ancient Shard"]
    ]
    start_color = (153, 142, 117, 200)
    end_color = (152, 147, 135, 250)
    colors = interpolate_colors(start_color, end_color, len(tiers))

    start_back = (5, 5, 0, 180)
    end_back = (15, 10, 5, 220)
    background_colors = interpolate_colors(start_back, end_back, len(tiers))

    sizes = interpolate(18, 36, len(tiers))
    volumes = [None, None, 10, 20, 30, 40, 50]
    icon_sizes = [None, None, None, 2, 2, 1, 1]

    for i in range(len(tiers)):
        members = '"' + '" "'.join(tiers[i]) + '"'
        color = " ".join(str(x) for x in colors[i])
        back = " ".join(str(x) for x in background_colors[i])

        output += textwrap.dedent(f"""\
            Show
                Class Currency
                BaseType == {members}
                SetBorderColor {color}
                SetTextColor {color}
                SetBackgroundColor {back}
                SetFontSize {sizes[i]}
                """)

        if volumes[i] is not None:
            output += f"    PlayAlertSound 3 {volumes[i]}\n"

        if icon_sizes[i] is not None:
            output += f"    MinimapIcon {icon_sizes[i]} Yellow Cross\n"

    with open(outfile, "w") as f:
        f.write(output)


def main():
    output_base = "filterparts/generated/"
    os.makedirs(output_base, exist_ok=True)
    make_divcards(output_base + "divcards.filterpart")
    make_levelingflasks(output_base + "leveling_flasks.filterpart")
    make_regularcurrency(output_base + "regular_currency.filterpart")
    make_currencyshards(output_base + "currency_shards.filterpart")

if __name__ == "__main__":
    main()
