# PoE Item Filter

A custom 'vanilla-like' item filter for Path of Exile.

* `ansq.filter` is the item filter itself. It is automatically generated and should not be edited directly.
* `ansq.filtertemplate` is a template file that contains item filter rules and references to other files in `filterparts/`
* `.filterpart` files are partial item filter chunks that get slotted into their appropriate place in `ansq.filtertemplate`
* `filtergen.py` generates `filterparts/generated/*.filterpart`:
    * `divcards.filterpart` based on current Div Card prices from [poe.ninja](https://poe.ninja/challenge/divination-cards).
    * `regular_currency`, `currency_shards`, and `leveling_flasks`
* `compile.py` generates `ansq.filter` from the template and filterparts (including running `filtergen`).

This product isn't affiliated with or endorsed by Grinding Gear Games in any way.
