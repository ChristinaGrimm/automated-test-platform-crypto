<template>
  <div class="container">
    <steps
      :current="current"
      :title-list="['组件设计', '算法设计', '安全性分析', '实现分析']"></steps>
    
    <!-- 第一步：组件设计 -->
    <div v-if="current === 1">
      <div class="step-content">
        <n-form label-placement="left" label-width="auto" require-mark-placement="right">
          <!-- 组件类型选择 -->
          <n-form-item label="选择设计类型:" required>
            <n-checkbox-group v-model:value="selectedComponents">
              <n-space>
                <n-checkbox value="linear">线性层设计</n-checkbox>
                <n-checkbox value="sbox">S盒设计</n-checkbox>
              </n-space>
            </n-checkbox-group>
          </n-form-item>

          <!-- 线性层设计部分 -->
          <div v-if="selectedComponents.includes('linear')" class="component-section">
            <n-h3>线性层设计</n-h3>
            <n-tabs
              type="line"
              class="card-tabs"
              v-model:value="linearType"
              size="large"
              animated>
              <!-- 分块阵 -->
              <n-tab-pane name="block" tab="分块阵">
                <n-card
                  title="分块阵参数输入"
                  size="small"
                  :segmented="{ content: true }"
                  class="mt-3">
                  <n-form
                    :label-width="120"
                    label-placement="left"
                    size="small"
                    :model="blockMatrixForm">
                    <n-form-item label="分组大小(比特)">
                      <n-select
                        placeholder="请选择分组大小"
                        :options="blockSizeList2"
                        v-model:value="blockMatrixForm.block_size" />
                    </n-form-item>
                    <n-form-item label="分块大小(比特)">
                      <n-input
                        placeholder="请输入分块大小"
                        v-model:value="blockMatrixForm.bit_size" />
                    </n-form-item>
                    <n-form-item label="分支数">
                      <n-input
                        placeholder="请输入分支数"
                        v-model:value="blockMatrixForm.branch_number" />
                    </n-form-item>
                    <n-form-item label="异或数">
                      <n-input
                        placeholder="请输入异或数上界"
                        v-model:value="blockMatrixForm.xor_count" />
                    </n-form-item>
                    <n-form-item label="全扩散次数">
                      <n-input
                        placeholder="请输入全扩散次数上界"
                        v-model:value="blockMatrixForm.dr" />
                    </n-form-item>
                    <n-form-item label="数量">
                      <n-input
                        placeholder="请输入数量"
                        v-model:value="blockMatrixForm.quantity" />
                    </n-form-item>
                    <n-space>
                      <n-button
                        type="primary"
                        @click="handleBlockMatrixConstruction"
                        >提交构造</n-button
                      >
                      <n-button @click="resetBlockMatrixForm">重置</n-button>
                    </n-space>
                  </n-form>
                </n-card>

                <!-- 分块阵构造结果 -->
                <n-card
                  v-if="blockMatrixResult.length > 0"
                  title="分块阵构造结果"
                  :segmented="{ content: true }"
                  size="small"
                  class="mt-3 construction-result">
                  <n-table class="result-table">
                    <thead class="text-center">
                      <tr>
                        <th class="column-number">编号</th>
                        <th class="column-cost">异或数</th>
                        <th class="column-dr">全扩散次数</th>
                        <th class="column-matrix">矩阵</th>
                        <th class="column-actions">操作</th>
                      </tr>
                    </thead>
                    <tbody class="table-body text-center">
                      <tr v-for="(item, index) in blockMatrixResult" :key="index">
                        <td class="column-number">{{ index + 1 }}</td>
                        <td class="column-cost">{{ item.cost }}</td>
                        <td class="column-dr">{{ item.dr }}</td>
                        <td class="column-matrix">
                          <n-scrollbar style="max-height: 200px">
                            <pre>{{
                              formatBlockMatrix(
                                JSON.parse(item.matrix),
                                Number(blockMatrixForm.bit_size),
                              )
                            }}</pre>
                          </n-scrollbar>
                        </td>
                        <td class="column-actions">
                          <n-space justify="center">
                            <n-button 
                              type="primary" 
                              size="small"
                              @click="saveBlockMatrix(index)"
                              class="action-button">
                              保存
                            </n-button>
                            <n-button 
                              type="info" 
                              size="small"
                              :disabled="!savedFiles.blockMatrix[index]"
                              @click="download(savedFiles.blockMatrix[index])"
                              class="action-button">
                              下载
                            </n-button>
                          </n-space>
                        </td>
                      </tr>
                    </tbody>
                  </n-table>
                </n-card>
              </n-tab-pane>

              <!-- 比特阵 -->
              <n-tab-pane name="bit" tab="比特阵">
                <n-card
                  title="比特阵参数输入"
                  size="small"
                  :segmented="{ content: true }"
                  class="mt-3">
                  <n-form
                    :label-width="130"
                    label-placement="left"
                    size="small"
                    :model="bitMatrixForm">
                    <n-form-item label="分组大小(比特)">
                      <n-select
                        placeholder="请选择分组大小"
                        :options="blockSizeList"
                        v-model:value="bitMatrixForm.block_size" />
                    </n-form-item>
                    <n-form-item label="分支数">
                      <n-input
                        placeholder="请输入分支数"
                        v-model:value="bitMatrixForm.branch_number" />
                    </n-form-item>
                    <n-form-item label="深度">
                      <n-input
                        placeholder="请输入深度"
                        v-model:value="bitMatrixForm.depth" />
                    </n-form-item>
                    <n-form-item label="异或数">
                      <n-input
                        placeholder="请输入异或数"
                        v-model:value="bitMatrixForm.xor_count" />
                    </n-form-item>
                    <n-form-item label="数量">
                      <n-input
                        placeholder="请输入数量"
                        v-model:value="bitMatrixForm.quantity" />
                    </n-form-item>
                    <n-space>
                      <n-button
                        type="primary"
                        @click="handleBitMatrixConstruction"
                        >提交构造</n-button
                      >
                      <n-button @click="resetBitMatrixForm">重置</n-button>
                    </n-space>
                  </n-form>
                </n-card>

                <!-- 比特阵构造结果 -->
                <n-card
                  v-if="bitMatrixResult.length > 0"
                  title="比特阵构造结果"
                  :segmented="{ content: true }"
                  size="small"
                  class="mt-3 construction-result">
                  <n-table class="result-table">
                    <thead class="text-center">
                      <tr>
                        <th class="column-number">编号</th>
                        <th class="column-matrix">矩阵</th>
                        <th class="column-actions">操作</th>
                      </tr>
                    </thead>
                    <tbody class="table-body text-center">
                      <tr v-for="(matrix, index) in bitMatrixResult" :key="index">
                        <td class="column-number">{{ index + 1 }}</td>
                        <td class="column-matrix">
                          <pre>{{ array2string(matrix) }}</pre>
                        </td>
                        <td class="column-actions">
                          <n-space justify="center">
                            <n-button 
                              type="primary" 
                              size="small"
                              @click="saveBitMatrix(index)"
                              class="action-button">
                              保存
                            </n-button>
                            <n-button 
                              type="info" 
                              size="small"
                              :disabled="!savedFiles.bitMatrix[index]"
                              @click="download(savedFiles.bitMatrix[index])"
                              class="action-button">
                              下载
                            </n-button>
                          </n-space>
                        </td>
                      </tr>
                    </tbody>
                  </n-table>
                </n-card>
              </n-tab-pane>
            </n-tabs>
          </div>

          <!-- S盒设计部分 -->
          <div v-if="selectedComponents.includes('sbox')" class="component-section">
            <n-h3>S盒设计</n-h3>
            <n-card
              title="S盒参数输入"
              size="small"
              :segmented="{ content: true }"
              class="mt-3">
              <n-form
                :label-width="120"
                label-placement="left"
                size="small"
                :model="sboxForm">
                <n-form-item label="S盒大小(比特)">
                  <n-input-number
                    placeholder="请输入S盒大小"
                    v-model:value="sboxForm.bit_num"
                    :show-button="false" />
                </n-form-item>
                <n-form-item label="差分均匀度">
                  <n-input-number
                    placeholder="请输入差分均匀度"
                    v-model:value="sboxForm.diff_uniform"
                    :show-button="false" />
                </n-form-item>
                <n-form-item label="线性度">
                  <n-input-number
                    placeholder="请输入线性度"
                    v-model:value="sboxForm.linear_uniform"
                    :show-button="false" />
                </n-form-item>
                <n-form-item label="差分分支数">
                  <n-input-number
                    placeholder="请输入差分分支数"
                    v-model:value="sboxForm.dbn"
                    :show-button="false" />
                </n-form-item>
                <n-form-item label="线性分支数">
                  <n-input-number
                    placeholder="请输入线性分支数"
                    v-model:value="sboxForm.lbn"
                    :show-button="false" />
                </n-form-item>
                <n-form-item label="差分BIBO">
                  <n-input-number
                    placeholder="请输入差分BIBO"
                    v-model:value="sboxForm.bibo_ddt"
                    :show-button="false" />
                </n-form-item>
                <n-form-item label="线性BIBO">
                  <n-input-number
                    placeholder="请输入线性BIBO"
                    v-model:value="sboxForm.bibo_lat"
                    :show-button="false" />
                </n-form-item>
                <n-form-item label="数量">
                  <n-input-number
                    placeholder="请输入数量"
                    v-model:value="sboxForm.quantity"
                    :show-button="false" />
                </n-form-item>
                <n-space>
                  <n-button type="primary" @click="constructSbox">提交构造</n-button>
                  <n-button @click="resetSboxForm">重置</n-button>
                </n-space>
              </n-form>
            </n-card>

            <!-- S盒构造结果 -->
            <n-card
              v-if="sboxResult.length > 0"
              title="S盒构造结果"
              :segmented="{ content: true }"
              size="small"
              class="mt-3 construction-result">
              <n-table class="result-table">
                <thead class="text-center">
                  <tr>
                    <th class="column-number">编号</th>
                    <th class="column-sbox">S盒内容</th>
                    <th class="column-gates">门个数</th>
                    <th class="column-area">面积</th>
                    <th class="column-actions">操作</th>
                  </tr>
                </thead>
                <tbody class="text-center">
                  <tr v-for="(sbox, index) in sboxResult" :key="index">
                    <td class="column-number">{{ index + 1 }}</td>
                    <td class="column-sbox">{{ sbox.join(', ') }}</td>
                    <td class="column-gates">8</td>
                    <td class="column-area">12.33GE</td>
                    <td class="column-actions">
                      <n-space justify="center">
                        <n-button 
                          type="primary" 
                          size="small"
                          @click="saveSbox(index)"
                          class="action-button">
                          保存
                        </n-button>
                        <n-button 
                          type="info" 
                          size="small"
                          :disabled="!savedFiles.sbox[index]"
                          @click="download(savedFiles.sbox[index])"
                          class="action-button">
                          下载
                        </n-button>
                      </n-space>
                    </td>
                  </tr>
                </tbody>
              </n-table>
            </n-card>
          </div>
        </n-form>
      </div>
    </div>

    <!-- 第二步：算法设计 -->
    <div v-if="current === 2">
      <div class="step-content">
        <n-form label-placement="left" label-width="auto">
          <!-- 输入分组长度 -->
          <n-form-item label="分组长度:" path="blockLength" required>
            <n-input-number placeholder="分组长度" v-model:value="form.blockLength" :min="1" />
          </n-form-item>

          <!-- 输入分支数 -->
          <n-form-item label="分支数:" path="branchNumber" required>
            <n-input-number placeholder="分支数" v-model:value="form.branchNumber" :min="1" />
          </n-form-item>

          <!-- 选择非线性组件 -->
          <n-form-item label="选择非线性组件:" required>
              <n-checkbox-group
                  :min="0"
                  :max="1"
                  v-model:value="selectNonLinearComponentValue"
                  @update:value="selectNonLinearComponent"
                >
                  <n-space>
                    <n-checkbox
                      v-for="item in nonLinearComponents"
                      :value="item.value"
                      :key="item.value"
                      :label="item.label"
                    />
                  </n-space>
                </n-checkbox-group>
            </n-form-item>


          <!-- 轮函数输入 -->
          <n-form-item label="轮函数描述:" required>
            <div style="display: flex; align-items: center; margin-bottom: 10px">
              <n-button type="primary" size="small" @click="submitRoundFunction(false)">
                提交轮函数代码
              </n-button>
            </div>
            <code-editor v-model:value="form.roundFunction" />
          </n-form-item>

          <!-- 密钥生成算法输入 -->
          <n-form-item label="密钥生成算法:" required>
            <div style="display: flex; align-items: center; margin-bottom: 10px">
              <n-button type="primary" size="small" @click="submitKeySchedule(false)">
                提交密钥生成算法
              </n-button>
            </div>
            <code-editor v-model:value="form.keySchedule" />
          </n-form-item>
        </n-form>
      </div>
    </div>

    <!-- 第三步：安全性分析 -->
    <div v-if="current === 3">
      <div class="step-content">
        <div class="step3">
          <h1>请选择算法分析类型</h1>
          <n-radio-group 
            name="analyzeType" 
            v-model:value="form.analyzeType" 
            size="large"
            class="analyze-type-group">
            <n-space justify="center">
              <n-radio-button
                v-for="type in analyzeTypes"
                :value="type.value"
                :key="type.value"
                :label="type.label"
                size="large" />
            </n-space>
          </n-radio-group>
          <div style="text-align: center; margin-top: 20px;">
            <n-button 
              type="primary" 
              size="large" 
              @click="submit"
              :disabled="!form.analyzeType">
              提交分析
            </n-button>
          </div>
        </div>

        <!-- 分析结果 -->
        <div class="analysis-results-section">
          <n-h3>分析结果</n-h3>
          <n-card class="result-card">
            <n-scrollbar style="max-height: 400px">
              <pre class="result-pre">{{ analyzeResult.result }}</pre>
            </n-scrollbar>
            <template #footer v-if="analyzeResult.result">
              <n-button type="primary" strong size="large" @click="showDownloadModal = true">
                下载报告
              </n-button>
            </template>
          </n-card>
        </div>
      </div>
    </div>

    <!-- 第四步：实现分析 -->
    <div v-if="current === 4">
      <div class="step-content">
        <div class="step4">
          <n-form label-placement="left" label-width="auto">

            <!-- 算法分组长度 -->
            <n-form-item label="算法分组长度:" required>
              <n-input-number 
                v-model:value="implForm.blockLength" 
                placeholder="请输入分组长度" 
                :min="1" />
            </n-form-item>

            <!-- 子密钥长度 -->
            <n-form-item label="子密钥长度:" required>
              <n-input-number 
                v-model:value="implForm.subKeyLength" 
                placeholder="请输入子密钥长度" 
                :min="1" />
            </n-form-item>

            <!-- 选择非线性组件-->
            <n-form-item label="选择非线性组件:" required>
              <n-checkbox-group v-model:value="selectednonLinearComponents">
                <n-space>
                  <n-checkbox value="sbox">S盒</n-checkbox>
                  <n-checkbox value="modulo">模加</n-checkbox>
                </n-space>
              </n-checkbox-group>
            </n-form-item>
            
            <!-- S盒 -->
            <n-form-item v-if="selectednonLinearComponents.includes('sbox')" 
              label="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;轮函数S盒个数:" required>
              <n-input-number 
                v-model:value="implForm.roundSboxCount" 
                placeholder="请输入轮函数S盒个数" 
                :min="1" 
              />
            </n-form-item>
            <n-form-item v-if="selectednonLinearComponents.includes('sbox')" label="&nbsp;&nbsp;密钥生成算法S盒个数:" required>
              <n-input-number 
                v-model:value="implForm.keySboxCount" 
                placeholder="请输入密钥生成算法S盒个数" 
                :min="1" 
              />
            </n-form-item>

            <!-- 模加 -->
            <n-form-item v-if="selectednonLinearComponents.includes('modulo')" 
              label="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;轮函数模加个数:" required>
              <n-input-number 
                v-model:value="implForm.roundModuloCount" 
                placeholder="请输入轮函数模加个数" 
                :min="1" 
              />
            </n-form-item>
            <n-form-item v-if="selectednonLinearComponents.includes('modulo')" label="&nbsp;&nbsp;密钥生成算法模加个数:" required>
              <n-input-number 
                v-model:value="implForm.keyModuloCount" 
                placeholder="请输入密钥生成算法模加个数" 
                :min="1" 
              />
            </n-form-item>

            <!-- 异或 -->
            <n-form-item label="轮函数异或个数:" required>
              <n-input-number 
                v-model:value="implForm.roundXorCount" 
                placeholder="请输入轮函数异或个数" 
                :min="1" 
              />
            </n-form-item>
            <n-form-item label="密钥生成算法异或个数:" required>
              <n-input-number 
                v-model:value="implForm.keyXorCount" 
                placeholder="请输入密钥生成算法异或个数" 
                :min="1" 
              />
            </n-form-item>
          </n-form>

          <!-- 提交分析按钮 -->
          <div style="margin-top: 20px;">
            <n-button 
              type="primary" 
              size="large" 
              @click="submitImplAnalysis">
              提交分析
            </n-button>
          </div>
        </div> 

        <!-- 分析结果 -->
        <div class="impl_analysis-results-section" style="margin-top: 20px;">
          <n-h3>分析结果</n-h3>
          <n-card class="result-card">
            <n-scrollbar style="max-height: 300px">
              <pre class="result-pre">总面积为：{{ implResult }}GE</pre>
            </n-scrollbar>
          </n-card>
        </div>
      </div>
    </div>

    <!-- 导航按钮 -->
    <div class="navigation-buttons">
      <n-button 
        type="warning" 
        size="large" 
        @click="prev"
        :disabled="current === 1">
        上一步
      </n-button>
      <n-button 
        type="primary" 
        size="large" 
        @click="next"
        v-if="current !== 4">
        下一步
      </n-button>
      <n-button 
      type="success" 
      size="large" 
      @click="finish"
      v-if="current === 4">
      结束
    </n-button>
    </div>
  </div>

  <!-- 模态框 -->
  <n-modal v-model:show="showDownloadModal">
    <n-card style="width: 600px" title="下载报告">
      <template #footer>
        <n-button @click="downloadFile('http://127.0.0.1:8000/result/result.txt')">下载分析结果</n-button>
        <n-button v-if="showRouteButton" @click="downloadFile('http://127.0.0.1:8000/result/route.txt')">
          下载{{ value2label(form.analyzeType) }}路线
        </n-button>
        <n-button v-if="showRouteButton" @click="downloadFile('http://127.0.0.1:8000/result/archive.zip')">
          下载打包结果
        </n-button>
      </template>
    </n-card>
  </n-modal>

  <n-modal v-model:show="showSpinModal">
    <n-spin size="large">
      <template #description> 正在分析中，请稍后... </template>
    </n-spin>
  </n-modal>

  <n-modal v-model:show="showErrorModal" preset="card" style="width: 400px">
    <n-result status="error" title="错误" :description="errorMessage" />
  </n-modal>
</template>

<script setup lang="ts">
import { analyzeAPI } from "@/apis/analyze"
// import { checkStepOneAPI,checkStepTwoAPI } from "@/apis/check"
// import request from "@/apis/request"
import CodeEditor from "@/components/code-editor/index.vue"
import Steps from "@/components/steps/index.vue"
import {
  NButton,
  NCard,
  NCheckbox,
  NCheckboxGroup,
  NForm,
  NFormItem,
  NInput,
  NInputNumber,
  NModal,
  NRadioButton,
  NRadioGroup,
  NScrollbar,
  NSelect,
  NSpace,
  NSpin,
  useNotification,
  NResult,
  NH3,
  NTabs,
  NTabPane,
} from "naive-ui"
import { ref, reactive } from "vue"
import { 
  bitMatrixConstructionAPI, 
  blockMatrixConstructionAPI, 
  sboxConstructionAPI 
} from "@/apis/construction"
import { saveBlockMatrixAPI, saveBitMatrixAPI, saveSboxAPI, downloadFileAPI } from "@/apis/file"
import {
  submitAlgorithmDesignAPI,
  validateAlgorithmCodeAPI,
  saveRoundFunctionAPI 
} from "@/apis/algorithm"
import { implAnalyzeAPI } from '@/apis/impl_analyze'
import axios from 'axios'
import { watch } from "vue"

const notification = useNotification()
const showDownloadModal = ref(false)
const showSpinModal = ref(false)
const showErrorModal = ref(false)
const errorMessage = ref("")
const current = ref(1)
const showRouteButton = ref(true)
const isSubmitCode = ref(false)


// 假设 current 是 ref
watch(current, (newVal) => {
  console.log("🔍 current 变化:", newVal, typeof newVal)
})

// 保存第一步和第二步结果
const constructionResult = ref<Record<string, any>>({})

// 用来绑定 checkbox-group 的值
const selectNonLinearComponentValue = ref<(string | number)[] | null>(null)

// 组件选择
const selectedComponents = ref<string[]>([])
const linearType = ref("block")

// 分块阵表单
const blockMatrixForm = reactive({ 
  block_size: null, 
  bit_size: null, 
  branch_number: null, 
  dr: null, 
  xor_count: null, 
  quantity: null 
})
// 比特阵表单
const bitMatrixForm = reactive({ 
  block_size: null, 
  branch_number: null, 
  depth: null, 
  xor_count: null, 
  quantity: null 
})
// S盒表单
const sboxForm = reactive({ 
  bit_num: null, 
  diff_uniform: null, 
  linear_uniform: null, 
  dbn: null, 
  lbn: null, 
  bibo_ddt: null, 
  bibo_lat: null, 
  quantity: null 
})

// 构造结果
const blockMatrixResult = ref<any[]>([])
const bitMatrixResult = ref<any[]>([])
const sboxResult = ref<number[][]>([])

// 分析表单
const form = ref<any>({
  blockLength: null,  // 分组长度
  branchNumber: null,  // 分支数
  bitPermutation: null,  // 比特级置换
  sBoxLength: null,  // S盒长度
  sBoxContent: null,  // S盒内容
  linearMatrix: null,  // 线性矩阵
  nonLinearComponent: null,  // 非线性组件
  roundFunction: `# 请在此输入轮函数代码\n\n`,  // 代码
  keySchedule: `# 请在此输入密钥生成算法\n\n`,
  analyzeType: null,  // 分析类型
})

// 选项列表
const blockSizeList2 = [
  { label: "16 比特", value: "16" },
  { label: "32 比特", value: "32" },
  { label: "64 比特", value: "64" },
]

const blockSizeList = [
  { label: "4 比特", value: "4" },
  { label: "6 比特", value: "6" },
  { label: "8 比特", value: "8" },
  { label: "10 比特", value: "10" },
  { label: "12 比特", value: "12" },
  { label: "14 比特", value: "14" },
  { label: "16 比特", value: "16" },
  { label: "32 比特", value: "32" },
]

// 非线性组件可选项
const nonLinearComponents = [
  { label: "S盒", value: "Sbox" },
  { label: "模加", value: "modulo" }
  // 如果以后要扩展，可以继续加
]

// 密码分析类型
const analyzeTypes = [
  { value: "dc", label: "差分分析" },
  { value: "lc", label: "线性分析" },
  { value: "idc", label: "不可能差分分析" },
  { value: "zlc", label: "零相关线性分析" },
  { value: "ic", label: "积分分析" },
]

// 分析结果
const analyzeResult = ref({
  result: "",
  url_result: "",
  url_route: "",
  url_archive: "",
})

// 第四步表单数据
const implForm = ref({
  blockLength: null,      // 算法分组长度
  subKeyLength: null,     // 子密钥长度
  nonLinearType: "sbox",  // 默认选择 S盒，可选 "sbox" 或 "add"

  // S盒个数
  roundSboxCount: null,
  keySboxCount: null,

  // 模加个数
  roundModuloCount: null,
  keyModuloCount: null,

  // 异或个数
  roundXorCount: null,
  keyXorCount: null,
})

// 非线性组件选择
const selectednonLinearComponents = ref<string[]>([])

// 实现分析结果
const implResult = ref("")

// 工具函数
const array2string = (arr: number[][]) => arr.map((item) => item.join(" ")).join("\n")

const formatBlockMatrix = (matrix: number[][], blockSize: number): string => {
  const nrows = matrix.length
  const ncols = matrix[0].length
  let output = ""
  for (let row = 0; row < nrows; row++) {
    if (row % blockSize === 0 && row !== 0) {
      output += "-".repeat(blockSize * 2)
      output += ("+" + "-".repeat(blockSize * 2 + 1)).repeat(Math.floor(ncols / blockSize) - 2)
      output += "+" + "-".repeat(blockSize * 2) + "\n"
    }
    for (let col = 0; col < ncols; col++) {
      if (col % blockSize === 0 && col !== 0) output += "| "
      output += `${matrix[row][col]} `
    }
    output = output.trim() + "\n"
  }
  return output
}

// 构造函数
// 分块阵构造
const handleBlockMatrixConstruction = async () => {
  try {
    notification.info({ content: "请稍等片刻", duration: 1000 })
    const res = await blockMatrixConstructionAPI(blockMatrixForm)
    if (res.code === 0) {
      notification.success({ content: "构造成功", duration: 3000 })

      // 更新表格数据
      blockMatrixResult.value = Object.values(res.data).map(item => ({
        ...item,
        matrix: JSON.stringify(item.matrix)
      }))

      // ✅ 保存到 constructionResult（直接用返回值）
      const firstMatrix = Object.values(res.data)[0]
      constructionResult.value.bitPermutation = "true"
      constructionResult.value.linearMatrix = firstMatrix.matrix
      constructionResult.value.blockLength = Number(blockMatrixForm.block_size)
      constructionResult.value.branchNumber = Number(blockMatrixForm.branch_number)
    } else {
      notification.error({ content: res.message || "构造失败", duration: 3000 })
    }
  } catch (e) {
    console.error("构造请求出错:", e)
    notification.error({ content: "请求失败，请稍后重试", duration: 3000 })
  }
}

// 比特阵构造
const handleBitMatrixConstruction = async () => {
  try {
    notification.info({ content: "请稍等片刻", duration: 1000 })
    const res = await bitMatrixConstructionAPI(bitMatrixForm)
    if (res.code === 0) {
      notification.success({ content: "构造成功", duration: 3000 })

      // 更新表格数据
      bitMatrixResult.value = Object.values(res.data) as any[]

      // ✅ 保存到 constructionResult
      const firstMatrix = Object.values(res.data)[0]
      constructionResult.value.bitPermutation = "true"
      constructionResult.value.linearMatrix = firstMatrix.matrix
      constructionResult.value.blockLength = Number(bitMatrixForm.block_size)
      constructionResult.value.branchNumber = Number(bitMatrixForm.branch_number)
    } else {
      notification.error({ content: res.message || "构造失败", duration: 3000 })
    }
  } catch (e) {
    console.error("构造请求出错:", e)
    notification.error({ content: "请求失败，请稍后重试", duration: 3000 })
  }
}

// S盒构造
const constructSbox = async () => {
  try {
    notification.info({ content: "请稍等片刻", duration: 1000 })
    const res = await sboxConstructionAPI(sboxForm)
    if (res.code === 0) {
      notification.success({ content: "构造成功", duration: 3000 })

      // 更新表格数据
      sboxResult.value = Object.values(res.data) as number[][]

      // ✅ 保存到 constructionResult
      const firstSbox = Object.values(res.data)[0]
      constructionResult.value.sBoxContent = (firstSbox as number[]).join(" ")
      constructionResult.value.sBoxLength = sboxForm.bit_num
    } else {
      notification.error({ content: res.message || "构造失败", duration: 3000 })
    }
  } catch (e) {
    console.error("S盒构造请求出错:", e)
    notification.error({ content: "请求失败，请稍后重试", duration: 3000 })
  }
}

// 选择非线性组件
const selectNonLinearComponent = (value: (string | number)[] | null) => {
  if (value && value.includes("Sbox")) {
    constructionResult.value.nonLinearComponent = "Sbox"  // ✅ 直接传字符串
    constructionResult.value.sBoxLength = constructionResult.value.sBoxLength
    constructionResult.value.sBoxContent = constructionResult.value.sBoxContent
  } else if (value && value.includes("modulo")) {
    constructionResult.value.nonLinearComponent = "modulo"
  }
}

// 提交轮函数
const submitRoundFunction = async (silent = false) => {
  try {
    // 第一步：验证代码
    const res = await validateAlgorithmCodeAPI({
      code: form.value.roundFunction,
      type: 'round_function'
    });

    if (res.code !== 0) {
      notification.error({ content: res.message || "代码验证失败", duration: 3000 });
      return false;
    }

    if (!silent) {
      notification.success({ content: "代码验证成功", duration: 3000 });
    }

    // 本地缓存（UI 用）
    constructionResult.value.roundFunction = form.value.roundFunction;

    // 第二步：保存到后端（使用我们在 algorithm.ts 中新增的封装）
    const saveRes = await saveRoundFunctionAPI({
      code: form.value.roundFunction
    });

    if (saveRes.code === 0) {
      if (!silent) {
        notification.success({ content: "轮函数保存成功", duration: 3000 });
      }
      return true;
    } else {
      notification.error({ content: saveRes.message || "轮函数保存失败", duration: 3000 });
      return false;
    }

  } catch (err) {
    notification.error({ content: "请求失败，请稍后重试", duration: 3000 });
    return false;
  }
};

// 提交密钥生成算法
const submitKeySchedule = async (silent = false) => {
  try {
    const res = await validateAlgorithmCodeAPI({
      code: form.value.keySchedule,
      type: 'key_schedule'
    })
    if (res.code === 0) {
      if (!silent) {
        notification.success({ content: "代码验证成功", duration: 3000 })
      }
      return true
    } else {
      notification.error({ content: res.data.message || "代码验证失败", duration: 3000 })
      return false
    }
  } catch {
    notification.error({ content: "请求失败，请稍后重试", duration: 3000 })
    return false
  }
}

// 安全性分析提交
const submit = () => {
  console.log("✅ submit() 被调用了")
  console.log("📌 analyzeAPI:", analyzeAPI)

  showSpinModal.value = true

  // ✅ 直接传 true/false
  const bitPermutation = constructionResult.value.bitPermutation === "true" ? "true" : "false"

  const payload = {
    blockLength: form.value.blockLength,
    branchNumber: form.value.branchNumber,
    bitPermutation,   // ✅ 改成字符串 true/false
    linearMatrix: constructionResult.value.linearMatrix || null,  // ✅ 新增，后端需要
    sBoxLength: constructionResult.value.sBoxLength || null,
    sBoxContent: constructionResult.value.sBoxContent
    ? constructionResult.value.sBoxContent.trim().split(/\s+/).map(Number)
    : null,   // ✅ 确保传的是数组
    nonLinearComponent: constructionResult.value.nonLinearComponent || null,
    code: constructionResult.value.roundFunction || "",
    analyzeType: form.value.analyzeType,
    // round: 不传，后端写死
  }

  console.log("分析 payload:", payload)

  analyzeAPI(payload)
    .then((res) => {
      showSpinModal.value = false
      if (res.code === 0) {
        notification.success({ content: "分析成功", duration: 3000 })
        // current.value++
        // ✅ 正确更新字段，而不是覆盖整个对象
        analyzeResult.value.result = res.data.result
        analyzeResult.value.url_result = res.data.url_result
        analyzeResult.value.url_route = res.data.url_route
        analyzeResult.value.url_archive = res.data.url_archive
      } else {
        notification.error({ content: "分析失败", duration: 3000 })
      }
    })
    .catch(() => {
      showSpinModal.value = false
      notification.error({ content: "分析失败", duration: 3000 })
    })
}

// 实现分析
const submitImplAnalysis = async () => {
  try {
    const res = await implAnalyzeAPI(implForm.value)
    console.log("✅ implAnalyzeAPI 返回结果:", res)

    if (res.code === 0) {
      implResult.value = res.data.implResult
      notification.success({ content: "分析成功", duration: 3000 })
    } else {
      notification.error({ content: "分析失败", duration: 3000 })
    }
  } catch (err) {
    notification.error({ content: "请求失败", duration: 3000 })
    console.error(err)
  }
}

const downloadFile = async (url: string) => {
  try {
    const res = await axios.get(url, { responseType: "blob" })
    const blob = new Blob([res.data])
    const downloadUrl = URL.createObjectURL(blob)

    const a = document.createElement("a")
    a.href = downloadUrl
    a.download = url.split("/").pop() || "download"
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)

    setTimeout(() => URL.revokeObjectURL(downloadUrl), 1000)
  } catch {
    notification.error({ content: "文件下载失败", duration: 3000 })
  }
}

// 保存后端返回的文件名
const savedFiles = reactive({
  blockMatrix: [] as string[],
  bitMatrix: [] as string[],
  sbox: [] as string[],
})

// 保存函数
const saveBlockMatrix = async (index: number) => {
  try {
    const matrixData = blockMatrixResult.value[index]
    const saveData = {
      dimension: blockMatrixForm.block_size,
      branch_number: blockMatrixForm.branch_number,
      depth: null,
      xor_count: matrixData.cost,
      matrix: JSON.stringify(JSON.parse(matrixData.matrix)),
      add_time: new Date().toLocaleString(),
    }
    const res = await saveBlockMatrixAPI(saveData)
    if (res.code === 0) {
      savedFiles.blockMatrix.push(res.filename)
      notification.success({ content: "分块阵保存成功", duration: 3000 })
    }
  } catch {
    notification.error({ content: "保存失败，请稍后重试", duration: 3000 })
  }
}

const saveBitMatrix = async (index: number) => {
  try {
    const matrixData = bitMatrixResult.value[index]
    const saveData = {
      dimension: bitMatrixForm.block_size,
      branch_number: bitMatrixForm.branch_number,
      depth: bitMatrixForm.depth,
      xor_count: bitMatrixForm.xor_count,
      matrix: JSON.stringify(matrixData),
      add_time: new Date().toLocaleString(),
    }
    const res = await saveBitMatrixAPI(saveData)
    if (res.code === 0) {
      savedFiles.bitMatrix.push(res.filename)
      notification.success({ content: "比特阵保存成功", duration: 3000 })
    }
  } catch {
    notification.error({ content: "保存失败，请稍后重试", duration: 3000 })
  }
}

const saveSbox = async (index: number) => {
  try {
    const sboxData = sboxResult.value[index]
    const saveData = { sbox: sboxData, add_time: new Date().toLocaleString() }
    const res = await saveSboxAPI(saveData)
    if (res.code === 0) {
      savedFiles.sbox.push(res.filename)
      notification.success({ content: "S盒保存成功", duration: 3000 })
    }
  } catch {
    notification.error({ content: "保存失败，请稍后重试", duration: 3000 })
  }
}

// 通用下载函数（从后端下载）
const download = async (filename: string) => {
  try {
    const res = await downloadFileAPI(filename)
    const blob = new Blob([res], { type: "text/plain;charset=utf-8" })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = filename
    a.click()
    window.URL.revokeObjectURL(url)
  } catch {
    notification.error({ content: "下载失败，请稍后重试", duration: 3000 })
  }
}

// 重置函数
const resetBlockMatrixForm = () => {
  Object.assign(blockMatrixForm, {
    block_size: null, bit_size: null, branch_number: null, dr: null, xor_count: null, quantity: null,
  })
  blockMatrixResult.value = []
}

const resetBitMatrixForm = () => {
  Object.assign(bitMatrixForm, {
    block_size: null, branch_number: null, depth: null, xor_count: null, quantity: null,
  })
  bitMatrixResult.value = []
}

const resetSboxForm = () => {
  Object.assign(sboxForm, {
    bit_num: null, diff_uniform: null, linear_uniform: null, dbn: null, lbn: null, bibo_ddt: null, bibo_lat: null, quantity: null,
  })
  sboxResult.value = []
}

// 将分析类型的值转换为label
const value2label = (value: string | null) => {
  return analyzeTypes.find((item) => item.value === value)?.label
}

// 导航函数
const next = async () => {
  if (current.value === 1) {
    if (selectedComponents.value.length === 0) {
      notification.warning({ content: "请至少选择一个设计类型", duration: 3000 })
      return
    }
    if (selectedComponents.value.includes('linear')) {
      if (linearType.value === 'block' && blockMatrixResult.value.length === 0) {
        notification.warning({ content: "请先完成分块阵构造", duration: 3000 })
        return
      }
      if (linearType.value === 'bit' && bitMatrixResult.value.length === 0) {
        notification.warning({ content: "请先完成比特阵构造", duration: 3000 })
        return
      }
    }
    if (selectedComponents.value.includes('sbox') && sboxResult.value.length === 0) {
      notification.warning({ content: "请先完成S盒构造", duration: 3000 })
      return
    }
    current.value++
  } else if (current.value === 2) {
    if (!form.value.roundFunction.trim()) {
      notification.warning({ content: "请输入轮函数描述", duration: 3000 })
      return
    }
    if (!form.value.keySchedule.trim()) {
      notification.warning({ content: "请输入密钥生成算法", duration: 3000 })
      return
    }
    const roundFunctionValid = await submitRoundFunction(true)
    const keyScheduleValid = await submitKeySchedule(true)
    if (!roundFunctionValid || !keyScheduleValid) return
    try {
      const res = await submitAlgorithmDesignAPI({
        round_function: form.value.roundFunction,
        algorithm_structure: form.value.algorithmStructure,
        key_schedule: form.value.keySchedule
      })
      if (res.code === 0) {
        notification.success({ content: "算法设计提交成功", duration: 3000 })
        current.value++
      } else {
        notification.error({ content: res.data.message || "提交失败", duration: 3000 })
      }
    } catch {
      notification.error({ content: "提交失败，请稍后重试", duration: 3000 })
    }
  } else if (current.value === 3) {
    if (!form.value.analyzeType) {
      notification.warning({ content: "请选择分析类型", duration: 3000 })
      return
    } else {
      if (form.value.analyzeType === "idc" || form.value.analyzeType === "zlc") {
        showRouteButton.value = false
      } else {
        showRouteButton.value = true
      }
      current.value++
    }
  }
}

const prev = () => {
  if (current.value === 4) isSubmitCode.value = false
  current.value--
}

const finish = () => {
  current.value = 1
}
</script>


<style scoped lang="less">
.container {
  width: 100%;
  min-height: calc(100vh - 60px);
  display: flex;
  flex-direction: column;
  position: relative;
}

.step-content {
  flex: 1;
  padding: 20px 50px;
  overflow-y: auto;
  margin-bottom: 60px;
}

.component-section {
  margin-top: 20px;
}

.construction-result {
  margin-top: 20px;

  /* 只在第一步构造结果中去掉 hover 效果 */
  .table-body tr:hover {
    background-color: inherit !important;
  }

  /* 表格内容居中 */
  .result-table th,
  .result-table td {
    text-align: center;
    vertical-align: middle;
  }
}

.result-table {
  width: 100%;
  margin-top: 10px;
  
  .column-number {
    width: 10%;
  }
  
  .column-cost {
    width: 15%;
  }
  
  .column-dr {
    width: 15%;
  }
  
  .column-matrix {
    width: 40%;
  }
  
  .column-actions {
    width: 20%;
  }
  
  .column-sbox {
    width: 40%;
  }
  
  .column-gates {
    width: 15%;
  }
  
  .column-area {
    width: 15%;
  }
}

.table-body {
  tr:hover {
    background-color: #f5f5f5;
  }
}

.action-button {
  min-width: 60px;
}

.navigation-buttons {
  position: fixed;
  bottom: 0;
  left: 250px;
  right: 0;
  height: 30px;
  background-color: #fff;
  padding: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1000;

  .n-button {
    min-width: 120px;
    height: 50px;
  }
}

.step3 {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  margin-bottom: 30px;
}

.analyze-type-group {
  margin-top: 20px;
}

.analysis-results-section {
  margin-top: 30px;
}

.result-card {
  margin-top: 20px;
}

.result-pre {
  white-space: pre-wrap;
  word-break: break-word;
  font-family: monospace;
  line-height: 1.5;
}
</style>