<template>
  <div>
    <canvas ref="sankeyDiagram"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, defineProps } from "vue";

import { Chart, registerables } from "chart.js";
import { SankeyController, Flow } from "chartjs-chart-sankey";
import { careerPathsToSankey } from "@/plugins/occupation";

Chart.register(SankeyController, Flow, ...registerables);

const props = defineProps({
  currentItem: {
    type: Object,
    default: () => {
      return null;
    },
  },
});

const sankeyDiagram = ref(null);

const buildData = (data) => {
  return careerPathsToSankey(data);
};

onMounted(() => {
  const configs = buildData(props.currentItem?.careerPaths);

  new Chart(sankeyDiagram.value, {
    type: "sankey",
    ...configs,
  });
});
</script>
