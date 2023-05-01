<template>
  <div class="resultDetail__container">
    <div class="resultDetail__head">
      <div class="resultDetail__head-title">{{ occupation.title }}</div>
      <div class="resultDetail__head-btns">
        <Button
          type="text"
          html-type="button"
          class="close-btn"
          @click="() => $emit('close')"
          ><CloseOutlined
        /></Button>
      </div>
    </div>
    <div class="resultDetail__body">
      <div class="resultDetail__item-content">
        <div class="resultDetail__item-code">O*Net SOC {{ occupation.id }}</div>
        <div class="resultDetail__item-description">
          {{ occupation.description }}
        </div>

        <div class="resultDetail__item-infos">
          <Collapse :bordered="false">
            <CollapsePanel key="task" :header="'Work Tasks'">
              <ul>
                <li v-for="task in splitTasks" :key="task">
                  {{ task }}
                </li>
              </ul>
            </CollapsePanel>
          </Collapse>
        </div>

        <h3>Career Paths</h3>
        <div class="resultDetail__item-infos-diagram">
          <ArcDiagram :data="careerPathsGraphData" :currentItem="occupation" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, defineProps } from "vue";
import { CloseOutlined } from "@ant-design/icons-vue";
import ArcDiagram from "@/components/library/ArcDiagram/ArcDiagram.vue";

import { careerPathsToGraph } from "@/plugins/occupation";

const props = defineProps({
  occupation: {
    type: Object,
    default: () => {
      return null;
    },
  },
});

// const emit = defineEmits(["close"]);

const splitText = (text) => {
  if (text) {
    return text.split("\t");
  }
  return [];
};

const splitTasks = computed(() => {
  return splitText(props.occupation.task);
});

const careerPathsGraphData = computed(() => {
  return careerPathsToGraph(props.occupation.careerPaths);
});
</script>

<style scoped>
.resultDetail__container {
  display: block;
  width: 100%;
  height: 100%;
  background: white;
}

.resultDetail__head {
  position: relative;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;
  height: 3rem;
  padding: 0.5rem 0.5rem;
  font-weight: bold;
}

.resultDetail__head-btns {
  padding: 0.25rem 0.25rem;
  position: absolute;
  top: 0;
  right: 0;
  display: flex;
  flex-direction: row;
}

.resultDetail__head-title {
  width: 100%;
  padding: 0.25rem;
}

.resultDetail__body {
  width: 100%;
  height: calc(100% - 3rem);
}

.h3 {
  font-weight: bold;
}

.resultDetail__body-content {
  width: 100%;
  height: 100%;
}

.resultDetail__item-content {
  width: 100%;
  height: 100%;
  padding: 2rem 2rem;
  overflow-y: auto;
}

.resultDetail__item-title {
  width: 100%;
  display: flex;
  font-weight: bold;
}
.resultDetail__item-code {
  width: 100%;
  font-size: 70%;
  font-weight: light;
}

.resultDetail__item-description {
  width: 100%;
}

.resultDetail__item-infos {
  text-align: left;
  width: 100%;
  padding: 2rem 0;
}

.resultDetail__item-infos-diagram {
  width: 100%;
  overflow: auto;
}
</style>
