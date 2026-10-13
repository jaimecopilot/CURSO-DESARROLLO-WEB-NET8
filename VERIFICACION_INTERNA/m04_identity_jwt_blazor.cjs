// E2E de página /perfil-jwt sobre API Identity conectada a LocalDB.
const { chromium } = require('playwright');
(async ()=>{
  const api='http://127.0.0.1:5086';
  const reg=await fetch(api+'/auth/registro',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:'alumno@example.test',password:'ClaveAlumnoSegura-2026!'})});
  if(reg.status!==201)throw Error('Registro Identity='+reg.status);
  const browser=await chromium.launch({headless:true});
  try{
    const page=await browser.newPage();
    await page.goto('http://127.0.0.1:5094/perfil-jwt',{waitUntil:'domcontentloaded'});
    await page.locator('#jwt-email').fill('alumno@example.test');
    await page.locator('#jwt-clave').fill('ClaveAlumnoSegura-2026!');
    await page.locator('#jwt-entrar').click();
    await page.locator('#jwt-sesion').waitFor({timeout:30000});
    await page.locator('#jwt-perfil').click();
    await page.locator('#jwt-perfil-respuesta').waitFor({timeout:30000});
    const perfil=await page.locator('#jwt-perfil-respuesta').innerText();
    if(!perfil.includes('Alumno'))throw Error('El perfil no contiene Alumno: '+perfil);
    await page.locator('#jwt-formador').click();
    await page.locator('#jwt-estado').getByText('HTTP 403',{exact:false}).waitFor({timeout:30000});
    await page.locator('#jwt-salir').click();
    await page.locator('#jwt-sesion').waitFor({state:'detached',timeout:30000});
    await page.locator('#jwt-email').fill('formador@ejemplo.local');
    await page.locator('#jwt-clave').fill('ClaveDemoSegura-2026!');
    await page.locator('#jwt-entrar').click();
    await page.locator('#jwt-sesion').waitFor({timeout:30000});
    await page.locator('#jwt-formador').click();
    await page.locator('#jwt-estado').getByText('Acceso permitido',{exact:false}).waitFor({timeout:30000});
    console.log('E2E Blazor Identity/JWT correcto: registro, token, perfil, 403, olvido local, Formador 200');
  } finally{await browser.close();}
})().catch(err=>{console.error(err);process.exit(1)});
