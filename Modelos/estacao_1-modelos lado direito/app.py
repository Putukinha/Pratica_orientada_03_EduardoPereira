from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from database import Base, SessionLocal, engine
from models import Book, User

app = Flask(__name__)

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


@app.route("/")
def index():
    with SessionLocal() as session:
        usuarios = session.scalars(
            select(User).options(joinedload(User.books)).order_by(User.nome)
        ).unique().all()
        livros = session.scalars(
            select(Book).options(joinedload(Book.user)).order_by(Book.titulo)
        ).all()
    return render_template("index.html", usuarios=usuarios, livros=livros)


@app.route("/usuario/novo", methods=["GET", "POST"])
def form_usuario():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()

        if not nome or not email:
            return render_template("form_usuario.html", erro="Preencha nome e email.")

        with SessionLocal() as session:
            usuario_existente = session.query(User).filter_by(email=email).first()
            if usuario_existente:
                return render_template("form_usuario.html", erro="Email já cadastrado.")

            session.add(User(nome=nome, email=email))
            session.commit()

        return redirect(url_for("index"))

    return render_template("form_usuario.html")


@app.route("/livros/novo", methods=["GET", "POST"])
def form_livro():
    with SessionLocal() as session:
        usuarios = session.scalars(select(User).order_by(User.nome)).all()

        if request.method == "POST":
            titulo = request.form.get("titulo", "").strip()
            usuario_id = request.form.get("usuario_id")

            if not titulo or not usuario_id:
                return render_template("form_livro.html", usuarios=usuarios, erro="Preencha título e usuário.")

            session.add(Book(titulo=titulo, usuario_id=int(usuario_id)))
            session.commit()
            return redirect(url_for("index"))

    return render_template("form_livro.html", usuarios=usuarios)


if __name__ == "__main__":
    app.run(debug=True)