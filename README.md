# PoE Item Filter

A custom 'vanilla-like' item filter for Path of Exile.

* `ansq.filter` is the item filter itself. It is automatically generated an should not be edited directly.
* `ansq.filtertemplate` is a template file that contains item filter rules and refereces to other files in `filterparts/`
* `filterparts/*.filterpart` are partial item filter chunks that get slotted into their appropriate place in `ansq.filtertemplate`
* `filtergen.py` generates `filterparts/divcards.filterpart` based on current Div Card prices from [poe.ninja](https://poe.ninja/challenge/divination-cards). It takes no arguments.
* `compile.py` generates `ansq.filter` from the template and filterparts. It takes no arguments.

This product isn't affiliated with or endorsed by Grinding Gear Games in any way.
