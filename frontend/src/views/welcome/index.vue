<template>
  <div class="welcome">
    <div class="main">

    
    <n-h1 > 欢迎来到对称密码算法全过程自动化辅助设计平台👏</n-h1>
    <n-h1>点击左侧<n-text type="primary" style="cursor: pointer" @click="router.push('/main')">
        开始 </n-text
      >进入主页面</n-h1
    >
  </div>
  </div>
</template>

<script lang="ts" setup>
import { NH1, NText } from "naive-ui"
import { useRouter } from "vue-router"
import { ref } from "vue"

const router = ref(useRouter())
</script>

<style scoped lang="less">
// 居中
.welcome {
  height: calc(100vh - 60px);
  .main {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
}
</style>
