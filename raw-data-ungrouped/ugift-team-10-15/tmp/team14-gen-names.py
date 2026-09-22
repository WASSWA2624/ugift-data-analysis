# -*- coding: utf-8 -*-
"""Build src/team14_media/names.py from chat bursts + OCR captions."""
from __future__ import annotations

import json
import os
import re
import sys
import textwrap

sys.path.insert(0, r"d:\coding\apps\ugift\src")
import team_registers as T

OCR_PATH = r"d:\coding\apps\ugift\tmp\team14-ocr.json"
OUT = r"d:\coding\apps\ugift\src\team14_media\names.py"

# Burst assignment from the chat, in send order. Already-filed originals are
# dropped later. start_at is the next NN in that folder (Simu Pondo already
# has 01).
BURSTS = [
    ("Sironko", "Simu Pondo HC III", 2, [
        "IMG-20260829-WA0505.jpg", "IMG-20260829-WA0524.jpg",
        "IMG-20260829-WA0519.jpg", "IMG-20260829-WA0546.jpg",
        "IMG-20260829-WA0541.jpg", "IMG-20260829-WA0512.jpg",
        "IMG-20260829-WA0526.jpg", "IMG-20260829-WA0534.jpg",
        "IMG-20260829-WA0535.jpg", "IMG-20260829-WA0516.jpg",
        "IMG-20260829-WA0530.jpg", "IMG-20260829-WA0510.jpg",
        "IMG-20260829-WA0525.jpg", "IMG-20260829-WA0529.jpg",
        "IMG-20260829-WA0521.jpg", "IMG-20260829-WA0520.jpg",
        "IMG-20260829-WA0514.jpg", "IMG-20260829-WA0509.jpg",
        "IMG-20260829-WA0506.jpg", "IMG-20260829-WA0527.jpg",
        "IMG-20260829-WA0515.jpg", "IMG-20260829-WA0543.jpg",
        "IMG-20260829-WA0517.jpg", "IMG-20260829-WA0511.jpg",
        "IMG-20260829-WA0536.jpg", "IMG-20260829-WA0545.jpg",
        "IMG-20260829-WA0539.jpg", "IMG-20260829-WA0537.jpg",
        "IMG-20260829-WA0528.jpg", "IMG-20260829-WA0538.jpg",
        "IMG-20260829-WA0540.jpg", "IMG-20260829-WA0532.jpg",
        "IMG-20260829-WA0522.jpg", "IMG-20260829-WA0513.jpg",
        "IMG-20260829-WA0542.jpg", "IMG-20260829-WA0523.jpg",
        "IMG-20260829-WA0544.jpg", "IMG-20260829-WA0507.jpg",
        "IMG-20260829-WA0508.jpg", "IMG-20260829-WA0533.jpg",
        "IMG-20260829-WA0531.jpg", "IMG-20260829-WA0518.jpg",
        "IMG-20260829-WA0504.jpg",
    ]),
    ("Sironko", "Bundege HC III", 1, [
        "IMG-20260829-WA0554.jpg", "IMG-20260829-WA0551.jpg",
        "IMG-20260829-WA0553.jpg", "IMG-20260829-WA0548.jpg",
        "IMG-20260829-WA0567.jpg", "IMG-20260829-WA0560.jpg",
        "IMG-20260829-WA0547.jpg", "IMG-20260829-WA0552.jpg",
        "IMG-20260829-WA0550.jpg", "IMG-20260829-WA0558.jpg",
        "IMG-20260829-WA0549.jpg", "IMG-20260829-WA0566.jpg",
        "IMG-20260829-WA0562.jpg", "IMG-20260829-WA0559.jpg",
        "IMG-20260829-WA0569.jpg", "IMG-20260829-WA0557.jpg",
        "IMG-20260829-WA0556.jpg", "IMG-20260829-WA0563.jpg",
        "IMG-20260829-WA0570.jpg", "IMG-20260829-WA0564.jpg",
        "IMG-20260829-WA0572.jpg", "IMG-20260829-WA0561.jpg",
        "IMG-20260829-WA0565.jpg", "IMG-20260829-WA0571.jpg",
        "IMG-20260829-WA0555.jpg", "IMG-20260829-WA0568.jpg",
    ]),
    ("Bulambuli", "Bulaago HC III", 1, [
        "IMG-20260830-WA0304.jpg", "IMG-20260830-WA0308.jpg",
        "IMG-20260830-WA0305.jpg", "IMG-20260830-WA0318.jpg",
        "IMG-20260830-WA0303.jpg", "IMG-20260830-WA0302.jpg",
        "IMG-20260830-WA0310.jpg", "IMG-20260830-WA0306.jpg",
        "IMG-20260830-WA0316.jpg", "IMG-20260830-WA0309.jpg",
        "IMG-20260830-WA0314.jpg", "IMG-20260830-WA0313.jpg",
        "IMG-20260830-WA0317.jpg", "IMG-20260830-WA0315.jpg",
        "IMG-20260830-WA0291.jpg", "IMG-20260830-WA0296.jpg",
        "IMG-20260830-WA0299.jpg", "IMG-20260830-WA0288.jpg",
        "IMG-20260830-WA0311.jpg", "IMG-20260830-WA0301.jpg",
        "IMG-20260830-WA0294.jpg", "IMG-20260830-WA0298.jpg",
        "IMG-20260830-WA0297.jpg", "IMG-20260830-WA0292.jpg",
        "IMG-20260830-WA0290.jpg", "IMG-20260830-WA0293.jpg",
        "IMG-20260830-WA0287.jpg", "IMG-20260830-WA0289.jpg",
        "IMG-20260830-WA0295.jpg", "IMG-20260830-WA0300.jpg",
        "IMG-20260830-WA0312.jpg", "IMG-20260830-WA0286.jpg",
        "IMG-20260830-WA0307.jpg",
    ]),
    ("Bulambuli", "Bwikhonge HC III", 1, [
        "IMG-20260830-WA0319.jpg", "IMG-20260830-WA0326.jpg",
        "IMG-20260830-WA0320.jpg", "IMG-20260830-WA0322.jpg",
        "IMG-20260830-WA0328.jpg", "IMG-20260830-WA0333.jpg",
        "IMG-20260830-WA0331.jpg", "IMG-20260830-WA0354.jpg",
        "IMG-20260830-WA0327.jpg", "IMG-20260830-WA0321.jpg",
        "IMG-20260830-WA0352.jpg", "IMG-20260830-WA0344.jpg",
        "IMG-20260830-WA0364.jpg", "IMG-20260830-WA0330.jpg",
        "IMG-20260830-WA0342.jpg", "IMG-20260830-WA0325.jpg",
        "IMG-20260830-WA0355.jpg", "IMG-20260830-WA0338.jpg",
        "IMG-20260830-WA0349.jpg", "IMG-20260830-WA0324.jpg",
        "IMG-20260830-WA0339.jpg", "IMG-20260830-WA0347.jpg",
        "IMG-20260830-WA0332.jpg", "IMG-20260830-WA0363.jpg",
        "IMG-20260830-WA0359.jpg", "IMG-20260830-WA0361.jpg",
        "IMG-20260830-WA0329.jpg", "IMG-20260830-WA0362.jpg",
        "IMG-20260830-WA0343.jpg", "IMG-20260830-WA0360.jpg",
        "IMG-20260830-WA0335.jpg", "IMG-20260830-WA0346.jpg",
        "IMG-20260830-WA0336.jpg", "IMG-20260830-WA0323.jpg",
        "IMG-20260830-WA0334.jpg", "IMG-20260830-WA0350.jpg",
        "IMG-20260830-WA0348.jpg", "IMG-20260830-WA0357.jpg",
        "IMG-20260830-WA0365.jpg", "IMG-20260830-WA0356.jpg",
        "IMG-20260830-WA0366.jpg", "IMG-20260830-WA0351.jpg",
        "IMG-20260830-WA0341.jpg", "IMG-20260830-WA0358.jpg",
        "IMG-20260830-WA0345.jpg", "IMG-20260830-WA0340.jpg",
        "IMG-20260830-WA0337.jpg", "IMG-20260830-WA0353.jpg",
        "IMG-20260831-WA0190.jpg", "IMG-20260831-WA0191.jpg",
        "IMG-20260831-WA0192.jpg", "IMG-20260831-WA0193.jpg",
        "IMG-20260831-WA0189.jpg",
    ]),
    ("Bulambuli", "Bunangaka HC III", 1, [
        "IMG-20260830-WA0421.jpg", "IMG-20260830-WA0391.jpg",
        "IMG-20260830-WA0418.jpg", "IMG-20260830-WA0367.jpg",
        "IMG-20260830-WA0369.jpg", "IMG-20260830-WA0370.jpg",
        "IMG-20260830-WA0419.jpg", "IMG-20260830-WA0403.jpg",
        "IMG-20260830-WA0404.jpg", "IMG-20260830-WA0368.jpg",
        "IMG-20260830-WA0422.jpg", "IMG-20260830-WA0387.jpg",
        "IMG-20260830-WA0396.jpg", "IMG-20260830-WA0390.jpg",
        "IMG-20260830-WA0424.jpg", "IMG-20260830-WA0414.jpg",
        "IMG-20260830-WA0411.jpg", "IMG-20260830-WA0388.jpg",
        "IMG-20260830-WA0406.jpg", "IMG-20260830-WA0400.jpg",
        "IMG-20260830-WA0385.jpg", "IMG-20260830-WA0383.jpg",
        "IMG-20260830-WA0416.jpg", "IMG-20260830-WA0378.jpg",
        "IMG-20260830-WA0375.jpg", "IMG-20260830-WA0395.jpg",
        "IMG-20260830-WA0372.jpg", "IMG-20260830-WA0410.jpg",
        "IMG-20260830-WA0412.jpg", "IMG-20260830-WA0397.jpg",
        "IMG-20260830-WA0408.jpg", "IMG-20260830-WA0407.jpg",
        "IMG-20260830-WA0402.jpg", "IMG-20260830-WA0401.jpg",
        "IMG-20260830-WA0386.jpg", "IMG-20260830-WA0405.jpg",
        "IMG-20260830-WA0382.jpg", "IMG-20260830-WA0377.jpg",
        "IMG-20260830-WA0371.jpg", "IMG-20260830-WA0373.jpg",
        "IMG-20260830-WA0389.jpg", "IMG-20260830-WA0394.jpg",
        "IMG-20260830-WA0379.jpg", "IMG-20260830-WA0409.jpg",
        "IMG-20260830-WA0415.jpg", "IMG-20260830-WA0420.jpg",
        "IMG-20260830-WA0417.jpg", "IMG-20260830-WA0399.jpg",
        "IMG-20260830-WA0413.jpg", "IMG-20260830-WA0423.jpg",
        "IMG-20260830-WA0384.jpg", "IMG-20260830-WA0392.jpg",
        "IMG-20260830-WA0393.jpg", "IMG-20260830-WA0376.jpg",
        "IMG-20260830-WA0398.jpg", "IMG-20260830-WA0374.jpg",
        "IMG-20260830-WA0381.jpg", "IMG-20260830-WA0380.jpg",
    ]),
    ("Bududa", "Nakatsi Seed Secondary School", 1, [
        "IMG-20260830-WA0434.jpg", "IMG-20260830-WA0439.jpg",
        "IMG-20260830-WA0426.jpg", "IMG-20260830-WA0425.jpg",
        "IMG-20260830-WA0431.jpg", "IMG-20260830-WA0428.jpg",
        "IMG-20260830-WA0427.jpg", "IMG-20260830-WA0441.jpg",
        "IMG-20260830-WA0437.jpg", "IMG-20260830-WA0438.jpg",
        "IMG-20260830-WA0429.jpg", "IMG-20260830-WA0435.jpg",
        "IMG-20260830-WA0430.jpg", "IMG-20260830-WA0440.jpg",
        "IMG-20260830-WA0436.jpg", "IMG-20260830-WA0432.jpg",
        "IMG-20260830-WA0433.jpg", "IMG-20260830-WA0442.jpg",
        "IMG-20260830-WA0444.jpg", "IMG-20260830-WA0443.jpg",
        "IMG-20260830-WA0445.jpg", "IMG-20260830-WA0447.jpg",
        "IMG-20260830-WA0446.jpg", "IMG-20260830-WA0460.jpg",
        "IMG-20260830-WA0498.jpg", "IMG-20260830-WA0512.jpg",
        "IMG-20260830-WA0504.jpg", "IMG-20260830-WA0496.jpg",
        "IMG-20260830-WA0511.jpg", "IMG-20260830-WA0476.jpg",
        "IMG-20260830-WA0488.jpg", "IMG-20260830-WA0510.jpg",
        "IMG-20260830-WA0451.jpg", "IMG-20260830-WA0492.jpg",
        "IMG-20260830-WA0508.jpg", "IMG-20260830-WA0479.jpg",
        "IMG-20260830-WA0499.jpg", "IMG-20260830-WA0491.jpg",
        "IMG-20260830-WA0500.jpg", "IMG-20260830-WA0477.jpg",
        "IMG-20260830-WA0487.jpg", "IMG-20260830-WA0481.jpg",
        "IMG-20260830-WA0455.jpg", "IMG-20260830-WA0458.jpg",
        "IMG-20260830-WA0465.jpg", "IMG-20260830-WA0462.jpg",
        "IMG-20260830-WA0502.jpg", "IMG-20260830-WA0471.jpg",
        "IMG-20260830-WA0448.jpg", "IMG-20260830-WA0473.jpg",
        "IMG-20260830-WA0468.jpg", "IMG-20260830-WA0480.jpg",
        "IMG-20260830-WA0489.jpg", "IMG-20260830-WA0507.jpg",
        "IMG-20260830-WA0509.jpg", "IMG-20260830-WA0501.jpg",
        "IMG-20260830-WA0485.jpg", "IMG-20260830-WA0475.jpg",
        "IMG-20260830-WA0469.jpg", "IMG-20260830-WA0497.jpg",
        "IMG-20260830-WA0483.jpg", "IMG-20260830-WA0457.jpg",
        "IMG-20260830-WA0472.jpg", "IMG-20260830-WA0495.jpg",
        "IMG-20260830-WA0450.jpg", "IMG-20260830-WA0464.jpg",
        "IMG-20260830-WA0478.jpg", "IMG-20260830-WA0466.jpg",
        "IMG-20260830-WA0486.jpg", "IMG-20260830-WA0454.jpg",
        "IMG-20260830-WA0490.jpg", "IMG-20260830-WA0467.jpg",
        "IMG-20260830-WA0452.jpg", "IMG-20260830-WA0493.jpg",
        "IMG-20260830-WA0449.jpg", "IMG-20260830-WA0503.jpg",
        "IMG-20260830-WA0459.jpg", "IMG-20260830-WA0494.jpg",
        "IMG-20260830-WA0470.jpg", "IMG-20260830-WA0453.jpg",
        "IMG-20260830-WA0461.jpg", "IMG-20260830-WA0482.jpg",
        "IMG-20260830-WA0506.jpg", "IMG-20260830-WA0505.jpg",
        "IMG-20260830-WA0463.jpg", "IMG-20260830-WA0484.jpg",
        "IMG-20260830-WA0474.jpg", "IMG-20260830-WA0456.jpg",
    ]),
    ("Bududa", "Bubungi HC III", 1, [
        "IMG-20260830-WA0514.jpg", "IMG-20260830-WA0526.jpg",
        "IMG-20260830-WA0536.jpg", "IMG-20260830-WA0528.jpg",
        "IMG-20260830-WA0516.jpg", "IMG-20260830-WA0537.jpg",
        "IMG-20260830-WA0515.jpg", "IMG-20260830-WA0517.jpg",
        "IMG-20260830-WA0533.jpg", "IMG-20260830-WA0548.jpg",
        "IMG-20260830-WA0552.jpg", "IMG-20260830-WA0524.jpg",
        "IMG-20260830-WA0532.jpg", "IMG-20260830-WA0530.jpg",
        "IMG-20260830-WA0550.jpg", "IMG-20260830-WA0531.jpg",
        "IMG-20260830-WA0519.jpg", "IMG-20260830-WA0520.jpg",
        "IMG-20260830-WA0539.jpg", "IMG-20260830-WA0575.jpg",
        "IMG-20260830-WA0583.jpg", "IMG-20260830-WA0544.jpg",
        "IMG-20260830-WA0543.jpg", "IMG-20260830-WA0545.jpg",
        "IMG-20260830-WA0540.jpg", "IMG-20260830-WA0522.jpg",
        "IMG-20260830-WA0527.jpg", "IMG-20260830-WA0566.jpg",
        "IMG-20260830-WA0523.jpg", "IMG-20260830-WA0547.jpg",
        "IMG-20260830-WA0529.jpg", "IMG-20260830-WA0521.jpg",
        "IMG-20260830-WA0534.jpg", "IMG-20260830-WA0576.jpg",
        "IMG-20260830-WA0541.jpg", "IMG-20260830-WA0546.jpg",
        "IMG-20260830-WA0551.jpg", "IMG-20260830-WA0535.jpg",
        "IMG-20260830-WA0579.jpg", "IMG-20260830-WA0542.jpg",
        "IMG-20260830-WA0549.jpg", "IMG-20260830-WA0559.jpg",
        "IMG-20260830-WA0564.jpg", "IMG-20260830-WA0567.jpg",
        "IMG-20260830-WA0581.jpg", "IMG-20260830-WA0560.jpg",
        "IMG-20260830-WA0554.jpg", "IMG-20260830-WA0562.jpg",
        "IMG-20260830-WA0563.jpg", "IMG-20260830-WA0578.jpg",
        "IMG-20260830-WA0557.jpg", "IMG-20260830-WA0569.jpg",
        "IMG-20260830-WA0565.jpg", "IMG-20260830-WA0553.jpg",
        "IMG-20260830-WA0561.jpg", "IMG-20260830-WA0556.jpg",
        "IMG-20260830-WA0525.jpg", "IMG-20260830-WA0573.jpg",
        "IMG-20260830-WA0570.jpg", "IMG-20260830-WA0584.jpg",
        "IMG-20260830-WA0555.jpg", "IMG-20260830-WA0518.jpg",
        "IMG-20260830-WA0538.jpg", "IMG-20260830-WA0580.jpg",
        "IMG-20260830-WA0568.jpg", "IMG-20260830-WA0582.jpg",
        "IMG-20260830-WA0558.jpg", "IMG-20260830-WA0574.jpg",
        "IMG-20260830-WA0577.jpg", "IMG-20260830-WA0572.jpg",
        "IMG-20260830-WA0571.jpg",
    ]),
    # 13:02 photos follow the Bumugibole note. Several frames are cut
    # BUMU/2020-2021/UGIFT or painted MUGIBOLE; the Bunamono note at the
    # tail of the same send is the next facility, not these photographs.
    ("Bulambuli", "Bumugibole HC III", 1, [
        "IMG-20260831-WA0203.jpg", "IMG-20260831-WA0206.jpg",
        "IMG-20260831-WA0197.jpg", "IMG-20260831-WA0213.jpg",
        "IMG-20260831-WA0202.jpg", "IMG-20260831-WA0200.jpg",
        "IMG-20260831-WA0207.jpg", "IMG-20260831-WA0194.jpg",
        "IMG-20260831-WA0214.jpg", "IMG-20260831-WA0195.jpg",
        "IMG-20260831-WA0196.jpg", "IMG-20260831-WA0208.jpg",
        "IMG-20260831-WA0216.jpg", "IMG-20260831-WA0212.jpg",
        "IMG-20260831-WA0218.jpg", "IMG-20260831-WA0210.jpg",
        "IMG-20260831-WA0209.jpg", "IMG-20260831-WA0201.jpg",
        "IMG-20260831-WA0205.jpg", "IMG-20260831-WA0215.jpg",
        "IMG-20260831-WA0211.jpg", "IMG-20260831-WA0204.jpg",
        "IMG-20260831-WA0199.jpg", "IMG-20260831-WA0221.jpg",
        "IMG-20260831-WA0217.jpg", "IMG-20260831-WA0220.jpg",
        "IMG-20260831-WA0219.jpg", "IMG-20260831-WA0222.jpg",
        "IMG-20260831-WA0198.jpg",
    ]),
    # Sent with the Bushiribo note; the frames themselves are cut
    # BUD/DLG/BUNAMONO HC III.
    ("Bududa", "Bunamono HC III", 1, [
        "IMG-20260831-WA0175.jpg", "IMG-20260831-WA0176.jpg",
        "IMG-20260831-WA0177.jpg", "IMG-20260831-WA0179.jpg",
        "IMG-20260831-WA0181.jpg", "IMG-20260831-WA0178.jpg",
        "IMG-20260831-WA0180.jpg", "IMG-20260831-WA0184.jpg",
        "IMG-20260831-WA0185.jpg", "IMG-20260831-WA0183.jpg",
        "IMG-20260831-WA0188.jpg", "IMG-20260831-WA0186.jpg",
        "IMG-20260831-WA0182.jpg", "IMG-20260831-WA0187.jpg",
    ]),
    # Classroom furniture and the school block, sent a minute later.
    ("Bududa", "Bushiribo Seed Secondary School", 1, [
        "IMG-20260831-WA0174.jpg", "IMG-20260831-WA0165.jpg",
        "IMG-20260831-WA0167.jpg", "IMG-20260831-WA0166.jpg",
        "IMG-20260831-WA0173.jpg", "IMG-20260831-WA0171.jpg",
        "IMG-20260831-WA0172.jpg", "IMG-20260831-WA0168.jpg",
        "IMG-20260831-WA0170.jpg", "IMG-20260831-WA0169.jpg",
    ]),
    ("Bududa", "Bumusi HC III", 1, [
        "IMG-20260831-WA0250.jpg", "IMG-20260831-WA0225.jpg",
        "IMG-20260831-WA0249.jpg", "IMG-20260831-WA0248.jpg",
        "IMG-20260831-WA0232.jpg", "IMG-20260831-WA0238.jpg",
        "IMG-20260831-WA0227.jpg", "IMG-20260831-WA0228.jpg",
        "IMG-20260831-WA0229.jpg", "IMG-20260831-WA0244.jpg",
        "IMG-20260831-WA0226.jpg", "IMG-20260831-WA0224.jpg",
        "IMG-20260831-WA0235.jpg", "IMG-20260831-WA0236.jpg",
        "IMG-20260831-WA0241.jpg", "IMG-20260831-WA0247.jpg",
        "IMG-20260831-WA0242.jpg", "IMG-20260831-WA0245.jpg",
        "IMG-20260831-WA0246.jpg", "IMG-20260831-WA0243.jpg",
        "IMG-20260831-WA0233.jpg", "IMG-20260831-WA0237.jpg",
        "IMG-20260831-WA0223.jpg", "IMG-20260831-WA0231.jpg",
        "IMG-20260831-WA0239.jpg", "IMG-20260831-WA0240.jpg",
        "IMG-20260831-WA0251.jpg", "IMG-20260831-WA0230.jpg",
        "IMG-20260831-WA0234.jpg",
        "IMG-20260831-WA0315.jpg", "IMG-20260831-WA0291.jpg",
        "IMG-20260831-WA0316.jpg", "IMG-20260831-WA0318.jpg",
        "IMG-20260831-WA0320.jpg", "IMG-20260831-WA0299.jpg",
        "IMG-20260831-WA0319.jpg", "IMG-20260831-WA0286.jpg",
        "IMG-20260831-WA0290.jpg", "IMG-20260831-WA0302.jpg",
        "IMG-20260831-WA0260.jpg", "IMG-20260831-WA0308.jpg",
        "IMG-20260831-WA0313.jpg", "IMG-20260831-WA0294.jpg",
        "IMG-20260831-WA0300.jpg", "IMG-20260831-WA0298.jpg",
        "IMG-20260831-WA0295.jpg", "IMG-20260831-WA0305.jpg",
        "IMG-20260831-WA0293.jpg", "IMG-20260831-WA0307.jpg",
        "IMG-20260831-WA0310.jpg", "IMG-20260831-WA0314.jpg",
        "IMG-20260831-WA0317.jpg", "IMG-20260831-WA0297.jpg",
        "IMG-20260831-WA0304.jpg", "IMG-20260831-WA0306.jpg",
        "IMG-20260831-WA0303.jpg", "IMG-20260831-WA0309.jpg",
        "IMG-20260831-WA0292.jpg", "IMG-20260831-WA0312.jpg",
        "IMG-20260831-WA0311.jpg", "IMG-20260831-WA0301.jpg",
        "IMG-20260831-WA0296.jpg",
    ]),
    ("Bulambuli", "Bumufuni Seed Secondary School", 1, [
        "IMG-20260831-WA0252.jpg", "IMG-20260831-WA0254.jpg",
    ]),
]

# OCR text that reassigns a photo away from its burst.
REASSIGN = [
    (r"BUNDEGE", ("Sironko", "Bundege HC III")),
    (r"SIMU\s*PONDO|SIMUPONDO", ("Sironko", "Simu Pondo HC III")),
    (r"BULAAGO|BULAAGA", ("Bulambuli", "Bulaago HC III")),
    (r"BWIKHONGE", ("Bulambuli", "Bwikhonge HC III")),
    (r"BUNANGAKA", ("Bulambuli", "Bunangaka HC III")),
    (r"BUMUFUNI|BUNAMUTI", ("Bulambuli", "Bumufuni Seed Secondary School")),
    (r"BUMUGIBOL|BUMUGIBOR|MUGIBOLE|BUMU/?\s*2020|RUMU/?\s*2020|PUMI/?1?20", ("Bulambuli", "Bumugibole HC III")),
    (r"NAKATSI|NAKATST", ("Bududa", "Nakatsi Seed Secondary School")),
    (r"BUBUNGI", ("Bududa", "Bubungi HC III")),
    (r"BUNAMONO|BUNAMQN|BUNAMOND|BUNA\s*NONO|BUD/?\s*/?\s*LG/?\s*/?\s*BUNA", ("Bududa", "Bunamono HC III")),
    (r"BUSHIRIBO", ("Bududa", "Bushiribo Seed Secondary School")),
    (r"BUMUSI", ("Bududa", "Bumusi HC III")),
    (r"BUDUDA HEALTH|BUDUDA HC", ("Bududa", "Bududa HC III")),
]

SPELL = [
    (r"labaratory", "laboratory"),
    (r"kangaro\b", "kangaroo"),
    (r"martenity", "maternity"),
    (r"planing", "planning"),
    (r"surggeries", "surgeries"),
    (r"refferal", "referral"),
    (r"heath\b", "health"),
    (r"centreiii", "centre-iii"),
    (r"h/c", "hc"),
    (r"windo[ws]+", "windows"),
    (r"locakable", "lockable"),
    (r"cabinents", "cabinets"),
    (r"todlers", "toddlers"),
    (r"cyclinders", "cylinders"),
    (r"auto clave", "autoclave"),
    (r"filling", "filing"),
    (r"healthy centre", "health-centre"),
    (r"wadrope", "wardrobe"),
    (r"cyclinder", "cylinder"),
    (r"gaslcylinder", "gas-cylinder"),
    (r"holderst", "holders"),
    (r"\bitrs\b", "litres"),
    (r"glovc", "glove"),
]

DROP_LINE = re.compile(
    r"^(allk|ton|ok|yes|no|\d+|l/min|o2|sn|gou|moh)$", re.I)

FACILITY_LINE = re.compile(
    r"bundege|simu\s*pondo|bulaago|bulaaga|bwikhonge|bunangaka|"
    r"bumufuni|bumugibol|mugibole|nakats[it]|bubungi|bunamono|buna\s*nono|"
    r"bushiribo|bumusi|bududa|sisiyi|mutufu|kamu|buyobo|buyaya|buteza|bugitimwa",
    re.I)


def already_mapped():
    mapped = set()
    cfg = T.TEAMS["team-14"]
    for _d, c in cfg["districts"].items():
        mapped.update(c.get("lg_docs", {}))
        for _fac, files in c.get("facilities", {}).items():
            mapped.update(files)
    mapped |= T.SKIP
    return mapped


def slug_desc(texts):
    candidates = []
    facility_hit = False
    for t in texts or []:
        t = t.strip()
        if len(t) < 3 or DROP_LINE.match(t):
            continue
        if FACILITY_LINE.search(t) and len(t) < 40:
            facility_hit = True
            continue
        candidates.append(t)
    raw = max(candidates, key=len) if candidates else ""
    if not raw:
        long = [t for t in (texts or []) if len(t) >= 8]
        raw = long[0] if long else ("facility-signboard" if facility_hit
                                    else "uncaptioned-asset")
    s = raw.lower()
    for pat, rep in SPELL:
        s = re.sub(pat, rep, s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    s = re.sub(r"-{2,}", "-", s)
    if not s or _garbage(s):
        s = "facility-signboard" if facility_hit else "uncaptioned-asset"
    return s[:70]


OK_WORD = re.compile(
    r"bed|chair|couch|tank|scale|autoclave|locker|cabinet|stool|table|"
    r"microscope|concentrator|suction|fridge|refrigerator|freezer|cot|"
    r"trolley|stretcher|wheelchair|bin|bucket|desk|bench|computer|"
    r"printer|projector|screen|latrine|toilet|block|gate|sign|"
    r"laborator|maternit|ward|oxygen|cylinder|weighing|examination|"
    r"delivery|solar|water|staff|classroom|welcome|fence|compound|"
    r"house|quarter|batter|panel|stove|instrument|wardrobe|shelf|"
    r"teacher|wifi|condition|recliner|dialysis|hydraulic|manual|"
    r"adult|height|meter|measuring|holder|tube|pit|lockable|steel|"
    r"toddler|resuscit|watch|filing|kangaroo|drip|stand|pediatric|"
    r"mattress|baby|inventory|education|difference|facility|"
    r"uncaptioned|cupboard|signboard|sluice|bowl|machine|services|"
    r"mission|vision|health|window|door|ramp|porch|latrine|privacy|"
    r"oxygen|gas|lockable|steril|centrifuge|microscope|binocular|"
    r"photocop|scanner|router|switch|server|camera|fire|extinguish|"
    r"blackboard|whiteboard|locker|cupboard|shelf|rack|trolley",
    re.I)


def _garbage(s):
    if s in ("uncaptioned-asset", "facility-signboard"):
        return False
    letters = [c for c in s if c.isalpha()]
    if len(letters) < 8:
        return True
    vowels = sum(c in "aeiou" for c in letters)
    if vowels / len(letters) < 0.22:
        return True
    parts = [p for p in s.split("-") if p]
    if parts and sum(1 for p in parts if len(p) <= 2) > len(parts) * 0.5:
        return True
    if not OK_WORD.search(s):
        return True
    return False


def ref_id(fn):
    m = re.search(r"IMG-(\d{8})-WA(\d{4})", fn)
    if not m:
        return "ref-unknown"
    return "ref%s-%s" % (m.group(1), m.group(2))


def why(texts, assigned, reassigned):
    overlay = " / ".join((texts or [])[:4]) or "no readable overlay"
    if reassigned:
        return (
            "Team overlay or marking on the photograph: %s. Filed under %s "
            "from that marking rather than from the batch it was sent with."
            % (overlay[:180], assigned[1])
        )
    if texts:
        return "Team overlay on the photograph: %s." % overlay[:180]
    return "Uncaptioned. Named from what the photograph shows."


def main():
    ocr = {}
    if os.path.isfile(OCR_PATH):
        ocr = json.load(open(OCR_PATH, encoding="utf-8"))
    mapped = already_mapped()
    placed = {}  # fn -> (district, fac)
    reassigned = set()
    for district, fac, _start, files in BURSTS:
        for fn in files:
            if fn in mapped:
                continue
            placed[fn] = (district, fac)

    # Files in the export that no burst claimed: assign from OCR if a
    # facility name is on the frame, otherwise leave them for the leftover
    # print so they can be placed by hand.
    wa = r"d:\coding\apps\ugift\tmp\team14-wa\all"
    leftover = []
    if os.path.isdir(wa):
        for fn in sorted(os.listdir(wa)):
            if not fn.lower().endswith(".jpg"):
                continue
            if fn in mapped or fn in placed:
                continue
            blob = " ".join(ocr.get(fn, []))
            dest = None
            for pat, d in REASSIGN:
                if re.search(pat, blob, re.I):
                    dest = d
                    break
            if dest:
                placed[fn] = dest
                reassigned.add(fn)
            else:
                leftover.append(fn)

    # OCR reassignment of burst photos that carry another facility's mark
    for fn, (district, fac) in list(placed.items()):
        blob = " ".join(ocr.get(fn, []))
        for pat, dest in REASSIGN:
            if re.search(pat, blob, re.I) and dest != (district, fac):
                placed[fn] = dest
                reassigned.add(fn)
                break

    # number per facility
    order = {}
    starts = {}
    for district, fac, start, files in BURSTS:
        starts[(district, fac)] = start
        order.setdefault((district, fac), [])
    for district, fac, start, files in BURSTS:
        for fn in files:
            if fn in placed and placed[fn] == (district, fac):
                if fn not in order[(district, fac)]:
                    order[(district, fac)].append(fn)
    # extras reassigned into a facility
    for fn, dest in placed.items():
        if fn not in order.setdefault(dest, []):
            order[dest].append(fn)

    names = {}
    used_desc = {}
    for key, files in order.items():
        nn = starts.get(key, 1)
        seen = {}
        for fn in files:
            if fn not in placed or placed[fn] != key:
                continue
            texts = ocr.get(fn, [])
            desc = slug_desc(texts)
            k = (key, desc)
            seen[desc] = seen.get(desc, 0) + 1
            if seen[desc] > 1:
                desc = "%s-view-%d" % (desc, seen[desc])
            new = "%02d_%s_%s.jpg" % (nn, desc, ref_id(fn))
            names.setdefault(key, {})[fn] = (
                new, why(texts, key, fn in reassigned))
            nn += 1

    # write
    lines = [
        "# -*- coding: utf-8 -*-",
        '"""New Team 14 photograph names. Generated from the later WhatsApp',
        "export; do not rename photographs already filed in team_registers.py.",
        '"""',
        "NAMES = {",
    ]
    for key in sorted(names, key=lambda k: (k[0], k[1])):
        lines.append(" (%r, %r): {" % key)
        for fn, (new, reason) in names[key].items():
            reason = reason.replace("\\", "\\\\").replace('"', '\\"')
            lines.append("  %r:" % fn)
            lines.append("   (%r," % new)
            wrapped = textwrap.fill(
                reason, width=88, initial_indent='    "',
                subsequent_indent='    "')
            # simpler: one string
            lines[-1] = "   (%r," % new
            lines.append("    %r)," % reason)
        lines.append(" },")
    lines.append("}")
    open(OUT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("wrote", OUT, "files", sum(len(v) for v in names.values()),
          "facilities", len(names), "reassigned", len(reassigned),
          "ocr", len(ocr), "leftover", len(leftover))
    if leftover:
        print("LEFTOVER")
        for fn in leftover:
            print(" ", fn, ocr.get(fn, [])[:6])


if __name__ == "__main__":
    main()
