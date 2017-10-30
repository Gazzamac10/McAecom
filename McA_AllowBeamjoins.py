# Unwrap
input = UnwrapElement(IN[0])
elements = []
# force input into list
try:
    for e in input:
        if e.Category.Name == "Structural Framing":
            elements.append(e)
except:
    if input.Category.Name == "Structural Framing":
        elements.append(input)

# Start Transaction
doc = DocumentManager.Instance.CurrentDBDocument
TransactionManager.Instance.EnsureInTransaction(doc)

for e in elements:
    Autodesk.Revit.DB.Structure.StructuralFramingUtils.AllowJoinAtEnd(e, 0)
    Autodesk.Revit.DB.Structure.StructuralFramingUtils.AllowJoinAtEnd(e, 1)

# End Transaction
TransactionManager.Instance.TransactionTaskDone()

# Wrap
OUT = elements