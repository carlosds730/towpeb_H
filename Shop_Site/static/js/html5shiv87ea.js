// HTML5 Shiv v3 | @jon_neal @afarkas @rem | MIT/GPL2 Licensed
// Uncompressed source: https://github.com/aFarkas/html5shiv
(function (a, b) {
    function f(a) {
        var c, d, e, f;
        b.documentMode > 7 ? (c = b.createElement("font"), c.setAttribute("data-html5shiv", a.nodeName.toLowerCase())) : c = b.createElement("shiv:" + a.nodeName);
        while (a.firstChild)c.appendChild(a.childNodes[0]);
        for (d = a.attributes, e = d.length, f = 0; f < e; ++f)d[f].specified && c.setAttribute(d[f].nodeName, d[f].nodeValue);
        c.style.cssText = a.style.cssText, a.parentNode.replaceChild(c, a), c.originalElement = a
    }

    function g(a) {
        var b = a.originalElement;
        while (a.childNodes.length)b.appendChild(a.childNodes[0]);
        a.parentNode.replaceChild(b, a)
    }

    function h(a, b) {
        b = b || "all";
        var c = -1, d = [], e = a.length, f, g;
        while (++c < e) {
            f = a[c], g = f.media || b;
            if (f.disabled || !/print|all/.test(g))continue;
            d.push(h(f.imports, g), f.cssText)
        }
        return d.join("")
    }

    function i(c) {
        var d = new RegExp("(^|[\\s,{}])(" + a.html5.elements.join("|") + ")", "gi"), e = c.split("{"), f = e.length, g = -1;
        while (++g < f)e[g] = e[g].split("}"), b.documentMode > 7 ? e[g][e[g].length - 1] = e[g][e[g].length - 1].replace(d, '$1font[data-html5shiv="$2"]') : e[g][e[g].length - 1] = e[g][e[g].length - 1].replace(d, "$1shiv\\:$2"), e[g] = e[g].join("}");
        return e.join("{")
    }

    var c = function (a) {
        return a.innerHTML = "<x-element></x-element>", a.childNodes.length === 1
    }(b.createElement("a")), d = function (a, b, c) {
        return b.appendChild(a), (c = (c ? c(a) : a.currentStyle).display) && b.removeChild(a) && c === "block"
    }(b.createElement("nav"), b.documentElement, a.getComputedStyle), e = {
        elements: "abbr article aside audio bdi canvas data datalist details figcaption figure footer header hgroup mark meter nav output progress section summary time video".split(" "), shivDocument: function (a) {
            a = a || b;
            if (a.documentShived)return;
            a.documentShived = !0;
            var f = a.createElement, g = a.createDocumentFragment, h = a.getElementsByTagName("head")[0], i = function (a) {
                f(a)
            };
            c || (e.elements.join(" ").replace(/\w+/g, i), a.createElement = function (a) {
                var b = f(a);
                return b.canHaveChildren && e.shivDocument(b.document), b
            }, a.createDocumentFragment = function () {
                return e.shivDocument(g())
            });
            if (!d && h) {
                var j = f("div");
                j.innerHTML = ["x<style>", "article,aside,details,figcaption,figure,footer,header,hgroup,nav,section{display:block}", "audio{display:none}", "canvas,video{display:inline-block;*display:inline;*zoom:1}", "[hidden]{display:none}audio[controls]{display:inline-block;*display:inline;*zoom:1}", "mark{background:#FF0;color:#000}", "</style>"].join(""), h.insertBefore(j.lastChild, h.firstChild)
            }
            return a
        }
    };
    e.shivDocument(b), a.html5 = e;
    if (c || !a.attachEvent)return;
    a.attachEvent("onbeforeprint", function () {
        if (a.html5.supportsXElement || !b.namespaces)return;
        b.namespaces.shiv || b.namespaces.add("shiv");
        var c = -1, d = new RegExp("^(" + a.html5.elements.join("|") + ")$", "i"), e = b.getElementsByTagName("*"), g = e.length, j, k = i(h(function (a, b) {
            var c = [], d = a.length;
            while (d)c.unshift(a[--d]);
            d = b.length;
            while (d)c.unshift(b[--d]);
            c.sort(function (a, b) {
                return a.sourceIndex - b.sourceIndex
            }), d = c.length;
            while (d)c[--d] = c[d].styleSheet;
            return c
        }(b.getElementsByTagName("style"), b.getElementsByTagName("link"))));
        while (++c < g)j = e[c], d.test(j.nodeName) && f(j);
        b.appendChild(b._shivedStyleSheet = b.createElement("style")).styleSheet.cssText = k
    }), a.attachEvent("onafterprint", function () {
        if (a.html5.supportsXElement || !b.namespaces)return;
        var c = -1, d = b.getElementsByTagName("*"), e = d.length, f;
        while (++c < e)f = d[c], f.originalElement && g(f);
        b._shivedStyleSheet && b._shivedStyleSheet.parentNode.removeChild(b._shivedStyleSheet)
    })
})(this, document)