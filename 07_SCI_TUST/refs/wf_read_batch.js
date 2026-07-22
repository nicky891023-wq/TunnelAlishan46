export const meta = {
  name: 'tust-read-batch',
  description: 'Deep-read one batch of references (quota-friendly)',
  phases: [{ title: 'Read', detail: 'one batch of per-paper deep readers' }],
}
phase('Read')
const S = {type:'object',properties:{
  access:{type:'string'}, note_file:{type:'string'},
  title_leads_with:{type:'string'}, method_words_in_title:{type:'boolean'},
  n_figs:{type:'integer'}, n_tables:{type:'integer'}, intro_paras:{type:'integer'},
  insights:{type:'array',items:{type:'string'}}},
  required:['access','note_file','title_leads_with','method_words_in_title','insights']}
const NOTES = 'C:/Users/Wade/Desktop/Tunnel_TX/07_SCI_TUST/refs/reading_notes'
const SCRATCH = 'C:/Users/Wade/AppData/Local/Temp/claude/C--Users-Wade-Desktop-Tunnel-TX/cbb5160b-36ec-49ec-b47c-cb290af4e241/scratchpad/papers'

function prompt(it) {
  return `深讀一篇期刊論文並萃取「寫作工藝」。目標文獻：
${it.authors} (${it.year}). ${it.title}. ${it.journal}. DOI: ${it.doi}

【省額度規則】先 Read 檢查 ${NOTES}/${it.id}.md 是否已存在且含 (a)-(h) 全部小節——
若完整，直接依它回傳結構化摘要，不重讀論文。

【取得全文，依序嘗試】
1. DOI 以 LOCAL: 開頭：該路徑是本機 docx，用 Bash python-docx 抽全文。
2. 本機 PDF：Glob C:/Users/Wade/Desktop/Wade_TD_SCI/Reference/**/*.pdf（含 trash/），
   以作者姓/年份/標題關鍵詞比對檔名；找到用 Read 分段讀完全文（每次≤20頁）。
3. 合法 OA：curl -s "https://api.openalex.org/works/doi:${it.doi}" 只看 best_oa_location.pdf_url；
   有就 curl -L -o "${SCRATCH}/${it.id}.pdf" 下載後 Read。【無直接 pdf_url 即放棄 OA，
   不爬 landing page、不試其他來源——省額度】嚴禁影子圖書館。
4. 皆無：curl -s "https://api.crossref.org/works/${it.doi}" 取 abstract；標 access=abstract-only。

【精讀鏡頭】(a) 題目解剖：開頭元素（案例/現象/機制/方法）、有無方法詞、構式
(b) 文章架構：節序與比重 (c) 前言手法：段數/各段角色/缺口staging/貢獻句式（轉述為主，
全文引語最多一句且<15字）(d) 結果敘事：圖領句?量化方式?機制詮釋? (e) 貢獻凸顯：位置與措辭
(f) 缺陷包裝：limitations 放哪、怎麼淡化（assumption/scope/future work/不提）
(g) 圖表數與類型 (h) 對我們（營運山岳鐵路隧道襯砌裂縫×地下水位循環×跨尺度FDM-DEM）啟示 2-4 條

【輸出】Write 繁中筆記 ${NOTES}/${it.id}.md（a-h 全節）＋回傳結構化摘要。
access ∈ {full-disk, full-oa, full-local, full-subscription, abstract-only}。`
}
const items = typeof args === 'string' ? JSON.parse(args) : args
const reads = await parallel(items.map(it => () =>
  agent(prompt(it), {label:`read:${it.id}`, phase:'Read', schema:S})))
const ok = reads.map((r,i)=>({r, it:items[i]})).filter(x=>x.r)
return {
  batch_done: ok.length, batch_total: items.length,
  access: ok.reduce((a,x)=>{a[x.r.access]=(a[x.r.access]||0)+1;return a},{}),
  abstract_only: ok.filter(x=>x.r.access==='abstract-only').map(x=>x.it.id),
  failed: reads.map((r,i)=>r?null:items[i].id).filter(Boolean),
}