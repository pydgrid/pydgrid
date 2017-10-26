PSCAD 4.2.0

Settings
 {
 Id = "1503160782.1503260472"
 Author = "Ingelectus.Ingelectus"
 Desc = ""
 Arch = "windows"
 Options = 32
 Build = 18
 Warn = 1
 Check = 15
 Libs = ""
 Source = ""
 RunInfo = 
  {
  Fin = 0.5
  Step = 1e-005
  Plot = 0.00025
  Chat = 0.001
  Brch = 5e-005
  Lat = 100
  Options = 0
  Advanced = 4479
  Debug = 0
  StartFile = ""
  OFile = "noname.out"
  SFile = "noname.snp"
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
  Desc = ""
  FileDate = 1503241125
  Nodes = 
   {
   }

  Graphics = 
   {
   Rectangle(-18,-18,18,18)
   }


  Page(A/A4,Landscape,16,[962,468],5)
   {
   -Wire-([180,126],0,0,-1)
    {
    Vertex="0,0;108,0"
    }
   0.xfmr-3p2w([360,162],0,0,-1)
    {
    Name = ""
    Tmva = "0.63 [MVA]"
    f = "60.0 [Hz]"
    YD1 = "0"
    YD2 = "1"
    Lead = "1"
    Xl = "0.04 [pu]"
    Ideal = "0"
    NLL = "0.0 [pu]"
    CuL = "0.01 [pu]"
    Tap = "0"
    View = "0"
    Dtls = "0"
    V1 = "0.4 [kV]"
    V2 = "20.0 [kV]"
    Enab = "1"
    Sat = "1"
    Xair = "0.2 [pu]"
    Tdc = "1.0 [s]"
    Xknee = "1.25 [pu]"
    Txk = "0.1 [s]"
    Im1 = "1 [%]"
    ILA1 = ""
    ILB1 = ""
    ILC1 = ""
    IAB1 = ""
    IBC1 = ""
    ICA1 = ""
    ILA2 = ""
    ILB2 = ""
    ILC2 = ""
    IAB2 = ""
    IBC2 = ""
    ICA2 = ""
    IMA = ""
    IMB = ""
    IMC = ""
    FLXA = ""
    FLXB = ""
    FLXC = ""
    IMAB = ""
    IMBC = ""
    IMCA = ""
    FLXAB = ""
    FLXBC = ""
    FLXCA = ""
    }
   0.voltmetergnd([468,126],0,0,30)
    {
    Name = "v_a2"
    }
   0.datalabel([864,126],0,0,-1)
    {
    Name = "Vsource"
    }
   0.const([720,162],0,0,120)
    {
    Name = ""
    Value = "0.57735026919"
    }
   0.datalabel([792,198],0,0,-1)
    {
    Name = "Fsource"
    }
   0.const([720,198],0,0,180)
    {
    Name = ""
    Value = "60.0"
    }
   -Wire-([756,198],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.source_3([558,162],2,0,490)
    {
    Name = "Source 1"
    Type = "6"
    Grnd = "1"
    View = "0"
    Spec = "0"
    VCtrl = "1"
    FCtrl = "1"
    Vm = "230.0 [kV]"
    Tc = "0.05 [s]"
    f = "60.0 [Hz]"
    Ph = "0.0 [deg]"
    Vbase = "34.50 [kV]"
    Sbase = "100.0 [MVA]"
    Vpu = "1.0 [pu]"
    PhT = "0.0 [deg]"
    Pinit = "0.0 [pu]"
    Qinit = "0.0 [pu]"
    R = "1.0 [ohm]"
    Rs = "1.0 [ohm]"
    Rp = "1.0 [ohm]"
    Lp = "0.1 [H]"
    R' = "1.0 [ohm]"
    L = "0.1 [H]"
    C = "1.0 [uF]"
    L' = "0.1 [H]"
    C' = "1.0 [uF]"
    IA = ""
    IB = ""
    IC = ""
    }
   0.const([684,126],0,0,70)
    {
    Name = ""
    Value = "20.0"
    }
   0.mult([756,126],0,0,470)
    {
    }
   0.datalabel([558,234],0,0,-1)
    {
    Name = "Vsource"
    }
   0.datalabel([594,234],0,0,-1)
    {
    Name = "Fsource"
    }
   0.mult([828,126],0,0,480)
    {
    }
   0.const([792,162],0,0,130)
    {
    Name = ""
    Value = "1.41421356237"
    }
   0.pgb([234,306],0,52406184,200)
    {
    Name = "i_a1_rms"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([54,306],0,0,-1)
    {
    Name = "i_a1"
    }
   -Wire-([180,162],0,0,-1)
    {
    Vertex="0,0;108,0"
    }
   -Wire-([180,198],0,0,-1)
    {
    Vertex="0,0;108,0"
    }
   0.ammeter([522,126],2,0,40)
    {
    Name = "i_a2"
    }
   -Wire-([432,126],0,0,-1)
    {
    Vertex="0,0;54,0"
    }
   0.voltmetergnd([468,162],0,0,80)
    {
    Name = "v_b2"
    }
   0.ammeter([522,162],2,0,90)
    {
    Name = "i_b2"
    }
   -Wire-([432,162],0,0,-1)
    {
    Vertex="0,0;54,0"
    }
   0.voltmetergnd([468,198],0,0,140)
    {
    Name = "v_c2"
    }
   0.ammeter([522,198],2,0,150)
    {
    Name = "i_c2"
    }
   -Wire-([432,198],0,0,-1)
    {
    Vertex="0,0;54,0"
    }
   -Wire-([180,234],0,0,-1)
    {
    Vertex="0,0;144,0"
    }
   0.voltmetergnd([216,126],0,0,20)
    {
    Name = "v_a1"
    }
   0.voltmetergnd([216,162],0,0,60)
    {
    Name = "v_b1"
    }
   0.voltmetergnd([216,198],0,0,110)
    {
    Name = "v_c1"
    }
   0.voltmetergnd([216,234],0,0,170)
    {
    Name = "v_n1"
    }
   0.resistor([54,126],0,0,-1)
    {
    R = "0.01 [ohm]"
    }
   0.resistor([54,162],0,0,-1)
    {
    R = "10.0 [ohm]"
    }
   0.resistor([54,198],0,0,-1)
    {
    R = "10.0 [ohm]"
    }
   -Wire-([18,126],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   -Wire-([18,162],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   -Wire-([18,198],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   -Wire-([18,126],0,0,-1)
    {
    Vertex="0,0;0,108"
    }
   -Wire-([90,126],0,0,-1)
    {
    Vertex="0,0;54,0"
    }
   0.ammeter([180,126],2,0,10)
    {
    Name = "i_a1"
    }
   0.ammeter([180,162],2,0,50)
    {
    Name = "i_b1"
    }
   0.ammeter([180,198],2,0,100)
    {
    Name = "i_c1"
    }
   0.ammeter([180,234],2,0,160)
    {
    Name = "i_n1"
    }
   -Wire-([90,162],0,0,-1)
    {
    Vertex="0,0;54,0"
    }
   -Wire-([90,198],0,0,-1)
    {
    Vertex="0,0;54,0"
    }
   -Wire-([18,234],0,0,-1)
    {
    Vertex="0,0;126,0"
    }
   0.rms-inst([126,306],0,0,190)
    {
    Type = "1"
    Ts = "0.01666 [s]"
    Scale = "1.0"
    freq = "60.0 [Hz]"
    NSAM = "64"
    Vinit = "0.0"
    }
   -Wire-([54,306],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.datalabel([198,306],0,0,-1)
    {
    Name = "i_a1_rms"
    }
   -Wire-([162,306],0,0,-1)
    {
    Vertex="0,0;18,0"
    }
   -Wire-([162,306],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   -Wire-([198,306],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.pgb([234,360],0,53100552,240)
    {
    Name = "i_b1_rms"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([54,360],0,0,-1)
    {
    Name = "i_b1"
    }
   0.rms-inst([126,360],0,0,230)
    {
    Type = "1"
    Ts = "0.01666 [s]"
    Scale = "1.0"
    freq = "60.0 [Hz]"
    NSAM = "64"
    Vinit = "0.0"
    }
   -Wire-([54,360],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.datalabel([198,360],0,0,-1)
    {
    Name = "i_b1_rms"
    }
   -Wire-([162,360],0,0,-1)
    {
    Vertex="0,0;18,0"
    }
   -Wire-([162,360],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   -Wire-([198,360],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.pgb([234,414],0,53102632,280)
    {
    Name = "i_c1_rms"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([54,414],0,0,-1)
    {
    Name = "i_c1"
    }
   0.rms-inst([126,414],0,0,270)
    {
    Type = "1"
    Ts = "0.01666 [s]"
    Scale = "1.0"
    freq = "60.0 [Hz]"
    NSAM = "64"
    Vinit = "0.0"
    }
   -Wire-([54,414],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.datalabel([198,414],0,0,-1)
    {
    Name = "i_c1_rms"
    }
   -Wire-([162,414],0,0,-1)
    {
    Vertex="0,0;18,0"
    }
   -Wire-([162,414],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   -Wire-([198,414],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.pgb([234,468],0,53398896,320)
    {
    Name = "i_n1_rms"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([54,468],0,0,-1)
    {
    Name = "i_n1"
    }
   0.rms-inst([126,468],0,0,310)
    {
    Type = "1"
    Ts = "0.01666 [s]"
    Scale = "1.0"
    freq = "60.0 [Hz]"
    NSAM = "64"
    Vinit = "0.0"
    }
   -Wire-([54,468],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.datalabel([198,468],0,0,-1)
    {
    Name = "i_n1_rms"
    }
   -Wire-([162,468],0,0,-1)
    {
    Vertex="0,0;18,0"
    }
   -Wire-([162,468],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   -Wire-([198,468],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.pgb([486,306],0,53902832,220)
    {
    Name = "v_a1_rms"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([306,306],0,0,-1)
    {
    Name = "v_a1"
    }
   0.rms-inst([378,306],0,0,210)
    {
    Type = "1"
    Ts = "0.01666 [s]"
    Scale = "1e-3"
    freq = "60.0 [Hz]"
    NSAM = "64"
    Vinit = "0.0"
    }
   -Wire-([306,306],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.datalabel([450,306],0,0,-1)
    {
    Name = "v_a1_rms"
    }
   -Wire-([414,306],0,0,-1)
    {
    Vertex="0,0;18,0"
    }
   -Wire-([414,306],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   -Wire-([450,306],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.pgb([486,360],0,53030144,260)
    {
    Name = "v_b1_rms"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([306,360],0,0,-1)
    {
    Name = "v_b1"
    }
   0.rms-inst([378,360],0,0,250)
    {
    Type = "1"
    Ts = "0.01666 [s]"
    Scale = "1e-3"
    freq = "60.0 [Hz]"
    NSAM = "64"
    Vinit = "0.0"
    }
   -Wire-([306,360],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.datalabel([450,360],0,0,-1)
    {
    Name = "v_b1_rms"
    }
   -Wire-([414,360],0,0,-1)
    {
    Vertex="0,0;18,0"
    }
   -Wire-([414,360],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   -Wire-([450,360],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.pgb([486,414],0,52624192,300)
    {
    Name = "v_c1_rms"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([306,414],0,0,-1)
    {
    Name = "v_c1"
    }
   0.rms-inst([378,414],0,0,290)
    {
    Type = "1"
    Ts = "0.01666 [s]"
    Scale = "1e-3"
    freq = "60.0 [Hz]"
    NSAM = "64"
    Vinit = "0.0"
    }
   -Wire-([306,414],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.datalabel([450,414],0,0,-1)
    {
    Name = "v_c1_rms"
    }
   -Wire-([414,414],0,0,-1)
    {
    Vertex="0,0;18,0"
    }
   -Wire-([414,414],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   -Wire-([450,414],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.pgb([486,468],0,52628648,340)
    {
    Name = "v_n1_rms"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([306,468],0,0,-1)
    {
    Name = "v_n1"
    }
   0.rms-inst([378,468],0,0,330)
    {
    Type = "1"
    Ts = "0.01666 [s]"
    Scale = "1e-3"
    freq = "60.0 [Hz]"
    NSAM = "64"
    Vinit = "0.0"
    }
   -Wire-([306,468],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.datalabel([450,468],0,0,-1)
    {
    Name = "v_n1_rms"
    }
   -Wire-([414,468],0,0,-1)
    {
    Vertex="0,0;18,0"
    }
   -Wire-([414,468],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   -Wire-([450,468],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.pgb([234,522],0,52215376,360)
    {
    Name = "i_a2_rms"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([54,522],0,0,-1)
    {
    Name = "i_a2"
    }
   0.rms-inst([126,522],0,0,350)
    {
    Type = "1"
    Ts = "0.01666 [s]"
    Scale = "0.001"
    freq = "60.0 [Hz]"
    NSAM = "64"
    Vinit = "0.0"
    }
   -Wire-([54,522],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.datalabel([198,522],0,0,-1)
    {
    Name = "i_a2_rms"
    }
   -Wire-([162,522],0,0,-1)
    {
    Vertex="0,0;18,0"
    }
   -Wire-([162,522],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   -Wire-([198,522],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.pgb([234,576],0,52219832,400)
    {
    Name = "i_b2_rms"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([54,576],0,0,-1)
    {
    Name = "i_b2"
    }
   0.rms-inst([126,576],0,0,390)
    {
    Type = "1"
    Ts = "0.01666 [s]"
    Scale = "1e-3"
    freq = "60.0 [Hz]"
    NSAM = "64"
    Vinit = "0.0"
    }
   -Wire-([54,576],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.datalabel([198,576],0,0,-1)
    {
    Name = "i_b2_rms"
    }
   -Wire-([162,576],0,0,-1)
    {
    Vertex="0,0;18,0"
    }
   -Wire-([162,576],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   -Wire-([198,576],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.pgb([234,630],0,52224288,440)
    {
    Name = "i_c2_rms"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([54,630],0,0,-1)
    {
    Name = "i_c2"
    }
   0.rms-inst([126,630],0,0,430)
    {
    Type = "1"
    Ts = "0.01666 [s]"
    Scale = "1e-3"
    freq = "60.0 [Hz]"
    NSAM = "64"
    Vinit = "0.0"
    }
   -Wire-([54,630],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.datalabel([198,630],0,0,-1)
    {
    Name = "i_c2_rms"
    }
   -Wire-([162,630],0,0,-1)
    {
    Vertex="0,0;18,0"
    }
   -Wire-([162,630],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   -Wire-([198,630],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.pgb([486,522],0,26810528,380)
    {
    Name = "v_a2_rms"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([306,522],0,0,-1)
    {
    Name = "v_a2"
    }
   0.rms-inst([378,522],0,0,370)
    {
    Type = "1"
    Ts = "0.01666 [s]"
    Scale = "1.0"
    freq = "60.0 [Hz]"
    NSAM = "64"
    Vinit = "0.0"
    }
   -Wire-([306,522],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.datalabel([450,522],0,0,-1)
    {
    Name = "v_a2_rms"
    }
   -Wire-([414,522],0,0,-1)
    {
    Vertex="0,0;18,0"
    }
   -Wire-([414,522],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   -Wire-([450,522],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.pgb([486,576],0,52892048,420)
    {
    Name = "v_b2_rms"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([306,576],0,0,-1)
    {
    Name = "v_b2"
    }
   0.rms-inst([378,576],0,0,410)
    {
    Type = "1"
    Ts = "0.01666 [s]"
    Scale = "1.0"
    freq = "60.0 [Hz]"
    NSAM = "64"
    Vinit = "0.0"
    }
   -Wire-([306,576],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.datalabel([450,576],0,0,-1)
    {
    Name = "v_b2_rms"
    }
   -Wire-([414,576],0,0,-1)
    {
    Vertex="0,0;18,0"
    }
   -Wire-([414,576],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   -Wire-([450,576],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.pgb([486,630],0,53164496,460)
    {
    Name = "v_c2_rms"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([306,630],0,0,-1)
    {
    Name = "v_c2"
    }
   0.rms-inst([378,630],0,0,450)
    {
    Type = "1"
    Ts = "0.01666 [s]"
    Scale = "1.0"
    freq = "60.0 [Hz]"
    NSAM = "64"
    Vinit = "0.0"
    }
   -Wire-([306,630],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.datalabel([450,630],0,0,-1)
    {
    Name = "v_c2_rms"
    }
   -Wire-([414,630],0,0,-1)
    {
    Vertex="0,0;18,0"
    }
   -Wire-([414,630],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   -Wire-([450,630],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   -Plot-([900,576],0)
    {
    Title = "$(GROUP) : Graphs"
    Draw = 1
    Area = [0,0,0,0]
    Posn = [900,576]
    Icon = [-1,-1]
    Extents = 0,0,576,288
    XLabel = " "
    AutoPan = "false,75"
    Graph([0,0],[0,0,576,225],"y")
     {
     Options = 128
     Units = ""
     Curve(52215376,"i_a2_rms",0,,,)
     Curve(52219832,"i_b2_rms",0,,,)
     Curve(52224288,"i_c2_rms",0,,,)
     }
    }
   -Plot-([72,666],0)
    {
    Title = "$(GROUP) : Graphs"
    Draw = 1
    Area = [0,0,576,342]
    Posn = [72,666]
    Icon = [-1,-1]
    Extents = 0,0,576,342
    XLabel = " "
    AutoPan = "false,75"
    Graph([0,0],[0,0,576,279],"y")
     {
     Options = 128
     Units = ""
     Curve(26810528,"v_a2_rms",0,,,)
     Curve(52892048,"v_b2_rms",0,,,)
     Curve(53164496,"v_c2_rms",0,,,)
     }
    }
   0.ground([360,234],0,0,-1)
    {
    }
   0.resistor([324,234],0,0,-1)
    {
    R = "1.0e6 [ohm]"
    }
   -Plot-([900,0],0)
    {
    Title = "$(GROUP) : Graphs"
    Draw = 1
    Area = [0,0,0,0]
    Posn = [900,0]
    Icon = [-1,-1]
    Extents = 0,0,576,288
    XLabel = " "
    AutoPan = "false,75"
    Graph([0,0],[0,0,576,225],"y")
     {
     Options = 130
     Units = ""
     Curve(52406184,"i_a1_rms",0,,,)
     Curve(53100552,"i_b1_rms",0,,,)
     Curve(53102632,"i_c1_rms",0,,,)
     Curve(53398896,"i_n1_rms",0,,,)
     }
    }
   -Plot-([900,288],0)
    {
    Title = "$(GROUP) : Graphs"
    Draw = 1
    Area = [0,0,0,0]
    Posn = [900,288]
    Icon = [-1,-1]
    Extents = 0,0,576,288
    XLabel = " "
    AutoPan = "false,75"
    Graph([0,0],[0,0,576,225],"y")
     {
     Options = 128
     Units = ""
     Curve(53902832,"v_a1_rms",0,,,)
     Curve(53030144,"v_b1_rms",0,,,)
     Curve(52624192,"v_c1_rms",0,,,)
     Curve(52628648,"v_n1_rms",0,,,)
     }
    }
   }
  }
 }

