# PoE Item Filter

A custom 'vanilla-like' item filter for Path of Exile.

* `ansq.filter` is the item filter itself. It is automatically generated and should not be edited directly.
* `ansq.filtertemplate` is a template file that contains item filter rules and references to other files in `filterparts/`
* `filterparts/*.filterpart` are partial item filter chunks that get slotted into their appropriate place in `ansq.filtertemplate`
* `filtergen.py`:
    * generates `filterparts/divcards.filterpart` based on current Div Card prices from [poe.ninja](https://poe.ninja/challenge/divination-cards).
    * generates `filterparts/levelingflasks.filterpart`.
* `compile.py` generates `ansq.filter` from the template and filterparts (including running `filtergen`).

This product isn't affiliated with or endorsed by Grinding Gear Games in any way.
