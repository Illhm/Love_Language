import json

languages = {
    "A": "Words of Affirmation",
    "B": "Quality Time",
    "C": "Receiving Gifts",
    "D": "Acts of Service",
    "E": "Physical Touch"
}

pairs = [
    # A vs B
    ("Menerima pesan cinta dari pasangan", "A", "Menghabiskan waktu berdua tanpa gangguan", "B"),
    ("Pasangan memuji saya di depan orang lain", "A", "Mengobrol santai dari hati ke hati dengan pasangan", "B"),
    ("Mendengar pasangan berkata 'Aku mencintaimu'", "A", "Melakukan hobi bersama pasangan", "B"),

    # A vs C
    ("Pasangan memuji penampilan saya", "A", "Menerima kejutan berupa barang dari pasangan", "C"),
    ("Pasangan mengatakan bahwa saya berharga", "A", "Pasangan membawakan oleh-oleh saat pulang", "C"),
    ("Pasangan mengucapkan terima kasih atas apa yang saya lakukan", "A", "Pasangan memberikan hadiah ulang tahun yang bermakna", "C"),

    # A vs D
    ("Pasangan mengingat dan memuji usaha saya", "A", "Pasangan membantu saya menyelesaikan tugas", "D"),
    ("Pasangan memberikan apresiasi verbal", "A", "Pasangan mengambil alih tanggung jawab saya saat saya lelah", "D"),
    ("Pasangan mengatakan betapa pentingnya saya baginya", "A", "Pasangan membuatkan minuman hangat untuk saya", "D"),

    # A vs E
    ("Pasangan menyemangati saya dengan kata-kata", "A", "Dipeluk oleh pasangan", "E"),
    ("Pasangan memuji ide-ide saya", "A", "Pasangan duduk berdekatan dengan saya", "E"),
    ("Pasangan memuji sifat atau karakter saya", "A", "Pasangan mengelus rambut saya", "E"),

    # B vs C
    ("Pergi jalan-jalan berdua dengan pasangan", "B", "Diberikan hadiah kecil dari pasangan", "C"),
    ("Memiliki jadwal rutin untuk kencan", "B", "Menerima hadiah kecil secara rutin", "C"),
    ("Menghabiskan liburan bersama pasangan", "B", "Pasangan membelikan makanan kesukaan saya", "C"),

    # B vs D
    ("Pasangan mendengarkan keluh kesah saya dengan penuh perhatian", "B", "Pasangan membantu saya tanpa diminta", "D"),
    ("Menonton film bersama pasangan", "B", "Pasangan memasakkan makanan untuk saya", "D"),
    ("Pasangan menatap mata saya saat saya berbicara", "B", "Pasangan membawakan barang bawaan saya yang berat", "D"),

    # B vs E
    ("Melakukan kegiatan bersama-sama dengan pasangan", "B", "Berpegangan tangan dengan pasangan", "E"),
    ("Bercerita dengan pasangan sebelum tidur", "B", "Pasangan mengusap punggung saya", "E"),
    ("Menghabiskan akhir pekan berdua saja", "B", "Duduk bersandar pada pasangan", "E"),

    # C vs D
    ("Menerima kado spesial dari pasangan", "C", "Pasangan membersihkan rumah untuk saya", "D"),
    ("Pasangan membuatkan kerajinan tangan atau hadiah", "C", "Pasangan membantu merawat saya saat saya sakit", "D"),
    ("Pasangan membelikan barang yang sudah lama saya idamkan", "C", "Pasangan mengurus keperluan rumah tangga", "D"),

    # C vs E
    ("Menerima kejutan saat perayaan tertentu", "C", "Pasangan mencium kening saya", "E"),
    ("Pasangan mengingat barang favorit saya dan membelikannya", "C", "Pasangan memijat saya saat saya lelah", "E"),
    ("Pasangan memberikan bunga atau hadiah romantis", "C", "Pasangan memeluk saya erat", "E"),

    # D vs E
    ("Pasangan diam-diam membelikan sesuatu untuk saya", "C", "Pasangan menyelesaikan pekerjaan yang tidak saya sukai", "D"), # Wait, this is C vs D. Need D vs E
    ("Pasangan memperbaiki barang saya yang rusak", "D", "Bersentuhan secara fisik saat mengobrol", "E"),
    ("Pasangan mengurus kendaraan saya", "D", "Pasangan memberikan sentuhan lembut", "E"),
]

# Fix the C vs D mistake above:
pairs[27] = ("Pasangan menyiapkan bekal atau sarapan", "D", "Bergandengan tangan saat berjalan", "E")

import random
random.seed(42) # for reproducibility
random.shuffle(pairs)

questions = []
for i, (txt1, lang1, txt2, lang2) in enumerate(pairs, 1):

    # Randomize order of A and B within the question
    options = [
        {"id": "A", "text": txt1, "language": languages[lang1]},
        {"id": "B", "text": txt2, "language": languages[lang2]}
    ]
    random.shuffle(options)
    # Re-assign IDs just to be sure it's always A and B
    options[0]["id"] = "A"
    options[1]["id"] = "B"

    q = {
        "id": i,
        "options": options
    }
    questions.append(q)

with open("questions.json", "w") as f:
    json.dump(questions, f, indent=2)

print("questions.json generated with 30 questions.")
