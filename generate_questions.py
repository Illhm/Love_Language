import json
import random

languages = {
    "A": "Words of Affirmation",
    "B": "Quality Time",
    "C": "Receiving Gifts",
    "D": "Acts of Service",
    "E": "Physical Touch"
}

pairs = [
    # A vs B
    ("Mendapat chat panjang dari pacar yang isinya sayang-sayangan", "A", "Nge-date berdua aja tanpa pegang HP sama sekali", "B"),
    ("Dipuji cantik/ganteng sama doi di depan temen-temen", "A", "Deep talk santai berdua dari hati ke hati", "B"),
    ("Denger langsung ucapan 'Aku sayang banget sama kamu'", "A", "Ngelakuin hobi atau aktivitas seru bareng-bareng", "B"),

    # A vs C
    ("Doi ngasih pujian tulus soal penampilan aku hari ini", "A", "Dikasih surprise kado kecil-kecilan dari pacar", "C"),
    ("Doi bilang kalau aku tuh berharga banget buat dia", "A", "Dibawain makanan atau oleh-oleh kesukaan pas dia abis main", "C"),
    ("Doi ngucapin makasih banget atas hal kecil yang aku lakuin", "A", "Dikasih kado ulang tahun yang super niat dan bermakna", "C"),

    # A vs D
    ("Pacar merhatiin dan muji usaha keras aku", "A", "Doi ngebantuin aku ngerjain tugas atau kerjaan yang numpuk", "D"),
    ("Dikasih kata-kata apresiasi yang bikin semangat", "A", "Pas aku lagi capek banget, doi yang gantiin beresin kamar/rumah", "D"),
    ("Doi ngomong betapa beruntungnya dia punya aku", "A", "Dibuatin kopi atau teh anget sama pacar", "D"),

    # A vs E
    ("Doi nyemangatin aku pakai kata-kata manis pas lagi down", "A", "Dipeluk erat dari belakang sama pacar", "E"),
    ("Ide atau pendapat aku dipuji sama doi", "A", "Doi duduk nempel-nempel pas kita lagi sebelahan", "E"),
    ("Doi muji kepribadian aku yang bikin dia jatuh cinta", "A", "Dielus-elus kepalanya sama doi", "E"),

    # B vs C
    ("Jalan-jalan seharian berdua aja keliling kota", "B", "Dikasih hadiah kecil yang random tapi unyu", "C"),
    ("Punya jadwal rutin buat pacaran (kayak movie night dsb)", "B", "Sering dikasih kejutan barang-barang lucu", "C"),
    ("Liburan atau staycation bareng pacar", "B", "Tiba-tiba dibeliin martabak atau boba kesukaan tanpa minta", "C"),

    # B vs D
    ("Doi beneran dengerin curhatan aku dengan fokus dan natep mata", "B", "Doi ngebantuin urusan aku tanpa aku harus minta tolong", "D"),
    ("Nonton series bareng berdua di kasur", "B", "Dimasakin makanan enak sama pacar", "D"),
    ("Ngasih full attention (perhatian penuh) pas aku lagi ngomong", "B", "Doi bawain barang bawaan aku pas lagi berat", "D"),

    # B vs E
    ("Ngabisin waktu ngelakuin kegiatan random bareng-bareng", "B", "Gandengan tangan sepanjang jalan pas lagi nge-date", "E"),
    ("Ngelanjutin ngobrol asik sebelum tidur", "B", "Diusap-usap punggungnya pas lagi capek", "E"),
    ("Weekend-an full berdua aja pokoknya", "B", "Nyender nyaman di bahu pacar", "E"),

    # C vs D
    ("Dapet kado spesial pas ngerayain anniversary", "C", "Doi bantuin beresin tempat aku yang berantakan", "D"),
    ("Doi bikinin kado DIY (handmade) yang effort banget", "C", "Dirawat dan dijagain sama doi pas aku lagi sakit", "D"),
    ("Dibelikan barang wishlist aku yang udah lama diidam-idamkan", "C", "Doi yang inisiatif nyuci piring abis kita makan", "D"),

    # C vs E
    ("Dapet kejutan di hari-hari spesial", "C", "Dicium keningnya sama pacar dengan lembut", "E"),
    ("Doi nginget barang favorit aku trus beliin secara random", "C", "Dipijitin kakinya pas lagi pegel-pegel", "E"),
    ("Dikasih bunga atau kado romantis", "C", "Dipeluk dengan hangat tanpa alasan", "E"),

    # D vs E
    ("Pacar nyiapin bekal atau sarapan buat aku", "D", "Tetep pegangan tangan pas lagi ngobrol serius", "E"),
    ("Doi ngebenerin barang aku yang rusak", "D", "Dikasih sentuhan sayang secara fisik secara random", "E"),
    ("Doi inisiatif manasin motor/mobil atau urusin kendaraan", "D", "Nyenderan sambil nonton atau main HP", "E"),
]

random.seed(42)
random.shuffle(pairs)

questions = []
for i, (txt1, lang1, txt2, lang2) in enumerate(pairs, 1):
    options = [
        {"id": "A", "text": txt1, "language": languages[lang1]},
        {"id": "B", "text": txt2, "language": languages[lang2]}
    ]
    random.shuffle(options)
    options[0]["id"] = "A"
    options[1]["id"] = "B"

    q = {
        "id": i,
        "options": options
    }
    questions.append(q)

with open("questions.json", "w") as f:
    json.dump(questions, f, indent=2)

print("Generated questions.json with modern/casual Indonesian")
