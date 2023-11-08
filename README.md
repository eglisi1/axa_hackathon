# 🦙 Dal-AI-Llama

⚡️ Getting liability assessments with ease ⚡

## 🏃🏼‍♂️ Running the app

be sure to run the code in the src/ directory

```bash
cd src/
uvicorn main:app --reload
```

Read the docs at <http://127.0.0.1:8000/docs>
Or don't, we don't care.

## 🤔 What is this?

Sascha...

## 🚀 What can this help with?

Sascha...

## 🏠 Architecture

```mermaid
flowchart TD
    A[Schadenmeldung / Schilderungen der Beteiligten / Zeugenberichte] -->|An Endpoint senden| B(Sachverhalt analysieren)
    B --> C[Relevante Gesetzartikel suchen]
    C --> D[Prüfen ob gegen Gesetzartikel verstossen wurde]
    D --> E{SLK relevant}
    E -->|Ja| F[Verhalten gegen Empfelung prüfen]
    F --> G[Haftungsquote mit Begrüdung]
    E -->|Nein| H[fa:fa-pen To be implemented]
```


## 📖 Documentation

Please, our code is self-documenting. Just read it.

## 🐍 Python Version

This project is built with Python 3.11.1.

## 💁 Contributing

As an open-source project in a rapidly developing field, we are extremely open to contributions, whether it be in the form of a new feature, improved infrastructure, or better documentation.

## 🫶🏼 Thanks

We want to thank our teacher Elena and our project lead Robin for their relentless suport and guidance.
