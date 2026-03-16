import os
import time

from .cvc_test import test


def out_result(flag_stop, flag_analyse, round_i, Sbox_num_min, result_list):
    if flag_stop == 0:
        result_list.append("成功！" + str(round_i) + "轮达到最少的S盒个数，个数为" + str(Sbox_num_min))
        print("成功！" + str(round_i) + "轮达到最少的S盒个数，个数为" + str(Sbox_num_min))
    elif flag_stop == 1:
        result_list.append(
            "运行超时！ 运行到" + str(round_i) + "轮，最少的活跃S盒个数为" + str(Sbox_num_min)
        )
        print("运行超时！ 运行到" + str(round_i) + "轮，最少S盒个数为" + str(Sbox_num_min))
    elif flag_stop == 2:
        result_list.append(
            "运行成功，运行到"
            + str(round_i)
            + "轮，最少的活跃S盒个数为"
            + str(Sbox_num_min)
            + "\n查看详情差分路线或掩码路线，请下载报告文档查看"
        )
        print(
            "运行成功，运行到"
            + str(round_i)
            + "轮，最少的活跃S盒个数为"
            + str(Sbox_num_min)
            + "\n查看详情差分路线或掩码路线，请下载报告文档查看"
        )
    elif flag_stop == 3:  # 模加差分概率
        result_list.append(
            "运行成功，运行到"
            + str(round_i)
            + "轮，差分路线的最高差分概率为2^{-"
            + str(Sbox_num_min)
            + "}"
            + "\n查看详情差分路线，请下载报告文档查看"
        )
        print(
            "运行成功，运行到"
            + str(round_i)
            + "轮，差分路线的最高差分概率为2^{-"
            + str(Sbox_num_min)
            + "}"
            + "\n查看详情差分路线，请下载报告文档查看"
        )
    elif flag_stop == 4:  # 模加掩码概率
        result_list.append(
            "运行成功，截止运行到"
            + str(round_i)
            + "轮，线性掩码路线的最高相关度为2^{-"
            + str(Sbox_num_min)
            + "}，"
            + "\n查看详情掩码路线，请下载报告文档查看"
        )
        print(
            "运行成功，截止运行到"
            + str(round_i)
            + "轮，线性掩码路线的最高相关度为2^{-"
            + str(Sbox_num_min)
            + "}，"
            + "\n查看详情掩码路线，请下载报告文档查看"
        )
    elif flag_stop == 5:
        result_list.append("运行成功，查看详情不可能差分路线，请下载报告文档查看")
        print("运行成功，查看详情不可能差分路线，请下载报告文档查看")
    elif flag_stop == 6:
        result_list.append("运行成功，查看详情零相关线性路线，请下载报告文档查看")
        print("运行成功，查看详情零相关线性路线，请下载报告文档查看")
    elif flag_stop == 7:
        result_list.append("运行成功，查看详情积分路线，请下载报告文档查看")
        print("运行成功，查看详情积分路线，请下载报告文档查看")

    else:
        print("Unknown error")
        return


def testDIFanalyse(
    Blocksize,
    Round,
    Branch_number,
    Sbox_bit,
    Sbox_content,
    Matrix,
    NonlinearType,
    Sbox_num_min,
):
    result_list = []

    for round_i in range(1, Round + 1):
        left = 0
        Mytest = test(
            Blocksize,
            round_i,
            Branch_number,
            Sbox_bit,
            Sbox_content,
            Matrix,
            NonlinearType,
        )
        # 注意这里创建Mytest对象的时候第二个参数为本轮的round_i
        # 每一轮都建立一个对象

        for S_num_i in range(left, Sbox_num_min):  # 从小到大开始试
            Mytest.DIFanalyze(S_num_i)

            time_start = time.time()
            re = os.popen("'stp' 'app/utils/analysis/cvc/DIF.cvc'")
            re = re.readlines()
            # print(re)
            time_end = time.time()
            timeuse = time_end - time_start

            if re[-1] == "Invalid.\n":
                left = S_num_i
                if NonlinearType == "Sbox":
                    print(
                        str(round_i)
                        + "轮，最少活跃S盒个数为"
                        + str(S_num_i)
                        + "    STP求解用时".ljust(10)
                        + str(format(timeuse, ".3f"))
                        + "秒"
                    )
                    result_list.append(str(round_i) + "轮，最少活跃S盒个数为" + str(S_num_i))
                else:
                    print(
                        str(round_i)
                        + "轮加密算法，差分路线的最高差分概率为2^{-"
                        + str(S_num_i)
                        + "}"
                        # + "    STP求解用时"
                        # + str(format(timeuse, ".3f"))
                        # + "秒"
                    )
                    result_list.append(
                        str(round_i)
                        + "轮加密算法，差分路线的最高差分概率为2^{-"
                        + str(S_num_i)
                        + "}"
                        # + "    STP求解用时"
                        # + str(format(timeuse, ".3f"))
                        # + "秒"
                    )
                if left == Sbox_num_min or timeuse >= 3000:
                    f = open(
                        "app/utils/analysis/result/差分.txt",
                        "w",
                    )
                    # print(f)
                    for line in re:
                        f.write(str(line))
                    f.close()

                    if left == Sbox_num_min:
                        out_result(0, "DIF", round_i, Sbox_num_min, result_list)
                        # print("success！"+str(round_i)+"轮达到最小S盒个数为"+str(Sbox_num_min))
                    elif timeuse >= 3000:
                        out_result(1, "DIF", round_i, S_num_i, result_list)
                        # print("time out!运行到第"+str(round_i)+"轮，最小S盒个数为"+str(S_num_i))

                    return result_list
                break
        if round_i == Round:
            if NonlinearType == "Sbox":
                f = open(
                    "app/utils/analysis/result/差分.txt",
                    "w",
                )
                # print(f)
                for line in re:
                    f.write(str(line))
                f.close()
                out_result(2, "DIF", round_i, S_num_i, result_list)
            else:
                f = open(
                    "app/utils/analysis/result/差分.txt",
                    "w",
                )
                # print(f)
                for line in re:
                    f.write(str(line))
                f.close()
                out_result(3, "DIF", round_i, S_num_i, result_list)
    return result_list


def testLinearanalyse(
    Blocksize,
    Round,
    Branch_number,
    Sbox_bit,
    Sbox_content,
    Matrix,
    NonlinearType,
    Sbox_num_min,
):
    result_list = []

    for round_i in range(1, Round + 1):
        left = 0
        Mytest = test(
            Blocksize,
            round_i,
            Branch_number,
            Sbox_bit,
            Sbox_content,
            Matrix,
            NonlinearType,
        )

        for S_num_i in range(left, Sbox_num_min):  # 从小到大开始试
            Mytest.Linearanalyze(S_num_i)

            time_start = time.time()
            re = os.popen("'stp' 'app/utils/analysis/cvc/Linear.cvc'")
            re = re.readlines()
            # print(re)
            time_end = time.time()
            timeuse = time_end - time_start

            if re[-1] == "Invalid.\n":
                left = S_num_i
                if NonlinearType == "Sbox":
                    # print(str(round_i) + "轮加密算法，最少活跃S盒个数为" + str(S_num_i) + "    STP求解用时" + str(timeuse) + "秒")
                    print(
                        str(round_i)
                        + "轮加密算法，最少活跃S盒个数为"
                        + str(S_num_i)
                        + "    STP求解用时"
                        + str(format(timeuse, ".3f"))
                        + "秒"
                    )
                    result_list.append(str(round_i) + "轮加密算法，最少活跃S盒个数为" + str(S_num_i))
                else:
                    print(
                        str(round_i)
                        + "轮加密算法，线性掩码路线的最高相关度为2^{-"
                        + str(S_num_i)
                        + "}"
                        # + "    STP求解用时"
                        # + str(format(timeuse, ".3f"))
                        # + "秒"
                    )
                    # print(str(round_i) + "轮加密算法，差分路线的最高差分概率为2^{-" + str(S_num_i) + "}    STP求解用时" + str(timeuse) +
                    # "秒")
                    result_list.append(
                        str(round_i)
                        + "轮加密算法，线性掩码路线的最高相关度为2^{-"
                        + str(S_num_i)
                        + "}"
                        # + "    STP求解用时"
                        # + str(format(timeuse, ".3f"))
                        # + "秒"
                    )

                if left == Sbox_num_min or timeuse >= 3000:
                    f = open("app/utils/analysis/result/线性.txt", "w")
                    # print(f)
                    for line in re:
                        f.write(str(line))
                    f.close()

                    if left == Sbox_num_min:
                        out_result(0, "Linear", round_i, Sbox_num_min, result_list)
                        # print("success！"+str(round_i)+"轮达到最小S盒个数为"+str(Sbox_num_min))
                    elif timeuse >= 3000:
                        out_result(1, "Linear", round_i, S_num_i, result_list)
                        # print("time out!运行到第"+str(round_i)+"轮，最小S盒个数为"+str(S_num_i))

                    return result_list
                break
        if round_i == Round:
            if NonlinearType == "Sbox":
                f = open("app/utils/analysis/result/线性.txt", "w")
                # print(f)
                for line in re:
                    f.write(str(line))
                f.close()
                out_result(2, "Linear", round_i, S_num_i, result_list)
            else:
                f = open("app/utils/analysis/result/线性.txt", "w")
                # print(f)
                for line in re:
                    f.write(str(line))
                f.close()
                out_result(4, "Linear", round_i, S_num_i, result_list)
    return result_list


def testImpossibleanalyse(
    Blocksize,
    Round,
    Branch_number,
    Sbox_bit,
    Sbox_content,
    Matrix,
    NonlinearType,
    Sbox_num_min,
):
    result_list = []

    for round_i in range(1, Round + 1):
        Mytest = test(
            Blocksize,
            round_i,
            Branch_number,
            Sbox_bit,
            Sbox_content,
            Matrix,
            NonlinearType,
        )
        count = 0
        S_num_i = 0
        for input in range(0, Mytest.Blocksize):
            for output in range(0, Mytest.Blocksize):
                Mytest.ImpossibleDifferentialAnalyse(input, output)

                time_start = time.time()
                re = os.popen("'stp'  'app/utils/analysis/cvc/Impossible.cvc'")
                re = re.readlines()
                # print(re)
                time_end = time.time()
                timeuse = time_end - time_start

                if re[-1] == "Valid.\n":
                    count = count + 1
                    if count == 1:
                        print(
                            str(round_i)
                            + "轮密码算法，存在不可能差分路线"
                            + "    STP求解用时"
                            + str(format(timeuse, ".3f"))
                            + "秒"
                        )
                    result_list.append(
                        str(round_i)
                        + "轮密码算法，存在不可能差分路线，"
                        + "\n输入差分为"
                        + "0bin"
                        + "0" * (Mytest.Blocksize - 1 - input)
                        + "1"
                        + "0" * input
                        + "，\n输出差分为"
                        + "0bin"
                        + "0" * (Mytest.Blocksize - 1 - output)
                        + "1"
                        + "0" * output
                        + "。"
                    )
                    # if(timeuse >= 3000):
                    break
            break
        if count == 0:
            print(str(round_i) + "轮密码算法不存在不可能差分路线")
            result_list.append(str(round_i) + "轮密码算法不存在不可能差分路线")
        if round_i == Round:
            out_result(5, "Impossible", round_i, S_num_i, result_list)
    return result_list


def testZeroCorrelationanalyse(
    Blocksize,
    Round,
    Branch_number,
    Sbox_bit,
    Sbox_content,
    Matrix,
    NonlinearType,
    Sbox_num_min,
):
    result_list = []

    for round_i in range(1, Round + 1):
        Mytest = test(
            Blocksize,
            round_i,
            Branch_number,
            Sbox_bit,
            Sbox_content,
            Matrix,
            NonlinearType,
        )
        count = 0
        S_num_i = 0
        for input in range(0, Mytest.Blocksize):
            for output in range(0, Mytest.Blocksize):
                Mytest.ZeroCorrelationLinearAnalyse(input, output)

                time_start = time.time()
                re = os.popen("'stp'  'app/utils/analysis/cvc/ZeroCorrelation.cvc'")
                re = re.readlines()
                # print(re)
                time_end = time.time()
                timeuse = time_end - time_start

                if re[-1] == "Valid.\n":
                    count = count + 1
                    if count == 1:
                        print(
                            str(round_i)
                            + "轮密码算法，存在零相关线性路线"
                            + "    STP求解用时"
                            + str(format(timeuse, ".3f"))
                            + "秒"
                        )
                    result_list.append(
                        str(round_i)
                        + "轮密码算法，存在零相关线性路线，"
                        + "\n输入掩码为"
                        + "0bin"
                        + "0" * (Mytest.Blocksize - 1 - input)
                        + "1"
                        + "0" * input
                        + "，\n输出掩码为"
                        + "0bin"
                        + "0" * (Mytest.Blocksize - 1 - output)
                        + "1"
                        + "0" * output
                        + "。"
                    )
                    # if(timeuse >= 3000):
                    break
            break
        if count == 0:
            print(str(round_i) + "轮密码算法不存在零相关线性路线")
            result_list.append(str(round_i) + "轮密码算法不存在零相关线性路线")
        if round_i == Round:
            out_result(6, "ZeroCorrelation", round_i, S_num_i, result_list)

    return result_list


def testIntegralanalyse(
    Blocksize,
    Round,
    Branch_number,
    Sbox_bit,
    Sbox_content,
    Matrix,
    NonlinearType,
    Sbox_num_min,
):
    result_list = []

    for round_i in range(1, Round + 1):
        Mytest = test(
            Blocksize,
            round_i,
            Branch_number,
            Sbox_bit,
            Sbox_content,
            Matrix,
            NonlinearType,
        )
        Mytest.Integralanalyse()
        S_num_i = 0

        time_start = time.time()
        re = os.popen("'stp'  'app/utils/analysis/cvc/Integral.cvc'")
        re = re.readlines()
        # print(re)
        time_end = time.time()
        timeuse = time_end - time_start

        if re[-1] == "Invalid.\n":
            print(
                str(round_i)
                + "轮密码算法，存在积分攻击路线    STP求解用时为"
                + str(format(timeuse, ".3f"))
                + "秒"
            )
            # print(str(round_i) + "轮密码算法，存在积分攻击路线")
            result_list.append(str(round_i) + "轮密码算法，存在积分攻击路线")

        if round_i == Round:
            f = open("app/utils/analysis/result/积分.txt", "w")
            # print(f)
            for line in re:
                f.write(str(line))
            f.close()
            out_result(7, "Integral", round_i, S_num_i, result_list)

    return result_list


def DifferentialAnalyse(
    Blocksize, Round, Branch_number, Sbox_bit, Sbox_content, Matrix, NonlinearType
):
    Sbox_num_min = 100
    result_context = []
    print("==========差分分析==========")
    DIF_context = testDIFanalyse(
        Blocksize,
        Round,
        Branch_number,
        Sbox_bit,
        Sbox_content,
        Matrix,
        NonlinearType,
        Sbox_num_min,
    )
    # print(DIF_context)

    result_context.append("========差分分析=======")
    result_context += DIF_context

    return result_context  # 这个return可以给分析报告用


def LinearAnalyse(
    Blocksize, Round, Branch_number, Sbox_bit, Sbox_content, Matrix, NonlinearType
):
    Sbox_num_min = 100
    result_context = []
    print("==========线性分析==========")
    Linear_context = testLinearanalyse(
        Blocksize,
        Round,
        Branch_number,
        Sbox_bit,
        Sbox_content,
        Matrix,
        NonlinearType,
        Sbox_num_min,
    )
    # print(Linear_context)

    result_context.append("========线性分析=======")
    result_context += Linear_context

    return result_context


def ImpossibleAnalyse(
    Blocksize, Round, Branch_number, Sbox_bit, Sbox_content, Matrix, NonlinearType
):
    result_context = []
    Sbox_num_min = 100
    print("==========不可能差分分析==========")
    Impossible_context = testImpossibleanalyse(
        Blocksize,
        Round,
        Branch_number,
        Sbox_bit,
        Sbox_content,
        Matrix,
        NonlinearType,
        Sbox_num_min,
    )

    result_context.append("========不可能差分分析=======")
    result_context += Impossible_context

    return result_context


def ZeroCorrelationAnalyse(
    Blocksize, Round, Branch_number, Sbox_bit, Sbox_content, Matrix, NonlinearType
):
    result_context = []
    Sbox_num_min = 100
    print("==========零相关线性分析==========")
    ZeroCorrelation_context = testZeroCorrelationanalyse(
        Blocksize,
        Round,
        Branch_number,
        Sbox_bit,
        Sbox_content,
        Matrix,
        NonlinearType,
        Sbox_num_min,
    )

    result_context.append("========零相关线性分析=======")
    result_context += ZeroCorrelation_context

    return result_context


def IntegralAnalyse(
    Blocksize, Round, Branch_number, Sbox_bit, Sbox_content, Matrix, NonlinearType
):
    result_context = []
    Sbox_num_min = 100
    print("==========积分分析==========")
    Integral_context = testIntegralanalyse(
        Blocksize,
        Round,
        Branch_number,
        Sbox_bit,
        Sbox_content,
        Matrix,
        NonlinearType,
        Sbox_num_min,
    )

    result_context.append("========积分分析=======")
    result_context += Integral_context

    return result_context
