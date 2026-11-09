"""Gera o index.html a partir do modelo (modelo/pagina.html) e do conteúdo (conteudo/site.json).

O conteúdo é editado pelo painel (Pages CMS); este script roda sozinho no GitHub
a cada alteração. Para rodar no computador: py gerar.py
"""
import json
import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from markupsafe import Markup, escape

PASTA = Path(__file__).parent


def src(caminho):
    # O painel grava as fotos como "/fotos/x.jpg"; o site usa caminho relativo.
    return str(caminho or "").lstrip("/")


def preco(valor):
    numero = float(valor)
    return str(int(numero)) if numero.is_integer() else f"{numero:.2f}".replace(".", ",")


def digitos(texto):
    return re.sub(r"\D", "", str(texto))


def _marcar(texto, tag):
    # No painel, **palavra** marca o trecho em destaque.
    return Markup(re.sub(r"\*\*(.+?)\*\*", rf"<{tag}>\1</{tag}>", str(escape(texto))))


def negrito(texto):
    return _marcar(texto, "b")


def destaque(texto):
    return _marcar(texto, "span")


def gerar():
    env = Environment(
        loader=FileSystemLoader(PASTA / "modelo"),
        autoescape=True,
        keep_trailing_newline=True,
        undefined=StrictUndefined,
    )
    env.filters.update(src=src, preco=preco, digitos=digitos, negrito=negrito, destaque=destaque)
    conteudo = json.loads((PASTA / "conteudo" / "site.json").read_text(encoding="utf-8"))
    html = env.get_template("pagina.html").render(**conteudo)
    (PASTA / "index.html").write_text(html, encoding="utf-8", newline="")


if __name__ == "__main__":
    gerar()
