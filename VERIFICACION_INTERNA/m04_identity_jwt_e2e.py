#!/usr/bin/env python3
"""E2E real contra SQL Server Express LocalDB: 400/401/403/200, JWT y roles."""
import json, urllib.request, urllib.error, base64
base='http://127.0.0.1:5086'
def call(path,method='GET',body=None,token=None):
    headers={'Content-Type':'application/json'}
    if token: headers['Authorization']='Bearer '+token
    data=json.dumps(body).encode() if body is not None else None
    req=urllib.request.Request(base+path,data=data,method=method,headers=headers)
    try:
        with urllib.request.urlopen(req) as x:
            return x.status,json.loads(x.read() or b'{}')
    except urllib.error.HTTPError as e:
        return e.code,{}
assert call('/api/identidad/yo')[0]==401
assert call('/api/identidad/formador')[0]==401
email='alumno@example.test'
pwd='ClaveAlumnoSegura-2026!'
invalid=call('/auth/registro','POST',{'email':email,'password':'123'})
assert invalid[0]==400,invalid
created=call('/auth/registro','POST',{'email':email,'password':pwd})
assert created[0]==201,created
assert created[1]['rol']=='Alumno'
duplicate=call('/auth/registro','POST',{'email':email,'password':pwd})
assert duplicate[0]==400,duplicate
assert call('/auth/login','POST',{'email':email,'password':'incorrecta'})[0]==401
status,payload=call('/auth/login','POST',{'email':email,'password':pwd})
assert status==200,payload
jwt=payload['accessToken']
assert jwt.count('.')==2 and payload['tokenType']=='Bearer'
h,b,s=jwt.split('.')
claims=json.loads(base64.urlsafe_b64decode(b+'='*(-len(b)%4)))
assert claims['iss']=='CursoWeb.M04.IdentityJwt'
assert claims['aud']=='CursoWeb.M04.Cliente'
assert 'exp' in claims and 'sub' in claims
status,yo=call('/api/identidad/yo',token=jwt)
assert status==200 and 'Alumno' in yo['roles'],(status,yo)
assert call('/api/identidad/formador',token=jwt)[0]==403
assert call('/api/identidad/yo',token=jwt[:-1]+('A' if jwt[-1]!='A' else 'B'))[0]==401
form=call('/auth/login','POST',{'email':'formador@ejemplo.local','password':'ClaveDemoSegura-2026!'})
assert form[0]==200,form
assert call('/api/identidad/formador',token=form[1]['accessToken'])[0]==200
print('E2E OK: 400 contraseña, 201 alta, 401 anónimo y credenciales, 200 JWT válido, 403 rol Alumno, 401 firma alterada, 200 rol Formador',flush=True)
