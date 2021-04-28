"""Sciter C API interface."""
from ctypes import *

from sciter.capi.sctypes import *
from sciter.capi.scdef import *
from sciter.capi.scdom import SCDOM_RESULT, HELEMENT, HNODE, HSARCHIVE, METHOD_PARAMS, REQUEST_PARAM
from sciter.capi.scbehavior import BEHAVIOR_EVENT_PARAMS
from sciter.capi.scvalue import VALUE_RESULT, SCITER_VALUE, FLOAT_VALUE
from sciter.capi.sctiscript import HVM, tiscript_native_interface
from sciter.capi.scgraphics import LPSciterGraphicsAPI
from sciter.capi.screquest import LPSciterRequestAPI
from sciter.capi.scmsg import SCITER_X_MSG


#
# sciter-x-api.h
#
SciterClassName = SCFN(c_utf16_p)
SciterVersion = SCFN(UINT, BOOL)
SciterDataReady = SCFN(BOOL, HWINDOW, LPCWSTR, LPCBYTE, UINT)
SciterDataReadyAsync = SCFN(BOOL, HWINDOW, LPCWSTR, LPCBYTE, UINT, LPVOID)

if SCITER_WIN:
	SciterProc = SCFN(LRESULT, HWINDOW, UINT, WPARAM, LPARAM)
	SciterProcND = SCFN(LRESULT, HWINDOW, UINT, WPARAM, LPARAM, POINTER(BOOL))
else:
	SciterProc = c_void_p
	SciterProcND = c_void_p

SciterLoadFile = SCFN(BOOL, HWINDOW, LPCWSTR)
SciterLoadHtml = SCFN(BOOL, HWINDOW, LPCBYTE, UINT, LPCWSTR)
SciterSetCallback = SCFN(VOID, HWINDOW, SciterHostCallback, LPVOID)
SciterSetMasterCSS = SCFN(BOOL, LPCBYTE, UINT)
SciterAppendMasterCSS = SCFN(BOOL, LPCBYTE, UINT)
SciterSetCSS = SCFN(BOOL, HWINDOW, LPCBYTE, UINT, LPCWSTR, LPCWSTR)
SciterSetMediaType = SCFN(BOOL, HWINDOW, LPCWSTR)
SciterSetMediaVars = SCFN(BOOL, HWINDOW, POINTER(SCITER_VALUE))
SciterGetMinWidth = SCFN(UINT, HWINDOW)
SciterGetMinHeight = SCFN(UINT, HWINDOW, UINT)
SciterCall = SCFN(BOOL, HWINDOW, LPCSTR, UINT, POINTER(SCITER_VALUE), POINTER(SCITER_VALUE))
SciterEval = SCFN(BOOL, HWINDOW, LPCWSTR, UINT, POINTER(SCITER_VALUE))
SciterUpdateWindow = SCFN(VOID, HWINDOW)

if SCITER_WIN:
	SciterTranslateMessage = SCFN(BOOL, POINTER(MSG))
else:
	SciterTranslateMessage = c_void_p

SciterSetOption = SCFN(BOOL, HWINDOW, UINT, UINT_PTR)
SciterGetPPI = SCFN(VOID, HWINDOW, POINTER(UINT), POINTER(UINT))
SciterGetViewExpando = SCFN(BOOL, HWINDOW, POINTER(SCITER_VALUE))

if SCITER_WIN:
	SciterRenderD2D = SCFN(BOOL, HWINDOW, POINTER(ID2D1RenderTarget))
	SciterD2DFactory = SCFN(BOOL, POINTER(ID2D1Factory))
	SciterDWFactory = SCFN(BOOL, POINTER(IDWriteFactory))
else:
	SciterRenderD2D = c_void_p
	SciterD2DFactory = c_void_p
	SciterDWFactory = c_void_p

SciterGraphicsCaps = SCFN(BOOL, LPUINT)
SciterSetHomeURL = SCFN(BOOL, HWINDOW, LPCWSTR)

if SCITER_OSX:
	SciterCreateNSView = SCFN(HWINDOW, LPRECT)
else:
	SciterCreateNSView = c_void_p

if SCITER_LNX:
	SciterCreateWidget = SCFN(HWINDOW, LPRECT)
else:
	SciterCreateWidget = c_void_p


SciterCreateWindow = SCFN(HWINDOW, UINT, LPRECT, SciterWindowDelegate, LPVOID, HWINDOW)
SciterSetupDebugOutput = SCFN(VOID, HWINDOW, LPVOID, DEBUG_OUTPUT_PROC)
# |
# | DOM Element API
# |
Sciter_UseElement = SCFN(SCDOM_RESULT, HELEMENT)
Sciter_UnuseElement = SCFN(SCDOM_RESULT, HELEMENT)
SciterGetRootElement = SCFN(SCDOM_RESULT, HWINDOW, POINTER(HELEMENT))
SciterGetFocusElement = SCFN(SCDOM_RESULT, HWINDOW, POINTER(HELEMENT))
SciterFindElement = SCFN(SCDOM_RESULT, HWINDOW, POINT, POINTER(HELEMENT))
SciterGetChildrenCount = SCFN(SCDOM_RESULT, HELEMENT, POINTER(UINT))
SciterGetNthChild = SCFN(SCDOM_RESULT, HELEMENT, UINT, POINTER(HELEMENT))
SciterGetParentElement = SCFN(SCDOM_RESULT, HELEMENT, POINTER(HELEMENT))
SciterGetElementHtmlCB = SCFN(SCDOM_RESULT, HELEMENT, BOOL, LPCBYTE_RECEIVER, LPVOID)
SciterGetElementTextCB = SCFN(SCDOM_RESULT, HELEMENT, LPCWSTR_RECEIVER, LPVOID)
SciterSetElementText = SCFN(SCDOM_RESULT, HELEMENT, LPCWSTR, UINT)
SciterGetAttributeCount = SCFN(SCDOM_RESULT, HELEMENT, LPUINT)
SciterGetNthAttributeNameCB = SCFN(SCDOM_RESULT, HELEMENT, UINT, LPCSTR_RECEIVER, LPVOID)
SciterGetNthAttributeValueCB = SCFN(SCDOM_RESULT, HELEMENT, UINT, LPCWSTR_RECEIVER, LPVOID)
SciterGetAttributeByNameCB = SCFN(SCDOM_RESULT, HELEMENT, LPCSTR, LPCWSTR_RECEIVER, LPVOID)
SciterSetAttributeByName = SCFN(SCDOM_RESULT, HELEMENT, LPCSTR, LPCWSTR)
SciterClearAttributes = SCFN(SCDOM_RESULT, HELEMENT)
SciterGetElementIndex = SCFN(SCDOM_RESULT, HELEMENT, LPUINT)
SciterGetElementType = SCFN(SCDOM_RESULT, HELEMENT, POINTER(LPCSTR))
SciterGetElementTypeCB = SCFN(SCDOM_RESULT, HELEMENT, LPCSTR_RECEIVER, LPVOID)
SciterGetStyleAttributeCB = SCFN(SCDOM_RESULT, HELEMENT, LPCSTR, LPCWSTR_RECEIVER, LPVOID)
SciterSetStyleAttribute = SCFN(SCDOM_RESULT, HELEMENT, LPCSTR, LPCWSTR)
SciterGetElementLocation = SCFN(SCDOM_RESULT, HELEMENT, LPRECT, UINT)
SciterScrollToView = SCFN(SCDOM_RESULT, HELEMENT, UINT)
SciterUpdateElement = SCFN(SCDOM_RESULT, HELEMENT, BOOL)
SciterRefreshElementArea = SCFN(SCDOM_RESULT, HELEMENT, RECT)
SciterSetCapture = SCFN(SCDOM_RESULT, HELEMENT)
SciterReleaseCapture = SCFN(SCDOM_RESULT, HELEMENT)
SciterGetElementHwnd = SCFN(SCDOM_RESULT, HELEMENT, POINTER(HWINDOW), BOOL)
SciterCombineURL = SCFN(SCDOM_RESULT, HELEMENT, LPWSTR, UINT)
SciterSelectElements = SCFN(SCDOM_RESULT, HELEMENT, LPCSTR, SciterElementCallback, LPVOID)
SciterSelectElementsW = SCFN(SCDOM_RESULT, HELEMENT, LPCWSTR, SciterElementCallback, LPVOID)
SciterSelectParent = SCFN(SCDOM_RESULT, HELEMENT, LPCSTR, UINT, POINTER(HELEMENT))
SciterSelectParentW = SCFN(SCDOM_RESULT, HELEMENT, LPCWSTR, UINT, POINTER(HELEMENT))
SciterSetElementHtml = SCFN(SCDOM_RESULT, HELEMENT, LPCBYTE, UINT, UINT)
SciterGetElementUID = SCFN(SCDOM_RESULT, HELEMENT, POINTER(UINT))
SciterGetElementByUID = SCFN(SCDOM_RESULT, HWINDOW, UINT, POINTER(HELEMENT))
SciterShowPopup = SCFN(SCDOM_RESULT, HELEMENT, HELEMENT, UINT)
SciterShowPopupAt = SCFN(SCDOM_RESULT, HELEMENT, POINT, UINT)
SciterHidePopup = SCFN(SCDOM_RESULT, HELEMENT)
SciterGetElementState = SCFN(SCDOM_RESULT, HELEMENT, POINTER(UINT))
SciterSetElementState = SCFN(SCDOM_RESULT, HELEMENT, UINT, UINT, BOOL)
SciterCreateElement = SCFN(SCDOM_RESULT, LPCSTR, LPCWSTR, POINTER(HELEMENT))
SciterCloneElement = SCFN(SCDOM_RESULT, HELEMENT, POINTER(HELEMENT))
SciterInsertElement = SCFN(SCDOM_RESULT, HELEMENT, HELEMENT, UINT)
SciterDetachElement = SCFN(SCDOM_RESULT, HELEMENT)
SciterDeleteElement = SCFN(SCDOM_RESULT, HELEMENT)
SciterSetTimer = SCFN(SCDOM_RESULT, HELEMENT, UINT, UINT_PTR)
SciterDetachEventHandler = SCFN(SCDOM_RESULT, HELEMENT, ElementEventProc, LPVOID)
SciterAttachEventHandler = SCFN(SCDOM_RESULT, HELEMENT, ElementEventProc, LPVOID)
SciterWindowAttachEventHandler = SCFN(SCDOM_RESULT, HWINDOW, ElementEventProc, LPVOID, UINT)
SciterWindowDetachEventHandler = SCFN(SCDOM_RESULT, HWINDOW, ElementEventProc, LPVOID)
SciterSendEvent = SCFN(SCDOM_RESULT, HELEMENT, UINT, HELEMENT, UINT_PTR, POINTER(BOOL))
SciterPostEvent = SCFN(SCDOM_RESULT, HELEMENT, UINT, HELEMENT, UINT_PTR)
SciterCallBehaviorMethod = SCFN(SCDOM_RESULT, HELEMENT, POINTER(METHOD_PARAMS))
SciterRequestElementData = SCFN(SCDOM_RESULT, HELEMENT, LPCWSTR, UINT, HELEMENT)
SciterHttpRequest = SCFN(SCDOM_RESULT, HELEMENT, LPCWSTR, UINT, UINT, POINTER(REQUEST_PARAM), UINT)
SciterGetScrollInfo = SCFN(SCDOM_RESULT, HELEMENT, LPPOINT, LPRECT, LPSIZE)
SciterSetScrollPos = SCFN(SCDOM_RESULT, HELEMENT, POINT, BOOL)
SciterGetElementIntrinsicWidths = SCFN(SCDOM_RESULT, HELEMENT, POINTER(INT), POINTER(INT))
SciterGetElementIntrinsicHeight = SCFN(SCDOM_RESULT, HELEMENT, INT, POINTER(INT))
SciterIsElementVisible = SCFN(SCDOM_RESULT, HELEMENT, POINTER(BOOL))
SciterIsElementEnabled = SCFN(SCDOM_RESULT, HELEMENT, POINTER(BOOL))
SciterSortElements = SCFN(SCDOM_RESULT, HELEMENT, UINT, UINT, ELEMENT_COMPARATOR, LPVOID)
SciterSwapElements = SCFN(SCDOM_RESULT, HELEMENT, HELEMENT)
SciterTraverseUIEvent = SCFN(SCDOM_RESULT, UINT, LPVOID, POINTER(BOOL))
SciterCallScriptingMethod = SCFN(SCDOM_RESULT, HELEMENT, LPCSTR, POINTER(SCITER_VALUE), UINT, POINTER(SCITER_VALUE))
SciterCallScriptingFunction = SCFN(SCDOM_RESULT, HELEMENT, LPCSTR, POINTER(SCITER_VALUE), UINT, POINTER(SCITER_VALUE))
SciterEvalElementScript = SCFN(SCDOM_RESULT, HELEMENT, LPCWSTR, UINT, POINTER(SCITER_VALUE))
SciterAttachHwndToElement = SCFN(SCDOM_RESULT, HELEMENT, HWINDOW)
SciterControlGetType = SCFN(SCDOM_RESULT, HELEMENT, POINTER(UINT))
SciterGetValue = SCFN(SCDOM_RESULT, HELEMENT, POINTER(SCITER_VALUE))
SciterSetValue = SCFN(SCDOM_RESULT, HELEMENT, POINTER(SCITER_VALUE))
SciterGetExpando = SCFN(SCDOM_RESULT, HELEMENT, POINTER(SCITER_VALUE), BOOL)
SciterGetObject = SCFN(SCDOM_RESULT, HELEMENT, POINTER(tiscript_value), BOOL)
SciterGetElementNamespace = SCFN(SCDOM_RESULT, HELEMENT, POINTER(tiscript_value))
SciterGetHighlightedElement = SCFN(SCDOM_RESULT, HWINDOW, POINTER(HELEMENT))
SciterSetHighlightedElement = SCFN(SCDOM_RESULT, HWINDOW, HELEMENT)
# |
# | DOM Node API
# |
SciterNodeAddRef = SCFN(SCDOM_RESULT, HNODE)
SciterNodeRelease = SCFN(SCDOM_RESULT, HNODE)
SciterNodeCastFromElement = SCFN(SCDOM_RESULT, HELEMENT, POINTER(HNODE))
SciterNodeCastToElement = SCFN(SCDOM_RESULT, HNODE, POINTER(HELEMENT))
SciterNodeFirstChild = SCFN(SCDOM_RESULT, HNODE, POINTER(HNODE))
SciterNodeLastChild = SCFN(SCDOM_RESULT, HNODE, POINTER(HNODE))
SciterNodeNextSibling = SCFN(SCDOM_RESULT, HNODE, POINTER(HNODE))
SciterNodePrevSibling = SCFN(SCDOM_RESULT, HNODE, POINTER(HNODE))
SciterNodeParent = SCFN(SCDOM_RESULT, HNODE, POINTER(HELEMENT))
SciterNodeNthChild = SCFN(SCDOM_RESULT, HNODE, UINT, POINTER(HNODE))
SciterNodeChildrenCount = SCFN(SCDOM_RESULT, HNODE, POINTER(UINT))
SciterNodeType = SCFN(SCDOM_RESULT, HNODE, POINTER(UINT))
SciterNodeGetText = SCFN(SCDOM_RESULT, HNODE, LPCWSTR_RECEIVER, LPVOID)
SciterNodeSetText = SCFN(SCDOM_RESULT, HNODE, LPCWSTR, UINT)
SciterNodeInsert = SCFN(SCDOM_RESULT, HNODE, UINT, HNODE)
SciterNodeRemove = SCFN(SCDOM_RESULT, HNODE, BOOL)
SciterCreateTextNode = SCFN(SCDOM_RESULT, LPCWSTR, UINT, POINTER(HNODE))
SciterCreateCommentNode = SCFN(SCDOM_RESULT, LPCWSTR, UINT, POINTER(HNODE))
# |
# | Value API
# |
ValueInit = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE))
ValueClear = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE))
ValueCompare = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), POINTER(SCITER_VALUE))
ValueCopy = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), POINTER(SCITER_VALUE))
ValueIsolate = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE))
ValueType = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), POINTER(UINT), POINTER(UINT))
ValueStringData = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), POINTER(LPCWSTR), POINTER(UINT))
ValueStringDataSet = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), LPCWSTR, UINT, UINT)
ValueIntData = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), POINTER(INT))
ValueIntDataSet = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), INT, UINT, UINT)
ValueInt64Data = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), POINTER(INT64))
ValueInt64DataSet = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), INT64, UINT, UINT)
ValueFloatData = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), POINTER(FLOAT_VALUE))
ValueFloatDataSet = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), FLOAT_VALUE, UINT, UINT)
ValueBinaryData = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), POINTER(LPCBYTE), POINTER(UINT))
ValueBinaryDataSet = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), LPCBYTE, UINT, UINT, UINT)
ValueElementsCount = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), POINTER(INT))
ValueNthElementValue = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), INT, POINTER(SCITER_VALUE))
ValueNthElementValueSet = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), INT, POINTER(SCITER_VALUE))
ValueNthElementKey = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), INT, POINTER(SCITER_VALUE))
ValueEnumElements = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), KeyValueCallback, LPVOID)
ValueSetValueToKey = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), POINTER(SCITER_VALUE), POINTER(SCITER_VALUE))
ValueGetValueOfKey = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), POINTER(SCITER_VALUE), POINTER(SCITER_VALUE))
ValueToString = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), UINT)
ValueFromString = SCFN(UINT, POINTER(SCITER_VALUE), LPCWSTR, UINT, UINT)
ValueInvoke = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), POINTER(SCITER_VALUE), UINT, POINTER(SCITER_VALUE), POINTER(SCITER_VALUE), LPCWSTR)
ValueNativeFunctorSet = SCFN(VALUE_RESULT, POINTER(SCITER_VALUE), NATIVE_FUNCTOR_INVOKE, NATIVE_FUNCTOR_RELEASE, POINTER(VOID))
ValueIsNativeFunctor = SCFN(BOOL, POINTER(SCITER_VALUE))

# tiscript VM API
TIScriptAPI = SCFN(POINTER(tiscript_native_interface))

SciterGetVM = SCFN(HVM, HWINDOW)

Sciter_v2V = SCFN(BOOL, HVM, tiscript_value, POINTER(SCITER_VALUE), BOOL)
Sciter_V2v = SCFN(BOOL, HVM, POINTER(SCITER_VALUE), POINTER(tiscript_value))

# sciter resources archive
SciterOpenArchive = SCFN(HSARCHIVE, LPCBYTE, UINT)
SciterGetArchiveItem = SCFN(BOOL, HSARCHIVE, LPCWSTR, POINTER(LPCBYTE), POINTER(UINT))
SciterCloseArchive = SCFN(BOOL, HSARCHIVE)

SciterFireEvent = SCFN(SCDOM_RESULT, POINTER(BEHAVIOR_EVENT_PARAMS), BOOL, POINTER(BOOL))

SciterGetCallbackParam = SCFN(LPVOID, HWINDOW)
SciterPostCallback = SCFN(UINT_PTR, HWINDOW, UINT_PTR, UINT_PTR, UINT)

# Graphics API
GetSciterGraphicsAPI = SCFN(LPSciterGraphicsAPI)
GetSciterRequestAPI = SCFN(LPSciterRequestAPI)

SciterProcX = SCFN(BOOL, HWINDOW, POINTER(SCITER_X_MSG))


# DirectX API
if SCITER_WIN:
	SciterCreateOnDirectXWindow = SCFN(BOOL, HWINDOW, POINTER(IDXGISwapChain))
	SciterRenderOnDirectXWindow = SCFN(BOOL, HWINDOW, HELEMENT, BOOL)
	SciterRenderOnDirectXTexture = SCFN(BOOL, HWINDOW, HELEMENT, POINTER(IDXGISurface))
else:
	SciterCreateOnDirectXWindow = c_void_p
	SciterRenderOnDirectXWindow = c_void_p
	SciterRenderOnDirectXTexture = c_void_p


class ISciterAPI(Structure):
    """Sciter API functions."""
    sciter_api = [
        "SciterClassName",
        "SciterVersion",
        "SciterDataReady",
        "SciterDataReadyAsync",
        # ifdef WINDOWS
        "SciterProc",
        "SciterProcND",
        # endif
        "SciterLoadFile",

        "SciterLoadHtml",
        "SciterSetCallback",
        "SciterSetMasterCSS",
        "SciterAppendMasterCSS",
        "SciterSetCSS",
        "SciterSetMediaType",
        "SciterSetMediaVars",
        "SciterGetMinWidth",
        "SciterGetMinHeight",
        "SciterCall",
        "SciterEval",
        "SciterUpdateWindow",
        # ifdef WINDOWS
        "SciterTranslateMessage",
        # endif
        "SciterSetOption",
        "SciterGetPPI",
        "SciterGetViewExpando",
        # ifdef WINDOWS
        "SciterRenderD2D",
        "SciterD2DFactory",
        "SciterDWFactory",
        # endif
        "SciterGraphicsCaps",
        "SciterSetHomeURL",
        # if defined(OSX)
        "SciterCreateNSView",
        # endif
        # if defined(LINUX)
        "SciterCreateWidget",           # since 3.2.0.1
        # endif

        "SciterCreateWindow",
        "SciterSetupDebugOutput",
        # |
        # | DOM Element API
        # |
        "Sciter_UseElement",
        "Sciter_UnuseElement",
        "SciterGetRootElement",
        "SciterGetFocusElement",
        "SciterFindElement",
        "SciterGetChildrenCount",
        "SciterGetNthChild",
        "SciterGetParentElement",
        "SciterGetElementHtmlCB",
        "SciterGetElementTextCB",
        "SciterSetElementText",
        "SciterGetAttributeCount",
        "SciterGetNthAttributeNameCB",
        "SciterGetNthAttributeValueCB",
        "SciterGetAttributeByNameCB",
        "SciterSetAttributeByName",
        "SciterClearAttributes",
        "SciterGetElementIndex",
        "SciterGetElementType",
        "SciterGetElementTypeCB",
        "SciterGetStyleAttributeCB",
        "SciterSetStyleAttribute",
        "SciterGetElementLocation",
        "SciterScrollToView",
        "SciterUpdateElement",
        "SciterRefreshElementArea",
        "SciterSetCapture",
        "SciterReleaseCapture",
        "SciterGetElementHwnd",
        "SciterCombineURL",
        "SciterSelectElements",
        "SciterSelectElementsW",
        "SciterSelectParent",
        "SciterSelectParentW",
        "SciterSetElementHtml",
        "SciterGetElementUID",
        "SciterGetElementByUID",
        "SciterShowPopup",
        "SciterShowPopupAt",
        "SciterHidePopup",
        "SciterGetElementState",
        "SciterSetElementState",
        "SciterCreateElement",
        "SciterCloneElement",
        "SciterInsertElement",
        "SciterDetachElement",
        "SciterDeleteElement",
        "SciterSetTimer",
        "SciterDetachEventHandler",
        "SciterAttachEventHandler",
        "SciterWindowAttachEventHandler",
        "SciterWindowDetachEventHandler",
        "SciterSendEvent",
        "SciterPostEvent",
        "SciterCallBehaviorMethod",
        "SciterRequestElementData",
        "SciterHttpRequest",
        "SciterGetScrollInfo",
        "SciterSetScrollPos",
        "SciterGetElementIntrinsicWidths",
        "SciterGetElementIntrinsicHeight",
        "SciterIsElementVisible",
        "SciterIsElementEnabled",
        "SciterSortElements",
        "SciterSwapElements",
        "SciterTraverseUIEvent",
        "SciterCallScriptingMethod",
        "SciterCallScriptingFunction",
        "SciterEvalElementScript",
        "SciterAttachHwndToElement",
        "SciterControlGetType",
        "SciterGetValue",
        "SciterSetValue",
        "SciterGetExpando",
        "SciterGetObject",
        "SciterGetElementNamespace",
        "SciterGetHighlightedElement",
        "SciterSetHighlightedElement",
        # |
        # | DOM Node API
        # |
        "SciterNodeAddRef",
        "SciterNodeRelease",
        "SciterNodeCastFromElement",
        "SciterNodeCastToElement",
        "SciterNodeFirstChild",
        "SciterNodeLastChild",
        "SciterNodeNextSibling",
        "SciterNodePrevSibling",
        "SciterNodeParent",
        "SciterNodeNthChild",
        "SciterNodeChildrenCount",
        "SciterNodeType",
        "SciterNodeGetText",
        "SciterNodeSetText",
        "SciterNodeInsert",
        "SciterNodeRemove",
        "SciterCreateTextNode",
        "SciterCreateCommentNode",
        # |
        # | Value API
        # |
        "ValueInit",
        "ValueClear",
        "ValueCompare",
        "ValueCopy",
        "ValueIsolate",
        "ValueType",
        "ValueStringData",
        "ValueStringDataSet",
        "ValueIntData",
        "ValueIntDataSet",
        "ValueInt64Data",
        "ValueInt64DataSet",
        "ValueFloatData",
        "ValueFloatDataSet",
        "ValueBinaryData",
        "ValueBinaryDataSet",
        "ValueElementsCount",
        "ValueNthElementValue",
        "ValueNthElementValueSet",
        "ValueNthElementKey",
        "ValueEnumElements",
        "ValueSetValueToKey",
        "ValueGetValueOfKey",
        "ValueToString",
        "ValueFromString",
        "ValueInvoke",
        "ValueNativeFunctorSet",
        "ValueIsNativeFunctor",

        # tiscript VM API
        "TIScriptAPI",

        "SciterGetVM",

        # since 3.1.0.12
        "Sciter_v2V",
        "Sciter_V2v",

        # since 3.1.0.18
        "SciterOpenArchive",
        "SciterGetArchiveItem",
        "SciterCloseArchive",

        # since 3.2.0.0
        "SciterFireEvent",

        "SciterGetCallbackParam",
        "SciterPostCallback",

        # since 3.3.1.0
        "GetSciterGraphicsAPI",

        # since 3.3.1.6 and it brokes compatibility with DX functions below
        "GetSciterRequestAPI",

        # ifdef WINDOWS
        # since 3.3.1.4
        "SciterCreateOnDirectXWindow",
        "SciterRenderOnDirectXWindow",
        "SciterRenderOnDirectXTexture",

        # since 4.0.0.0
        "SciterProcX",

        # since 4.4.2.14
        "SciterAtomValue",
        "SciterAtomNameCB",

        # since 4.4.2.16
        "SciterSetGlobalAsset",

        # since 4.4.4.7
        "SciterGetElementAsset",

        # since 4.4.4.6 (yet disabled)
        "SciterSetVariable",
        "SciterGetVariable",

        # since 4.4.5.4
        "SciterElementUnwrap",
        "SciterElementWrap",
        "SciterNodeUnwrap",
        "SciterNodeWrap",

        ]
    # END OF ISciterAPI.

    def _make_fields(names):
        #
        # Patch the ISciterAPI structure.
        #
        # This works by conditionally defining the function types first in the global scope,
        # then defining *all* the possible API names in a single array,
        # and filtering the array eliminating those that don't exist in the global context.
        #
        context = globals()
        fields = [(name, context[name]) for name in names if name in context]
        fields.insert(0, ("version", UINT))
        return fields

    _fields_ = _make_fields(sciter_api)
# end

SCITER_LOAD_ERROR = """%s%s was not found in PATH.
  Please verify that Sciter SDK is installed and its binaries (SDK/bin, bin.osx or bin.gtk) are available in the path.""" % (SCITER_DLL_NAME, SCITER_DLL_EXT)


def SciterAPI():
    """Bind Sciter API."""
    if hasattr(SciterAPI, "_api"):
        return SciterAPI._api

    import sys
    import ctypes

    scdll = None
    errors = []

    if SCITER_WIN:
        # load 4.x version by default
        # note: somehow `ctypes.WinDLL(dllname)` does not work in Python 3.8 anymore;
        # now we use the full path if found.
        import ctypes.util
        try:
            dll = ctypes.util.find_library(SCITER_DLL_NAME)
            if not dll:
                dll = SCITER_DLL_NAME
            scdll = ctypes.WinDLL(dll)
        except OSError as e:
            errors.append("'%s': %s" % (dll, str(e)))

            # try to find 3.x version
            try:
                dllname = "sciter64.dll" if sys.maxsize > 2**32 else "sciter32.dll"
                dll = ctypes.util.find_library(dllname)
                if not dll:
                    dll = dllname
                scdll = ctypes.WinDLL(dll)
            except OSError as e:
                errors.append("'%s': %s" % (dll, str(e)))

    else:
        # same behavior for OSX & Linux
        def find_sciter(dllname):
            import ctypes.util
            dllfile = dllname + SCITER_DLL_EXT
            dllpath = ctypes.util.find_library(dllname)
            if not dllpath:
                # try $LD_LIBRARY_PATH
                def find_in_path(dllname, envname):
                    import os
                    if envname in os.environ:
                        for directory in os.environ[envname].split(os.pathsep):
                            fname = os.path.join(directory, dllname)
                            if os.path.isfile(fname):
                                return fname
                    return None

                dllpath = find_in_path(dllfile, 'DYLD_LIBRARY_PATH' if SCITER_OSX else 'LD_LIBRARY_PATH')

                # try $PATH
                if not dllpath:
                    dllpath = find_in_path(dllfile, 'PATH')

            if not dllpath:
                # last chance: try to load .so
                dllpath = dllfile
            try:
                RTLD_LAZY = 1
                return ctypes.CDLL(dllpath, ctypes.RTLD_LOCAL | RTLD_LAZY)
            except OSError as e:
                errors.append(str(e))
                return None

        # try default name (4.1.4+)
        scdll = find_sciter(SCITER_DLL_NAME)

        if SCITER_LNX and scdll is None:
            # try the old name
            import sys
            scdll = find_sciter("libsciter-gtk-64" if sys.maxsize > 2**32 else "libsciter-gtk-32")

    if not scdll:
        raise ImportError(SCITER_LOAD_ERROR + "\n" + "\n".join(errors))

    scdll.SciterAPI.restype = POINTER(ISciterAPI)
    SciterAPI._api = scdll.SciterAPI().contents
    return SciterAPI._api
# end


if __name__ == "__main__":
    print("loading sciter dll: ")

    scapi = SciterAPI()

    apiver = scapi.version
    clsname = scapi.SciterClassName()
    high = scapi.SciterVersion(True)
    low = scapi.SciterVersion(False)
    version = (high >> 16, high & 0xFFFF, low >> 16, low & 0xFFFF)

    print("sciter version %s, api v%d, class name: %s" % ('.'.join(map(str, version)), apiver, clsname))
    scapi = None
