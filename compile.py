#!/usr/bin/env python3

import filtergen

template_fname = "ansq.filtertemplate"
output_fname = "ansq.filter"


def process_line(line, output_f):
    if line[0] != "{":
        output_f.write(line)
    else:
        partname = line.strip()[1:-1]
        part_fname = f"filterparts/{partname}.filterpart"
        print(f"Part: {part_fname}")
        with open(part_fname) as part_f:
            for part_line in part_f:
                process_line(part_line, output_f)


def main():
    print(f"Template: {template_fname}")
    print(f"Output: {output_fname}")

    filtergen.main()

    with open(template_fname) as template_f, open(output_fname, "w") as output_f:
        output_f.write("# ################\n")
        output_f.write("# /!\ This file is automatically generated.\n")
        output_f.write("#     Edit the .filtertemplate and .filterpart files instead.\n")
        output_f.write("# ################\n\n")

        for template_line in template_f:
            process_line(template_line, output_f)


if __name__ == "__main__":
    main()