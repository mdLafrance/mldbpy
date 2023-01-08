from mldbpy.table import Relation, Attribute

mytable = Relation(["ID", "NAME", Attribute("value", "\d+")])

mytable.add_entry((1, "max", 9000))
mytable.add_entry((2, "fooo", 25))
mytable.add_entry((1, "goo", 1234))

mytable.print()
