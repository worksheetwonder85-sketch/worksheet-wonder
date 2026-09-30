/**
 * Generates Grade1_Data_Handling_Question_Paper.docx
 * Zero-dependency: builds the OOXML package and a STORE-method ZIP by hand.
 * Run: node generate_docx.js
 */
'use strict';
const fs = require('fs');
const path = require('path');

/* ------------------------------------------------------------------ */
/* ZIP plumbing (store method, UTF-8 names)                            */
/* ------------------------------------------------------------------ */
const CRC_TABLE = (() => {
  const t = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    t[n] = c >>> 0;
  }
  return t;
})();
function crc32(buf) {
  let c = 0xffffffff;
  for (let i = 0; i < buf.length; i++) c = CRC_TABLE[(c ^ buf[i]) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}
function buildZip(entries) {
  const DOS_TIME = (12 << 11) | (0 << 5) | 0;           // fixed 2026-09-15 12:00
  const DOS_DATE = ((2026 - 1980) << 9) | (9 << 5) | 15;
  const locals = [];
  const centrals = [];
  let offset = 0;
  for (const [name, content] of entries) {
    const nameBuf = Buffer.from(name, 'utf8');
    const data = Buffer.from(content, 'utf8');
    const crc = crc32(data);
    const lfh = Buffer.alloc(30);
    lfh.writeUInt32LE(0x04034b50, 0);
    lfh.writeUInt16LE(20, 4);            // version needed
    lfh.writeUInt16LE(0x0800, 6);        // flags: UTF-8
    lfh.writeUInt16LE(0, 8);             // method: store
    lfh.writeUInt16LE(DOS_TIME, 10);
    lfh.writeUInt16LE(DOS_DATE, 12);
    lfh.writeUInt32LE(crc, 14);
    lfh.writeUInt32LE(data.length, 18);
    lfh.writeUInt32LE(data.length, 22);
    lfh.writeUInt16LE(nameBuf.length, 26);
    lfh.writeUInt16LE(0, 28);
    locals.push(lfh, nameBuf, data);

    const cdh = Buffer.alloc(46);
    cdh.writeUInt32LE(0x02014b50, 0);
    cdh.writeUInt16LE(20, 4);            // version made by
    cdh.writeUInt16LE(20, 6);            // version needed
    cdh.writeUInt16LE(0x0800, 8);
    cdh.writeUInt16LE(0, 10);
    cdh.writeUInt16LE(DOS_TIME, 12);
    cdh.writeUInt16LE(DOS_DATE, 14);
    cdh.writeUInt32LE(crc, 16);
    cdh.writeUInt32LE(data.length, 20);
    cdh.writeUInt32LE(data.length, 24);
    cdh.writeUInt16LE(nameBuf.length, 28);
    cdh.writeUInt16LE(0, 30);            // extra len
    cdh.writeUInt16LE(0, 32);            // comment len
    cdh.writeUInt16LE(0, 34);            // disk start
    cdh.writeUInt16LE(0, 36);            // internal attrs
    cdh.writeUInt32LE(0, 38);            // external attrs
    cdh.writeUInt32LE(offset, 42);       // local header offset
    centrals.push(cdh, nameBuf);
    offset += 30 + nameBuf.length + data.length;
  }
  const cdBuf = Buffer.concat(centrals);
  const eocd = Buffer.alloc(22);
  eocd.writeUInt32LE(0x06054b50, 0);
  eocd.writeUInt16LE(0, 4);
  eocd.writeUInt16LE(0, 6);
  eocd.writeUInt16LE(entries.length, 8);
  eocd.writeUInt16LE(entries.length, 10);
  eocd.writeUInt32LE(cdBuf.length, 12);
  eocd.writeUInt32LE(offset, 16);
  eocd.writeUInt16LE(0, 20);
  return Buffer.concat([...locals, cdBuf, eocd]);
}

/* ------------------------------------------------------------------ */
/* WordprocessingML helpers                                            */
/* ------------------------------------------------------------------ */
const esc = (s) =>
  s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

function run(text, { b = false, sz = 22, color = null, font = 'Comic Sans MS' } = {}) {
  const rpr =
    `<w:rPr>` +
    `<w:rFonts w:ascii="${font}" w:hAnsi="${font}" w:cs="${font}"/>` +
    (b ? `<w:b/>` : ``) +
    (color ? `<w:color w:val="${color}"/>` : ``) +
    `<w:sz w:val="${sz}"/><w:szCs w:val="${sz}"/>` +
    `</w:rPr>`;
  return `<w:r>${rpr}<w:t xml:space="preserve">${esc(text)}</w:t></w:r>`;
}

function para(runsXml, { jc = null, before = 0, after = 100, tabs = null, border = false } = {}) {
  let ppr = `<w:pPr>`;
  if (border)
    ppr += `<w:pBdr><w:bottom w:val="single" w:sz="8" w:space="1" w:color="333333"/></w:pBdr>`;
  if (tabs) ppr += `<w:tabs>${tabs}</w:tabs>`;
  ppr += `<w:spacing w:before="${before}" w:after="${after}" w:line="240" w:lineRule="auto"/>`;
  if (jc) ppr += `<w:jc w:val="${jc}"/>`;
  ppr += `</w:pPr>`;
  return `<w:p>${ppr}${runsXml}</w:p>`;
}

const tab = () => `<w:r><w:tab/></w:r>`;
const RTAB = `<w:tab w:val="right" w:pos="9638"/>`;
const L = (pos) => `<w:tab w:val="left" w:pos="${pos}"/>`;
const pageBreak = () =>
  `<w:p><w:pPr><w:spacing w:after="0"/></w:pPr><w:r><w:br w:type="page"/></w:r></w:p>`;

/* ------------------------------------------------------------------ */
/* Paper content                                                       */
/* ------------------------------------------------------------------ */
const EMOJI_FONT = 'Segoe UI Emoji';
const pic = (emo, n) => run(Array(n).fill(emo).join('  '), { font: EMOJI_FONT, sz: 30 });
const marks = (t) => [tab(), run(t, { sz: 18, color: '555555' })];

const body = [];

/* ---- PAGE 1 ---- */
body.push(para(run('GRADE 1 \u2013 MATHEMATICS', { b: true, sz: 32 }), { jc: 'center', after: 40 }));
body.push(para(run('DATA HANDLING \u2013 PRACTICE QUESTION PAPER', { b: true, sz: 26 }), { jc: 'center', after: 80 }));
body.push(para('', { border: true, after: 160 }));

body.push(para([
  run('School: ____________________________', { sz: 22 }), tab(),
  run('Date: ________________', { sz: 22 }),
], { tabs: RTAB, after: 80 }));
body.push(para([
  run('Name: _____________________________', { sz: 22 }), tab(),
  run('Marks: _______ / 20        Time: 40 min', { sz: 22 }),
], { tabs: RTAB, after: 200 }));

body.push(para([
  run('SECTION A \u2013 Fill in the blanks. ', { b: true, sz: 24 }), ...marks('(4 \u00d7 1 = 4 marks)'),
], { tabs: RTAB, before: 60, after: 120 }));
[
  '(a)  The collection of information is called ______________ .',
  '(b)  A ______________ shows data through pictures.',
  '(c)  Data handling means to record and ______________ information.',
  '(d)  We ______________ and collect data from our surroundings.',
].forEach((q) => body.push(para(run(q), { after: 110 })));

body.push(para([
  run('SECTION B \u2013 Look at the pictograph and answer the questions. ', { b: true, sz: 24 }),
  ...marks('(6 \u00d7 1 = 6 marks)'),
], { tabs: RTAB, before: 160, after: 60 }));
body.push(para(run('Riya counted the fruits in a basket. One picture  =  one fruit.', { sz: 22 }), { after: 120 }));

const fruitRows = [
  ['Mangoes', '\u{1F96D}', 6],
  ['Bananas', '\u{1F34C}', 9],
  ['Apples',  '\u{1F34E}', 7],
];
for (const [label, emo, n] of fruitRows)
  body.push(para([run(label, { b: true }), tab(), pic(emo, n)], { tabs: L(2400), after: 90 }));
body.push(para('', { after: 60 }));

const fruitQs = [
  '1.  How many mangoes are there?',
  '2.  How many bananas are there?',
  '3.  How many apples are there?',
  '4.  Which fruit is the MOST in number?',
  '5.  Which fruit is the LEAST in number?',
  '6.  How many fruits are there in all?',
];
for (const q of fruitQs)
  body.push(para([run(q), tab(), run('Ans: __________________', { sz: 22 })], { tabs: L(5600), after: 110 }));

body.push(pageBreak());

/* ---- PAGE 2 ---- */
body.push(para([
  run('SECTION C \u2013 Observe the data and answer the questions. ', { b: true, sz: 24 }),
  ...marks('(6 \u00d7 1 = 6 marks)'),
], { tabs: RTAB, after: 60 }));
body.push(para(run('Riya counted the vehicles on her road. One picture  =  one vehicle.', { sz: 22 }), { after: 120 }));

const vehicleRows = [
  ['Buses',    '\u{1F68C}', 3],
  ['Cars',     '\u{1F697}', 5],
  ['Bicycles', '\u{1F6B2}', 4],
];
for (const [label, emo, n] of vehicleRows)
  body.push(para([run(label, { b: true }), tab(), pic(emo, n)], { tabs: L(2400), after: 90 }));
body.push(para('', { after: 60 }));

const vehicleQs = [
  '1.  How many cars did Riya see?',
  '2.  How many buses did Riya see?',
  '3.  How many bicycles did Riya see?',
  '4.  Which vehicle did she see the MOST?',
  '5.  How many buses and bicycles are there in all?',
  '6.  How many vehicles are there in all?',
];
for (const q of vehicleQs)
  body.push(para([run(q), tab(), run('Ans: __________________', { sz: 22 })], { tabs: L(5600), after: 110 }));

body.push(para([
  run('SECTION D \u2013 Count the pictures. Write the number in the box. ', { b: true, sz: 24 }),
  ...marks('(4 \u00d7 1 = 4 marks)'),
], { tabs: RTAB, before: 160, after: 140 }));

const countRows = [
  ['\u{1F404}', 4, 'Cows'],
  ['\u{1F414}', 6, 'Hens'],
  ['\u{1F407}', 3, 'Rabbits'],
  ['\u{1F434}', 2, 'Horses'],
];
countRows.forEach(([emo, n, label], i) => {
  body.push(para([
    run(`${i + 1}.`, { b: true }), tab(), pic(emo, n), tab(),
    run(label, { b: true }), tab(), run('[          ]', { b: true, sz: 26 }),
  ], { tabs: `${L(900)}${L(4600)}${L(7000)}`, after: 130 }));
});

body.push(para(run('GOOD JOB! YOU FINISHED! \u2B50', { b: true, sz: 26 }), { jc: 'center', before: 160 }));

body.push(pageBreak());

/* ---- PAGE 3 : ANSWER KEY ---- */
body.push(para(run('ANSWER KEY', { b: true, sz: 30 }), { jc: 'center', after: 40 }));
body.push(para(run('(For Parent / Teacher only)', { sz: 22, color: '555555' }), { jc: 'center', after: 80 }));
body.push(para('', { border: true, after: 160 }));

const key = [
  ['SECTION A \u2013 Fill in the blanks  (4 marks)', [
    '(a) data        (b) pictograph        (c) present        (d) observe',
  ]],
  ['SECTION B \u2013 Fruit pictograph  (6 marks)', [
    'Pictograph data:  Mangoes = 6,  Bananas = 9,  Apples = 7',
    '1. 6 mangoes      2. 9 bananas      3. 7 apples',
    '4. Bananas (most)      5. Mangoes (least)      6. 6 + 9 + 7 = 22 fruits',
  ]],
  ['SECTION C \u2013 Vehicle data  (6 marks)', [
    'Data:  Buses = 3,  Cars = 5,  Bicycles = 4',
    '1. 5 cars      2. 3 buses      3. 4 bicycles',
    '4. Cars (most)      5. 3 + 4 = 7      6. 3 + 5 + 4 = 12 vehicles',
  ]],
  ['SECTION D \u2013 Count and write  (4 marks)', [
    '1. Cows = 4      2. Hens = 6      3. Rabbits = 3      4. Horses = 2',
  ]],
  ['TOTAL: 20 marks', [
    '18\u201320 Excellent  \u2B50        14\u201317 Very Good        10\u201313 Good, keep practising',
    'Below 10 \u2013 Revise the chapter together, then try again.',
  ]],
];
for (const [head, lines] of key) {
  body.push(para(run(head, { b: true, sz: 23 }), { before: 120, after: 60 }));
  for (const ln of lines) body.push(para(run(ln, { sz: 22 }), { after: 70 }));
}

/* ------------------------------------------------------------------ */
/* Package parts                                                       */
/* ------------------------------------------------------------------ */
const W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"';
const R = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"';

const documentXml =
  `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>` +
  `<w:document ${W} ${R}><w:body>` +
  body.join('') +
  `<w:sectPr>` +
  `<w:footerReference w:type="default" r:id="rId3"/>` +
  `<w:pgSz w:w="11906" w:h="16838"/>` +
  `<w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="708" w:footer="708" w:gutter="0"/>` +
  `</w:sectPr></w:body></w:document>`;

const stylesXml =
  `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>` +
  `<w:styles ${W}>` +
  `<w:docDefaults><w:rPrDefault><w:rPr>` +
  `<w:rFonts w:ascii="Comic Sans MS" w:hAnsi="Comic Sans MS" w:cs="Comic Sans MS"/>` +
  `<w:sz w:val="22"/><w:szCs w:val="22"/>` +
  `</w:rPr></w:rPrDefault>` +
  `<w:pPrDefault><w:pPr><w:spacing w:after="100" w:line="240" w:lineRule="auto"/></w:pPr></w:pPrDefault>` +
  `</w:docDefaults>` +
  `<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>` +
  `</w:styles>`;

const footerXml =
  `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>` +
  `<w:ftr ${W}><w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="0"/></w:pPr>` +
  run('Worksheet Wonder  \u2022  Page ', { sz: 18, color: '888888' }) +
  `<w:r><w:rPr><w:rFonts w:ascii="Comic Sans MS" w:hAnsi="Comic Sans MS"/><w:color w:val="888888"/><w:sz w:val="18"/></w:rPr>` +
  `<w:fldChar w:fldCharType="begin"/></w:r>` +
  `<w:r><w:rPr><w:rFonts w:ascii="Comic Sans MS" w:hAnsi="Comic Sans MS"/><w:color w:val="888888"/><w:sz w:val="18"/></w:rPr>` +
  `<w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>` +
  `<w:r><w:rPr><w:rFonts w:ascii="Comic Sans MS" w:hAnsi="Comic Sans MS"/><w:color w:val="888888"/><w:sz w:val="18"/></w:rPr>` +
  `<w:fldChar w:fldCharType="end"/></w:r>` +
  `</w:p></w:ftr>`;

const contentTypes =
  `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>` +
  `<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">` +
  `<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>` +
  `<Default Extension="xml" ContentType="application/xml"/>` +
  `<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>` +
  `<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>` +
  `<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>` +
  `<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>` +
  `</Types>`;

const rootRels =
  `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>` +
  `<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">` +
  `<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>` +
  `<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>` +
  `</Relationships>`;

const docRels =
  `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>` +
  `<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">` +
  `<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>` +
  `<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>` +
  `</Relationships>`;

const now = new Date().toISOString().replace(/\.\d+Z$/, 'Z');
const coreXml =
  `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>` +
  `<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" ` +
  `xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" ` +
  `xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">` +
  `<dc:title>Grade 1 Mathematics - Data Handling Practice Question Paper</dc:title>` +
  `<dc:creator>Worksheet Wonder</dc:creator>` +
  `<cp:lastModifiedBy>Worksheet Wonder</cp:lastModifiedBy>` +
  `<dcterms:created xsi:type="dcterms:W3CDTF">${now}</dcterms:created>` +
  `<dcterms:modified xsi:type="dcterms:W3CDTF">${now}</dcterms:modified>` +
  `</cp:coreProperties>`;

/* ------------------------------------------------------------------ */
/* Build, write, verify                                                */
/* ------------------------------------------------------------------ */
const entries = [
  ['[Content_Types].xml', contentTypes],
  ['_rels/.rels', rootRels],
  ['docProps/core.xml', coreXml],
  ['word/document.xml', documentXml],
  ['word/styles.xml', stylesXml],
  ['word/footer1.xml', footerXml],
  ['word/_rels/document.xml.rels', docRels],
];

const outPath = path.join(__dirname, 'Grade1_Data_Handling_Question_Paper.docx');
fs.writeFileSync(outPath, buildZip(entries));

/* --- structural verification of the written file --- */
const buf = fs.readFileSync(outPath);
const eocdSig = buf.lastIndexOf(Buffer.from([0x50, 0x4b, 0x05, 0x06]));
if (eocdSig < 0) throw new Error('EOCD not found');
const count = buf.readUInt16LE(eocdSig + 10);
const cdOffset = buf.readUInt32LE(eocdSig + 16);
let p = cdOffset;
const seen = [];
for (let i = 0; i < count; i++) {
  if (buf.readUInt32LE(p) !== 0x02014b50) throw new Error(`bad central dir sig @${p}`);
  const nameLen = buf.readUInt16LE(p + 28);
  const crc = buf.readUInt32LE(p + 16);
  const size = buf.readUInt32LE(p + 24);
  const lfhOff = buf.readUInt32LE(p + 42);
  const name = buf.toString('utf8', p + 46, p + 46 + nameLen);
  if (buf.readUInt32LE(lfhOff) !== 0x04034b50) throw new Error(`bad local sig for ${name}`);
  const dataStart = lfhOff + 30 + buf.readUInt16LE(lfhOff + 26) + buf.readUInt16LE(lfhOff + 28);
  const data = buf.subarray(dataStart, dataStart + size);
  if (crc32(data) !== crc) throw new Error(`CRC mismatch for ${name}`);
  seen.push(`${name} (${size} B)`);
  p += 46 + nameLen;
}
console.log('OK:', outPath);
console.log(`Entries verified (${count}/${count}):`);
seen.forEach((s) => console.log('  \u2713 ' + s));
