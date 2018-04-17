// This is just a sample script. Paste your real code (javascript or HTML) here.
/**
 *
 *   AceGrammar
 *   @version: 4.2.1
 *
 *   Transform a grammar specification in JSON format, into an ACE syntax-highlight parser mode
 *   https://github.com/foo123/ace-grammar
 *   https://github.com/foo123/editor-grammar
 *
 **/
! function(e, t, n) {
    "use strict";
    "object" == typeof module && module.exports ? (module.$deps = module.$deps || {}) && (module.exports = module.$deps[t] = n.call(e)) : "function" == typeof define && define.amd && "function" == typeo
    f require && "function" == typeof require.specified && require.specified(t) ? define(t, ["module"], function(t) {
            return n.moduleUri = t.uri, n.call(e)
        }) : t in e || (e[t] = n.call(e) || 1) && "function" == typeof define && define.amd &&
        define(function() {
            return e[t]
        })
}(this, "AceGrammar", function() {
        "use strict";

        function e(e) {
            var t = 0;
            return null === e ? t = jt : !0 === e || !1 === e || e instanceof Boolean ? t = It : vt === e ? t = Tt : (t = Vt[Ot.call(e)] || Dt, t = Rt === t |
                |
                e instanceof Number ? isNaN(e) ? Ft : isFinite(e) ? Rt : Ct : At === t || e instanceof String ? 1 === e.length ? Nt : At : zt === t || e instanceof Array ? zt : Wt === t || e instanceof RegExp ? Wt : Gt === t || e instanceof Date ? Gt : Bt === t || e instanc eof Function ? Bt : Ut === t ? Ut : Dt), t
        }

        function t(e, t, n, o) {
            var r, l, a, i, s, c, u = e.length;
            if (arguments.length < 4 && (o = u - 1), 0 > o && (o += u), arguments.length < 3 && (n = 0), n > o) return [];
            if (n === o) return [t(e[n], n, n, o)];
            for (a = o - n + 1, i = 15 & a, s = 1 & i, c = new Array(a), s && (c[0] = t(e[n], n, n, o)), r = s; i > r; r += 2) l = n + r, c[r] = t(e[l], l, n, o), c[r + 1] = t(e[l + 1], l + 1, n, o);
            for (r = i; a > r; r += 16) l = n + r, c[r] = t(e[l], l, n, o), c[r + 1] = t(e[l + 1], l + 1, n, o), c[r + 2] = t(e[l + 2], l + 2, n, o), c[r + 3] = t(e[l + 3], l + 3, n, o), c[r + 4] = t(e[l + 4], l + 4, n, o), c[r + 5] = t(e[l + 5], l + 5, n, o), c[r + 6] = t(e[l + 6], l + 6, n, o), c[r + 7] = t(e[l + 7], l + 7, n, o), c[r + 8] = t(e[l + 8], l + 8, n, o), c[r + 9] = t(e[l + 9], l + 9, n, o), c[r + 10] = t(e[l + 10], l + 10, n, o),
                c[r + 11] = t(e[l + 11], l + 11, n, o), c[r + 12] = t(e[l + 12], l + 12, n, o), c[r + 13] = t(e[l + 13], l + 13, n, o), c[r + 14] = t(e[l + 14], l + 14, n, o), c[r + 15] = t(e[l + 15], l + 15, n, o);
            return c
        }

        function n(e, t, n, o, r) {
            var l, a, i, s, c, u = e.length,
                p = n;
            if (ar guments.length < 5 && (r = u - 1), 0 > r && (r += u), arguments.length < 4 && (o = 0), o > r) return p;
            if (o === r) return t(p, e[o], o);
            for (i = r - o + 1, s = 15 & i, c = 1 & s, c && (p = t(p, e[o], o)), l = c; s > l; l += 2) a = o + l, p = t(t(p, e[a], a), e[a + 1], a + 1);
            for (l = s; i >
                l; l += 16) a = o + l, p = t(t(t(t(t(t(t(t(t(t(t(t(t(t(t(t(p, e[a], a), e[a + 1], a + 1), e[a + 2], a + 2), e[a + 3], a + 3), e[a + 4], a + 4), e[a + 5], a + 5), e[a + 6], a + 6), e[a + 7], a + 7), e[a + 8], a + 8), e[a + 9], a + 9), e[a + 10], a + 10), e[a + 11], a + 11), e[a + 12], a +
                12), e[a + 13], a + 13), e[a + 14], a + 14), e[a + 15], a + 15);
            return p
        }

        function o(e, t, n, o) {
            if (t > n) return o;
            if (t === n) return e(t, o, t, n), o;
            var r, l, a = n - t + 1,
                i = 15 & a,
                s = 1 & i;
            for (s && e(t, o, t, n), r = s; i > r; r += 2) l = t + r, e(l, o, t, n), e(++l, o,
                t, n);
            for (r = i; a > r; r += 16) l = t + r, e(l, o, t, n), e(++l, o, t, n), e(++l, o, t, n), e(++l, o, t, n), e(++l, o, t, n), e(++l, o, t, n), e(++l, o, t, n), e(++l, o, t, n), e(++l, o, t, n), e(++l, o, t, n), e(++l, o, t, n), e(++l, o, t, n), e(++l, o, t, n), e(++l, o, t, n), e(++l, o, t, n), e(++l, o, t, n);
            return o
        }

        function r(t, n) {
            var o, l, a, i, s = e(t),
                c = 0;
            if (Rt === e(n) ? n > 0 ? (c = n, n = !0) : n = !1 : n = !1 !== n, Ut === s) {
                l = {};
                for (a in t) St.call(t, a) && Et.call(t, a) && (o = e(t[a]), Ut === o ? l[a] = n ? r(t[a], c >
                    0 ? c - 1 : n) : t[a] : zt === o ? l[a] = n ? r(t[a], c > 0 ? c - 1 : n) : t[a].slice() : Gt === o ? l[a] = new Date(t[a]) : At & o ? l[a] = t[a].slice() : Rt & o ? l[a] = 0 + t[a] : l[a] = t[a])
            } else if (zt === s)
                for (i = t.length, l = new Array(i), a = 0; i > a; a++) o = e(t[a]),
                    Ut === o ? l[a] = n ? r(t[a], c > 0 ? c - 1 : n) : t[a] : zt === o ? l[a] = n ? r(t[a], c > 0 ? c - 1 : n) : t[a].slice() : Gt === o ? l[a] = new Date(t[a]) : At & o ? l[a] = t[a].slice() : Rt & o ? l[a] = 0 + t[a] : l[a] = t[a];
            else l = Gt === s ? new Date(t) : At & s ? t.slice() : Rt & s ?
                0 + t : t;
            return l
        }

        function l() {
            var t, n, o, a, i, s, c, u, p, f, m = arguments,
                h = m.length;
            if (1 > h) return null;
            for (n = r(m[0]), o = 1; h > o; o++)
                if (t = m[o])
                    for (a in t)
                        if (St.call(t, a) && Et.call(t, a))
                            if (St.call(n, a) && Et.call(n, a)) {
                                if (
                                    p = e(n[a]), f = e(t[a]), Ut === p && Ut === f) n[a] = l(n[a], t[a]);
                                else if (zt === p && zt === f) {
                                    if (c = n[a], u = t[a], s = u.length, !s) continue;
                                    if (c.length)
                                        for (i = 0; s > i; i++) 0 > c.indexOf(u[i]) && c.push(u[i]);
                                    else n[a] = u.slice()
                                }
                            } else n[
                                a] = r(t[a]);
            return n
        }

        function a() {
            return !0
        }

        function i(t, n) {
            return n || zt !== e(t) ? [t] : t
        }

        function s(t, n) {
            return t = i(t), (n || zt !== e(t[0])) && (t = [t]), t
        }

        function c(t, n) {
            return At & e(n) && At & e(t) && n.length && n.length <= t
                .length && n === t.substr(0, n.length)
        }

        function u(e, t, n) {
            return n ? e[t] = vt : delete e[t], e
        }

        function p(e) {
            return (e || "id_") + ++nn
        }

        function f(e) {
            return (e || "uuid") + "_" + ++nn + "_" + (new Date).getTime()
        }

        function m() {
            var t, n, o, r, l, a, i = arguments,
                s = i.length;
            for (t = i[0] || {}, l = 1; s > l; l++)
                if (n = i[l], Ut === e(n))
                    for (r in n) St.call(n, r) && Et.call(n, r) && (o = n[r], a = e(o), Rt & a ? t[r] = 0 + o : Gt & a ? t[r] = new Date(o) : Ht & a ? t[r] = o.slice() : t[r] = o);
            return
            t
        }

        function h(e, t) {
            var n, o = arguments.length,
                r = "constructor";
            return 0 === o ? (e = Object, t = {}) : 1 === o ? (t = e || {}, e = Object) : (e = e || Object, t = t || {}), St.call(t, r) || (t[r] = function() {}), n = t[r], delete t[r], n[yt] = m(xt(e[yt]), t), n[yt][r] = n, n
        }

        function d(e) {
            return e.replace(on, "\\$1")
        }

        function k(e, t) {
            t = t || {
                l: 0,
                x: 0,
                i: 0,
                g: 0
            };
            var e = new RegExp(e, (t.g ? "g" : "") + (t.i ? "i" : ""));
            return e.xflags = t, e
        }

        function g(e, t, n, o) {
            var r, l = e.pos || 0,
                a = e
                .length,
                i = t.length,
                s = "";
            if (n)
                if (o)
                    for (; a > l;)
                        if (r = !1, n === e[qt](l) && (r = !0, l += 1), t === e.substr(l, i)) {
                            if (l += i, !r) break;
                            s += t
                        } else s += e[qt](l++);
            else
                for (; a > l;)
                    if (r = !1, n === e[qt](l) && (r = !0, l += 1, s += n), t === e.substr(
                            l, i)) {
                        if (l += i, !r) break;
                        s += t
                    } else s += e[qt](l++);
            else
                for (; a > l;) {
                    if (t === e.substr(l, i)) {
                        l += i;
                        break
                    }
                    s += e[qt](l++)
                }
            return e.pos = l, s
        }

        function $(t, n, o, r) {
            var l, a, i, s, c, u = !0 === o ? 0 : 1,
                p = r ? "\\" : "$",
                f = r ? 92 : 36;
            for (At & e(n) && (r && (n = d(n)), n = [n, n, n], u = 0), a = t.length, c = "", l = 0; a > l;) i = t[qt](l), a > l + 1 && p === i ? (s = t.charCodeAt(l + 1), f === s ? (c += p, l += 2) : s >= 48 && 57 >= s ? (c += n[u + s - 48] || "", l += 2) : (c += i, l += 1)) : (c += i, l += 1);
            return c
        }

        function v(t,
            n, o, r) {
            if (!t || (Rt | Wt) & e(t)) return t;
            var l, a = n ? n.length || 0 : 0,
                i = "",
                s = {
                    g: 0,
                    i: 0,
                    x: 0,
                    l: 0
                };
            if (At & e(r) ? i = r : r && (i = ln), a && t.substr(0, a) === n) {
                var c, u, p, l, f, m = t.substr(a),
                    h = m[qt](0);
                for (l = m.length; l-- && (f = m[qt](l), h!
                        ==
                        f);) "i" === f.toLowerCase() ? s.i = 1 : "x" === f.toLowerCase() ? s.x = 1 : "l" === f.toLowerCase() && (s.l = 1);
                return c = m.substring(1, l), "^" === c.charAt(0) ? (s.l = 1, u = "^(" + c.slice(1) + ")") : u = "^(" + c + ")", p = u, (s.x || s.l || s.i) && (u = (
                    s.l ? "l" : "") + (s.x ? "x" : "") + (s.i ? "i" : "") + "::" + u), o[u] || (p = k(p, s), o[u] = p), o[u]
            }
            return i ? (p = u = "^(" + d(t) + ")" + i, o[u] || (p = k(p, s), o[u] = p), o[u]) : t
        }

        function y(n, o, r) {
            var l, a = "";
            return At & e(o) ? a = o : o && (a = ln), l = t(n.sort(Xt), d).join("|"), [k("^(" + l + ")" + a, {
                l: 0,
                x: 0,
                i: r ? 1 : 0
            }), 1]
        }

        function b(t, n, o, r) {
            var l = e(n);
            if (Rt === l) return n;
            if (r[t]) return r[t];
            o = o || 0;
            var a, i = 0;
            return n && n.isCharList && (i = 1, u(n, "isCharList")), a = jt === l ? new F(Ne, t, n, jt, o) : Nt === l ? new F(Ne, t, n, Nt, o) : Kt & l ? new F(Ne, t, n, Wt, o) : At & l ? new F(Ne, t, n, i ? Pt : At, o) : n, r[t] = a
        }

        function x(t, n, o, r, l, a, s, u) {
            if (s[t]) return s[t];
            var p, f, m, h, d, k, g, $ = 0,
                w = 0,
                _ = 1,
                M = At & e(r) ? !0 : !!r;
            if (p = i(n), m = p.length, 1 === m) g = b(t, v(p[0], o, a, r), 0, s);
            else if (m > 1) {
                for (h = (m >>> 1) + 1, f = 0; h >= f; f++) d = e(p[f]), k = e(p[m - 1 - f]), Nt === d && Nt === k || (_ = 0), zt & d || zt & k ? $ = 1 : (Wt & d || Wt & k || c(p[f], o) || c(p[m - 1 - f], o)) && (w = 1);
                if (_ && !M) p = p
                    .slice().join(""), p.isCharList = 1, g = b(t, p, 0, s);
                else if (!M || $ || w)
                    if ($ || w) {
                        for (f = 0; m > f; f++) zt & e(p[f]) ? p[f] = x(t + "_" + f, p[f], o, r, l, a, s) : p[f] = b(t + "_" + f, v(p[f], o, a), f, s);
                        g = m > 1 ? new F(Pe, t, p) : p[0]
                    } else {
                        for (u && (u.key words = i(n).slice()), p = p.sort(Xt), f = 0; m > f; f++) p[f] = b(t + "_" + f, v(p[f], o, a), f, s);
                        g = m > 1 ? new F(Pe, t, p) : p[0]
                    }
                else u && (u.keywords = i(n).slice()), g = b(t, y(p, r, l), 0, s)
            }
            return s[t] = g
        }

        function w(t, n, r, l, a) {
            if (a[t]) retur
            n a[t];
            var i = s(n),
                u = [],
                p = [];
            return o(function(n) {
                var o, s, f, m;
                o = b(t + "_0_" + n, v(i[n][0], r, l), n, a), i[n].length > 1 ? (f = c(i[n][1], r), m = f && an.test(i[n][1]), Wt !== o.ptype || At !== e(i[n][1]) || !m && f ? s = b(t + "_1_" + n, v(i[n][
                    1
                ], r, l), n, a) : m ? (s = new String(i[n][1]), s.regex_pattern = r) : s = i[n][1]) : s = o, u.push(o), p.push(s)
            }, 0, i.length - 1), a[t] = new F(ze, t, [u, p])
        }

        function _(e, t) {
            var n = s(e.tokens.slice());
            o(function(e) {
                var o = n[e][0],
                    r = n[e].length > 1 ? n[e][1] : n[e][0],
                    l = n[e].length > 2 ? n[e][2] : "";
                null === r ? (t.line = t.line || [], t.line.push(o)) : (t.block = t.block || [], t.block.push([o, r, l]))
            }, 0, n.length - 1)
        }

        function M(e, n, o, r) {
            var l = e.meta || o,
                a = !(!e.caseI nsesitive && !e.ci),
                i = t(n, function(e) {
                    return {
                        word: e,
                        meta: l,
                        ci: a
                    }
                });
            return r.autocomplete = (r.autocomplete || []).concat(i), i
        }

        function q(t) {
            t.Lex || (t.Lex = {}), t.Syntax || (t.Syntax = {});
            var n, o, r, a, i, s, c, p, f, m, h, d = t
                .Lex,
                k = t.Syntax,
                g = [d, k],
                $ = g.length;
            for (h = 0; $ > h;) {
                m = g[h++];
                for (r in m) St.call(m, r) && (n = r.split(":"), o = n[1] && Jt(n[1]).length ? Jt(n[1]) : null, n = Jt(n[0]), n.length || (n = r, o = null), n !== r && (m[n] = m[r], u(m, r), o && (o = o[M t](), a = m[n], i = e(a), Ut === i ? m[n].type || (m[n].type = o) : (m[n] = {
                                        type: o
                                    }, "error" === o ? (m[n].type = "action", m[n].error = a) : "nop" === o ? (m[n].type = "action", m[n].nop = !0) : "group" === o ? (m[n].type = "sequence", m[n].tokens = a) : "
                                    action "===o&&At===i?m[n][a]=!0:m[n].tokens=a))),d===m&&(Qt&e(m[n])&&(m[n]={type:"
                                    simple ",tokens:m[n]}),a=m[n],a.type&&(p=a.type=a.type[Mt](),"
                                    line - block "===p?(a.type="
                                    block ",a.multiline=!1,a.escape=!1):"
                                    es caped - line - block "===p?(a.type="
                                    block ",a.multiline=!1,a.escape="\\
                                    "):"
                                    escaped - block "===p&&(a.type="
                                    block ",a.multiline=!0,a.escape="\\
                                    "))))}m=d;for(n in m)if(St.call(m,n))for(a=m[n];a.extend;)s=a.extend,u(a,
                                    "extend"), c = d[s], c && (Qt & e(c) && (c = d[s] = {
                                    type: "simple",
                                    tokens: c
                                }), a = l(c, a)); m = d;
                                for (n in m) St.call(m, n) && (a = m[n], a.type ? (p = a.type = a.type[Mt](), "action" === p ? a.options = a.options || {} : "line-block" === p ? (a.type = "b
                                            lock ",a.multiline=!1,a.escape=!1):"
                                            escaped - line - block "===p?(a.type="
                                            block ",a.multiline=!1,a.escape="\\
                                            "):"
                                            escaped - block "===p&&(a.type="
                                            block ",a.multiline=!0,a.escape="\\
                                            ")):a["
                                            escaped - line - block "]?(a.type=
                                            "block", a.multiline = !1, a.escape || (a.escape = "\\"), a.tokens = a["escaped-line-block"], u(a, "escaped-line-block")) : a["escaped-block"] ? (a.type = "block", a.multiline = !0, a.escape || (a.escape = "\\"), a.tokens = a["escaped-
                                            block "],u(a,"
                                            escaped - block ")):a["
                                            line - block "]?(a.type="
                                            block ",a.multiline=!1,a.escape=!1,a.tokens=a["
                                            line - block "],u(a,"
                                            line - block ")):a.comment?(a.type="
                                            comment ",a.escape=!1,a.tokens=a.comment,u(a,"
                                            comment "
                                        )) : a.block ? (a.type = "block", a.tokens = a.block, u(a, "block")) : a.simple ? (a.type = "simple", a.tokens = a.simple, u(a, "simple")) : a.nop ? (a.type = "action", a.options = a.options || {}, a.action = ["nop", a.nop, a.options], a.nop = !0) : a.error ? (a.type = "action", a.options = a.options || {}, a.action = ["error", a.error, a.options], u(a, "error")) : St.call(a, "hypercontext") ? (a.type = "action", a.options = a.options || {}, a.action = [a.hypercontext ? "hyperconte
                                            xt - start ":"
                                            hypercontext - end ",a.hypercontext,a.options],u(a,"
                                            hypercontext ")):St.call(a,"
                                            context ")?(a.type="
                                            action ",a.options=a.options||{},a.action=[a.context?"
                                            context - start ":"
                                            context - end ",a.context,a.optio
                                            ns
                                        ], u(a, "context")) : a.indent ? (a.type = "action", a.options = a.options || {}, a.action = ["indent", a.indent, a.options], u(a, "indent")) : a.outdent ? (a.type = "action", a.options = a.options || {}, a.action = ["outdent", a.outdent,
                                            a.options
                                        ], u(a, "outdent")) : a.define ? (a.type = "action", a.options = a.options || {}, a.action = ["define", At & e(a.define) ? ["*", a.define] : a.define, a.options], u(a, "define")) : a.undefine ? (a.type = "action", a.options = a.opti ons || {}, a.action = ["undefine", At & e(a.undefine) ? ["*", a.undefine] : a.undefine, a.options], u(a, "undefine")) : a.defined ? (a.type = "action", a.options = a.options || {}, a.action = ["defined", At & e(a.defined) ? ["*", a.defined] :
                                            a.defined, a.options
                                        ], u(a, "defined")) : a.notdefined ? (a.type = "action", a.options = a.options || {}, a.action = ["notdefined", At & e(a.notdefined) ? ["*", a.notdefined] : a.notdefined, a.options], u(a, "notdefined")) : a.unique ? (
                                            a.type = "action", a.options = a.options || {}, a.action = ["unique", At & e(a.unique) ? ["*", a.unique] : a.unique, a.options], u(a, "unique")) : a.push ? (a.type = "action", a.options = a.options || {}, a.action = ["push", a.push, a.options], u(a, "push")) : St.call(a, "pop") ? (a.type = "action", a.options = a.options || {}, a.action = ["pop", a.pop, a.options], u(a, "pop")) : a.type = "simple", "action" === a.type ? (a.options = a.options || {}, a.options["in-context"] = !(!a
                                            .options["in-context"] && !a["in-context"]), a.options["in-hypercontext"] = !(!a.options["in-hypercontext"] && !a["in-hypercontext"]), a.options.ci = a.ci = !!(a.options.caseInsesitive || a.options.ci || a.caseInsesitive |
                                            |
                                            a.ci), a.options.autocomplete = !(!a.options.autocomplete && !a.autocomplete), a.options.mode = a.options.mode || a.mode) : "block" === a.type || "comment" === a.type ? (a.multiline = St.call(a, "multiline") ? !!a.multiline : !0, At &
                                            e(a.escape) || (a.escape = !1)) : "simple" === a.type && (a.meta = a.autocomplete && At & e(a.meta) ? a.meta : null, a.ci = !(!a.caseInsesitive && !a.ci))); m = k;
                                        for (n in m) St.call(m, n) && (a = m[n], Ut !== e(a) || a.type ? a.type && (p = a.type =
                                                    a.type[Mt](), "group" === p && a.match ? (i = e(a.match), At & i ? (f = a.match[Mt](), "alternation" === f || "either" === f ? (a.type = "alternation", u(a, "match")) : "sequence" === f || "all" === f ? (a.type = "sequence", u(a, "match")) : "zerooro
                                                        ne "===f?(a.type="
                                                        zeroOrOne ",u(a,"
                                                        match ")):"
                                                        zeroormore "===f?(a.type="
                                                        zeroOrMore ",u(a,"
                                                        match ")):"
                                                        oneormore "===f?(a.type="
                                                        oneOrMore ",u(a,"
                                                        match ")):(a.type="
                                                        sequence ",u(a,"
                                                        match "))):zt&i&&(a.type="
                                                        repeat ",a.re
                                                        peat = a.match, u(a, "match"))) : "either" === p ? a.type = "alternation" : "all" === p ? a.type = "sequence" : "lookahead" === p ? a.type = "positiveLookahead" : "grammar" === p && (a.type = "subgrammar"), "subgrammar" !== a.type || a.tokens || (a
                                                        .tokens = n)) : a.ngram || a["n-gram"] ? (a.type = "ngram", a.tokens = a.ngram || a["n-gram"], a["n-gram"] ? u(a, "n-gram") : u(a, "ngram")) : a.sequence || a.all ? (a.type = "sequence", a.tokens = a.sequence || a.all, a.all ? u(a, "all") : u(a, "
                                                        sequence ")):a.alternation||a.either?(a.type="
                                                        alternation ",a.tokens=a.alternation||a.either,a.either?u(a,"
                                                        either "):u(a,"
                                                        alternation ")):a.zeroOrOne?(a.type="
                                                        zeroOrOne ",a.tokens=a.zeroOrOne,u(a,"
                                                        zeroOrOne ")):
                                                        a.zeroOrMore ? (a.type = "zeroOrMore", a.tokens = a.zeroOrMore, u(a, "zeroOrMore")) : a.oneOrMore ? (a.type = "oneOrMore", a.tokens = a.oneOrMore, u(a, "oneOrMore")) : a.positiveLookahead || a.lookahead ? (a.type = "positiveLookahead
                                                            ",a.tokens=a.positiveLookahead||a.lookahead,a.lookahead?u(a,"
                                                            lookahead "):u(a,"
                                                            positiveLookahead ")):a.negativeLookahead?(a.type="
                                                            negativeLookahead ",a.tokens=a.negativeLookahead,u(a,"
                                                            negativeLookahead ")):(a.
                                                            subgrammar || a.grammar) && (a.type = "subgrammar", a.tokens = a.subgrammar || a.grammar, a.subgrammar ? u(a, "subgrammar") : u(a, "grammar")));
                                                    return t
                                                }

                                                function O(e, t) {
                                                    t = t || [];
                                                    var n, o, r, l;
                                                    for (n = e.ctx; n;) {
                                                        for (o = n.val.symb; o;) l = o.val[1], l[7] && t.push({
                                                            word: l[5],
                                                            meta: (l[6] || "") + " at (" + (l[0] + 1) + "," + (l[1] + 1) + ")",
                                                            ci: l[8],
                                                            token: l[6],
                                                            pos: [l[0] + 1, l[1] + 1, l[2] + 1, l[3] + 1]
                                                        }), o = o.prev;
                                                        o = n.val.tabl;
                                                        for (r in o) St.call(o, r) && o[r][7] && (l = o[r], t.push({
                                                            word: l[5],
                                                            meta: (l[6] || "") + " at (" + (l[0] + 1) + "," + (l[1] + 1) + ")",
                                                            ci: l[8],
                                                            token: l[6],
                                                            pos: [l[0] + 1, l[1] + 1, l[2] + 1, l[3] + 1]
                                                        }));
                                                        n = n.prev
                                                    }
                                                    for (n = e.hctx; n;) {
                                                        for (o = n.val.symb; o;) l = o.val[1], l[7] && t.push({
                                                            word: l[5],
                                                            meta: (l[6] || "") + " at (" + (l[0] + 1) + "," + (l[1] + 1) + ")",
                                                            ci: l[8],
                                                            token: l[6],
                                                            pos: [l[0] + 1, l[1] + 1, l[2] + 1, l[3] + 1]
                                                        }), o = o.prev;
                                                        o = n.val.tabl;
                                                        for (r in o) St.call(o, r) && o[r][7] && (l = o[r], t.push({
                                                                word: l[5],
                                                                meta: (l[6] || "") + "
                                                                at("+(l[0]+1)+", "+(l[1]+1)+")
                                                                ",ci:l[8],token:l[6],pos:[l[0]+1,l[1]+1,l[2]+1,l[3]+1]}));n=n.prev}for(o=e.symb;o;)l=o.val[1],l[7]&&t.push({word:l[5],meta:(l[6]||"
                                                                ")+"
                                                                at("+(l[0]+1)+", "+(l[1]+1)+")
                                                                ",ci:l[8
                                                            ], token: l[6], pos: [l[0] + 1, l[1] + 1, l[2] + 1, l[3] + 1]
                                                        }), o = o.prev;
                                                        o = e.tabl;
                                                        for (r in o) St.call(o, r) && o[r][7] && (l = o[r], t.push({
                                                            word: l[5],
                                                            meta: (l[6] || "") + " at (" + (l[0] + 1) + "," + (l[1] + 1) + ")",
                                                            ci: l[8],
                                                            token: l[6],
                                                            pos: [l[0] +
                                                                1, l[1] + 1, l[2] + 1, l[3] + 1
                                                            ]
                                                        }));
                                                        return t
                                                    }

                                                    function S(t, n, o, r) {
                                                        if (o = o || {}, n = n || [], !t || !t.length) return n;
                                                        var l, a, i, s, c, u, p;
                                                        for (l = 0, a = t.length; a > l; l++)
                                                            if (c = t[l])
                                                                if (Qe === c.type) {
                                                                    if (r && r.length && c.name)
                                                                        for (i = r.leng th - 1; i >= 0; i--) r[i].token && (c.name === r[i].token || c.name.length > r[i].token.length && c.name.slice(0, r[i].token.length) === r[i].token || c.name.length < r[i].token.length && c.name === r[i].token.slice(0, c.name.length)) &&
                                                                            (r[i].meta = c.name + " at (" + r[i].pos[0] + "," + r[i].pos[1] + ")", n.push(r[i]), r.splice(i, 1));
                                                                    if (c.autocompletions)
                                                                        for (i = 0, s = c.autocompletions.length; s > i; i++) p = c.autocompletions[i], St.call(o, "w_" + p.word) || (n.pus h(p), o["w_" + p.word] = 1);
                                                                    else At === c.token.ptype && At & e(c.token.pattern) && c.token.pattern.length > 1 && (St.call(o, "w_" + c.token.pattern) || (n.push({
                                                                        word: "" + c.token.pattern,
                                                                        meta: c.name,
                                                                        ci: !!c.ci
                                                                    }), o["w_" + c.token.pa ttern] = 1))
                                                                } else if (Je === c.type) S(c.token, n, o, r);
                                                        else if (ct & c.type) {
                                                            i = 0, s = c.token.length;
                                                            do S([u = c.token[i++]], n, o, r); while (s > i && (et & u.type && 1 > u.min || Ue === u.type))
                                                        } else et & c.type && S([c.token[0]], n, o, r);
                                                        retu
                                                        rn n
                                                    }

                                                    function E(t, n, o, r) {
                                                        for (var l; At & e(l = n[t] || o[t]);) t = l;
                                                        return r ? t : n[t] || o[t] || t
                                                    }

                                                    function L(e, t) {
                                                        return e.length > 1 ? o(t ? function(t, n) {
                                                            var o = n[n.length - 1],
                                                                r = e[t];
                                                            o === r || n.push(r)
                                                        } : function(t, n) {
                                                            var o = n[n.length - 1],
                                                                r = e[t];
                                                            sn.test(r) && sn.test(o) && o === r || n.push(r)
                                                        }, 1, e.length - 1, [e[0]]) : e
                                                    }

                                                    function D(n, o, l) {
                                                        var a, i, s, c, u, p, f, m, h, d, $, v, y, b, x, w = !1;
                                                        if (x = n.modifier ? n.modifier : null, m = new String(Jt(n)), m.pos = 0, 1 === m.length) v = "" + n, o[v] || l[v] || (o[v] = {
                                                            type: "simple",
                                                            tokens: n
                                                        }), n = v;
                                                        else {
                                                            for (a = [], i = [], s = "", y = []; m.pos < m.length;)
                                                                if (h = m[qt](m.pos++), rn.test(h))
                                                                    if (s.length && (w ? (i.length && ($ = i[i.length - 1], v = $ + "." + s, p = o[v] || l[v],
                                                                            p || (f = E($, o, l), l[v] = At & e(f) ? new String(f) : r(f), l[v].modifier = s), i[i.length - 1] = v), w = !1) : "0" === s ? (o[gt] || (o[gt] = {
                                                                            type: "simple",
                                                                            tokens: 0
                                                                        }), i.push(gt)) : "^^" === s ? (o[ft] || (o[ft] = {
                                                                            type: "simple",
                                                                            tokens: Be
                                                                        }), i.push(ft)) : "^^1" === s ? (o[mt] || (o[mt] = {
                                                                            type: "simple",
                                                                            tokens: We
                                                                        }), i.push(mt)) : "^" === s ? (o[ht] || (o[ht] = {
                                                                            type: "simple",
                                                                            tokens: Ye
                                                                        }), i.push(ht)) : "$" === s ? (o[dt] || (o[dt] = {
                                                                            type: "simple",
                                                                            tokens: Ge
                                                                        }), i.push(dt)) : (o[s] || l[s] ||
                                                                            (o[s] = {
                                                                                type: "simple",
                                                                                tokens: s
                                                                            }), i.push(s)), s = ""), "." === h) i.length && m.pos < m.length && !rn.test(m[qt](m.pos)) ? w = !0 : s += h;
                                                                    else if ('"' === h || "'" === h) c = g(m, h, "\\", 1), c.length ? (v = "" + c, o[v] || (o[v] = {
                                                                type: "simple",
                                                                to
                                                                kens: c
                                                            }), i.push(v)) : (o[$t] || (o[$t] = {
                                                                type: "simple",
                                                                tokens: ""
                                                            }), i.push($t));
                                                            else if ("[" === h) h = m[qt](m.pos + 1), "^" === h ? m.pos++ : h = "", c = g(m, "]", "\\", 0), v = "[" + h + c + "]", o[v] || (o[v] = {
                                                                type: "simple",
                                                                tokens: k("^([" + h + c +
                                                                    "])")
                                                            }), i.push(v);
                                                            else {
                                                                if ("]" === h) {
                                                                    s += h;
                                                                    continue
                                                                }
                                                                if ("/" === h) c = g(m, h, "\\", 0), d = "", c.length && (m.pos < m.length && "i" === m[qt](m.pos) && (m.pos++, d = "i"), v = "/" + c + "/" + d, o[v] || (o[v] = {
                                                                    type: "simple",
                                                                    tokens: k("^(" + c + ")", {
                                                                        l: 0,
                                                                        x: 0,
                                                                        i: "i" === d
                                                                    })
                                                                }), i.push(v));
                                                                else if ("*" === h || "+" === h || "?" === h) i.length ? ($ = i[i.length - 1], v = "" + $ + h, l[v] || (l[v] = {
                                                                        type: "*" === h ? "zeroOrMore" : "+" === h ? "oneOrMore" : "zeroOrOne",
                                                                        tokens: [$]
                                                                    }), i[i.length - 1] = v) :
                                                                    s += h;
                                                                else if ("{" === h) i.length ? (u = g(m, "}", 0, 0), u = t(u.split(","), Jt), u[0].length ? u[0] = parseInt(u[0], 10) || 0 : u[0] = 0, 0 > u[0] && (u[0] = 0), 2 > u.length ? u.push(u[0]) : u[1].length ? u[1] = parseInt(u[1], 10) || Lt : u[1] = Lt, 0 > u[1] && (u[1] = 0), $ = i[i.length - 1], v = "" + $ + ["{", u[0], ",", isFinite(u[1]) ? u[1] : "", "}"].join(""), l[v] || (l[v] = {
                                                                    type: "repeat",
                                                                    repeat: [u[0], u[1]],
                                                                    tokens: [$]
                                                                }), i[i.length - 1] = v) : s += h;
                                                                else {
                                                                    if ("}" === h) {
                                                                        s += h;
                                                                        continue
                                                                    }
                                                                    "&" === h
                                                                        ||
                                                                        "!" === h ? i.length ? ($ = i[i.length - 1], v = "" + $ + h, l[v] || (l[v] = {
                                                                            type: "!" === h ? "negativeLookahead" : "positiveLookahead",
                                                                            tokens: [$]
                                                                        }), i[i.length - 1] = v) : s += h : "|" === h ? (w = !1, i = L(i), i.length > 1 ? (v = "" + i.join(" "), l[v] || (l[
                                                                            v] = {
                                                                            type: "sequence",
                                                                            tokens: i
                                                                        }), a.push(v)) : i.length ? a.push(i[0]) : s += h, i = []) : "(" === h ? (y.push([i, a, s]), i = [], a = [], s = "") : ")" === h && (i = L(i), i.length > 1 ? (v = "" + i.join(" "), l[v] || (l[v] = {
                                                                            type: "sequence",
                                                                            tokens: i
                                                                        }), a.p ush(v)) : i.length && a.push(i[0]), i = [], a = L(a, 1), a.length > 1 ? (v = "" + a.join(" | "), l[v] || (l[v] = {
                                                                            type: "alternation",
                                                                            tokens: a
                                                                        })) : a.length && (v = a[0]), a = [], b = y.pop(), i = b[0], a = b[1], s = b[2], $ = v, v = "(" + $ + ")", l[v] || (l[v] = r(
                                                                            E($, o, l))), i.push(v))
                                                                }
                                                            } else s += h;
                                                            s.length && (w ? (i.length && ($ = i[i.length - 1], v = $ + "." + s, p = o[v] || l[v], p || (f = E($, o, l), l[v] = At & e(f) ? new String(f) : r(f), l[v].modifier = s), i[i.length - 1] = v), w = !1) : "0" === s ? (o[gt] || (o[gt] = {
                                                                type: "simple",
                                                                tokens: 0
                                                            }), i.push(gt)) : "^^" === s ? (o[ft] || (o[ft] = {
                                                                type: "simple",
                                                                tokens: Be
                                                            }), i.push(ft)) : "^^1" === s ? (o[mt] || (o[mt] = {
                                                                type: "simple",
                                                                tokens: We
                                                            }), i.push(mt)) : "^" === s ? (o[ht] || (o[ht] = {
                                                                type: "simple",
                                                                tokens: Ye
                                                            }), i.push(ht)) : "$" === s ? (o[dt] || (o[dt] = {
                                                                type: "simple",
                                                                tokens: Ge
                                                            }), i.push(dt)) : (o[s] || l[s] || (o[s] = {
                                                                type: "simple",
                                                                tokens: s
                                                            }), i.push(s))), s = "", i = L(i), i.length > 1 ? (v = "" + i.join(" "), l[v] || (l[v] = {
                                                                type: "se
                                                                quence ",tokens:i}),a.push(v)):i.length&&a.push(i[0]),i=[],a=L(a,1),a.length>1?(v="
                                                                "+a.join(" | "),l[v]||(l[v]={type:"
                                                                alternation ",tokens:a}),n=v):a.length&&(n=a[0]),a=[]}return x&&(o[n]||l[n])&&((o[n]||l[n
                                                            ]).modifier = x), n
                                                        }

                                                        function T(r, l, a, c, u, p, f, m, h, d, k) {
                                                            var g, $, v, y, b, q, O, S = null,
                                                                L = null,
                                                                j = null;
                                                            if (Be === r || We === r || Ye === r || Ge === r) return new N(r, Be === r ? ft : We === r ? $T_FBNL$ : Ye === r ? ht : dt, r, L);
                                                            if (!1 === r || 0 === r) retur
                                                            n new N(He, gt, 0, L);
                                                            if ("" === r) return new N(Ke, $t, "", L);
                                                            if (null === r) return new N(Qe, kt, jt, L, j);
                                                            if (zt & e(r) && (v = r, r = "NGRAM_" + v.join("_"), c[r] || (c[r] = {
                                                                    type: "ngram",
                                                                    tokens: v
                                                                })), r = "" + r, m[r]) return m[r];
                                                            if (b = E(r, a, c), At & e(b) && (b = D(b, a, c), b = a[b] || c[b] || null), !b) return null;
                                                            if (g = b.type ? pt[b.type[Mt]().replace(tn, "")] || Qe : Qe, L = b.msg || null, j = b.modifier || null, $ = b.tokens, Qe & g) {
                                                                if (Be === $ || We === $ || Ye === $ || Ge === $ || !1 === $ || 0 ===
                                                                    $) return S = new N($ || He, r, $ || 0, L), m[r] = S, S;
                                                                if ("" === $) return S = new N(Ke, r, "", L), m[r] = S, S;
                                                                if (null === $) return S = new N(Qe, r, jt, L, j), m[r] = S, S;
                                                                if (!$) return null
                                                            }
                                                            if (Ue & g) b.options = b.options || {}, b.options["in-co
                                                                ntext "]=!(!b.options[" in -context "]&&!b[" in -context "]),b.options[" in -hypercontext "]=!(!b.options[" in -hypercontext "]&&!b[" in -hypercontext "]),b.options.ci=b.ci=!!(b.options.caseInsesitive||b.options.ci||b.cas
                                                                eInsesitive || b.ci), b.options.autocomplete = !(!b.options.autocomplete && !b.autocomplete), b.options.mode = b.options.mode || b.mode, St.call(b, "action") ? "nop" === b.action[0] ? b.action[0] = _e : "error" === b.action[0] ? b.ac
                                                            tion[0] = Me: "context-start" === b.action[0] ? b.action[0] = De : "context-end" === b.action[0] ? b.action[0] = Te : "hypercontext-start" === b.action[0] ? b.action[0] = je : "hypercontext-end" === b.action[0] ? b.action[0] = Re : "push" == = b.action[0] ? b.action[0] = Ce : "pop" === b.action[0] ? b.action[0] = Fe : "define" === b.action[0] ? b.action[0] = qe : "undefine" === b.action[0] ? b.action[0] = Oe : "defined" === b.action[0] ? b.action[0] = Se : "notdefined" === b.action[0
