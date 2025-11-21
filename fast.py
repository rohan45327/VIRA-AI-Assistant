from fastapi import FastAPI,Request,HTTPException,File,UploadFile,Form, templating
from vira import web_command,get_summary
from fastapi.middleware.cors import CORSMiddleware
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
myapp=FastAPI()
myapp.add_middleware(     
    CORSMiddleware,       
    allow_origins=['*'],     
    allow_headers=['*'],   
    allow_methods=['*']    
)
@myapp.get('/')
def home():
    return{
        "Vira Server is connected Now you can send commands"
    }
@myapp.post('/command')
async def handel(cmd:Request):
    try:
        data=await cmd.json()
        command=data.get('command')
    except:
        raise HTTPException(status_code=400, detail="Invalid or missing command data.")
    if not command:
        return "Error command not found"
    msg=web_command(command)
    print(f'Vira: {msg}')
    return{
        'response':f'{msg}'
    }
@myapp.post('/upload')
def upload(filen: UploadFile = File(...),prompt: str = Form(None)):
    if not filen:
        raise HTTPException(status_code=400,detail='Nothing found in the give file')
    usr=prompt if prompt!=None else ''
    file_typ=filen.content_type
    file_nam=filen.filename
    if file_typ == 'application/pdf' or file_nam.lower().endswith('.pdf'):
        response=get_summary(usr,filen.file)
    else:
        return{
            'Vira':'Sorry I cant proceed with that file Currently i only support .pdf files'
        }
    return{
        'Vira': response.json()
    }