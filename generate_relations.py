from collections import defaultdict
import networkx

dig = networkx.DiGraph()
relations = defaultdict(set)
all_items = set()

with open("pou_relations.dot", "rt") as fp:
    pou_relations_dot = fp.read()


for line in pou_relations_dot.splitlines():
    if "{" in line:  # }
        line = line.split("{")[1]  # }

    if "->" in line:
        from_, to = line.split("->")
        from_ = from_.strip()
        to = to.strip("; ")
        relations[from_].add(to)

        all_items.add(from_)
        all_items.add(to)
        networkx.add_path(dig, [from_, to])


with open(f"graphs/full_project.dot", "wt") as fp:
    print(pou_relations_dot, file=fp)


for item in sorted(all_items):
    # all_connected = networkx.descendants(dig.to_undirected(), item)
    all_connected = list(dig.to_undirected().neighbors(item))
    print("neighbors of", item, all_connected)
    with open(f"graphs/{item}.dot", "wt") as fp:
        print(f"digraph {item} {{", file=fp)  # }}
        print(f"     node [style=filled]", file=fp)  # }}
        print(f"    {item} [fillcolor = bisque];", file=fp)
        for from_, to_set in sorted(relations.items()):
            for to in sorted(to_set):
                if from_ == item or to == item:
                    print(f"    {from_} -> {to};", file=fp)
        print(f"}}", file=fp)
