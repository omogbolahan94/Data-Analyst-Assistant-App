import Papa from "papaparse";
import * as XLSX from "xlsx";


export async function parseCSV(file) {
    return new Promise((resolve) => {
        Papa.parse(file, {
            header: true,
            preview: 20,
            complete: (results) => {
                resolve({ fields: results.meta.fields || [], data: results.data.slice(0, 10) });
            },
        });
    });
}


export async function parseExcel(file) {
    const buffer = await file.arrayBuffer();
    const workbook = XLSX.read(buffer, { type: "array" });
    const sheetName = workbook.SheetNames[0];
    const sheet = workbook.Sheets[sheetName];
    const json = XLSX.utils.sheet_to_json(sheet, { header: 1 });
    const [headerRow, ...rows] = json;
    const objs = rows.slice(0, 10).map((r) => {
        const obj = {};
        headerRow.forEach((h, i) => (obj[h || `col_${i}`] = r[i]));
        return obj;
    });
    return { fields: headerRow || [], data: objs };
}