import os
from uuid import uuid4      #create a uniq hash code

def create_random_code(count):
    import random
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
from kavenegar import *
def send_sms(mobile_number,token):   
    pass
    # 1000689696
    try:
        api =KavenegarAPI('3135443531774145637938476F58584E355A47326F356F4F77386B35594739323543434A622F64763778383D')
        params = {
             'receptor': mobile_number,
             'template' :'verifyy',
             'token': token,
             'type':'sms',
        }
        response = api.verify_lookup(params)
        return response 
    except APIException as error:
        print(f'error1:{error}')
    except HTTPException as error:
        print(f'error2:{error}')