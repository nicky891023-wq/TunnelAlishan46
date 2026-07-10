# ⚠ 無效跑次診斷檔（07-04 17:20–19:24，凍結岩箱 staged）— 勿當成果使用

本目錄 = couple_staged_v2 第一次啟動的 CONTROL-0 與 stage 1 輸出。該輪**無效**：
Couple_Initial(free2) 繼承了 couple_servo_v6:47 的 `zone gridpoint fix velocity`
（球安裝期全域凍岩，從未解凍）→ 岩箱是剛性模具，驅動只拖動邊界皮層。

證據（本目錄檔案可重演）：
- log 收斂行 `mech Zone Main (0.0000e+00)`＝zone 側殘差恆零＝gp 全固定。
- cs_s1_cwall：解讀帶(y870-900)洞壁 |u|=0.000mm；小模同帶 med 3.56mm → G2 全敗。
- cs_s1_cracks：18,683 條新裂縫 100% 在兩端環（y860-865: 8412、y905-910: 10271）
  ＝被驅動的端面岩壁 vs 不動端平台把端環剪爆的假象；解讀帶零新增（僅 42 條底噪簇）。

教訓：**staged gate 必須檢查 zone ratio 有參與收斂**（恆 0.0000e+00 = 傳遞介質根本沒變形）。
處置：STEP G（couple_stepG_freerock.f3dat）→ Couple_Initial_G → staged 重跑。
