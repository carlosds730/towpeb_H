/* Modernizr 2.6.1 (Custom Build) | MIT & BSD
 * Build: http://modernizr.com/download/#-input
 */
;
window.Modernizr = function (a, b, c) {
    function t(a) {
        i.cssText = a
    }

    function u(a, b) {
        return t(prefixes.join(a + ";") + (b || ""))
    }

    function v(a, b) {
        return typeof a === b
    }

    function w(a, b) {
        return !!~("" + a).indexOf(b)
    }

    function x(a, b, d) {
        for (var e in a) {
            var f = b[a[e]];
            if (f !== c)return d === !1 ? a[e] : v(f, "function") ? f.bind(d || b) : f
        }
        return !1
    }

    function y() {
        e.input = function (c) {
            for (var d = 0, e = c.length; d < e; d++)n[c[d]] = c[d]in j;
            return n.list && (n.list = !!b.createElement("datalist") && !!a.HTMLDataListElement), n
        }("autocomplete autofocus list placeholder max min multiple pattern required step".split(" "))
    }

    var d = "2.6.1", e = {}, f = b.documentElement, g = "modernizr", h = b.createElement(g), i = h.style, j = b.createElement("input"), k = {}.toString, l = {}, m = {}, n = {}, o = [], p = o.slice, q, r = {}.hasOwnProperty, s;
    !v(r, "undefined") && !v(r.call, "undefined") ? s = function (a, b) {
        return r.call(a, b)
    } : s = function (a, b) {
        return b in a && v(a.constructor.prototype[b], "undefined")
    }, Function.prototype.bind || (Function.prototype.bind = function (b) {
        var c = this;
        if (typeof c != "function")throw new TypeError;
        var d = p.call(arguments, 1), e = function () {
            if (this instanceof e) {
                var a = function () {
                };
                a.prototype = c.prototype;
                var f = new a, g = c.apply(f, d.concat(p.call(arguments)));
                return Object(g) === g ? g : f
            }
            return c.apply(b, d.concat(p.call(arguments)))
        };
        return e
    });
    for (var z in l)s(l, z) && (q = z.toLowerCase(), e[q] = l[z](), o.push((e[q] ? "" : "no-") + q));
    return e.input || y(), e.addTest = function (a, b) {
        if (typeof a == "object")for (var d in a)s(a, d) && e.addTest(d, a[d]); else {
            a = a.toLowerCase();
            if (e[a] !== c)return e;
            b = typeof b == "function" ? b() : b, enableClasses && (f.className += " " + (b ? "" : "no-") + a), e[a] = b
        }
        return e
    }, t(""), h = j = null, e._version = d, e
}(this, this.document);