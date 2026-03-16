<template>
  <div class="login-page">
    <div class="bgspace"></div>
    <div class="bgstars1"></div>
    <div class="bgstars2"></div>
    <div class="picture">
      <img src="@/assets/screen1.webp" alt="" />
    </div>
    <n-card class="login-card" :bordered="false">
      <h1 class="login-title">对称密码算法全过程自动化辅助设计平台</h1>
      <n-form label-placement="left" label-width="70">
        <n-form-item label="用户名" required label-style="color:#fff;">
          <n-input placeholder="请输入用户名" v-model:value="loginForm.username" />
        </n-form-item>
        <n-form-item label="密码" required label-style="color:#fff;">
          <n-input placeholder="请输入密码" type="password" v-model:value="loginForm.password">
            <template #suffix>
              <n-button type="primary" text @click="">忘记密码</n-button>
            </template>
          </n-input>
        </n-form-item>
        <n-button type="primary" block secondary strong @click="loginClick">点击登录</n-button>
        <br />
        <n-button type="warning" block secondary strong @click="loginClick">注册用户</n-button>
      </n-form>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { NCard, NForm, NFormItem, NInput, NButton, useMessage } from "naive-ui"
import { useRouter } from "vue-router"
import { adminLoginAPI, getAdminInfoAPI } from "@/apis/admin"
import { ref } from "vue"
import { storageData } from "@/utils/stored-data"
const message = useMessage()
const router = useRouter()

const loginForm = ref({
  username: "",
  password: "",
})

const loginClick = () => {
  adminLoginAPI(loginForm.value).then((res) => {
    if (res.code === 0) {
      storageData.set("access_token", res.data.token, 60 * 24 * 7)
      getAdminInfoAPI().then((res) => {
        if (res.code === 0) {
          message.success("登录成功")
          storageData.set("admin_info", res.data.admin_info, 7 * 24 * 60)
          router.push({ name: "Welcome" })
        }
      })
    }
  })
}
</script>

<style lang="less" scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  // background-image: url("@/assets/2.jpg");
  /* 替换成你的背景图片路径 */
  background-size: cover;
  background-position: center;
  background:
    linear-gradient(43.53deg, #00095e 21%, #000427 53%, #0c0c1f 100%) no-repeat center left,
    #0c0c1f;
  .bgspace {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: 1;
    /* background:red; */
    background: linear-gradient(136.49deg, #00095e 21%, #000427 53%, #0c0c1f 100%) no-repeat center
      left;
    animation: bgfadeIn 5s ease infinite;
  }

  .bgstars1 {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: 1;
    background: url("@/assets/zz.svg") repeat;
    background-size: 500px 500px;
    animation:
      bgMoveStars 20s ease-in infinite,
      bgfadStars1 20s linear infinite,
      bgMoveStarsPosition 20s linear infinite;
  }

  .bgstars2 {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: 1;
    background: url("@/assets/zz.svg") repeat;
    background-size: 500px 500px;
    opacity: 0;
    animation:
      bgMoveStars 20s ease-in 10s infinite,
      bgfadStars2 20s linear infinite,
      bgMoveStarsPosition 20s linear 10s infinite;
    /* animation: bgMoveStars 20s linear 9s infinite, bgfadStars2 20s linear 2s infinite, bgMoveStarsPosition 60s linear infinite;; */
  }

  @keyframes bgfadeIn {
    0% {
      opacity: 0;
    }

    50% {
      opacity: 1;
    }

    100% {
      opacity: 0;
    }
  }

  @keyframes bgfadStars1 {
    0% {
      opacity: 0;
    }

    10% {
      opacity: 1;
    }

    60% {
      opacity: 0;
    }

    100% {
      opacity: 0;
    }
  }

  @keyframes bgfadStars2 {
    0% {
      opacity: 0;
    }

    40% {
      opacity: 0;
    }

    80% {
      opacity: 1;
    }

    100% {
      opacity: 0;
    }
  }

  @keyframes bgMoveStars {
    50% {
      background-size: 600px 600px;
    }
  }

  @keyframes bgMoveStarsPosition {
    50% {
      background-position: -150px -300px;
    }
  }
  .login-card {
    // 设置在最上层
    z-index: 2;
    max-width: 460px;
    padding: 10px;
    background-color: rgba(255, 255, 255, 0);
    margin-left: 60%;
    /* 设置背景模糊*/
    // backdrop-filter: blur(20px);
    // /* 设置内阴影*/
    // box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.2);
    // border-radius: 10px;
  }

  .login-title {
    font-size: 21px;
    margin-bottom: 20px;
    text-align: center;
    color: #fff;
  }

  // 设置label颜色

  .n-form-item-label {
    color: #fff;
  }

  .picture {
    position: fixed;
    top: 10;
    left: 60px;
    z-index: 1;
    width: 56%;
    // height: 50%;
    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }
}
</style>
