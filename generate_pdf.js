const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
    try {
        const browser = await puppeteer.launch({ headless: 'new' });
        const page = await browser.newPage();

        // Cargar el HTML local
        const filePath = `file://${path.resolve(__dirname, 'presentacion_capital.html')}`;
        await page.goto(filePath, { waitUntil: 'networkidle0' });

        // Generar el PDF
        await page.pdf({
            path: 'Presentacion_CapitalTradeIberia.pdf',
            format: 'A4',
            landscape: true,
            printBackground: true,
            margin: { top: 0, right: 0, bottom: 0, left: 0 }
        });

        console.log('PDF generado exitosamente: Presentacion_CapitalTradeIberia.pdf');
        await browser.close();
    } catch (err) {
        console.error('Error generando PDF:', err);
    }
})();
