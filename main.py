import json
import uuid
import urllib.parse
from typing import Optional, Dict
import uvicorn

from fastapi import FastAPI, Request, Form, HTTPException, Cookie, Response, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Inisialisasi folder untuk file HTML
templates = Jinja2Templates(directory="templates")

# Mount folder static (opsional, jika kamu punya file CSS/JS di folder 'static')
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Load questions
try:
    with open("questions.json", "r") as f:
        QUESTIONS = json.load(f)
except FileNotFoundError:
    print("Warning: File questions.json tidak ditemukan. Buat file tersebut agar aplikasi berjalan normal.")
    QUESTIONS = []

# In-memory session store (for simple double-submission prevention)
# In production, use Redis or a proper database
sessions: Dict[str, bool] = {}

def get_session_id(request: Request, response: Response):
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
        response.set_cookie(key="session_id", value=session_id, httponly=True)
    return session_id

@app.get("/", response_class=HTMLResponse)
async def read_instructions(request: Request, response: Response):
    session_id = get_session_id(request, response)
    # If session has already submitted, clear it to allow retaking, or just let them
    # For now, we'll allow retaking by navigating to root
    if session_id in sessions:
        del sessions[session_id]

    return templates.TemplateResponse(request=request, name="index.html", context={"questions": QUESTIONS})

@app.post("/submit", response_class=HTMLResponse)
async def submit_test(request: Request, response: Response):
    session_id = request.cookies.get("session_id")
    if not session_id:
        return RedirectResponse(url="/", status_code=303)

    if session_id in sessions and sessions[session_id]:
        # Simple double submission check
        return templates.TemplateResponse(request=request, name="error.html", context={"message": "Anda sudah mengisi tes ini."})

    form_data = await request.form()

    # 1. Validation and Scoring
    scores = {
        "Words of Affirmation": 0,
        "Acts of Service": 0,
        "Receiving Gifts": 0,
        "Quality Time": 0,
        "Physical Touch": 0
    }

    total_questions = len(QUESTIONS)
    if total_questions == 0:
        raise HTTPException(status_code=500, detail="Data pertanyaan kosong.")

    for q in QUESTIONS:
        q_id = str(q["id"])
        if q_id not in form_data:
            raise HTTPException(status_code=400, detail=f"Pertanyaan {q_id} wajib diisi.")

        selected_option_id = form_data[q_id]

        # Find the language for the selected option
        selected_language = None
        for opt in q["options"]:
            if str(opt["id"]) == str(selected_option_id):
                selected_language = opt["language"]
                break

        if not selected_language:
             raise HTTPException(status_code=400, detail=f"Pilihan untuk pertanyaan {q_id} tidak valid.")

        scores[selected_language] += 1

    # 3. Identify Primary Love Language
    primary_language = max(scores, key=scores.get)
    max_score = scores[primary_language]

    # Check for ties
    tied_languages = [lang for lang, score in scores.items() if score == max_score]

    if len(tied_languages) > 1:
         primary_display = " & ".join(tied_languages)
    else:
         primary_display = primary_language

    # Mark session as submitted
    sessions[session_id] = True

    # Calculate percentages and sort descending for the UI
    ranked_scores = sorted(
        [{"language": lang, "score": score, "percentage": int((score / total_questions) * 100)} for lang, score in scores.items()],
        key=lambda x: x["score"],
        reverse=True
    )

    # 4. Generate Share Link (WhatsApp)
    wa_message = f"Saya baru saja mengikuti tes Love Language For Couples!\n\nBahasa Cinta Primer saya adalah: *{primary_display}*!\n\nRincian Skor:\n"
    for item in ranked_scores:
        wa_message += f"- {item['language']}: {item['percentage']}%\n"
    wa_message += f"\nCari tahu bahasa cintamu juga!"

    encoded_message = urllib.parse.quote(wa_message)
    whatsapp_link = f"https://wa.me/?text={encoded_message}"

    return templates.TemplateResponse(request=request, name="result.html", context={
        "ranked_scores": ranked_scores,
        "primary_language": primary_display,
        "primary_percentage": ranked_scores[0]["percentage"],
        "whatsapp_link": whatsapp_link,
        "total_questions": total_questions
    })

# --- BLOK INI UNTUK MENJALANKAN SERVER DI PORT 8000 ---
if __name__ == "__main__":
    print("Menjalankan server di http://127.0.0.1:8080")
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
