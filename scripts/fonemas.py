# -*- coding: utf-8 -*-
"""
Reglas grafema -> articulema para español, devolviendo los nombres de archivo
del set ARTICULEMAS/ (_A_, _BV_, _CH_, _CZ_, _D_, _E_, _F_, _GJ_, _GU_, _H_,
_I_, _K_, _LLY_, _L_, _M_, _N_, _Ñ_, _O_, _P_, _RR_, _R_, _S_, _T_, _U_, _X_).

Convenios del proyecto (ver CLAUDE.md):
  - B y V comparten articulema  -> BV
  - C ante e/i y Z              -> CZ      | C ante a/o/u y QU -> K
  - G ante e/i y J              -> GJ
  - G dura (ga/go/gu)           -> GU      | si la U suena (gua/guo) se añade U
  - GUE/GUI (u muda)            -> GU      (la U no se representa)
  - LL e Y consonántica         -> LLY     | Y vocálica -> I
  - RR, y R fuerte inicial o tras L/N/S -> RR ; el resto -> R
  - H es muda pero SÍ tiene articulema (boca tachada) -> H
"""

VOCALES = set("AEIOUÁÉÍÓÚÜ")
SIN_TILDE = str.maketrans("ÁÉÍÓÚÜ", "AEIOUU")


def fonemas(palabra):
    """Devuelve la lista de articulemas de una palabra española (en mayúsculas)."""
    p = palabra.upper().replace("-", "").replace(" ", "")
    out = []
    i = 0
    n = len(p)

    def sig(k=1):
        return p[i + k] if i + k < n else ""

    while i < n:
        c = p[i]
        nxt = sig()

        if c in "ÁÉÍÓÚ":
            out.append(c.translate(SIN_TILDE))
            i += 1
        elif c in "AEIOU":
            out.append(c)
            i += 1
        elif c == "Ü":
            out.append("U")
            i += 1
        elif c == "C":
            if nxt == "H":
                out.append("CH")
                i += 2
            elif nxt in "EIÉÍ":
                out.append("CZ")
                i += 1
            else:
                out.append("K")
                i += 1
        elif c == "Z":
            out.append("CZ")
            i += 1
        elif c == "Q":
            # QUE / QUI: la U es muda
            out.append("K")
            i += 2 if nxt == "U" else 1
        elif c == "K":
            out.append("K")
            i += 1
        elif c in "BV":
            out.append("BV")
            i += 1
        elif c == "W":
            out.append("BV")
            i += 1
        elif c == "G":
            if nxt in "EIÉÍ":
                out.append("GJ")
                i += 1
            elif nxt == "U" and sig(2) in "EIÉÍ":
                # GUE / GUI: u muda
                out.append("GU")
                i += 2
            elif nxt == "Ü":
                # GÜE / GÜI: la u suena
                out.append("GU")
                out.append("U")
                i += 2
            elif nxt == "U":
                # GUA / GUO: la u suena
                out.append("GU")
                out.append("U")
                i += 2
            else:
                out.append("GU")
                i += 1
        elif c == "J":
            out.append("GJ")
            i += 1
        elif c == "L":
            if nxt == "L":
                out.append("LLY")
                i += 2
            else:
                out.append("L")
                i += 1
        elif c == "Y":
            # vocálica si va sola o cierra sílaba (no seguida de vocal)
            if nxt == "" or nxt not in VOCALES:
                out.append("I")
            else:
                out.append("LLY")
            i += 1
        elif c == "R":
            if nxt == "R":
                out.append("RR")
                i += 2
            elif i == 0 or p[i - 1] in "LNS":
                out.append("RR")
                i += 1
            else:
                out.append("R")
                i += 1
        elif c == "H":
            out.append("H")
            i += 1
        elif c == "Ñ":
            out.append("Ñ")
            i += 1
        elif c == "X":
            out.append("X")
            i += 1
        elif c in "DFMNPST":
            out.append(c)
            i += 1
        else:
            out.append(c)
            i += 1

    return out


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    for w in ["ENCIMA", "DEBAJO", "DENTRO", "CHUTAR", "GUITARRA", "PÁJARO",
              "LLOVER", "AÑADIR", "QUITAR", "EXPRESAR", "IGUAL", "HABLAR"]:
        print(f"{w:<10}", fonemas(w))
