บันทึกการเปลี่ยนแปลง

    การแก้ไขโมเดล (train_and_save_model.ipynb)
        ลบ features ที่เกี่ยวกับการชำระเงินและสัญญาออก
            ลบ 'Contract' ออกจาก categorical_columns
            ลบ 'PaymentMethod' ออกจาก categorical_columns
        เทรนโมเดลใหม่หลังจากลบ features
        ผลลัพธ์โมเดลใหม่:
            Test Accuracy: 0.8091 (80.91%)
            ROC-AUC: 0.8514 (85.14%)

    การแก้ไขหน้า UI (app.py)

        ลบส่วน "การชำระเงินและสัญญา" ออกทั้งหมด
            ลบฟิลด์ "ประเภทสัญญา"
            ลบฟิลด์ "วิธีการชำระเงิน"
            ลบฟิลด์ "รับบิลแบบออนไลน์ (Paperless)"
            ลบฟิลด์ "ค่าใช้บริการรายเดือน ($)"
            ลบฟิลด์ "ยอดชำระสะสม ($)"

        กำหนดค่าเริ่มต้นสำหรับฟิลด์ที่จำเป็นต้องส่งให้โมเดล
            Contract = "Month-to-month"
            PaymentMethod = "Bank transfer (automatic)"
            PaperlessBilling = "No"
            MonthlyCharges = 70.0
            TotalCharges = MonthlyCharges * tenure

    ไฟล์ที่ถูกอัพเดต
        churn_model.h5 (โมเดลที่เทรนใหม่)
        scaler.pkl (ตัว normalize feature ใหม่)
        feature_columns.json (รายชื่อคอลัมน์ที่ใช้ - ไม่รวม Contract และ PaymentMethod)

