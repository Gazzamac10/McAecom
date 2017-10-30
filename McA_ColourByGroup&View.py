import clr

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit

clr.ImportExtensions(Revit.Elements)

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

import sys

pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

# The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN


def isiterable(x):
    if hasattr(type(x), "__iter__"):
        return x
    else:
        return [x]


elements = [UnwrapElement(item) for item in isiterable(IN[0])]
overridegraphics = isiterable(IN[1])
viewlist = [UnwrapElement(item) for item in isiterable(IN[2])]


def overrideelement(listofelements, override):
    listofoverrides = []
    for i in range(len(listofelements)):
        listofoverrides.append(override)
    return listofoverrides


ret = []
for i in range(len(elements)):
    ret.append(overrideelement(elements[i], overridegraphics[i]))


def makeoverrides(list1, list2, view):
    list = []
    for i in range(len(list1)):
        list.append(view.SetElementOverrides(list1[i].Id, list2[i]))
    return list


def testing(e, r, v):
    test = []
    for i in range(len(e)):
        test.append(makeoverrides(e[i], r[i], v))
    return test


try:
    errorReport = None
    TransactionManager.Instance.EnsureInTransaction(doc)

    T = []
    for item in (viewlist):
        T.append(testing(elements, ret, item))

    TransactionManager.Instance.TransactionTaskDone()
except:
    # if error accurs anywhere in the process catch it
    import traceback

    errorReport = traceback.format_exc()

# Assign your output to the OUT variable
if errorReport == None:
    OUT = elements
else:
    OUT = errorReport