<template>
  <code-mirror v-model:value="props.code" :options="cmOptions" style="height: 200px; width: 99%; font-size: 16px" />
</template>

<script lang="ts" setup>
import CodeMirror from "codemirror-editor-vue3";
// import { CodeMirror } from "node_modules/codemirror-editor-vue3/dist/packages";
// placeholder
import "codemirror/addon/display/placeholder.js";

// language
import "codemirror/mode/python/python.js";
// placeholder
import "codemirror/addon/display/placeholder.js";
// theme
import "codemirror/theme/seti.css";

// 定义props.code, 用于接收父组件传递的代码, 并且在子组件中修改props.code的值, 也会影响到父组件中的值
const props = defineProps({
  code: String,
});

const cmOptions = {
  mode: "python", // Language mode
  theme: "seti", // Theme
  lineNumbers: true, // 是否显示行号
  placeholder: "请输入代码", // 占位符
  indentUnit: 4, // 缩进单位
};
</script>
