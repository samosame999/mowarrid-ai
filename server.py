import os
import json
import sqlite3
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

try:
    from google import genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

app = FastAPI(title="Mowarrid AI - Enterprise Agent Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def init_db():
    conn = sqlite3.connect("dubai_trade.db", check_same_thread=False)
    c = conn.cursor()
    
    # إعادة ضبط الجداول لضمان ترميز عربي سليم 100% وخالٍ من أي تشوه سابق
    c.execute("DROP TABLE IF EXISTS suppliers")
    c.execute("DROP TABLE IF EXISTS customs_hs")

    c.execute('''CREATE TABLE suppliers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        zone TEXT,
        category TEXT,
        license_no TEXT,
        phone TEXT,
        delivery_hours INTEGER,
        discount_flexibility REAL
    )''')
    c.execute('''CREATE TABLE customs_hs (
        category TEXT PRIMARY KEY,
        hs_code TEXT,
        description TEXT,
        duty_rate REAL
    )''')

    suppliers_data = [
        (1, "شركة الخليج للتجهيزات الفندقية ذ.م.م", "المنطقة الحرة بجبل علي (JAFZA)", "hotel", "CN-449102", "+971-4-881-4200", 24, 0.149),
        (2, "الإمارات للمعدات التجارية والصناعية", "القوز الصناعية 3", "hotel", "DED-772190", "+971-4-338-9100", 48, 0.091),
        (3, "النخبة للاستيراد والتوريد التجاري", "رأس الخور الصناعية", "hotel", "DED-610294", "+971-4-289-1122", 120, 0.100),
        (4, "دبي للطاقة الشمسية والمقاولات الحديثة", "المنطقة الحرة بجبل علي (JAFZA)", "construction", "CN-992011", "+971-4-883-5500", 24, 0.155),
        (5, "الرواد للكابلات والمحولات الصناعية", "مجمع دبي للاستثمار (DIP)", "construction", "DED-551920", "+971-4-885-1234", 48, 0.095),
        (6, "ميديكال هب للتجهيزات الطبية (معتمد DHA)", "مدينة دبي الطبية (DHCC)", "medical", "DHCC-1102", "+971-4-429-8800", 24, 0.140),
        (7, "الشفاء لتوريد أجهزة الليزر والعيادات", "القصيص الصناعية", "medical", "DED-339104", "+971-4-267-4411", 72, 0.085)
    ]
    c.executemany("INSERT INTO suppliers VALUES (?,?,?,?,?,?,?,?)", suppliers_data)

    customs_data = [
        ("hotel", "8419.81.00", "معدات تحضير المشروبات الساخنة والتبريد الفندقي التجاري", 0.0),
        ("construction", "8541.43.00", "خلايا وألواح ضوئية فولطية ومحولات صناعية", 0.0),
        ("medical", "9018.90.00", "أجهزة ومعدات طبية وجراحية وليزر معتمدة من هيئة الصحة بدبي", 0.0)
    ]
    c.executemany("INSERT INTO customs_hs VALUES (?,?,?,?)", customs_data)
    conn.commit()
    conn.close()

init_db()

def query_customs_tool(category: str) -> dict:
    conn = sqlite3.connect("dubai_trade.db", check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT hs_code, description, duty_rate FROM customs_hs WHERE category=?", (category,))
    row = c.fetchone()
    conn.close()
    if row:
        return {"hs_code": row[0], "description": row[1], "duty_rate": row[2]}
    return {"hs_code": "8479.89.99", "description": "معدات وتجهيزات تجارية عامة", "duty_rate": 0.05}

def query_suppliers_tool(category: str, base_budget: float) -> list:
    conn = sqlite3.connect("dubai_trade.db", check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT name, zone, license_no, phone, delivery_hours, discount_flexibility FROM suppliers WHERE category=?", (category,))
    rows = c.fetchall()
    conn.close()

    results = []
    multipliers = [1.02, 1.06, 1.11]
    for idx, r in enumerate(rows):
        mult = multipliers[idx % len(multipliers)]
        initial_price = round(base_budget * mult, -2)
        negotiated_price = round(initial_price * (1.0 - r[5]), -2)
        vat_total = round(negotiated_price * 1.05, 0)
        results.append({
            "name": r[0],
            "zone": r[1],
            "license_no": r[2],
            "phone": r[3],
            "delivery_hours": r[4],
            "discount_pct": round(r[5] * 100, 1),
            "initial_price": initial_price,
            "negotiated_price": negotiated_price,
            "final_with_vat": vat_total,
            "is_winner": (idx == 0)
        })
    return results

class RFQRequest(BaseModel):
    rfq_text: str
    budget: float
    priority: str
    category: str
    api_key: str = ""

class DocAnalyzeRequest(BaseModel):
    filename: str
    category: str

@app.post("/api/run-agent")
def execute_agent(req: RFQRequest):
    customs_info = query_customs_tool(req.category)
    suppliers_list = query_suppliers_tool(req.category, req.budget)
    winner = suppliers_list[0]
    savings = winner["initial_price"] - winner["negotiated_price"]

    priority_label = "السرعة والتوريد الفوري من مستودعات دبي" if req.priority == "speed" else "أقل تكلفة وخصم الدفع النقدي"
    ai_plan_summary = (
        f"تحليل الأولوية: ({priority_label}). "
        f"قرر الوكيل توجيه البحث إلى ({winner['zone']}) لضمان الإعفاء الجمركي تحت الرمز ({customs_info['hs_code']}) والتسليم خلال {winner['delivery_hours']} ساعة."
    )
    
    agent_voice_pitch = (
        f"مرحباً {winner['name']}، معكم وكيل المشتريات الذكي مُورّد. "
        f"عرضكم الأولي هو {int(winner['initial_price'])} درهم. "
        f"لدينا تعميد فوري اليوم ودفع نقدي مباشر إذا تم تخفيض السعر إلى {int(winner['negotiated_price'])} درهم شامل التوصيل."
    )
    vendor_voice_reply = (
        f"أهلاً بك. بما أن الدفع نقدي والتعميد اليوم، نحن في {winner['name']} موافقون على السعر الجديد "
        f"بقيمة {int(winner['negotiated_price'])} درهم، وسنحرك الشاحنة من {winner['zone']} خلال {winner['delivery_hours']} ساعة."
    )

    return {
        "status": "success",
        "customs": customs_info,
        "suppliers": suppliers_list,
        "winner": winner,
        "savings": savings,
        "ai_plan": ai_plan_summary,
        "voice_dialog": {
            "agent_pitch": agent_voice_pitch,
            "vendor_reply": vendor_voice_reply
        }
    }

# مسار تحليل المستندات والفواتير (يعمل عبر JSON لتجنب خطأ مكتبة python-multipart)
@app.post("/api/analyze-document")
def analyze_document(doc: DocAnalyzeRequest):
    extracted_map = {
        "hotel": f"تم استخراج البنود من الفاتورة ({doc.filename}): مطلوب 15 ماكينة إسبريسو إيطالية (3 رؤوس) + 20 ثلاجة عرض فندقية شاملة التوريد والتركيب في دبي مارينا.",
        "construction": f"تم استخراج جدول الكميات من المستند ({doc.filename}): مطلوب 500 لوح طاقة شمسية بقدرة 550 واط + 10 محولات صناعية لمشروع الخليج التجاري.",
        "medical": f"تم استخراج المواصفات الطبية من الملف ({doc.filename}): مطلوب 4 أجهزة ليزر معتمدة من هيئة الصحة بدبي (DHA) + 15 سرير فحص كهربائي لعيادة جميرا."
    }
    return {
        "status": "success",
        "filename": doc.filename,
        "extracted_requirements": extracted_map.get(doc.category, extracted_map["hotel"])
    }

@app.get("/", response_class=HTMLResponse)
def serve_ui():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    import uvicorn
    print("Mowarrid AI Enterprise Server Running on: http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)