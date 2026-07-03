# Route B（已棄用，勿參考）
分離 rock tet + 結構 hex 襯砌殼 + zone attach by-face 的建法。
棄用原因：attach 產生洞壁 zero-stiffness gridpoint，solve elastic 直接停機。
現行版=Route C 共形建法（process/build_small_conformal.py）。rock.inp/lining.inp 已刪（可由本資料夾腳本重生）。
