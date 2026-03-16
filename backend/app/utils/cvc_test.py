from .analysis.DIF import Difference
from .analysis.Linear import Linear
from .analysis.Impossible import Impossible
from .analysis.ZeroCorrelation import ZeroCorrelation
from .analysis.Integral import Integral


class test:
    def __init__(
        self,
        Blocksize,
        Round,
        Branch_number,
        Sbox_bit,
        Sbox_content,
        Matrix,
        NonlinearType,
    ):
        self.Blocksize = Blocksize
        self.Round = Round
        self.Branch_number = Branch_number
        self.Sbox_bit = Sbox_bit
        self.NonlinearType = NonlinearType
        self.Matrix = Matrix
        self.HalfofBlocksize = self.Blocksize / 2
        self.QuarterBlocksize = self.Blocksize / 4
        self.HalfofQuarterBlocksize = self.Blocksize / 8

        self.MyDIF = Difference(
            Blocksize,
            Round,
            Branch_number,
            Sbox_bit,
            Sbox_content,
            Matrix,
            NonlinearType,
        )
        self.MyLinear = Linear(
            Blocksize,
            Round,
            Branch_number,
            Sbox_bit,
            Sbox_content,
            Matrix,
            NonlinearType,
        )
        self.MyImpossible = Impossible(
            Blocksize,
            Round,
            Branch_number,
            Sbox_bit,
            Sbox_content,
            Matrix,
            NonlinearType,
        )
        self.MyZeroCorrelation = ZeroCorrelation(
            Blocksize,
            Round,
            Branch_number,
            Sbox_bit,
            Sbox_content,
            Matrix,
            NonlinearType,
        )
        self.MyIntegral = Integral(
            Blocksize,
            Round,
            Branch_number,
            Sbox_bit,
            Sbox_content,
            Matrix,
            NonlinearType,
        )

    def DIFanalyze(self, S_num):
        # 在每次分析前清空历史数据
        self.MyDIF.sum = []
        self.MyDIF.sum1 = []

        DIFresult1 = self.MyDIF.genEncryptSubjection(self.MyDIF.Round)
        DIFresult2 = self.MyDIF.getVars(self.MyDIF.Round)
        # 这里需要改为你的目录
        # DIFlp_file = (
        #     r"/Users/yaaannn/Documents/workspace/Team-BC-Backend-fastapi/static/cvc/DIF.cvc"
        # )
        DIFlp_file = (
            r"/home/lys/projects/automated_design/backend/app/utils/analysis/cvc/DIF.cvc"
        )
        # print(self.Blocksize // self.Branch_number // self.Sbox_bit)
        # print(self.NonlinearType)
        if self.NonlinearType == "modulo":
            with open(DIFlp_file, "w") as OFile:

                for i in DIFresult2:
                    OFile.write(i + "\n")

                for i in DIFresult1:
                    OFile.write(i + "\n")

                OFile.write(
                    "ASSERT(BVGT(input1_r1@input2_r1 , "
                    + "0bin"
                    + "0" * self.Blocksize
                    + "));"
                    + "\n"
                )

                cunjieguo = []
                for i in range(1, self.MyDIF.Round + 1):
                    for j in range(0, self.Blocksize // self.Branch_number - 1):
                        cunjieguo.append("0bin0000000@w_r%s[%s:%s]" % (i, j, j))

                OFile.write(
                    "ASSERT(BVPLUS(8, 0bin00000000, "
                    + ",".join(cunjieguo)
                    + ")"
                    + " = zonggeshu);\n"
                )
                OFile.write(
                    "ASSERT(zonggeshu = 0bin" + bin(S_num)[2:].zfill(8) + ");" + "\n"
                )

                OFile.write("QUERY(FALSE); \n")
                OFile.write("COUNTEREXAMPLE; \n")

                OFile.close()

        else:
            with open(DIFlp_file, "w") as OFile:

                OFile.write("S: ARRAY BITVECTOR(16) OF BITVECTOR(1);\n")
                for i in self.MyDIF.DDT:
                    OFile.write(i + "\n")

                for i in DIFresult2:
                    OFile.write(i + "\n")

                for i in DIFresult1:
                    OFile.write(i + "\n")

                # print(self.MyDIF.sum1)
                OFile.write(
                    "ASSERT(BVPLUS(8, 0bin00000000, "
                    + ",".join(
                        [
                            "0bin0000000@(%s)" % (self.MyDIF.sum1[i])
                            for i in range(
                                self.MyDIF.Round
                                * (
                                    self.Blocksize
                                    // self.Branch_number
                                    // self.Sbox_bit
                                )
                            )
                        ]
                    )
                    + ")"
                    + " = "
                    + "zonggeshu"
                    + ");"
                    + "\n"
                )

                OFile.write(
                    "ASSERT(BVLE(zonggeshu, 0bin" + bin(S_num)[2:].zfill(8) + "));\n"
                )
                OFile.write(
                    "ASSERT(BVGT(input1_r1@input2_r1, "
                    + "0bin"
                    + "0" * (self.Blocksize)
                    + "));\n"
                )

                OFile.write("QUERY(FALSE); \n")
                OFile.write("COUNTEREXAMPLE; \n")

                OFile.close()

    # test_instance = test(4,1,2,2,[0,1,2,3], [[0,1],[1,0]])
    # print(test_instance.MyDIF.Sbox_content)
    # test_instance.DIFanalyze(8)

    # for item in test_instance.MyDIF.DDT:
    #     OFile.write(i + '\n')
    # print(test_instance.MyDIF.DDT())

    def Linearanalyze(self, S_num):
        # 清理历史数据
        self.MyLinear.sum = []
        self.MyLinear.sum1 = []

        Linearresult1 = self.MyLinear.genEncryptSubjection(self.MyLinear.Round)
        Linearresult2 = self.MyLinear.getVars(self.MyLinear.Round)
        Linearlp_file = (
            r"/home/lys/projects/automated_design/backend/app/utils/analysis/cvc/Linear.cvc"
        )

        # print(self.Blocksize // self.Branch_number // self.Sbox_bit)

        if self.NonlinearType == "modulo":
            with open(Linearlp_file, "w") as OFile:

                for i in Linearresult2:
                    OFile.write(i + "\n")

                for i in Linearresult1:
                    OFile.write(i + "\n")

                OFile.write(
                    "ASSERT(BVGT(input1_r1@input2_r1 , "
                    + "0bin"
                    + "0" * self.Blocksize
                    + "));\n"
                )

                command = "ASSERT(BVPLUS(16,"
                for i in range(1, self.MyLinear.Round + 1):
                    for j in range(1, self.Blocksize // self.Branch_number):
                        if i == self.MyLinear.Round and j == (
                            self.Blocksize // self.Branch_number - 1
                        ):
                            command += (
                                "0bin000000000000000@s_r"
                                + str(i)
                                + "["
                                + str(j)
                                + ":"
                                + str(j)
                                + "]"
                                + ") = 0bin"
                                + bin(S_num)[2:].zfill(16)
                                + ");"
                            )
                        else:
                            command += (
                                "0bin000000000000000@s_r"
                                + str(i)
                                + "["
                                + str(j)
                                + ":"
                                + str(j)
                                + "]"
                                + ","
                            )

                OFile.write(command + "\n")

                OFile.write("QUERY FALSE; \n")
                OFile.write("COUNTEREXAMPLE; \n")

                OFile.close()

        else:
            with open(Linearlp_file, "w") as OFile:

                OFile.write("S: ARRAY BITVECTOR(16) OF BITVECTOR(1);\n")

                for i in self.MyLinear.LAT:
                    OFile.write(i + "\n")

                for i in Linearresult2:
                    OFile.write(i + "\n")

                for i in Linearresult1:
                    OFile.write(i + "\n")

                OFile.write(
                    "ASSERT(BVPLUS(8, 0bin00000000, "
                    + ",".join(
                        [
                            "0bin0000000@(%s)" % (self.MyLinear.sum1[i])
                            for i in range(
                                self.MyLinear.Round
                                * (
                                    self.Blocksize
                                    // self.Branch_number
                                    // self.Sbox_bit
                                )
                            )
                        ]
                    )
                    + ")"
                    + " = "
                    + "zonggeshu"
                    + ");"
                    + "\n"
                )

                OFile.write(
                    "ASSERT(BVLE(zonggeshu, 0bin" + bin(S_num)[2:].zfill(8) + "));\n"
                )
                OFile.write(
                    "ASSERT(BVGT(input2_r1, "
                    + "0bin"
                    + "0" * (self.Blocksize // 2)
                    + "));\n"
                )

                OFile.write("QUERY(FALSE); \n")
                OFile.write("COUNTEREXAMPLE; \n")

                OFile.close()

    def ImpossibleDifferentialAnalyse(self, num_input, num_output):
        # 清理历史数据
        self.MyImpossible.sum = []
        self.MyImpossible.sum1 = []

        Impossibleresult1 = self.MyImpossible.genEncryptSubjection(
            self.MyImpossible.Round
        )
        Impossibleresult2 = self.MyImpossible.getVars(self.MyImpossible.Round)
        # 这里需要改为你的目录
        # Impossiblelp_file = (
        #     r"/Users/yaaannn/Documents/workspace/Team-BC-Backend-fastapi/static/cvc/Impossible.cvc"
        # )
        Impossiblelp_file = (
            r"/home/lys/projects/automated_design/backend/app/utils/analysis/cvc/Impossible.cvc"
        )

        if self.NonlinearType == "modulo":
            with open(Impossiblelp_file, "w") as OFile:

                OFile.write("S: ARRAY BITVECTOR(16) OF BITVECTOR(1);\n")

                for i in Impossibleresult2:
                    OFile.write(i + "\n")

                for i in Impossibleresult1:
                    OFile.write(i + "\n")

                # 输入非零
                OFile.write(
                    "ASSERT(BVGT(input1_r1@input2_r1 , "
                    + "0bin"
                    + "0" * self.Blocksize
                    + "));"
                    + "\n"
                )

                # 控制输入的值
                OFile.write(
                    f"ASSERT(input1_r1@input2_r1 = "
                    + "0bin"
                    + "0" * (self.Blocksize - 1 - num_input)
                    + "1"
                    + "0" * num_input
                    + ");\n"
                )

                # 控制输出的值
                OFile.write(
                    f"ASSERT("
                    f"{'output1_r{0}@'.format(self.Round) + 'output2_r{0}'.format(self.Round) + ' = 0bin' + '0' * (self.Blocksize - 1 - num_output) + '1' + '0' * num_output});\n"
                )

                OFile.write("QUERY(FALSE); \n")
                OFile.write("COUNTEREXAMPLE; \n")

                OFile.close()

        else:
            with open(Impossiblelp_file, "w") as OFile:

                OFile.write("S: ARRAY BITVECTOR(16) OF BITVECTOR(1);\n")

                for i in self.MyImpossible.DDT_Impossible:
                    OFile.write(i + "\n")

                for i in Impossibleresult2:
                    OFile.write(i + "\n")

                for i in Impossibleresult1:
                    OFile.write(i + "\n")

                # 控制输入的值
                OFile.write(
                    f"ASSERT(input1_r1@input2_r1 = "
                    + "0bin"
                    + "0" * (self.Blocksize - 1 - num_input)
                    + "1"
                    + "0" * num_input
                    + ");\n"
                )

                # 控制输出的值
                OFile.write(
                    f"ASSERT("
                    f"{'output1_r{0}@'.format(self.Round) + 'output2_r{0}'.format(self.Round) + ' = 0bin' + '0'*(self.Blocksize - 1 - num_output) + '1' + '0'*num_output});\n"
                )

                # 控制输入的汉明重量为1
                # OFile.write(f"ASSERT(BVPLUS("
                #             f"{'{0}'.format(self.Blocksize) +', ' + ', '.join(f'0bin000@input1_r1[{i}:{i}]'for i in range(self.Blocksize//self.Branch_number))  + ', ' + ', '.join((f'0bin000@input2_r1[{i}:{i}]'for i in range(self.Blocksize//self.Branch_number))) + ') = 0bin' + '0' * (self.Blocksize - 1) + '1'});\n")

                # 控制输出的汉明重量为1
                # OFile.write(f"ASSERT(BVPLUS("
                #             f"{'{0}'.format(self.Blocksize) + ', ' + ', '.join(f'0bin000@output1_r{self.Round}[{i}:{i}]' for i in range(self.Blocksize // self.Branch_number)) + ', ' + ', '.join((f'0bin000@output2_r{self.Round}[{i}:{i}]' for i in range(self.Blocksize // self.Branch_number))) + ') = 0bin' + '0' * (self.Blocksize - 1) + '1'});\n")

                OFile.write(
                    "ASSERT(BVGT(input1_r1@input2_r1, "
                    + "0bin"
                    + "0" * (self.Blocksize)
                    + "));\n"
                )

                OFile.write("QUERY(FALSE); \n")
                OFile.write("COUNTEREXAMPLE; \n")

                OFile.close()

    def ZeroCorrelationLinearAnalyse(self, num_input, num_output):
        # 清理历史数据
        self.MyZeroCorrelation.sum = []
        self.MyZeroCorrelation.sum1 = []

        ZeroCorrelationresult1 = self.MyZeroCorrelation.genEncryptSubjection(
            self.MyZeroCorrelation.Round
        )
        ZeroCorrelationresult2 = self.MyZeroCorrelation.getVars(
            self.MyZeroCorrelation.Round
        )
        # 这里需要改为你的目录
        # ZeroCorrelationlp_file = r"/Users/yaaannn/Documents/workspace/Team-BC-Backend-fastapi/static/cvc/ZeroCorrelation.cvc"
        ZeroCorrelationlp_file = r"/home/lys/projects/automated_design/backend/app/utils/analysis/cvc/ZeroCorrelation.cvc"

        if self.NonlinearType == "modulo":
            with open(ZeroCorrelationlp_file, "w") as OFile:

                OFile.write("S: ARRAY BITVECTOR(16) OF BITVECTOR(1);\n")

                for i in ZeroCorrelationresult2:
                    OFile.write(i + "\n")

                for i in ZeroCorrelationresult1:
                    OFile.write(i + "\n")

                # 输入非零
                OFile.write(
                    "ASSERT(BVGT(input1_r1@input2_r1 , "
                    + "0bin"
                    + "0" * self.Blocksize
                    + "));"
                    + "\n"
                )

                # 控制输入的值
                OFile.write(
                    f"ASSERT(input1_r1@input2_r1 = "
                    + "0bin"
                    + "0" * (self.Blocksize - 1 - num_input)
                    + "1"
                    + "0" * num_input
                    + ");\n"
                )

                # 控制输出的值
                OFile.write(
                    f"ASSERT("
                    f"{'output1_r{0}@'.format(self.Round) + 'output2_r{0}'.format(self.Round) + ' = 0bin' + '0' * (self.Blocksize - 1 - num_output) + '1' + '0' * num_output});\n"
                )

                OFile.write("QUERY(FALSE); \n")
                OFile.write("COUNTEREXAMPLE; \n")

                OFile.close()

        else:
            with open(ZeroCorrelationlp_file, "w") as OFile:

                OFile.write("S: ARRAY BITVECTOR(16) OF BITVECTOR(1);\n")

                for i in self.MyZeroCorrelation.LAT_ZeroCorrelation:
                    OFile.write(i + "\n")

                for i in ZeroCorrelationresult2:
                    OFile.write(i + "\n")

                for i in ZeroCorrelationresult1:
                    OFile.write(i + "\n")

                # 控制输入的值
                OFile.write(
                    f"ASSERT(input1_r1@input2_r1 = "
                    + "0bin"
                    + "0" * (self.Blocksize - 1 - num_input)
                    + "1"
                    + "0" * num_input
                    + ");\n"
                )

                # 控制输出的值
                OFile.write(
                    f"ASSERT("
                    f"{'output1_r{0}@'.format(self.Round) + 'output2_r{0}'.format(self.Round) + ' = 0bin' + '0' * (self.Blocksize - 1 - num_output) + '1' + '0' * num_output});\n"
                )

                # 控制输入的汉明重量为1
                # OFile.write(f"ASSERT(BVPLUS("
                #             f"{'{0}'.format(self.Blocksize) + ', ' + ', '.join(f'0bin000@input1_r1[{i}:{i}]' for i in range(self.Blocksize // self.Branch_number)) + ', ' + ', '.join((f'0bin000@input2_r1[{i}:{i}]' for i in range(self.Blocksize // self.Branch_number))) + ') = 0bin' + '0' * (self.Blocksize - 1) + '1'});\n")

                # #控制输出的汉明重量为1
                # OFile.write(f"ASSERT(BVPLUS("
                #             f"{'{0}'.format(self.Blocksize) + ', ' + ', '.join(f'0bin000@input1_r{self.Round + 1}[{i}:{i}]' for i in range(self.Blocksize //self.Branch_number)) + ', ' + ', '.join((f'0bin000@input2_r{self.Round + 1}[{i}:{i}]' for i in range(self.Blocksize //self.Branch_number))) + ') = 0bin' + '0' * (self.Blocksize - 1) + '1'});\n")

                OFile.write(
                    "ASSERT(BVGT(input1_r1@input2_r1, "
                    + "0bin"
                    + "0" * (self.Blocksize)
                    + "));\n"
                )

                OFile.write("QUERY(FALSE); \n")
                OFile.write("COUNTEREXAMPLE; \n")

                OFile.close()

    def Integralanalyse(self):
        # 清理历史数据
        self.MyIntegral.sum = []
        self.MyIntegral.sum1 = []

        Integralresult1 = self.MyIntegral.genEncryptSubjection(
            self.MyZeroCorrelation.Round
        )
        Integralresult2 = self.MyIntegral.getVars(self.MyZeroCorrelation.Round)
        # 这里需要改为你的目录
        # Integrallp_file = (
        #     r"/Users/yaaannn/Documents/workspace/Team-BC-Backend-fastapi/static/cvc/Integral.cvc"
        # )
        Integrallp_file = (
            r"/home/lys/projects/automated_design/backend/app/utils/analysis/cvc/Integral.cvc"
        )

        with open(Integrallp_file, "w") as OFile:

            for i in Integralresult2:
                OFile.write(i + "\n")

            for i in Integralresult1:
                OFile.write(i + "\n")

            OFile.write("ASSERT(BVGT(input1_1_r1, 0bin00));\n")
            OFile.write("ASSERT(BVGT(input1_2_r1, 0bin00));\n")
            OFile.write("ASSERT(BVGT(input1_3_r1, 0bin00));\n")
            OFile.write("ASSERT(BVGT(input1_4_r1, 0bin00));\n")
            OFile.write("ASSERT(BVGT(input1_5_r1, 0bin00));\n")
            OFile.write("ASSERT(BVGT(input1_6_r1, 0bin00));\n")
            OFile.write("ASSERT(BVGT(input1_7_r1, 0bin00));\n")
            OFile.write("ASSERT(BVGT(input1_8_r1, 0bin00));\n")

            OFile.write("ASSERT(BVGT(input2_1_r1, 0bin00));\n")
            OFile.write("ASSERT(BVGT(input2_2_r1, 0bin00));\n")
            OFile.write("ASSERT(BVGT(input2_3_r1, 0bin00));\n")
            OFile.write("ASSERT(BVGT(input2_4_r1, 0bin00));\n")
            OFile.write("ASSERT(BVGT(input2_5_r1, 0bin00));\n")
            OFile.write("ASSERT(BVGT(input2_6_r1, 0bin00));\n")
            OFile.write("ASSERT(BVGT(input2_7_r1, 0bin00));\n")
            OFile.write("ASSERT(BVGT(input2_8_r1, 0bin00));\n")

            OFile.write(
                f"ASSERT(BVGT(output1_r"
                f"{'{0}@output2_r{0}'.format(self.MyIntegral.Round) + ', 0bin' + '0' * 32}));\n"
            )
            OFile.write("\n")

            OFile.write("QUERY(FALSE); \n")
            OFile.write("COUNTEREXAMPLE; \n")

            OFile.close()
