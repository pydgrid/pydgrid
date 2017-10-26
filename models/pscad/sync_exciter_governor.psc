PSCAD 4.2.0

Settings
 {
 Id = "913240978.1508852396"
 Author = "jayas.Ingelectus"
 Desc = "GENERATOR WITH GOVERNER/EXCITER"
 Arch = "windows"
 Options = 0
 Build = 6
 Warn = 1
 Check = 15
 Libs = ""
 Source = ""
 RunInfo = 
  {
  Fin = 5
  Step = 5e-005
  Plot = 0.01
  Chat = 0.001
  Brch = 0.0005
  Lat = 100
  Options = 0
  Advanced = 511
  Debug = 0
  StartFile = ""
  OFile = "Untitled.out"
  SFile = "AutoSnap.snp"
  SnapTime = 0.3
  Mruns = 10
  Mrunfile = 0
  StartType = 0
  PlotType = 0
  SnapType = 0
  MrunType = "mrun"
  }

 }

Definitions
 {
 Module("Main")
  {
  Desc = " EXAMPLE 11"
  FileDate = 1508852326
  Nodes = 
   {
   }

  Graphics = 
   {
   Rectangle(-18,-18,18,18)
   }


  Page(A/A4,Portrait,144,[960,452],100)
   {
   0.annotation([450,648],0,0,-1)
    {
    AL1 = "2 PU"
    AL2 = "RESISTANCE"
    }
   0.ground([450,612],1,0,-1)
    {
    }
   0.resistor([450,612],3,0,-1)
    {
    R = "0.1 [ohm]"
    }
   0.sync_machine([288,468],0,0,90)
    {
    Name = "HydroGener"
    Nqaxw = "1"
    Cnfg = "0"
    MM = "1"
    CfRa = "1"
    MSat = "0"
    icTyp = "1"
    Iscl = "0"
    View = "1"
    itrfa = "0"
    izro = "0"
    Icsp = "0"
    Icmp = "0"
    Immd = "0"
    Ifmlt = "0"
    Term = "3"
    Ts = "0.02 [s]"
    Iexc = "1"
    Igov = "1"
    Ospd = "1"
    machsw = "S2M"
    Enab = "LRR"
    npadjs = "0"
    pset = "0.0 [MW]"
    nftrsw = "0"
    hmult = "1.0"
    sdmftr = "1.0"
    sdmspd = "1.0"
    npadjm = "0"
    fldmlt = "1.0"
    nfldsw = "0"
    Vbase = "7.967 [kV]"
    Ibase = "5.02 [kA]"
    OMO = "376.992 [rad/s]"
    H = "3.117 [s]"
    D = "0.0 [pu]"
    RNeut = "1.0E4 [pu]"
    XNeut = "0.0 [pu]"
    Ri = "300.0 [pu]"
    NOM = "1.0"
    Rs1 = "0.002 [pu]"
    XS1 = "0.14 [pu]"
    XMD0 = "1.66 [pu]"
    R2D = "1.4068E-03 [pu]"
    X2D = "6.1789E-02 [pu]"
    R3D = "4.0699E-03 [pu]"
    X3D = "5.4581E-03 [pu]"
    X230 = "0.0 [pu]"
    XMQ = "1.58 [pu]"
    R2Q = "1.4145E-02 [pu]"
    X2Q = "0.32928 [pu]"
    R3Q = "8.1942E-03 [pu]"
    X3Q = "9.4199E-02 [pu]"
    X231 = "0.0 [pu]"
    Ra = "0.0051716 [pu]"
    Ta = "0.332 [s]"
    Xp = "0.163 [pu]"
    Xd = "1.014 [pu]"
    Xd' = "0.314 [pu]"
    Tdo' = "6.55 [s]"
    Xd'' = "0.28 [pu]"
    Tdo'' = "0.039 [s]"
    Gfld = "1.0E+2 [pu]"
    Xkf = "1.0E+2 [pu]"
    Xq = "0.77 [pu]"
    Xq' = "0.228 [pu]"
    Tqo' = "0.85 [s]"
    Xq'' = "0.375 [pu]"
    Tqo'' = "0.071 [s]"
    AGFC = "1.0"
    X1 = "0.0"
    Y1 = "0.0 [pu]"
    X2 = "0.5"
    Y2 = "0.5 [pu]"
    X3 = "0.8"
    Y3 = "0.8 [pu]"
    X4 = "1.0"
    Y4 = "1.0 [pu]"
    X5 = "1.2"
    Y5 = "1.2 [pu]"
    X6 = "1.5"
    Y6 = "1.5 [pu]"
    X7 = "1.8"
    Y7 = "1.8 [pu]"
    X8 = "2.2"
    Y8 = "2.2 [pu]"
    X9 = "3.2"
    Y9 = "3.2 [pu]"
    X10 = "4.2"
    Y10 = "4.2 [pu]"
    VT = "1.0 [pu]"
    Pheta = "0.0 [rad]"
    Trmpv = "0.1 [s]"
    Sysfl = "100.0 [pu]"
    Ptcon = "0.2 [s]"
    P0 = "60.0 [MW]"
    Q0 = "0.0 [MVAR]"
    Theti = "3.141592 [rad]"
    Idi = "0.0 [pu]"
    Iqi = "0.0 [pu]"
    Ifi = "0.0 [pu]"
    Spdi = "1.0 [pu]"
    POut = "POUT"
    QOut = "QOUT"
    Vneut = ""
    Cneut = ""
    Lang = ""
    Theta = "Rang"
    Wang = ""
    Tesmt = ""
    PQscl = "0"
    InExc = "InitEx"
    InGov = "InitGv"
    Mon1 = "1"
    Chn1 = ""
    Mon2 = "1"
    Chn2 = ""
    Mon3 = "1"
    Chn3 = ""
    Mon4 = "1"
    Chn4 = ""
    Mon5 = "1"
    Chn5 = ""
    Mon6 = "1"
    Chn6 = ""
    }
   -Wire-([324,468],0,0,-1)
    {
    Vertex="0,0;54,0"
    }
   0.datalabel([216,594],4,0,-1)
    {
    Name = "W"
    }
   0.timerdefn([288,1044],0,0,50)
    {
    Timsw = "0.3 [s]"
    }
   0.timerdefn([108,1044],4,0,40)
    {
    Timsw = "0.4 [s]"
    }
   0.pgb([306,918],0,26797984,30)
    {
    Name = "TERMINAL VOLTAGE"
    Group = "Terminal Voltage"
    Display = "0"
    Scale = "1.0"
    Units = "kV"
    mrun = "0"
    Pol = "0"
    Min = "0"
    Max = "20"
    }
   -Wire-([252,396],0,0,-1)
    {
    Vertex="0,0;0,-54"
    }
   -Wire-([288,396],0,0,-1)
    {
    Vertex="0,0;0,-54"
    }
   0.annotation([144,1080],0,0,-1)
    {
    AL1 = "Enab Mech Dynamics"
    AL2 = "0->1 @ 0.4 Sec"
    }
   0.annotation([270,1080],0,0,-1)
    {
    AL1 = "Change to Machine"
    AL2 = "0->1 @ 0.3 Sec"
    }
   0.datalabel([252,378],1,0,-1)
    {
    Name = "EF"
    }
   0.datalabel([288,378],3,0,-1)
    {
    Name = "IF"
    }
   0.datalabel([288,558],2,0,-1)
    {
    Name = "TM"
    }
   0.pgb([306,954],0,26801768,150)
    {
    Name = "FIELD VOLTAGE"
    Group = "Field Voltage"
    Display = "0"
    Scale = "1.0"
    Units = "pu"
    mrun = "0"
    Pol = "0"
    Min = "0"
    Max = "3.5"
    }
   0.pgb([126,954],0,26802680,170)
    {
    Name = "REAL POWER"
    Group = "Synchronous Machine"
    Display = "0"
    Scale = "120"
    Units = "MW"
    mrun = "0"
    Pol = "0"
    Min = "0"
    Max = "120"
    }
   0.pgb([126,990],0,26927336,140)
    {
    Name = "REACTIVE POWER"
    Group = "Synchronous Machine"
    Display = "0"
    Scale = "120"
    Units = "MVAR"
    mrun = "0"
    Pol = "0"
    Min = "0"
    Max = "120"
    }
   -Wire-([90,954],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   -Wire-([90,990],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.datalabel([90,954],0,0,-1)
    {
    Name = "POUT"
    }
   0.datalabel([90,990],0,0,-1)
    {
    Name = "QOUT"
    }
   0.pgb([216,954],0,26930224,160)
    {
    Name = "MECHANICAL TORQUE"
    Group = "Synchronous Machine"
    Display = "0"
    Scale = "1.0"
    Units = "pu"
    mrun = "0"
    Pol = "0"
    Min = "0"
    Max = "0.6"
    }
   -Wire-([180,954],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   -Wire-([270,954],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.datalabel([270,954],0,0,-1)
    {
    Name = "EF"
    }
   0.datalabel([180,954],0,0,-1)
    {
    Name = "TM"
    }
   0.datalabel([522,1044],3,0,-1)
    {
    Name = "BRK"
    }
   0.annotation([504,1080],0,0,-1)
    {
    AL1 = "Close Breaker"
    AL2 = "@ 1.0 Sec."
    }
   0.datalabel([270,990],0,0,-1)
    {
    Name = "IF"
    }
   -Wire-([270,990],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.pgb([306,990],0,26912296,120)
    {
    Name = "FIELD CURRENT"
    Group = "Field Current"
    Display = "0"
    Scale = "1.0"
    Units = "pu"
    mrun = "0"
    Pol = "0"
    Min = "0"
    Max = "1.8"
    }
   0.datalabel([180,990],0,0,-1)
    {
    Name = "W"
    }
   -Wire-([180,990],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.pgb([216,990],0,26914592,130)
    {
    Name = "OMEGA"
    Group = "Synchronous Machine"
    Display = "0"
    Scale = "376.99118"
    Units = "rad/s"
    mrun = "0"
    Pol = "0"
    Min = "376"
    Max = "382"
    }
   -Wire-([144,702],0,0,-1)
    {
    Vertex="0,0;108,0"
    }
   0.datalabel([324,594],0,0,-1)
    {
    Name = "Tmstdy"
    }
   0.const([108,702],0,0,20)
    {
    Name = ""
    Value = "1.0"
    }
   0.datalabel([144,1044],0,0,-1)
    {
    Name = "LRR"
    }
   -Wire-([144,594],0,0,-1)
    {
    Vertex="0,0;108,0"
    }
   -Wire-([252,540],0,0,-1)
    {
    Vertex="0,0;0,54"
    }
   -Wire-([288,540],0,0,-1)
    {
    Vertex="0,0;0,54"
    }
   0.datalabel([252,1044],0,0,-1)
    {
    Name = "S2M"
    }
   -Wire-([324,540],0,0,-1)
    {
    Vertex="0,0;0,54"
    }
   0.sandhdefn([270,162],0,0,70)
    {
    Iand = "1"
    }
   -Wire-([234,162],0,0,-1)
    {
    Vertex="0,0;0,72;18,72"
    }
   0.datalabel([270,198],0,0,-1)
    {
    Name = "S2M"
    }
   0.excac([288,306],0,0,80)
    {
    TYPE = "1"
    INIT = "InitEx"
    OVR = "1"
    RC = "0.0 [pu]"
    XC = "0.0 [pu]"
    TR = "0.0 [s]"
    STAB = "0"
    TC_1 = "0.0 [s]"
    TB_1 = "0.0 [s]"
    KA_1 = "400.0 [pu]"
    TA_1 = "0.02 [s]"
    VAMX_1 = "14.5 [pu]"
    VAMN_1 = "-14.5 [pu]"
    UEL_1 = "0"
    OEL_1 = "0"
    VRMX_1 = "6.03 [pu]"
    VRMN_1 = "-5.43 [pu]"
    KF_1 = "0.03 [pu]"
    TF_1 = "1.0 [s]"
    TE_1 = "0.80 [s]"
    KE_1 = "1.00 [pu]"
    KC_1 = "0.20 [pu]"
    KD_1 = "0.38 [pu]"
    SE1_1 = "0.10 [pu]"
    VE1_1 = "4.18 [pu]"
    SE2_1 = "0.03 [pu]"
    VE2_1 = "3.14 [pu]"
    VUEL_1 = "-1.0E10 [pu]"
    VOEL_1 = "1.0E10 [pu]"
    TC_2 = "0.0 [s]"
    TB_2 = "0.0 [s]"
    KA_2 = "400.0 [pu]"
    TA_2 = "0.01 [s]"
    VAMX_2 = "8.0 [pu]"
    VAMN_2 = "-8.0 [pu]"
    KB_2 = "25.0 [pu]"
    UEL_2 = "0"
    OEL_2 = "0"
    VRMX_2 = "105. [pu]"
    VRMN_2 = "-95. [pu]"
    KF_2 = "0.03 [pu]"
    TF_2 = "1.0 [s]"
    KH_2 = "1.0 [pu]"
    TE_2 = "0.60 [s]"
    VFMX_2 = "4.4 [pu]"
    KE_2 = "1.00 [pu]"
    KC_2 = "0.28 [pu]"
    KD_2 = "0.35 [pu]"
    SE1_2 = "0.037 [pu]"
    VE1_2 = "4.4 [pu]"
    SE2_2 = "0.012 [pu]"
    VE2_2 = "3.3 [pu]"
    VUEL_2 = "-1.0E10 [pu]"
    VOEL_2 = "1.0E10 [pu]"
    TC_3 = "0.0 [s]"
    TB_3 = "0.0 [s]"
    UEL_3 = "0"
    KA_3 = "45.62 [pu]"
    TA_3 = "0.013 [s]"
    VAMX_3 = "1.0 [pu]"
    VAMN_3 = "-0.95 [pu]"
    KR_3 = "3.77 [pu]"
    VLV_3 = "0.790 [pu]"
    KLV_3 = "0.194 [pu]"
    KF_3 = "0.143 [pu]"
    KN_3 = "0.05 [pu]"
    EFDN_3 = "2.36 [pu]"
    TF_3 = "1.0 [s]"
    TE_3 = "1.17 [s]"
    VFMX_3 = "16.0 [pu]"
    KE_3 = "1.00 [pu]"
    KC_3 = "0.104 [pu]"
    KD_3 = "0.499 [pu]"
    SE1_3 = "1.143 [pu]"
    VE1_3 = "6.24 [pu]"
    SE2_3 = "0.10 [pu]"
    VE2_3 = "4.68 [pu]"
    VUEL_3 = "-1.0E10 [pu]"
    VIMX_4 = "10.0 [pu]"
    VIMN_4 = "-10.0 [pu]"
    TC_4 = "1.0 [s]"
    TB_4 = "10.0 [s]"
    UEL_4 = "0"
    KA_4 = "200.0 [pu]"
    TA_4 = "0.015 [s]"
    VRMX_4 = "5.64 [pu]"
    VRMN_4 = "-4.53 [pu]"
    KC_4 = "0.0 [pu]"
    VUEL_4 = "-1.0E10 [pu]"
    KA_5 = "400.0 [pu]"
    TA_5 = "0.02 [s]"
    VRMX_5 = "7.3 [pu]"
    VRMN_5 = "-7.3 [pu]"
    TE_5 = "0.80 [s]"
    KE_5 = "1.00 [pu]"
    SE1_5 = "0.86 [pu]"
    EF1_5 = "5.60 [pu]"
    SE2_5 = "0.50 [pu]"
    EF2_5 = "4.20 [pu]"
    KF_5 = "0.03 [pu]"
    TF1_5 = "1.0 [s]"
    TF2_5 = "0.0 [s]"
    TF3_5 = "0.0 [s]"
    UEL_6 = "0"
    KA_6 = "53.6 [pu]"
    TK_6 = "0.18 [s]"
    TA_6 = "0.086 [s]"
    TC_6 = "3.0 [s]"
    TB_6 = "9.0 [s]"
    VAMX_6 = "75. [pu]"
    VAMN_6 = "-75. [pu]"
    VRMX_6 = "44. [pu]"
    VRMN_6 = "-36. [pu]"
    TE_6 = "1.0 [s]"
    KE_6 = "1.6 [pu]"
    KC_6 = "0.173 [pu]"
    KD_6 = "1.91 [pu]"
    SE1_6 = "0.214 [pu]"
    VE1_6 = "7.4 [pu]"
    SE2_6 = "0.044 [pu]"
    VE2_6 = "5.55 [pu]"
    VFLM_6 = "19.0 [pu]"
    KH_6 = "92.0 [pu]"
    VHMX_6 = "75.0 [pu]"
    TH_6 = "0.08 [s]"
    TJ_6 = "0.02 [s]"
    VUEL_6 = "0.00 [pu]"
    UEL_7 = "0"
    KRP_7 = "12.77 [pu]"
    KRI_7 = "20.0 [pu]"
    VRMX_7 = "5.0 [pu]"
    VRMN_7 = "-5.0 [pu]"
    KAP_7 = "20. [pu]"
    KAI_7 = "1.0 [pu]"
    VAMX_7 = "1.0 [pu]"
    VAMN_7 = "-1.0 [pu]"
    KP_7 = "6.41 [pu]"
    VLV_7 = "0.79 [pu]"
    KL_7 = "26.2 [pu]"
    VFMX_7 = "6.1 [pu]"
    SE1_7 = "1.195 [pu]"
    VE1_7 = "4.025 [pu]"
    SE2_7 = "0.097 [pu]"
    VE2_7 = "3.02 [pu]"
    TE_7 = "1.945 [s]"
    KE_7 = "1.0 [pu]"
    KD_7 = "0.567 [pu]"
    KC_7 = "0.172 [pu]"
    KF_7 = "1.0 [pu]"
    VUEL_7 = "0.0 [pu]"
    KP_8 = "17.0 [pu]"
    KI_8 = "13.0 [pu]"
    KD_8 = "6.0 [pu]"
    TD_8 = "0.03 [s]"
    KA_8 = "1.0 [pu]"
    TA_8 = "0.0 [s]"
    VRMX_8 = "10.0 [pu]"
    VRMN_8 = "0.0 [pu]"
    TE_8 = "1.0 [s]"
    KE_8 = "1.0 [pu]"
    SE1_8 = "1.5 [pu]"
    EF1_8 = "4.5 [pu]"
    SE2_8 = "1.36 [pu]"
    EF2_8 = "3.38 [pu]"
    }
   -Wire-([216,396],0,0,-1)
    {
    Vertex="0,0;0,-90"
    }
   -Wire-([324,396],0,0,-1)
    {
    Vertex="0,0;0,-90"
    }
   0.hy_tur([288,666],0,0,110)
    {
    WC = "0"
    ST = "0"
    JD = "0"
    RV = "0"
    INIT = "InitGv"
    HR = "1.0 [pu]"
    PR = "1.0 [pu]"
    ZR = "1.0 [pu]"
    QG = "0"
    QNL = "0.05 [pu]"
    ZNL = "0.05 [pu]"
    PM0 = "Tmstdy"
    HI = "1.0 [pu]"
    TW_1 = "2.0 [s]"
    FP_1 = "0.02 [pu]"
    D_1 = "0.5 [pu]"
    TW_2 = "2.0 [s]"
    TE_2 = "2.0 [s]"
    FP_2 = "0.02 [pu]"
    D_2 = "0.5 [pu]"
    TW1_3 = "2.0 [s]"
    FP1_3 = "0.02 [pu]"
    TW2_3 = "2.0 [s]"
    FP2_3 = "0.02 [pu]"
    TS_3 = "100.0 [s]"
    FO_3 = "0.02 [pu]"
    D_3 = "0.5 [pu]"
    TW1_4 = "2.0 [s]"
    TE_4 = "2.0 [s]"
    FP1_4 = "0.02 [pu]"
    TW2_4 = "2.0 [s]"
    FP2_4 = "0.02 [pu]"
    TS_4 = "100.0 [s]"
    FO_4 = "0.02 [pu]"
    D_4 = "0.5 [pu]"
    P_IN = ""
    P_OUT = ""
    HEAD = ""
    FLOW = ""
    Q_NT = ""
    Q_RLF = "RelVlv"
    Q_DEF = "JetDef"
    P_FLOW = ""
    P_HEAD = ""
    S_FLOW = ""
    S_HEAD = ""
    }
   0.hy_gov([180,666],0,0,100)
    {
    H_GOV = "1"
    INIT = "InitGv"
    DB = "0.0 [pu]"
    RP = "0.04 [pu]"
    GMAX = "1.0 [pu]"
    GMIN = "0.0 [pu]"
    MGOR = "0.16 [pu/s]"
    MGCR = "0.16 [pu/s]"
    TP_1 = "0.05 [s]"
    Q_1 = "5.0 [pu]"
    TG_1 = "0.2 [s]"
    RT_1 = "0.40 [pu]"
    TR_1 = "5.0 [s]"
    KP_2 = "3.0 [pu]"
    KI_2 = "0.7 [pu]"
    KD_2 = "0.5 [pu]"
    TA_2 = "0.05 [s]"
    TC_2 = "0.2 [s]"
    TD_2 = "0.2 [s]"
    JET_D = "0"
    RELF = "0"
    TP_3 = "0.02 [s]"
    TR_3 = "8.0 [s]"
    RT_3 = "0.45 [pu]"
    TG_3 = "0.5 [s]"
    MJOR_3 = "0.1 [pu/s]"
    MJCR_3 = "0.1 [pu/s]"
    Z_CUT = "0.0 [pu]"
    MBOR_3 = "0.1 [pu/s]"
    MBCR_3 = "0.1 [pu/s]"
    RVCR_3 = "0.1 [pu]"
    RVMX_3 = "1.0 [pu]"
    }
   -Sticky-([36,18],0)
    {
    Name = "Untitled"
    Font = 2
    Bounds = 36,18,1170,54
    Alignment = 1
    Style = 0
    Arrow = 0
    Color = 0,15792890
    Text = "SYNCHRONOUS MACHINE WITH EXCITER AND GOVERNOR"
    }
   -Plot-([630,72],0)
    {
    Title = ""
    Draw = 1
    Area = [0,0,522,1098]
    Posn = [630,72]
    Icon = [-1,-1]
    Extents = 0,0,522,1098
    XLabel = ""
    AutoPan = "false,75"
    Graph([0,0],[0,0,522,148],"Power")
     {
     Options = 0
     Units = ""
     Curve(26802680,"REAL POWER",0,,,)
     }
    Graph([0,148],[0,0,522,148],"Reactive Power")
     {
     Options = 0
     Units = ""
     Curve(26927336,"REACTIVE POWER",0,,,)
     }
    Graph([0,296],[0,0,522,148],"speed")
     {
     Options = 0
     Units = ""
     Curve(26914592,"OMEGA",0,,,)
     }
    Graph([0,444],[0,0,522,148],"Torque")
     {
     Options = 0
     Units = ""
     Curve(26930224,"MECHANICAL TORQUE",0,,,)
     }
    Graph([0,592],[0,0,522,148],"Field Current")
     {
     Options = 0
     Units = ""
     Curve(26912296,"FIELD CURRENT",0,,,)
     }
    Graph([0,740],[0,0,522,148],"Field Voltage")
     {
     Options = 0
     Units = ""
     Curve(26801768,"FIELD VOLTAGE",0,,,)
     }
    Graph([0,888],[0,0,522,147],"Voltage")
     {
     Options = 0
     Units = ""
     Curve(26797984,"TERMINAL VOLTAGE",0,,,)
     }
    }
   0.tbreakn([486,1044],4,0,60)
    {
    NUMS = "1"
    INIT = "1"
    TO1 = "1.0 [s]"
    TO2 = "1.05 [s]"
    }
   -Wire-([306,162],0,0,-1)
    {
    Vertex="0,0;0,72;-18,72"
    }
   0.multimeter([396,468],4,0,10)
    {
    MeasI = "0"
    MeasV = "0"
    MeasP = "0"
    MeasQ = "0"
    RMS = "1"
    MeasPh = "0"
    S = "1.0 [MVA]"
    BaseV = "1.0 [kV]"
    TS = "0.02 [s]"
    Freq = "60.0 [Hz]"
    Dis = "0"
    CurI = ""
    VolI = ""
    P = ""
    Q = ""
    Vrms = "Vrms"
    Ph = ""
    hide1 = "0"
    hide2 = "0"
    Pd = ""
    Qd = ""
    Vd = ""
    }
   -Wire-([450,576],0,0,-1)
    {
    Vertex="0,0;0,-108"
    }
   -Wire-([270,918],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.datalabel([270,918],0,0,-1)
    {
    Name = "Vrms"
    }
   -Wire-([414,468],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   }
  }
 }

