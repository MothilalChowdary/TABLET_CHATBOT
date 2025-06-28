from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)
df = pd.read_csv('processed_medicine.csv')

def get_drug_info(query):
    query = query.strip().lower()
    query_words = query.split()

    if len(query_words) == 1:
        matches = df[df["name"].str.lower().str.split().str[0] == query]
    else:
        matches = df[df["name"].str.lower().str.startswith(query)]

    if matches.empty:
        return "Drug not found."

    responses = []
    for _, row in matches.iterrows():
        lines = [f"<strong>Name:</strong> {row['name']}"]

        if pd.notna(row['Consolidated_Side_Effects']) and row['Consolidated_Side_Effects'].strip():
            lines.append(f"<strong>Side Effects:</strong> {row['Consolidated_Side_Effects']}")

        uses = [row[f"use{i}"] for i in range(5)
                if pd.notna(row[f"use{i}"]) and str(row[f"use{i}"]).strip()]
        if uses:
            lines.append(f"<strong>Uses:</strong> {', '.join(uses)}")

        if pd.notna(row['Therapeutic Class']) and row['Therapeutic Class'].strip():
            lines.append(f"<strong>Therapeutic Class:</strong> {row['Therapeutic Class']}")

        if pd.notna(row['Action Class']) and row['Action Class'].strip():
            lines.append(f"<strong>Action Class:</strong> {row['Action Class']}")

        responses.append("<br>".join(lines))

    return "<hr>".join(responses)

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    reply = get_drug_info(user_input)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)