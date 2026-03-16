<template>

  <n-layout>
    <n-layout-header>
      <div class="header-bar">
        <div class="header-content">
          <div class="header-left">
            <h1 class="title">对称密码算法全过程自动化辅助设计平台</h1>
          </div>
          <div class="header-right">
            <n-switch @update:value="dark">
              <template #checked> 浅色模式 </template>
              <template #unchecked> 深色模式 </template>
            </n-switch>

            <span style="font-size: 16px">欢迎您，{{ admin_info.username }}</span>
            <n-button type="error" size="small" @click="logout">退出登录</n-button>
          </div>
        </div>
      </div>
    </n-layout-header>
  </n-layout>
  <n-layout has-sider>
    <n-layout-sider
      bordered
      collapse-mode="width"
      :collapsed-width="64"
      :width="250"

      >
      <n-menu :options="menuOptions" :default-value="defaultKey" />
      <!-- <div class="footer">版权所有，请勿二次开发</div> -->
    </n-layout-sider>
    <router-view></router-view>
  </n-layout>

  <!--
  <n-modal v-model:show="showDocModal">
    <n-card
      style="width: 1000px"
      closable
      title="《对称密码设计与安全性评估辅助平台》说明文档"
      @close="showDocModal = false">
      <n-layout has-sider>
        <n-layout-sider>
          <n-anchor style="width: 200px">
            <n-anchor-link title="背景" href="#背景" />
            <n-anchor-link title="正文" href="#正文" />
            <n-anchor-link title="差分分析" href="#差分分析">
              <n-anchor-link title="定义变量函数" href="#dif_vars" />
              <n-anchor-link title="定义组件函数" href="#dif_comps" />
            </n-anchor-link>
            <n-anchor-link title="线性分析" href="#线性分析">
              <n-anchor-link title="定义变量函数" href="#l_vars" />
              <n-anchor-link title="定义组件函数" href="#l_comps" />
            </n-anchor-link>
            <n-anchor-link title="不可能差分分析" href="#不可能差分分析">
              <n-anchor-link title="定义变量函数" href="#n_vars" />
              <n-anchor-link title="定义组件函数" href="#n_comps" />
            </n-anchor-link>
            <n-anchor-link title="零相关线性分析" href="#零相关线性分析">
              <n-anchor-link title="定义变量函数" href="#z_vars" />
              <n-anchor-link title="定义组件函数" href="#z_comps" />
            </n-anchor-link>
            <n-anchor-link title="积分分析" href="#积分分析">
              <n-anchor-link title="定义变量函数" href="#i_vars" />
              <n-anchor-link title="定义组件函数" href="#i_comps" />
            </n-anchor-link>
            <n-anchor-link title="下载分析报告" href="#download_report" />
          </n-anchor>
        </n-layout-sider>
        <n-layout style="padding: 20px">
          <n-scrollbar style="max-height: 500px">
            <h1>《对称密码设计与安全性评估辅助平台》说明文档</h1>
            <p>
              本对称密码设计与安全性评估辅助平台旨在辅助用户进行对称密码的安全性评估，包括差分分析、线性分析、不可能差分分析、零相关线性分析、积分分析。
              算法目标对象包含已有的所有算法结构，算法结构可由用户自行设计，该平台所含线性组件和非线性组件种类齐全，使用简单，对用户知识要求低。
            </p>
            <h2 id="背景">背景</h2>
            <p>
              密码学作为保障数据安全传输的理论基础，在信息安全日益得到人们重视的大背景下，逐渐成为热点研究方向。其中，对称密码的强适应性、高灵活性的优势，使得对称密码得以广泛应用。当今人们对于加密算法的需求也日益多元化，我们开发的对称密码设计与安全性评估辅助平台，可以允许用户根据自己特定需求和场景来设计用户想要的加密算法，对于某些应用，自己设计的密码算法意味着用户不需要依赖公开的密码算法，从而减少了潜在的信息泄露风险。加密算法在使用过程中的安全性是首要的，我们也集成了对用户设计的加密算法的安全性评估，这样可以有效的减少人力物力资源，具体而言，我们将差分攻击、线性攻击、不可能差分攻击、零相关线性攻击、积分攻击进行模块化实现，通过解析的方法将用户的加密算法基本描述和各模块进行链接，能对目标加密算法的安全性进行评估并返回报告。
            </p>
            <h2 id="正文">正文</h2>
            <p>
              本对称密码设计与安全性评估辅助平台支持用户自定义设计密码算法结构，用户输入密码算法的基本信息分组大小、分支数、置换线性矩阵（可选）、非线性组件类型，即可开始自定义设计密码算法。在设计密码算法部分，用户需使用本文件中给定的函数来设置变量，通过控制各变量之间的约束条件来描述轮函数，用户编辑的轮函数会上传到后台，后台脚本文件会自动生成CVC语言的文件并调用STP求解器，后台得到求解结果后会在前端返回安全性评估结果，支持用户下载分析报告。
            </p>
            <p>下面介绍不同攻击方式所支持的变量函数及组件函数：</p>
            <h2 id="差分分析">差分分析</h2>
            <h3 id="dif_vars">定义变量函数</h3>
            <p>
              <n-ol>
                <n-li
                  >用户可以自行定义每一轮输入变量个数，下面给出四个输入差分变量和输出差分变量以供参考：
                  <n-ul>
                    <n-li>input1_At_Round(r)</n-li>
                    <n-li>input2_At_Round(r)</n-li>
                    <n-li>input3_At_Round(r)</n-li>
                    <n-li>input4_At_Round(r)</n-li>
                    <n-li>output1_At_Round(r)</n-li>
                    <n-li>output2_At_Round(r)</n-li>
                    <n-li>output3_At_Round(r)</n-li>
                    <n-li>output4_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
                <n-li>
                  S盒的输入差分变量和输出差分变量：
                  <n-ul>
                    <n-li>S_in_At_Round(r)</n-li>
                    <n-li>S_out_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
                <n-li>
                  异或的两个输入差分变量和一个输出差分变量：
                  <n-ul>
                    <n-li>XOR_input1_At_Round(r)</n-li>
                    <n-li>XOR_input2_At_Round(r)</n-li>
                    <n-li>XOR_output_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
                <n-li>
                  比特级置换的输入差分变量与输出差分变量：
                  <n-ul>
                    <n-li>permutationIn_At_Round(r)</n-li>
                    <n-li>permutationOut_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
                <n-li>
                  模加的两个输入差分变量和一个输出差分变量：
                  <n-ul>
                    <n-li>modulo_input1_At_Round(r)</n-li>
                    <n-li>modulo_input2_At_Round(r)</n-li>
                    <n-li>modulo_output_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
                <n-li>
                  模加差分概率的统计变量：
                  <n-ul>
                    <n-li>weight_zhi_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
                <n-li>
                  非线性组件OR的两个输入差分变量和一个输出差分变量：
                  <n-ul>
                    <n-li>OR_input1_At_Round(r)</n-li>
                    <n-li>OR_input2_At_Round(r)</n-li>
                    <n-li>OR_output_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
                <n-li>
                  非线性组件AND的两个输入差分变量和一个输出差分变量：
                  <n-ul>
                    <n-li>AND_input1_At_Round(r)</n-li>
                    <n-li>AND_input2_At_Round(r)</n-li>
                    <n-li>AND_output_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
              </n-ol>
            </p>
            <h3 id="dif_comps">定义组件函数</h3>
            <p>
              <n-ul>
                <n-li>
                  BVXOR(input1, input2, output)：异或运算，接受两个输入差分变量和一个输出差分变量
                </n-li>
                <n-li>
                  Permutation(inP, outP)：比特级置换，接受一个输入差分变量和一个输出差分变量
                </n-li>
                <n-li> equal(var1, var2)：相等操作，用于各个组件变量之间的连接 </n-li>
                <n-li> left_shift(var, num)：左移位操作：接受变量和左移值 </n-li>
                <n-li> right_shift(var, num)：右移位操作：接受变量和右移值 </n-li>
                <n-li>
                  modulo_addition(input1, input2,
                  output)：差分通过非线性组件模加，接受两个输入差分变量和一个输出差分变量
                </n-li>
                <n-li>
                  Weight(input1, input2, output,
                  weight_zhi)：此函数是为了计算模加差分的概率，最终变量weight_zhi的汉明重量即为总概率的以2为底的负对数
                </n-li>
                <n-li>
                  Function_Sbox(input,
                  output)：差分通过非线性组件S盒，接受S盒的输入差分变量和输出差分变量
                </n-li>
                <n-li>
                  Function_OR(input1, input2,
                  output)：差分通过非线性组件”OR”，接受两个输入差分变量和一个输出差分变量
                </n-li>
                <n-li>
                  Function_AND(input1, input2,
                  output)：差分通过非线性组件“AND”，接受两个输入差分变量和一个输出差分变量
                </n-li>
                <n-li> cyclic_left_shift(var, num)：循环左移操作，接受输入变量和左移位值 </n-li>
                <n-li> cyclic_right_shift(var, num)：循环右移操作，接受输入变量和右移位值 </n-li>
              </n-ul>
            </p>
            <h2 id="线性分析">线性分析</h2>
            <h3 id="l_vars">定义变量函数</h3>
            <p>
              <n-ol>
                <n-li>
                  用户可以自行定义每一轮输入变量个数，下面给出四个输入线性变量和输出线性变量以供参考：
                  <n-ul>
                    <n-li>input1_At_Round(r)</n-li>
                    <n-li>input2_At_Round(r)</n-li>
                    <n-li>input3_At_Round(r)</n-li>
                    <n-li>input4_At_Round(r)</n-li>
                    <n-li>output1_At_Round(r)</n-li>
                    <n-li>output2_At_Round(r)</n-li>
                    <n-li>output3_At_Round(r)</n-li>
                    <n-li>output4_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
                <n-li>
                  S盒的输入线性变量和输出线性变量：
                  <n-ul>
                    <n-li>S_in_At_Round(r)</n-li>
                    <n-li>S_out_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
                <n-li>
                  异或的两个输入线性变量和一个输出线性变量：
                  <n-ul>
                    <n-li>XOR_input1_At_Round(r)</n-li>
                    <n-li>XOR_input2_At_Round(r)</n-li>
                    <n-li>XOR_output_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
                <n-li>
                  比特级置换的输入线性变量与输出线性变量：
                  <n-ul>
                    <n-li>permutationIn_At_Round(r)</n-li>
                    <n-li>permutationOut_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
                <n-li>
                  模加的两个输入线性变量和一个输出线性变量：
                  <n-ul>
                    <n-li>modulo_input1_At_Round(r)</n-li>
                    <n-li>modulo_input2_At_Round(r)</n-li>
                    <n-li>modulo_output_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
                <n-li>
                  模加线性概率的统计变量：
                  <n-ul>
                    <n-li>weight_zhi_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
                <n-li>
                  非线性组件OR的两个输入线性变量和一个输出线性变量：
                  <n-ul>
                    <n-li>OR_input1_At_Round(r)</n-li>
                    <n-li>OR_input2_At_Round(r)</n-li>
                    <n-li>OR_output_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
                <n-li>
                  非线性组件AND的两个输入线性变量和一个输出线性变量：
                  <n-ul>
                    <n-li>AND_input1_At_Round(r)</n-li>
                    <n-li>AND_input2_At_Round(r)</n-li>
                    <n-li>AND_output_At_Round(r)</n-li>
                  </n-ul>
                </n-li>

                <n-li>
                  由于线性掩码在分支运算这一结构传播时所满足的约束条件是：输入掩码为α，输出掩码分别为β_1
                  、β_2，则β_1⨁β_2=α
                  用户可以自行定义分支运算的数量，下面给出两个分支的掩码变量以供参考：
                  <n-ul>
                    <n-li>Split1_input1_At_Round(r)</n-li>
                    <n-li>Split1_input2_At_Round(r)</n-li>
                    <n-li>Split1_output_At_Round(r)</n-li>
                    <n-li>Split2_input1_At_Round(r)</n-li>
                    <n-li>Split2_input2_At_Round(r)</n-li>
                    <n-li>Split2_output_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
              </n-ol>
            </p>
            <h3 id="l_comps">定义组件函数</h3>
            <p>
              <n-ul>
                <n-li>
                  BVXOR(input1, input2, output)：异或运算，接受两个输入线性变量和一个输出线性变量
                </n-li>
                <n-li>
                  Permutation(inP, outP)：比特级置换，接受一个输入线性变量和一个输出线性变量
                </n-li>
                <n-li> equal(var1, var2)：相等操作，用于各个组件变量之间的连接 </n-li>
                <n-li> left_shift(var, num)：左移位操作：接受变量和左移值 </n-li>
                <n-li> right_shift(var, num)：右移位操作：接受变量和右移值 </n-li>
                <n-li>
                  Split(input1, input2,
                  output)：分支操作：由于线性掩码在分支运算这一结构传播时所满足的约束条件是：输入掩码为α，输出掩码分别为β_1
                  、β_2，则β_1⨁β_2= α，由于异或操作的性质，若接收两个输入掩码α_1
                  、α_2和一个输出掩码β，则有α_1⨁α_2=β. Split函数接受两个输入掩码α_1
                  、α_2和一个输出掩码β
                </n-li>
                <n-li>
                  modulo_addition(input1, input2,
                  output)：线性通过非线性组件模加，接受两个输入线性变量和一个输出线性变量
                </n-li>
                <n-li>
                  Function_Sbox(input,
                  output)：线性通过非线性组件S盒，接受S盒的输入线性变量和输出线性变量
                </n-li>
                <n-li>
                  Function_OR(input1, input2,
                  output)：线性通过非线性组件”OR”，接受两个输入线性变量和一个输出线性变量
                </n-li>
                <n-li>
                  Function_AND(input1, input2,
                  output)：线性通过非线性组件“AND”，接受两个输入线性变量和一个输出线性变量
                </n-li>
                <n-li> cyclic_left_shift(var, num)：循环左移操作，接受输入变量和左移位值 </n-li>
                <n-li> cyclic_right_shift(var, num)：循环右移操作，接受输入变量和右移位值 </n-li>
              </n-ul>
            </p>
            <h2 id="不可能差分分析">不可能差分分析</h2>
            <h3 id="n_vars">定义变量函数</h3>
            <p>
              <n-ol>
                <n-li>
                  用户可以自行定义每一轮输入变量个数，下面给出四个输入差分变量和输出差分变量以供参考：
                  <n-ul>
                    <n-li>input1_At_Round(r)</n-li>
                    <n-li>input2_At_Round(r)</n-li>
                    <n-li>input3_At_Round(r)</n-li>
                    <n-li>input4_At_Round(r)</n-li>
                    <n-li>output1_At_Round(r)</n-li>
                    <n-li>output2_At_Round(r)</n-li>
                    <n-li>output3_At_Round(r)</n-li>
                    <n-li>output4_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
                <n-li>
                  S盒的输入差分变量和输出差分变量：
                  <n-ul>
                    <n-li>S_in_At_Round(r)</n-li>
                    <n-li>S_out_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
                <n-li>
                  异或的两个输入差分变量和一个输出差分变量：
                  <n-ul>
                    <n-li>XOR_input1_At_Round(r)</n-li>
                    <n-li>XOR_input2_At_Round(r)</n-li>
                    <n-li>XOR_output_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
                <n-li>
                  比特级置换的输入差分变量与输出差分变量：
                  <n-ul>
                    <n-li>permutationIn_At_Round(r)</n-li>
                    <n-li>permutationOut_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
                <n-li>
                  模加的两个输入差分变量和一个输出差分变量：
                  <n-ul>
                    <n-li>modulo_input1_At_Round(r)</n-li>
                    <n-li>modulo_input2_At_Round(r)</n-li>
                    <n-li>modulo_output_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
                <n-li>
                  模加差分概率的统计变量：
                  <n-ul>
                    <n-li>weight_zhi_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
                <n-li>
                  非线性组件OR的两个输入差分变量和一个输出差分变量：
                  <n-ul>
                    <n-li>OR_input1_At_Round(r)</n-li>
                    <n-li>OR_input2_At_Round(r)</n-li>
                    <n-li>OR_output_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
                <n-li>
                  非线性组件AND的两个输入差分变量和一个输出差分变量：
                  <n-ul>
                    <n-li>AND_input1_At_Round(r)</n-li>
                    <n-li>AND_input2_At_Round(r)</n-li>
                    <n-li>AND_output_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
              </n-ol>
            </p>
            <h3 id="n_comps">定义组件函数</h3>
            <p>
              <n-ul>
                <n-li>
                  BVXOR(input1, input2, output)：异或运算，接受两个输入差分变量和一个输出差分变量
                </n-li>
                <n-li>
                  Permutation(inP, outP)：比特级置换，接受一个输入差分变量和一个输出差分变量
                </n-li>
                <n-li> equal(var1, var2)：相等操作，用于各个组件变量之间的连接 </n-li>
                <n-li> left_shift(var, num)：左移位操作：接受变量和左移值 </n-li>
                <n-li> right_shift(var, num)：右移位操作：接受变量和右移值 </n-li>
                <n-li>
                  modulo_addition(input1, input2,
                  output)：差分通过非线性组件模加，接受两个输入差分变量和一个输出差分变量
                </n-li>
                <n-li>
                  Weight(input1, input2, output,
                  weight_zhi)：此函数是为了计算模加差分的概率，最终变量weight_zhi的汉明重量即为总概率的以2为底的负对数
                </n-li>
                <n-li>
                  Function_Sbox(input,
                  output)：差分通过非线性组件S盒，接受S盒的输入差分变量和输出差分变量
                </n-li>
                <n-li>
                  Function_OR(input1, input2,
                  output)：差分通过非线性组件”OR”，接受两个输入差分变量和一个输出差分变量
                </n-li>
                <n-li>
                  Function_AND(input1, input2,
                  output)：差分通过非线性组件“AND”，接受两个输入差分变量和一个输出差分变量
                </n-li>
                <n-li> cyclic_left_shift (var, num)：循环左移操作，接受输入变量和左移位值 </n-li>
                <n-li> cyclic_right_shift(var, num)：循环右移操作，接受输入变量和右移位值 </n-li>
              </n-ul>
            </p>
            <h2 id="零相关线性分析">零相关线性分析</h2>
            <h3 id="z_vars">定义变量函数</h3>
            <p>
              <n-ol>
                <n-li>
                  用户可以自行定义每一轮输入变量个数，下面给出四个输入线性变量和输出线性变量以供参考：
                  <n-ul>
                    <n-li>input1_At_Round(r)</n-li>
                    <n-li>input2_At_Round(r)</n-li>
                    <n-li>input3_At_Round(r)</n-li>
                    <n-li>input4_At_Round(r)</n-li>
                    <n-li>output1_At_Round(r)</n-li>
                    <n-li>output2_At_Round(r)</n-li>
                    <n-li>output3_At_Round(r)</n-li>
                    <n-li>output4_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
                <n-li>
                  S盒的输入线性变量和输出线性变量：
                  <n-ul>
                    <n-li>S_in_At_Round(r)</n-li>
                    <n-li>S_out_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
                <n-li>
                  异或的两个输入线性变量和一个输出线性变量：
                  <n-ul>
                    <n-li>XOR_input1_At_Round(r)</n-li>
                    <n-li>XOR_input2_At_Round(r)</n-li>
                    <n-li>XOR_output_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
                <n-li>
                  比特级置换的输入线性变量与输出线性变量：
                  <n-ul>
                    <n-li>permutationIn_At_Round(r)</n-li>
                    <n-li>permutationOut_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
                <n-li>
                  模加的两个输入线性变量和一个输出线性变量：
                  <n-ul>
                    <n-li>modulo_input1_At_Round(r)</n-li>
                    <n-li>modulo_input2_At_Round(r)</n-li>
                    <n-li>modulo_output_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
                <n-li>
                  模加线性概率的统计变量：
                  <n-ul>
                    <n-li>weight_zhi_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
                <n-li>
                  非线性组件OR的两个输入线性变量和一个输出线性变量：
                  <n-ul>
                    <n-li>OR_input1_At_Round(r)</n-li>
                    <n-li>OR_input2_At_Round(r)</n-li>
                    <n-li>OR_output_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
                <n-li>
                  非线性组件AND的两个输入线性变量和一个输出线性变量：
                  <n-ul>
                    <n-li>AND_input1_At_Round(r)</n-li>
                    <n-li>AND_input2_At_Round(r)</n-li>
                    <n-li>AND_output_At_Round(r)</n-li>
                  </n-ul>
                </n-li>

                <n-li>
                  由于线性掩码在分支运算这一结构传播时所满足的约束条件是：输入掩码为α，输出掩码分别为β_1
                  、β_2，则β_1⨁β_2=α
                  用户可以自行定义分支运算的数量，下面给出两个分支的掩码变量以供参考：
                  <n-ul>
                    <n-li>Split1_input1_At_Round(r)</n-li>
                    <n-li>Split1_input2_At_Round(r)</n-li>
                    <n-li>Split1_output_At_Round(r)</n-li>
                    <n-li>Split2_input1_At_Round(r)</n-li>
                    <n-li>Split2_input2_At_Round(r)</n-li>
                    <n-li>Split2_output_At_Round(r)</n-li>
                  </n-ul>
                </n-li>
              </n-ol>
            </p>
            <h3 id="z_comps">定义组件函数</h3>
            <p>
              <n-ul>
                <n-li>
                  BVXOR(input1, input2, output)：异或运算，接受两个输入线性变量和一个输出线性变量
                </n-li>
                <n-li>
                  Permutation(inP, outP)：比特级置换，接受一个输入线性变量和一个输出线性变量
                </n-li>
                <n-li> equal(var1, var2)：相等操作，用于各个组件变量之间的连接 </n-li>
                <n-li> left_shift(var, num)：左移位操作：接受变量和左移值 </n-li>
                <n-li> right_shift(var, num)：右移位操作：接受变量和右移值 </n-li>
                <n-li>
                  Split(input1, input2,
                  output)：分支操作：由于线性掩码在分支运算这一结构传播时所满足的约束条件是：输入掩码为α，输出掩码分别为β_1
                  、β_2，则β_1⨁β_2= α，由于异或操作的性质，若接收两个输入掩码α_1
                  、α_2和一个输出掩码β，则有α_1⨁α_2=β. Split函数接受两个输入掩码α_1
                  、α_2和一个输出掩码β
                </n-li>
                <n-li>
                  modulo_addition(input1, input2,
                  output)：线性通过非线性组件模加，接受两个输入线性变量和一个输出线性变量
                </n-li>
                <n-li>
                  Function_Sbox(input,
                  output)：线性通过非线性组件S盒，接受S盒的输入线性变量和输出线性变量
                </n-li>
                <n-li>
                  Function_OR(input1, input2,
                  output)：线性通过非线性组件”OR”，接受两个输入线性变量和一个输出线性变量
                </n-li>
                <n-li>
                  Function_AND(input1, input2,
                  output)：线性通过非线性组件“AND”，接受两个输入线性变量和一个输出线性变量
                </n-li>
                <n-li> cyclic_left_shift (var, num)：循环左移操作，接受输入变量和左移位值 </n-li>
                <n-li> cyclic_right_shift(var, num)：循环右移操作，接受输入变量和右移位值 </n-li>
              </n-ul>
            </p>
            <h2 id="积分分析">积分分析</h2>
            <h3 id="i_vars">定义变量函数</h3>
          </n-scrollbar>
        </n-layout>
      </n-layout>
    </n-card>
  </n-modal>
  -->
</template>

<script setup lang="ts">
import { storageData } from "@/utils/stored-data"
import {
  NLayout,
  NLayoutSider,
  NMenu,
  NLayoutHeader,
  NButton,
  NSwitch,
  // NModal,
  // NScrollbar,
  // NCard,
  // NOl,
  // NLi,
  // NUl,
  // NAnchor,
  // NAnchorLink,
} from "naive-ui"
import { ref, h, onBeforeMount } from "vue"
import { RouterLink } from "vue-router"
import { useThemeStore } from "@/stores/theme-store"
import { useRoute } from "vue-router"

// const showDocModal = ref(false)
const route = useRoute()
const themeStore = useThemeStore()
const dark = () => {
  themeStore.toggleDarkMode()
}
const admin_info = ref({
  id: "",
  username: "",
  email: "",
})

const defaultKey = ref("")
const menuOptions = [
  {
    label: () =>
      h(
        RouterLink,
        {
          to: {
            name: "Welcome",
          },
        },
        { default: () => "欢迎页" },
      ),
    key: "welcome",
  },
  /*
  {
    label: "说明文档",
    key: "doc",
    onClick: () => {
      showDocModal.value = true
    },
  },
  */
  {
    label: () =>
      h(
        RouterLink,
        {
          to: {
            name: "Main",
          },
        },
        { default: () => "开始" },
      ),
  },
]

const logout = () => {
  storageData.remove("access_token")
  storageData.remove("admin_info")
  window.location.reload()
}

const routeNameToKey = () => {
  switch (route.name) {
    case "Welcome":
      return "welcome"
    case "Main":
      return "main"
    default:
      return "welcome"
  }
}

onBeforeMount(() => {
  // 从url中获取当前路由
  defaultKey.value = routeNameToKey()

  const adminInfo = storageData.get("admin_info")
  if (adminInfo) {
    admin_info.value = adminInfo
  }
})
</script>

<style lang="less" scoped>

.header-bar {
  display: flex;
  align-items: center;
  width: 100%;
  height: 60px;

  .header-content {
    margin: 0 10px;
    width: 100vi;
    height: 50px;
    display: flex;
    // justify-content: space-between;

    .header-left {
      display: flex;
      align-items: center;
      width: 300px;

      .title {
        // color: rgba(0, 0, 0, .85);
        margin: 1px;
        font-size: 16px;
        font-weight: 500;
        color: #63e2b7;

        // background-image: linear-gradient(45deg, #63e2b7 25%, transparent 25%);
      }
    }

    .header-right {
      // 靠右对齐
      margin-left: auto;
      display: flex;
      align-items: center;
      // 设置元素间隙
      gap: 10px;
    }
  }
}

// .footer {
//   position: absolute;
//   bottom: 0;
//   width: 100%;
//   height: 60px;
//   line-height: 60px;
//   text-align: center;
// }
// .p {
//   text-indent: 2em;
// }
</style>
