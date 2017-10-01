#!/usr/bin/env python

import requests
import json


cards = [
    ["House of Mirrors",
    "The Doctor",
    "The Fiend",
    "Mawr Blaidd",
    "The Spark and the Flame",
    "The Queen",
    "Hunter's Reward",
    "The Immortal",
    "The Standoff"],
    ["Abandoned Wealth",
    "The King's Heart",
    "Pride Before the Fall",
    "The Dragon's Heart",
    "The Wolf",
    "The Last One Standing",
    "Wealth and Power",
    "Last Hope",
    "The Celestial Justicar",
    "The Hunger",
    "The Wolven King's Bite"],
    ["The Brittle Emperor",
    "The Saint's Treasure",
    "The Vast",
    "The Valkyrie",
    "The Artist",
    "The Thaumaturgist",
    "Heterochromia",
    "The Fletcher",
    "The Sephirot",
    "Bowyer's Dream",
    "Time-Lost Relic"],
    ["The Void",
    "The Enlightened",
    "The Ethereal",
    "The Polymath",
    "The Hoarder",
    "The Offering",
    "The Dapper Prodigy",
    "The Formless Sea",
    "The Wind",
    "Chaotic Disposition",
    "The Risk",
    "Lucky Deck",
    "The Cartographer",
    "The Valley of Steel Boxes",
    "The Wretched",
    "The Porcupine",
    "Emperor of Purity",
    "Merciless Armament",
    "Jack in the Box",
    "Scholar of the Seas",
    "The Avenger",
    "The Body",
    "The Chains that Bind",
    "The Dark Mage",
    "The Lion",
    "The Stormcaller",
    "The Warlord",
    "Vinia's Token",
    "The Cursed King",
    "Lucky Connections",
    "The Soul"],
    ["Humility",
    "The Inventor",
    "The Jester",
    "Lingering Remnants",
    "Dialla's Subjugation",
    "Earth Drinker",
    "Emperor's Luck",
    "Glimmer of Hope",
    "Hope",
    "Hubris",
    "Hunter's Resolve",
    "Lysah's Respite",
    "Rats",
    "The Aesthete",
    "The Arena Champion",
    "The Battle Born",
    "The Calling",
    "The Cataclysm",
    "The Drunken Aristocrat",
    "The Endurance",
    "The Gentleman",
    "The One With All",
    "The Penitent",
    "The Poet",
    "The Road to Power",
    "The Spoiled Prince",
    "The Throne",
    "The Tyrant",
    "The Union",
    "The Wrath",
    "Treasure Hunter",
    "Mitts",
    "The Forsaken",
    "Atziri's Arsenal",
    "The Demoness",
    "The Harvester",
    "The Traitor",
    "Blind Venture",
    "The Scavenger",
    "The Gladiator",
    "The Pact",
    "Gemcutter's Promise",
    "The Survivalist",
    "Lost Worlds",
    "The Mercenary",
    "The Encroaching Darkness",
    "The Surveyor",
    "The Garish Power"],
    ["The Fox",
    "Audacity",
    "Shard of Fate",
    "Three Faces in the Dark",
    "Light and Truth",
    "Boundless Realms",
    "The Dragon",
    "The Doppelganger",
    "The Lord in Black",
    "The Gambler",
    "The Sun",
    "The Scholar"],
    ["Gift of the Gemling Queen",
    "The Opulent",
    "A Mother's Parting Gift",
    "Anarchy's Price",
    "Assassin's Favour",
    "Birth of the Three",
    "Cartographer's Delight",
    "Coveted Possession",
    "Death",
    "Destined to Crumble",
    "Doedre's Madness",
    "Dying Anguish",
    "Grave Knowledge",
    "Her Mask",
    "Loyalty",
    "Prosperity",
    "Rain of Chaos",
    "Rain Tempter",
    "The Betrayal",
    "The Catalyst",
    "The Conduit",
    "The Explorer",
    "The Feast",
    "The Gemcutter",
    "The Hermit",
    "The Inoculated",
    "The Lich",
    "The Lunaris Priestess",
    "The Oath",
    "The Pack Leader",
    "The Rabid Rhoa",
    "The Scarred Meadow",
    "The Sigil",
    "The Siren",
    "The Summoner",
    "The Surgeon",
    "The Tower",
    "The Trial",
    "The Twins",
    "The Visionary",
    "The Warden",
    "The Watcher",
    "The Web",
    "The Wolf's Shadow",
    "Tranquillity",
    "Turn the Other Cheek",
    "Volatile Power",
    "Call to the First Ones",
    "The Coming Storm",
    "The Wolverine",
    "Might is Right",
    "Struck by Lightning",
    "The Metalsmith's Gift",
    "The Carrion Crow",
    "Lantador's Lost Love",
    "The King's Blade",
    "The Lover",
    "The Incantation",
    "The Flora's Gift",
    "Thunderous Skies"]
]


def interpolate(start, end, steps):
    diff = end - start
    step_size = float(diff) / (steps - 1)
    return [int(round(start+step*step_size)) for step in range(steps)]


def interpolate_colors(start, end, steps):
    diff = [x[0]-x[1] for x in zip(end, start)]
    step_sizes = [float(x)/(steps-1) for x in diff]
    return [[int(round(x[0]+step*x[1])) for x in zip(start, step_sizes)] for step in range(steps)]


def tiers(border0, border1, text0, text1, back0, back1, size0, size1, volume0, volume1, steps, sounds, members, invert=None):
    border = interpolate_colors(border0, border1, steps)
    text   = interpolate_colors(text0,   text1, steps)
    back   = interpolate_colors(back0,   back1, steps)
    size   = interpolate(size0,   size1, steps)
    volume = interpolate(volume0, volume1, steps)

    if invert is not None:
        tmp = back[invert]
        back[invert] = text[invert]
        text[invert] = tmp
        border[invert] = tmp

    for i in range(steps):
        print \
        "Show #\n"\
        "    Class Card\n"\
        "    BaseType {members}\n"\
        "    SetBorderColor     {border[0]} {border[1]} {border[2]}\n"\
        "    SetTextColor       {text[0]} {text[1]} {text[2]}\n"\
        "    SetBackgroundColor {back[0]} {back[1]} {back[2]} 250\n"\
        "    SetFontSize {size}\n"\
        "    PlayAlertSound {sound} {volume}" \
        .format(members=members[i], border=border[i], text=text[i], back=back[i], size=size[i], sound=sounds[i], volume=min(volume[i],300))


def main():
    members = ['"'+'" "'.join(x)+'"' for x in cards]
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
    sounds = [1] + [4]*(steps-1)

    tiers(border0, border1, text0, text1, back0, back1, size0, size1, volume0, volume1, steps, sounds, members, invert=0)


if __name__ == "__main__":
    main()
