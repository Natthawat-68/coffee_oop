# Green Grounds Coffee - POS System

โปรแกรมระบบขายหน้าร้านสำหรับร้านกาแฟ พัฒนาด้วย PyQt6 และหลักการ OOP

## สมาชิกทีม

- Natthawat Khaokaew - Developer

## วิธีการติดตั้ง

### 1. Clone Repository

```bash
git clone https://github.com/Natthawat-68/coffee_oop.git
cd coffee_oop
```

### 2. สร้าง Virtual Environment (แนะนำ)

```bash
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### 3. ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

หรือใช้ poetry:

```bash
pip install poetry
poetry install
```

### 4. รันโปรแกรม

```bash
python main.py
```

## โครงสร้างโปรเจกต์

```
coffee_oop/
├── main.py
├── styles.py
├── models/
│   ├── __init__.py
│   ├── menu.py
│   └── order.py
├── assets/images/
├── requirements.txt
├── pyproject.toml
└── README.md
```

## วิธีใช้งาน

1. **เลือกเมนู** - คลิกปุ่ม + ที่การ์ดเมนูเพื่อเพิ่มรายการ
2. **แก้ไขรายการ** - ปรับจำนวนหรือลบรายการใน Order List
3. **ระบุลูกค้า** - กรอกชื่อและเลขโต๊ะ (ทานที่ร้าน) หรือเลือกซื้อกลับบ้าน
4. **ยืนยันคำสั่ง** - กดปุ่ม Confirm Order เพื่อสร้างใบเสร็จ

## โครงสร้าง OOP

- **Encapsulation**: `MenuItem`, `OrderItem`, `Order` encapsulate ข้อมูล
- **Inheritance**: `Beverage`, `Snack` สืบทอดจาก `MenuItem`
- **Polymorphism**: `get_display_price()` แสดงผลต่างกันตามประเภท
- **Composition**: `Order` ประกอบด้วย `OrderItem` หลายรายการ
- **SOLID**: SRP (คลาสเดียวหนึ่งหน้าที่)
- **Design Patterns**: Factory (`create_menu_item`)
