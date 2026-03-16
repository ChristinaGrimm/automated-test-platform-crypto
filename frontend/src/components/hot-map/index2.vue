<template>
  <div ref="chartRef" class="heatmap-container"></div>
</template>

<script lang="ts" setup>
import { ref, watch, onMounted, onBeforeUnmount } from "vue"
import * as echarts from "echarts"

// 定义 Props
const props = defineProps<{ matrixData: number[][] }>()
const { matrixData } = props

// 定义 X 和 Y 轴标签
const x = Array.from({ length: 16 }, (_, i) => i)
const y = x

// 初始化图表引用
const chartRef = ref<HTMLDivElement | null>(null)
let chartInstance: echarts.ECharts | null = null

// 格式化数据函数
const formatData = (data: number[][]) => {
  const data0 = data.reduce((acc, row, rowIndex) => {
    return acc.concat(
      row.map((cell, cellIndex) => {
        return [cellIndex, rowIndex, cell]
      }),
    )
  }, [] as number[][])
  return data0.map((item) => [item[1], item[0], item[2] || "-"])
}

// 图表选项
const createOption = (data: number[][]) => ({
  tooltip: {
    position: "top",
  },
  grid: {
    height: "80%",
    top: "5%",
  },
  xAxis: {
    type: "category",
    data: x,
    splitArea: {
      show: true,
    },
  },
  yAxis: {
    type: "category",
    data: y,
    splitArea: {
      show: true,
    },
  },
  visualMap: {
    min: Math.min(...data.flat()),
    max: Math.max(...data.flat()),
    calculable: true,
    orient: "vertical",
    left: "right",
    top: "center",
    inRange: {
      color: ["#fde5dc", "#fbb4ae", "#de2d26"], // 渐变色方案
    },
  },
  series: [
    {
      name: "Heatmap",
      type: "heatmap",
      data: formatData(data),
      label: {
        show: false, // 不显示每个格子的值
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowColor: "rgba(0, 0, 0, 0.5)",
        },
      },
    },
  ],
})

// 初始化图表
const initChart = () => {
  if (chartRef.value) {
    chartInstance = echarts.init(chartRef.value)
    updateChart()
  }
}

// 更新图表数据
const updateChart = () => {
  if (chartInstance) {
    const option = createOption(matrixData)
    chartInstance.setOption(option)
  }
}

// 监听 `matrixData` 数据变化，动态更新图表
watch(
  () => matrixData,
  () => {
    updateChart()
  },
  { deep: true },
)

// 生命周期管理
onMounted(() => {
  initChart()
})

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
})
</script>

<style scoped>
.heatmap-container {
  width: 100%;
  height: 500px;
}
</style>
