/* Generated by Yosys 0.38 (git sha1 543faed9c8c, clang++ 17.0.6 -fPIC -Os) */

module pipeline_8b_adder(A_XX, B_YY, C_in, clk_XXYY, rst, Sum_XXYY, C_out);
  wire _000_;
  wire _001_;
  wire _002_;
  wire _003_;
  wire _004_;
  wire _005_;
  wire _006_;
  wire _007_;
  wire _008_;
  wire _009_;
  wire _010_;
  wire _011_;
  wire _012_;
  wire _013_;
  wire _014_;
  wire _015_;
  wire _016_;
  wire _017_;
  wire _018_;
  wire _019_;
  wire _020_;
  wire _021_;
  wire _022_;
  wire _023_;
  wire _024_;
  wire _025_;
  wire _026_;
  wire _027_;
  wire _028_;
  wire _029_;
  wire _030_;
  wire _031_;
  wire _032_;
  wire _033_;
  wire _034_;
  wire _035_;
  wire _036_;
  wire _037_;
  wire _038_;
  wire _039_;
  wire _040_;
  wire _041_;
  wire _042_;
  wire _043_;
  wire _044_;
  wire _045_;
  wire _046_;
  wire _047_;
  wire _048_;
  wire _049_;
  wire _050_;
  wire _051_;
  wire _052_;
  wire _053_;
  wire _054_;
  wire _055_;
  wire _056_;
  wire _057_;
  wire _058_;
  wire _059_;
  wire _060_;
  input [7:0] A_XX;
  wire [7:0] A_XX;
  input [7:0] B_YY;
  wire [7:0] B_YY;
  input C_in;
  wire C_in;
  output C_out;
  wire C_out;
  output [7:0] Sum_XXYY;
  wire [7:0] Sum_XXYY;
  wire \a41.A_XX[0] ;
  wire \a41.A_XX[1] ;
  wire \a41.A_XX[2] ;
  wire \a41.A_XX[3] ;
  wire \a41.B_YY[0] ;
  wire \a41.B_YY[1] ;
  wire \a41.B_YY[2] ;
  wire \a41.B_YY[3] ;
  wire \a41.C_in ;
  input clk_XXYY;
  wire clk_XXYY;
  input rst;
  wire rst;
  sky130_fd_sc_hd__or2_2 _061_ (
    .A(\a41.A_XX[0] ),
    .B(\a41.B_YY[0] ),
    .X(_021_)
  );
  sky130_fd_sc_hd__nand2_2 _062_ (
    .A(\a41.A_XX[0] ),
    .B(\a41.B_YY[0] ),
    .Y(_022_)
  );
  sky130_fd_sc_hd__nand2_2 _063_ (
    .A(_021_),
    .B(_022_),
    .Y(_023_)
  );
  sky130_fd_sc_hd__xnor2_2 _064_ (
    .A(\a41.C_in ),
    .B(_023_),
    .Y(Sum_XXYY[4])
  );
  sky130_fd_sc_hd__a21boi_2 _065_ (
    .A1(\a41.C_in ),
    .A2(_021_),
    .B1_N(_022_),
    .Y(_024_)
  );
  sky130_fd_sc_hd__nor2_2 _066_ (
    .A(\a41.A_XX[1] ),
    .B(\a41.B_YY[1] ),
    .Y(_025_)
  );
  sky130_fd_sc_hd__nand2_2 _067_ (
    .A(\a41.A_XX[1] ),
    .B(\a41.B_YY[1] ),
    .Y(_026_)
  );
  sky130_fd_sc_hd__and2b_2 _068_ (
    .A_N(_025_),
    .B(_026_),
    .X(_027_)
  );
  sky130_fd_sc_hd__xnor2_2 _069_ (
    .A(_024_),
    .B(_027_),
    .Y(Sum_XXYY[5])
  );
  sky130_fd_sc_hd__nor2_2 _070_ (
    .A(\a41.A_XX[2] ),
    .B(\a41.B_YY[2] ),
    .Y(_028_)
  );
  sky130_fd_sc_hd__nand2_2 _071_ (
    .A(\a41.A_XX[2] ),
    .B(\a41.B_YY[2] ),
    .Y(_029_)
  );
  sky130_fd_sc_hd__and2b_2 _072_ (
    .A_N(_028_),
    .B(_029_),
    .X(_030_)
  );
  sky130_fd_sc_hd__o21a_2 _073_ (
    .A1(_024_),
    .A2(_025_),
    .B1(_026_),
    .X(_031_)
  );
  sky130_fd_sc_hd__xnor2_2 _074_ (
    .A(_030_),
    .B(_031_),
    .Y(Sum_XXYY[6])
  );
  sky130_fd_sc_hd__and2_2 _075_ (
    .A(\a41.A_XX[3] ),
    .B(\a41.B_YY[3] ),
    .X(_032_)
  );
  sky130_fd_sc_hd__nor2_2 _076_ (
    .A(\a41.A_XX[3] ),
    .B(\a41.B_YY[3] ),
    .Y(_033_)
  );
  sky130_fd_sc_hd__nor2_2 _077_ (
    .A(_032_),
    .B(_033_),
    .Y(_034_)
  );
  sky130_fd_sc_hd__o21a_2 _078_ (
    .A1(_028_),
    .A2(_031_),
    .B1(_029_),
    .X(_035_)
  );
  sky130_fd_sc_hd__xnor2_2 _079_ (
    .A(_034_),
    .B(_035_),
    .Y(Sum_XXYY[7])
  );
  sky130_fd_sc_hd__o21bai_2 _080_ (
    .A1(_033_),
    .A2(_035_),
    .B1_N(_032_),
    .Y(C_out)
  );
  sky130_fd_sc_hd__and2_2 _081_ (
    .A(A_XX[3]),
    .B(B_YY[3]),
    .X(_036_)
  );
  sky130_fd_sc_hd__nand2_2 _082_ (
    .A(A_XX[2]),
    .B(B_YY[2]),
    .Y(_037_)
  );
  sky130_fd_sc_hd__inv_2 _083_ (
    .A(_037_),
    .Y(_038_)
  );
  sky130_fd_sc_hd__and2_2 _084_ (
    .A(A_XX[1]),
    .B(B_YY[1]),
    .X(_039_)
  );
  sky130_fd_sc_hd__nand2_2 _085_ (
    .A(A_XX[0]),
    .B(B_YY[0]),
    .Y(_040_)
  );
  sky130_fd_sc_hd__inv_2 _086_ (
    .A(_040_),
    .Y(_041_)
  );
  sky130_fd_sc_hd__or2_2 _087_ (
    .A(A_XX[0]),
    .B(B_YY[0]),
    .X(_042_)
  );
  sky130_fd_sc_hd__and3_2 _088_ (
    .A(C_in),
    .B(_040_),
    .C(_042_),
    .X(_043_)
  );
  sky130_fd_sc_hd__or2_2 _089_ (
    .A(A_XX[1]),
    .B(B_YY[1]),
    .X(_044_)
  );
  sky130_fd_sc_hd__nand2_2 _090_ (
    .A(A_XX[1]),
    .B(B_YY[1]),
    .Y(_045_)
  );
  sky130_fd_sc_hd__o211a_2 _091_ (
    .A1(_041_),
    .A2(_043_),
    .B1(_044_),
    .C1(_045_),
    .X(_046_)
  );
  sky130_fd_sc_hd__or2_2 _092_ (
    .A(A_XX[2]),
    .B(B_YY[2]),
    .X(_047_)
  );
  sky130_fd_sc_hd__o211a_2 _093_ (
    .A1(_039_),
    .A2(_046_),
    .B1(_047_),
    .C1(_037_),
    .X(_048_)
  );
  sky130_fd_sc_hd__nand2_2 _094_ (
    .A(A_XX[3]),
    .B(B_YY[3]),
    .Y(_049_)
  );
  sky130_fd_sc_hd__or2_2 _095_ (
    .A(A_XX[3]),
    .B(B_YY[3]),
    .X(_050_)
  );
  sky130_fd_sc_hd__o211a_2 _096_ (
    .A1(_038_),
    .A2(_048_),
    .B1(_049_),
    .C1(_050_),
    .X(_051_)
  );
  sky130_fd_sc_hd__buf_1 _097_ (
    .A(rst),
    .X(_052_)
  );
  sky130_fd_sc_hd__o21a_2 _098_ (
    .A1(_036_),
    .A2(_051_),
    .B1(_052_),
    .X(_000_)
  );
  sky130_fd_sc_hd__and2_2 _099_ (
    .A(_052_),
    .B(A_XX[4]),
    .X(_053_)
  );
  sky130_fd_sc_hd__buf_1 _100_ (
    .A(_053_),
    .X(_001_)
  );
  sky130_fd_sc_hd__and2_2 _101_ (
    .A(_052_),
    .B(A_XX[5]),
    .X(_054_)
  );
  sky130_fd_sc_hd__buf_1 _102_ (
    .A(_054_),
    .X(_002_)
  );
  sky130_fd_sc_hd__and2_2 _103_ (
    .A(_052_),
    .B(A_XX[6]),
    .X(_055_)
  );
  sky130_fd_sc_hd__buf_1 _104_ (
    .A(_055_),
    .X(_003_)
  );
  sky130_fd_sc_hd__and2_2 _105_ (
    .A(_052_),
    .B(A_XX[7]),
    .X(_056_)
  );
  sky130_fd_sc_hd__buf_1 _106_ (
    .A(_056_),
    .X(_004_)
  );
  sky130_fd_sc_hd__and2_2 _107_ (
    .A(_052_),
    .B(B_YY[4]),
    .X(_057_)
  );
  sky130_fd_sc_hd__buf_1 _108_ (
    .A(_057_),
    .X(_005_)
  );
  sky130_fd_sc_hd__and2_2 _109_ (
    .A(_052_),
    .B(B_YY[5]),
    .X(_058_)
  );
  sky130_fd_sc_hd__buf_1 _110_ (
    .A(_058_),
    .X(_006_)
  );
  sky130_fd_sc_hd__and2_2 _111_ (
    .A(_052_),
    .B(B_YY[6]),
    .X(_059_)
  );
  sky130_fd_sc_hd__buf_1 _112_ (
    .A(_059_),
    .X(_007_)
  );
  sky130_fd_sc_hd__and2_2 _113_ (
    .A(_052_),
    .B(B_YY[7]),
    .X(_060_)
  );
  sky130_fd_sc_hd__buf_1 _114_ (
    .A(_060_),
    .X(_008_)
  );
  sky130_fd_sc_hd__a21o_2 _115_ (
    .A1(_040_),
    .A2(_042_),
    .B1(C_in),
    .X(_013_)
  );
  sky130_fd_sc_hd__and3b_2 _116_ (
    .A_N(_043_),
    .B(_013_),
    .C(_052_),
    .X(_014_)
  );
  sky130_fd_sc_hd__buf_1 _117_ (
    .A(_014_),
    .X(_009_)
  );
  sky130_fd_sc_hd__a211o_2 _118_ (
    .A1(_045_),
    .A2(_044_),
    .B1(_043_),
    .C1(_041_),
    .X(_015_)
  );
  sky130_fd_sc_hd__and3b_2 _119_ (
    .A_N(_046_),
    .B(_015_),
    .C(rst),
    .X(_016_)
  );
  sky130_fd_sc_hd__buf_1 _120_ (
    .A(_016_),
    .X(_010_)
  );
  sky130_fd_sc_hd__a211o_2 _121_ (
    .A1(_037_),
    .A2(_047_),
    .B1(_046_),
    .C1(_039_),
    .X(_017_)
  );
  sky130_fd_sc_hd__and3b_2 _122_ (
    .A_N(_048_),
    .B(_017_),
    .C(rst),
    .X(_018_)
  );
  sky130_fd_sc_hd__buf_1 _123_ (
    .A(_018_),
    .X(_011_)
  );
  sky130_fd_sc_hd__a211o_2 _124_ (
    .A1(_049_),
    .A2(_050_),
    .B1(_038_),
    .C1(_048_),
    .X(_019_)
  );
  sky130_fd_sc_hd__and3b_2 _125_ (
    .A_N(_051_),
    .B(_019_),
    .C(rst),
    .X(_020_)
  );
  sky130_fd_sc_hd__buf_1 _126_ (
    .A(_020_),
    .X(_012_)
  );
  sky130_fd_sc_hd__dfxtp_2 _127_ (
    .CLK(clk_XXYY),
    .D(_000_),
    .Q(\a41.C_in )
  );
  sky130_fd_sc_hd__dfxtp_2 _128_ (
    .CLK(clk_XXYY),
    .D(_001_),
    .Q(\a41.A_XX[0] )
  );
  sky130_fd_sc_hd__dfxtp_2 _129_ (
    .CLK(clk_XXYY),
    .D(_002_),
    .Q(\a41.A_XX[1] )
  );
  sky130_fd_sc_hd__dfxtp_2 _130_ (
    .CLK(clk_XXYY),
    .D(_003_),
    .Q(\a41.A_XX[2] )
  );
  sky130_fd_sc_hd__dfxtp_2 _131_ (
    .CLK(clk_XXYY),
    .D(_004_),
    .Q(\a41.A_XX[3] )
  );
  sky130_fd_sc_hd__dfxtp_2 _132_ (
    .CLK(clk_XXYY),
    .D(_005_),
    .Q(\a41.B_YY[0] )
  );
  sky130_fd_sc_hd__dfxtp_2 _133_ (
    .CLK(clk_XXYY),
    .D(_006_),
    .Q(\a41.B_YY[1] )
  );
  sky130_fd_sc_hd__dfxtp_2 _134_ (
    .CLK(clk_XXYY),
    .D(_007_),
    .Q(\a41.B_YY[2] )
  );
  sky130_fd_sc_hd__dfxtp_2 _135_ (
    .CLK(clk_XXYY),
    .D(_008_),
    .Q(\a41.B_YY[3] )
  );
  sky130_fd_sc_hd__dfxtp_2 _136_ (
    .CLK(clk_XXYY),
    .D(_009_),
    .Q(Sum_XXYY[0])
  );
  sky130_fd_sc_hd__dfxtp_2 _137_ (
    .CLK(clk_XXYY),
    .D(_010_),
    .Q(Sum_XXYY[1])
  );
  sky130_fd_sc_hd__dfxtp_2 _138_ (
    .CLK(clk_XXYY),
    .D(_011_),
    .Q(Sum_XXYY[2])
  );
  sky130_fd_sc_hd__dfxtp_2 _139_ (
    .CLK(clk_XXYY),
    .D(_012_),
    .Q(Sum_XXYY[3])
  );
endmodule
