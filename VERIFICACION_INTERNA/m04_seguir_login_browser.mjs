import { chromium } from 'playwright';

const base = process.env.BASE_URL ?? 'http://127.0.0.1:5094';
const browser = await chromium.launch({ headless: true });
try {
  const page = await browser.newPage();
  await page.goto(base + '/seguridad', { waitUntil: 'domcontentloaded' });
  await page.locator('#anonimo-demo').waitFor({ timeout: 30000 });

  let response = await page.request.get(base + '/demo/privado');
  if (response.status() !== 401) throw Error('Anónimo: se esperaba 401');

  await page.locator('#codigo-demo').fill('curso-demo-44');
  await page.locator('#entrar-demo').click();
  await page.locator('#usuario-demo').waitFor({ timeout: 30000 });
  await page.locator('#formador-demo').waitFor({ timeout: 30000 });
  response = await page.request.get(base + '/demo/privado');
  if (response.status() !== 200) throw Error('Autenticado Formador: se esperaba 200');

  await page.locator('#salir-demo').click();
  await page.locator('#anonimo-demo').waitFor({ timeout: 30000 });
  response = await page.request.get(base + '/demo/privado');
  if (response.status() !== 401) throw Error('Después de salir: se esperaba 401');
  console.log('Autenticación de demostración validada en navegador real: 401, entrada, rol, 200, salida, 401.');
} finally {
  await browser.close();
}
