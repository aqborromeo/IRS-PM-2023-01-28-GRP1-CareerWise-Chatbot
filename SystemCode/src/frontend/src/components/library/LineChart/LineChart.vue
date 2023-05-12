<template>
  <canvas ref="container"></canvas>
</template>

<script setup>
import { ref, defineProps, onMounted } from "vue";
import { Chart } from "chart.js";

const props = defineProps({
  data: {
    type: Array,
    default: () => {
      return null;
    },
  },
});

const container = ref(null);

onMounted(() => {
  debugger;
  if (props.data && props.data.length) {
    const values = props.data
      .map((item) => {
        return item.grossMonthlyMedian;
      })
      .filter((item) => item);
    const datasets = [
      {
        label: "Median monthly salary",
        data: values,
      },
    ];

    if (values && values.length) {
      new Chart(container.value, {
        type: "line",
        data: {
          labels: props.data.map((row) => row.year),
          datasets,
        },
        // options: {
        //   scales: {
        //     x: [
        //       {
        //         gridLines: {
        //           color: "rgba(0, 0, 0, 0)",
        //         },
        //       },
        //     ],
        //     y: [
        //       {
        //         gridLines: {
        //           color: "rgba(0, 0, 0, 0)",
        //         },
        //       },
        //     ],
        //   },
        // },
      });
    }
  }
});
</script>
