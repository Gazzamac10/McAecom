# python nodes in dynamo 0.7
# proposed by Julien Benoit @jbenoit44
# http://aecuandme.wordpress.com/
import clr

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit

clr.ImportExtensions(Revit.Elements)
# Import geometry conversion extension methods
clr.ImportExtensions(Revit.GeometryConversion)
# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
from System.Collections.Generic import *

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

Activate = IN[0]

collector = FilteredElementCollector(doc)
impinst = collector.OfClass(ImportInstance).ToElements()
linkedlist = list()
importlist = list()
if Activate == True:
    for item in impinst:
        if item.IsLinked:
            linkedlist.append(item)
        else:
            importlist.append(item)
li = (linkedlist + importlist)

elt = []
for i in li:
    elt.append(UnwrapElement(i).Id)

# Start Transaction
TransactionManager.Instance.EnsureInTransaction(doc)

cantdelete = []
for item in elt:
    try:
        doc.Delete(item)
    except:
        cantdelete.append(item)

# End Transaction
TransactionManager.Instance.TransactionTaskDone()
doc.Regenerate()
OUT = cantdelete