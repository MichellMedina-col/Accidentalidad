import json

nb_path = r"c:\Users\SEC EDU 92\Music\M3351614\Figueredo\Proyecto SENA\Accidentalidad\Proyecto_accidentes.ipynb"
out_path = r"c:\Users\SEC EDU 92\Music\M3351614\Figueredo\Proyecto SENA\Accidentalidad\notebook_cells.txt"

with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

with open(out_path, "w", encoding="utf-8") as f_out:
    for i, c in enumerate(nb["cells"]):
        cell_type = c["cell_type"]
        source = "".join(c["source"])
        f_out.write(f"=== Cell {i} ({cell_type}) ===\n{source}\n\n")

print("Done dumping notebook!")
