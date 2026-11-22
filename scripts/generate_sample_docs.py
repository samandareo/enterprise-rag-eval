from pathlib import Path
import fitz # so here is PyMuPDF (installed automatically with pymupdf4llm)
from docx import Document

RAW_DIR = Path("data/raw_docs")
RAW_DIR.mkdir(parents=True, exist_ok=True)


def create_pdf_from_html(filename: str, html_content: str) -> None:
    """PyMuPDF's HTML engine to render UTF-8 Cyrillic/Latin text and real tables into  a PDF"""
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)
    rect = fitz.Rect(40, 40, 555, 802)
    page.insert_htmlbox(rect, html_content)
    doc.save(RAW_DIR / filename)
    doc.close()
    print(f"Created PDF: {RAW_DIR / filename}")

def generate_hr_policy_ru() -> None:
    html = """
    <style>
        body { font-family: sans-serif; font-size: 11pt; line-height: 1.4; }
        table { border-collapse: collapse; width: 100%; margin: 12px 0; }
        th, td { border: 1px solid #333; padding: 6px; text-align: left; }
        th { background-color: #eee; }
    </style>
    <h1>Политика отпусков и удаленной работы (HR-2026)</h1>
    <h2>1. Ежегодный оплачиваемый отпуск</h2>
    <p>Каждый штатный сотрудник компании имеет право на 24 календарных дня оплачиваемого отпуска в год.
    Заявку на отпуск необходимо подать в системе HR-Portal минимум за 14 календарных дней до начала отпуска.</p>

    <h2>2. Таблица видов отпусков и согласования</h2>
    <table>
        <tr><th>Тип отпуска</th><th>Длительность</th><th>Кто согласует</th></tr>
        <tr><td>Ежегодный основной</td><td>24 дня</td><td>Тимлид + HR</td></tr>
        <tr><td>Больничный (без справки)</td><td>До 3 дней в год</td><td>Тимлид</td></tr>
        <tr><td>Учебный отпуск</td><td>До 10 дней</td><td>Руководитель департамента</td></tr>
    </table>

    <h2>3. Удаленная работа</h2>
    <p>Сотрудники инженерного отдела могут работать удаленно до 3 дней в неделю.
    Для полной удаленной работы из другой страны требуется согласование с отделом безопасности (форма SEC-109).</p>
    """
    create_pdf_from_html("hr_policy_ru.pdf", html)


def generate_finance_faq_uz_cyr() -> None:
    html = """
    <style>
        body { font-family: sans-serif; font-size: 11pt; line-height: 1.4; }
        table { border-collapse: collapse; width: 100%; margin: 12px 0; }
        th, td { border: 1px solid #333; padding: 6px; text-align: left; }
        th { background-color: #eee; }
    </style>
    <h1>Молиявий харажатлар ва хизмат сафарлари қоидалари (FIN-2026)</h1>
    <h2>1. Хизмат сафари лимитлари</h2>
    <p>Ходимлар хизмат сафаридан қайтгандан сўнг 5 иш куни ичида барча чекларни Молия бўлимига топширишлари шарт.
    Кечиктирилган ҳисоботлар фақат Молия директори рухсати билан қопланади.</p>

    <h2>2. Кунлик харажатлар жадвали</h2>
    <table>
        <tr><th>Йўналиш</th><th>Меҳмонхона лимити (кунига)</th><th>Овқатланиш (кунига)</th></tr>
        <tr><td>Ўзбекистон ичида</td><td>800 000 сўм</td><td>250 000 сўм</td></tr>
        <tr><td>МДҲ давлатлари</td><td>120 USD</td><td>50 USD</td></tr>
        <tr><td>Европа ва АҚШ</td><td>220 USD</td><td>85 USD</td></tr>
    </table>

    <h2>3. Корпоратив карта блокировкаси</h2>
    <p>Агар корпоратив карта йўқолса, дарҳол Молия бўлимига ёки 24/7 колл-центрга мурожаат қилиб,
    FIN-BLOCK-99 коди орқали картани блоклаш талаб этилади.</p>
    """
    create_pdf_from_html("finance_faq_uz_cyr.pdf", html)

def generate_it_support_uz_lat() -> None:
    doc = Document()
    doc.add_heading("IT yordam va xavfsizlik yo'riqnomasi (IT-2026)", level=1)
    
    doc.add_heading("1. VPN unalish muammolari", level=2)
    doc.add_paragraph(
        "Agar korporativ VPN ulanmasa va ekranda ERR-4092 xatosi chiqsa, bu sizning "
        "SSO sertifikatingiz muddati tugaganini anglatadi. Uni yangilash uchun "
        "portal.company.uz/cert sahifasiga kiring va yangi profilni yuklab oling."
    )
    doc.add_paragraph(
        "Agar VPN-503 xatosi paydo bo'lsa, ofis tarmog'ida texnik ishlar olib borilmoqda. "
        "15 daqiqadan so'ng qayta urinib ko'ring yoki zaxira server (vpn-eu2.company.uz) ni tanlang."
    )

    doc.add_heading("2. IT yordam SLA jadvali", level=2)
    table = doc.add_table(rows=4, cols=3)
    table.style = "Table Grid"
    headers = ["Muammo darajasi", "Javob berish vaqti", "Misol"]
    rows_data = [
        ["Kritik (P1)", "15 daqiqa", "Production server ishlamayapti, VPN to'liq o'chgan"],
        ["Yuqori (P2)", "2 soat", "Xodimning noutbuki bloklangan, ERR-4092"],
        ["Oddiy (P3)", "24 soat", "Yangi dastur o'rnatish so'rovi"],
    ]

    for i, h in enumerate(headers):
        table.rows[0].cells[i].text = h
    for r_idx, row in enumerate(rows_data, start=1):
        for c_idx, val in enumerate(row):
            table.rows[r_idx].cells[c_idx].text = val

    doc.add_heading("3. Parolni tiklash qoidalari", level=2)
    doc.add_paragraph(
        "Parolni tiklash uchun xodim IT-suppor botiga murojaat qilishi yoki "
        "shaxsiy guvohnoma bilan IT bo'limiga kelishi kerak. Parol kamida 12 ta belgidan iborat bo'lishi shart."
    )

    out_path = RAW_DIR / "it_support_uz_lat.docx"
    doc.save(out_path)
    print(f"Created DOCX: {out_path}")

if __name__ == "__main__":
    generate_hr_policy_ru()
    generate_finance_faq_uz_cyr()
    generate_it_support_uz_lat()
