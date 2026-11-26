from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for
import sqlite3

app = Flask(__name__)

# Configuração do Banco de Dados SQLite
DB_NAME = "signos.db"


def init_db():
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            data_nascimento TEXT NOT NULL,
            signo TEXT NOT NULL,
            elemento TEXT NOT NULL,
            data_consulta TEXT NOT NULL
        )
    """)
  conn.commit()
  conn.close()


# Função para descobrir o signo baseado no dia e mês
def obter_signo(dia, mes):
  if (mes == 3 and dia >= 21) or (mes == 4 and dia <= 19):
    return (
        "Áries",
        "Fogo",
        "Corajoso, enérgico, pioneiro e impulsivo.",
        "Marte",
    )
  elif (mes == 4 and dia >= 20) or (mes == 5 and dia <= 20):
    return (
        "Touro",
        "Terra",
        "Confiável, paciente, determinado e perseverante.",
        "Vênus",
    )
  elif (mes == 5 and dia >= 21) or (mes == 6 and dia <= 20):
    return (
        "Gêmeos",
        "Ar",
        "Adaptável, versátil, comunicativo e curioso.",
        "Mercúrio",
    )
  elif (mes == 6 and dia >= 21) or (mes == 7 and dia <= 22):
    return (
        "Câncer",
        "Água",
        "Emocional, intuitivo, protetor e carinhoso.",
        "Lua",
    )
  elif (mes == 7 and dia >= 23) or (mes == 8 and dia <= 22):
    return "Leão", "Fogo", "Generoso, caloroso, criativo e entusiasta.", "Sol"
  elif (mes == 8 and dia >= 23) or (mes == 9 and dia <= 22):
    return (
        "Virgem",
        "Terra",
        "Analítico, inteligente, prestativo e organizado.",
        "Mercúrio",
    )
  elif (mes == 9 and dia >= 23) or (mes == 10 and dia <= 22):
    return "Libra", "Ar", "Diplomático, justo, sociável e cooperativo.", "Vênus"
  elif (mes == 10 and dia >= 23) or (mes == 11 and dia <= 21):
    return "Escorpião", "Água", "Passional, decidido, magnético e intenso.", "Plutão"
  elif (mes == 11 and dia >= 22) or (mes == 12 and dia <= 21):
    return (
        "Sagitário",
        "Fogo",
        "Otimista, amante da liberdade, divertido e sincero.",
        "Júpiter",
    )
  elif (mes == 12 and dia >= 22) or (mes == 1/1 and dia <= 1 / 19):  # Ajustado
    return "Capricórnio", "Terra", "Prático, prudente, ambicioso e disciplinado.", "Saturno"
  elif (mes == 1 and dia >= 20) or (mes == 2 and dia <= 18):
    return "Aquário", "Ar", "Original, independente, humanitário e visionário.", "Urano"
  else:
    return (
        "Peixes",
        "Água",
        "Imaginativo, sensível, compassivo e altruísta.",
        "Netuno",
    )


# Rota Principal (Formulário e Resultado)
@app.route("/", methods=["GET", "POST"])
def index():
  resultado = None
  if request.method == "POST":
    nome = request.form.get("nome")
    data_str = request.form.get("data_nascimento")

    # Converter string da data para objeto datetime
    data_dt = datetime.strptime(data_str, "%Y-%m-%d")
    dia = data_dt.day
    mes = data_dt.month

    signo, elemento, caracteristicas, planeta = obter_signo(dia, mes)
    data_consulta = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Salvar no Banco de Dados
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
            INSERT INTO historico (nome, data_nascimento, signo, elemento, data_consulta)
            VALUES (?, ?, ?, ?, ?)
        """,
        (
            nome,
            data_dt.strftime("%d/%m/%Y"),
            f"{signo} ({elemento})",
            caracteristicas,
            data_consulta,
        ),
    )
    conn.commit()
    conn.close()

    resultado = {
        "nome": nome,
        "signo": signo,
        "elemento": elemento,
        "caracteristicas": caracteristicas,
        "planeta": planeta,
    }

  return render_template("index.html", resultado=resultado)


# Rota do Histórico
@app.route("/historico")
def historico():
  conn = sqlite3.connect(DB_NAME)
  cursor = conn.cursor()
  cursor.execute(
      "SELECT nome, data_nascimento, signo, elemento, data_consulta FROM historico"
      " ORDER BY id DESC"
  )
  registros = cursor.fetchall()
  conn.close()
  return render_template("historico.html", registros=registros)


if __name__ == "__main__":
  init_db()
  app.run(debug=True)