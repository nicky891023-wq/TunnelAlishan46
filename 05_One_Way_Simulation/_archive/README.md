# ⚠ 隔離區——歷史過程檔，內含已知錯誤，勿直接沿用配方

接手請以 `../RUN_STATUS.md`＋`../docs/` 定版為準。本區價值＝「哪些路走不通、為什麼」。

## 分區

- **early_tests_0626_0701/**（原頂層 _archive_05_testfiles）：05 啟動期的研究/試錯全紀錄——門檻率定 tracks A–E、襯砌表示法實驗（E 折減/軟化/殼替代）、耦合 BC 研究、大小模 in-situ 迭代、Codex 審查判決（codex_*.txt）。**內含多個被推翻的結論**。
- **pre_redo_0628_0629/**：力平衡重做前的耦合鏈（couple_full4 等）＋審查文件。該輪驅動被 codex_overturn 判無效。
- **redo_runs_0701_0702/**：4 階段版大模與小模 driven runs 1–3。被 11 階段版取代（水位差過大→改漸升降）。
- **opus_0702/**：OPUS 的 small_staged 首版。
- **cap_tests_0703/**：shell cap 設計 5 輪短測。

## 試錯總結（犯過的錯，勿重複）

1. **`cmodel assign` 會重置全部 zone 屬性**——換本構後漏補 cohesion/friction/tension → c=φ=0 → q_th=0 → 100% creep-active＋零強度塑性崩壞（opus_0702 的 runaway 真因）。**換本構必附完整屬性清單。**
2. **邊界固定時機**：`zone gridpoint free velocity` 之後若把重新固定放到後面的相位 → 中間任何 solve 都在無邊界浮動箱上解（爆炸 −152m）。**tag 時就地 fix。**
3. **shell 應力是增量累積制**：`struct.shell.young` 折減只能擋未來增長、不消既有應力；且 cycling 中寫入不觸發勁度重組（需 solve 重啟或 struct.force.update）。**cap 要放在段界、單次執行**；被 cap 殼的應力值是虛擬記錄，襯砌受力交付量以耦合 PFC 模為準。
4. **勿在 creep 過程反覆 toggle 程序＋force.update 迭代**（cap 迭代版：能量注入失穩、隧道外脹 290mm）——官方 SEL 警語情境。
5. **`model solve creep time-total` 是累積制時鐘**——傳每階段時長會讓第 2 階段起只跑一步（大模 07-02 首跑）。用累積天數計數器。
6. **門檻 T 與初始態耦合**：無拉裸岩鬆弛後大片 zone 貼在包絡線上，T=0.6 乾態即 44–77% active、「低水位平」不可能；T=0.8（統一、大小模同值）才有 flat-then-onset。逐階段調 T=數值作弊（Wade 判定），遇水軟化是唯一可接受的解釋彈性。
7. **耦合 solve**：一次性釋放 in-situ 會剪退化 wall-zone facet（solveForX 系列崩潰 8+ 次）→ 必須 servo/漸進；`model mechanical timestep scale` 在 zone 側是官方 no-op；耦合短測要跑過 ~1500 cycles 驗 ratio 單調下降。
8. **驅動場**：剛體必須扣（Kabsch）且用「應變恆等 gate」證明無損；「殘差只佔位移 4%」不是傳遞失敗，是坡地平移本來就無應變貢獻。
