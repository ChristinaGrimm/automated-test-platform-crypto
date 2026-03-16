<template>
  <div class="overflow-x-auto overflow-y-auto max-h-96">
    <table class="border-collapse border border-gray-400 table-fixed">
      <tbody>
        <tr v-for="(row, rowIndex) in matrixData" :key="rowIndex">
          <td
            v-for="(cell, cellIndex) in row"
            :key="cellIndex"
            class="border border-gray-400 w-6 h-6 text-center">
            {{ cell }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
defineProps<{ matrixData: number[][] }>()
</script>
