function registerGA() {
    for (var e = document.getElementsByTagName("form"), n = 0; n < e.length; n++)try {
        if ("post" == e[n].method) {
            var t = document.createElement("input");
            t.type = "hidden", t.name = URCHINFIELD, t.value = getUrchinFieldValue(), e[n].appendChild(t)
        }
    } catch (o) {
    }
}
!function () {
    var e = window.onload;
    void 0 === e || null == e ? window.onload = function () {
        registerGA()
    } : window.onload = function () {
        registerGA(), e()
    }
}();