import os
from uuid import uuid4      #create a uniq hash code
import random
from sms_ir import SmsIr
# -----------------------------------------------------------------------------
def create_random_code(count):
    count-=1
    return random.randint(10**count,10**(count+1)-1)

# -----------------------------------------------------------------------------
class FileUpload:
    def __init__(self,dir,prefix):
        self.dir=dir
        self.prefix=prefix
    
    def upload_to(self,instans,filename):
        filename,ext=os.path.splitext(filename)
        return f"{self.dir}/{self.prefix}/{uuid4()}{ext}"

# -----------------------------------------------------------------------------
def send_sms(number, code):
    try:
        sms_ir = SmsIr(api_key='xSXrnqLkAuAojUGThAxYiK5G4qyOYTULYsJ3uYGha88dWj3VWEXAC3kLO8ch2xtd')
        result = sms_ir.send_verify_code(
            number=str(number),
            template_id=654532,
            parameters=[
                {
                    "name": "CODE",
                    "value": str(code)
                }
            ],
        )
        # بررسی پاسخ به صورت JSON
        if result.status_code == 200:  # بررسی اینکه آیا درخواست موفق بوده است
            result_data = result.json()  # تبدیل پاسخ به فرمت JSON
            if result_data.get("status"):
                print("پیامک با موفقیت ارسال شد.")
            else:
                print(f"خطا در ارسال پیامک: {result_data.get('message', 'اطلاعات بیشتر وجود ندارد.')}")
        else:
            print(f"خطا در ارسال پیامک: کد وضعیت HTTP: {result.status_code}")
    except Exception as e:
        print(f"خطا در ارسال پیامک: {e}")
