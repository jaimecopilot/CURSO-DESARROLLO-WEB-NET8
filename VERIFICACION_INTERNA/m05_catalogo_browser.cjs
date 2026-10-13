// P5.1: browser real sobre Blazor Interactive Server y API de productos.
const { chromium } = require('playwright');
(async () => {
  const api='http://127.0.0.1:5081';
  const browser=await chromium.launch({headless:true});
  try {
    const page=await browser.newPage();
    await page.goto('http://127.0.0.1:5092/catalogo-remoto',{waitUntil:'domcontentloaded'});
    await page.locator('#productos-api').getByText('Cuaderno',{exact:false}).waitFor({timeout:30000});
    await page.locator('#recargar-api').click();
    await page.locator('#productos-api').getByText('Lápiz',{exact:false}).waitFor({timeout:30000});

    await page.locator('#nombre-api').fill('');
    await page.locator('#precio-api').fill('0');
    await page.locator('#crear-api').click();
    await page.locator('#resultado-api').getByText('Indica un nombre',{exact:false}).waitFor({timeout:30000});

    await page.locator('#nombre-api').fill('Regla');
    await page.locator('#precio-api').fill('1.75');
    await page.locator('#crear-api').click();
    await page.locator('#resultado-api').getByText('Producto creado: Regla',{exact:false}).waitFor({timeout:30000});
    await page.locator('#productos-api').getByText('Regla',{exact:false}).waitFor({timeout:30000});

    const response=await fetch(api+'/api/productos',{
      method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({nombre:'Archivador',precio:5.25})
    });
    if(response.status!==201)throw Error('POST externo no devuelve 201: '+response.status);
    if((await page.locator('#productos-api').innerText()).includes('Archivador'))
      throw Error('Blazor recibió actualización sin solicitar GET; no era el contrato');
    await page.locator('#recargar-api').click();
    await page.locator('#productos-api').getByText('Archivador',{exact:false}).waitFor({timeout:30000});
    console.log('Blazor navegador real: carga GET, recarga, invalidación local, POST, actualización por GET: OK');
  } finally {
    await browser.close();
  }
})().catch(e=>{console.error(e);process.exit(1)});
