<template>
  <div class="steps" style="--active-color: #63e2b7">
    <ul class="list">
      <li class="item" v-for="(item, index) in props.titleList" :key="index">
        <div class="step">
          <span class="process" :class="{ ' active': index + 1 <= props.current }">0{{ index + 1 }}</span>
          <div class="title" :class="{ 'active-title': index + 1 <= props.current }">
            <span>{{ item }}</span>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  current: number;
  titleList: Array<string>;
}>();
</script>

<style lang="less">
.steps {
  box-sizing: border-box;
  padding: 20px 40px;
  width: 100%;

  .list {
    list-style: none;
    display: flex;
    align-items: center;
    justify-content: center;

    .item {
      /* 利用伪类来控制样式去掉首尾的横线 */
      &:first-child {
        .process {
          &::after {
            display: none;
          }
        }
      }

      &:last-child {
        .process {
          &::before {
            display: none;
          }
        }
      }
    }
  }
}

.step {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  font-weight: 400;
  text-align: center;

  .process {
    width: 64px;
    height: 64px;
    background: #707072;
    border-radius: 50%;
    font-size: 32px;
    font-family: Impact;
    font-weight: 400;
    color: #fff;
    line-height: 64px;
    margin: 0 90px;
    position: relative;

    &:before,
    &:after {
      content: "";
      width: 95px;
      height: 1px;
      border-bottom: 4px solid #707072;
      display: inline-block;
      position: absolute;
      top: 30px;
    }

    &:before {
      left: 60px;
    }

    &:after {
      right: 60px;
    }
  }

  .title {
    max-width: 165px;
    height: 16px;
    font-size: 16px;
    font-family: Source Han Sans CN;
    font-weight: 400;
    color: #818181;
    margin-top: 25px;
  }

  .active-title {
    color: var(--active-color);
  }

  .active {
    background: var(--active-color);

    &:before,
    &:after {
      border-bottom: 4px solid var(--active-color) !important;
    }
  }
}
</style>
