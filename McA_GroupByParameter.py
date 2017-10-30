import clr
clr.AddReference('ProtoGeometry')
clr.AddReference('ProtoGeometry')
clr.AddReference("RevitNodes")
clr.AddReference("RevitServices")
clr.AddReference("RevitAPI")
import Revit
import System
import RevitServices
import Autodesk
from Revit.Elements import *
from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)
from Autodesk.DesignScript.Geometry import *
doc = DocumentManager.Instance.CurrentDBDocument
app =  DocumentManager.Instance.CurrentUIApplication.Application


def ifequal(b,a):
	indiceslist = []
	for lA in a:
		counter = 0
		for lB in b:
			if (lA == lB):
				indiceslist.append(counter)
			counter += 1
	return indiceslist

def makelist(listing,indexing):
    return [listing[item]for item in indexing]



posselements = UnwrapElement(IN[0])

elements = posselements
parameter = IN[1]

values = []
if hasattr(elements, "__iter__"):
	output = []
	for elem in elements:
		if hasattr(elem, "__iter__"):
			vals = []
			for e in elem:
				for p in elem.Parameters:
					if p.Definition.Name == parameter:
						parm = p.AsValueString()
						if (parm is None):
							parm = p.AsString()
				vals.append(parm)
			values.append(vals)
		else:
			for p in elem.Parameters:
				if p.Definition.Name == parameter:
					parm = p.AsValueString()
					if (parm is None):
							parm = p.AsString()
			values.append(parm)
	output.append(values)
else:
	parm = 	elements.Parameter[parameter].AsValueString()
	output = parm


names = output[0]

un = [item for item in set(names)]

uniqueitems = []
for i in range(len(un)):
	uniqueitems.append(str(un[i]))

x = names
y = uniqueitems

list = []
for i in range(len(y)):
    list.append(ifequal(x,[y[i]]))

gazlist = []
for i in range(len(list)):
	gazlist.append(makelist(posselements,list[i]))

OUT = gazlist