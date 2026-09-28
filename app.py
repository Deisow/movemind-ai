import os
import json
import urllib.error
import urllib.request

from flask import Flask, render_template, request


app = Flask(__name__)


def create_health_plan(age, goal, activity_level, limitations):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return (
            "Demo-svar eftersom GROQ_API_KEY saknas:\n\n"
            f"For en person som ar {age} ar och har malet '{goal}' kan en bra start vara "
            "att promenera 10-20 minuter per dag, dricka vatten regelbundet och ta korta "
            "pauser fran stillasittande. Borja lugnt och oka stegvis.\n\n"
            "Veckoplan:\n"
            "1. Promenad 10-20 minuter, 4 dagar i veckan.\n"
            "2. Latt stretching 5 minuter efter promenad.\n"
            "3. Sov 7-8 timmar om mojligt.\n"
            "4. At mer gronsaker och protein.\n"
            "5. Kontakta vard om du har stark smarta, yrsel eller sjukdomssymtom."
        )

    prompt = f"""
Du ar en enkel och trygg AI-halsocoach. Ge allmanna tips, inte medicinsk diagnos.
Svara pa enkel svenska.

Anvandarens information:
- Alder: {age}
- Mal: {goal}
- Aktivitetsniva: {activity_level}
- Begransningar/smarta: {limitations}

Skapa:
1. En kort sammanfattning
2. En enkel veckoplan for rorelse
3. Tips for mat, vatten, somn och stress
4. En sakerhetsnotis om nar personen bor kontakta vard
"""

    request_data = json.dumps(
        {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {
                    "role": "system",
                    "content": "Du ger enkla, sakra och allmanna halsotips.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
            "max_tokens": 700,
        }
    ).encode("utf-8")

    ai_request = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=request_data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(ai_request, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))

    return data["choices"][0]["message"]["content"]


@app.route("/", methods=["GET", "POST"])
def index():
    plan = None
    error = None

    if request.method == "POST":
        age = request.form.get("age", "").strip()
        goal = request.form.get("goal", "").strip()
        activity_level = request.form.get("activity_level", "").strip()
        limitations = request.form.get("limitations", "").strip() or "Inga"

        if not age or not goal or not activity_level:
            error = "Fyll i alder, mal och aktivitetsniva."
        else:
            try:
                plan = create_health_plan(age, goal, activity_level, limitations)
            except (urllib.error.URLError, KeyError, json.JSONDecodeError):
                error = "AI-tjansten svarade inte just nu. Kontrollera API-nyckel och forsok igen."

    return render_template("index.html", plan=plan, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
