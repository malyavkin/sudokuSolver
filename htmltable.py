def table(puzzle):
    style = """
        <style>
            table, td {
                border:3px solid black;
                border-collapse:collapse;
                padding: 0.5em;

            }
            td{

            }
        </style>
    """
    txt = "<table>" +\
          "".join(["<tr>" +
                   "".join(["<td>{}</td>".format("" if cell == "X" else cell) for cell in row]) +
                   "</tr>" for row in puzzle]) + \
          "</table>"
    with open("su.html", "w") as file:
        file.write(style+txt)
