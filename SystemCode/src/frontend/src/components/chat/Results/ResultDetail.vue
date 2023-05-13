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

        <div class="resultDetail__item-section">
          <Collapse>
            <CollapsePanel key="task" :header="'Work Tasks'">
              <ul class="resultDetail__item-ul">
                <li v-for="task in splitTasks" :key="task">
                  {{ task }}
                </li>
              </ul>
            </CollapsePanel>
          </Collapse>
        </div>

        <div
          class="resultDetail__item-section"
          v-if="occupation && occupation.ssocJobs && occupation.ssocJobs.length"
        >
          <Collapse>
            <CollapsePanel key="salary" :header="'Job Titles & Salary'">
              <Table :dataSource="ssocJobs" :columns="ssocJobsColumns"></Table>
            </CollapsePanel>
          </Collapse>
        </div>

        <div
          class="resultDetail__item-section"
          v-if="
            occupation &&
            occupation.careerPaths &&
            occupation.careerPaths.length
          "
        >
          <Collapse :defaultActiveKey="['path']">
            <CollapsePanel key="path" :header="'Career Paths'">
              <SankeyDiagram :currentItem="occupation" />
            </CollapsePanel>
          </Collapse>
        </div>

        <div
          class="resultDetail__item-section"
          v-if="
            occupation &&
            occupation.careerPaths &&
            occupation.careerPaths.length
          "
        >
          <Collapse :defaultActiveKey="['program']">
            <CollapsePanel key="program" :header="'Education Programs'">
              <List
                size="small"
                :data-source="programs"
                item-layout="horizontal"
              >
                <template #renderItem="{ item }">
                  <ListItem>
                    <ListItemMeta
                      :style="{
                        textAlign: 'left',
                        margin: '0 2rem 0 0',
                      }"
                    >
                      <template #title>
                        <a href="#">{{ item.degree }}</a>
                      </template>
                      <template #description>
                        <ResultEducationDescription :item="item" />
                      </template>
                    </ListItemMeta>

                    <div style="min-width: 10%; max-width: 40%">
                      <LineChart :data="item.programTrends" />
                    </div>
                  </ListItem>
                </template>
              </List>
            </CollapsePanel>
          </Collapse>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, defineProps } from "vue";
import { CloseOutlined } from "@ant-design/icons-vue";
import {
  Collapse,
  CollapsePanel,
  Button,
  Table,
  List,
  ListItem,
  ListItemMeta,
} from "ant-design-vue";
import LineChart from "@/components/library/LineChart/LineChart.vue";
import SankeyDiagram from "@/components/library/SankeyDiagram/SankeyDiagram.vue";
import ResultEducationDescription from "@/components/chat/Results/ResultEducationDescription.vue";

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

const displaySalary = (salary) => {
  return salary ? `$${salary.toLocaleString()}` : "-";
};

const ssocJobs = computed(() => {
  return props.occupation.ssocJobs
    .map((d) => ({
      ...d,
      minSalaryDisplay: displaySalary(d.minSalary),
      maxSalaryDisplay: displaySalary(d.minSalary),
      key: d.id,
    }))
    .sort((a, b) => b.minSalary - a.minSalary);
});

const ssocJobsColumns = [
  {
    title: "Title",
    dataIndex: "ssocJobTitle",
    key: "ssocJobTitle",
  },
  {
    title: "ISCO Code",
    dataIndex: "iscoCode",
    key: "iscoCode",
  },
  {
    title: "Min. Salary",
    dataIndex: "minSalaryDisplay",
    key: "minSalaryDisplay",
  },
  {
    title: "Max. Salary",
    dataIndex: "maxSalaryDisplay",
    key: "maxSalaryDisplay",
  },
];

const getLatestTrend = (programTrends) => {
  return programTrends?.length
    ? programTrends[programTrends?.length - 1]
    : null;
};

const programs = computed(() => {
  return props.occupation.programs
    .map((d) => ({
      ...d,
      programTrends: d.programTrends
        ? d.programTrends.sort((a, b) => a.year - b.year)
        : null,
      key: d.id,
    }))
    .sort((a, b) => {
      const aParams = getLatestTrend(a.programTrends);
      const bParams = getLatestTrend(b.programTrends);
      return bParams?.grossMonthlyMedian - aParams?.grossMonthlyMedian;
    });
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
  padding: 2rem 0;
}

.resultDetail__item-infos {
  text-align: left;
  width: 100%;
  padding: 2rem 0;
}

.resultDetail__item-ul {
  text-align: left;
}

.resultDetail__item-infos-section {
  width: 100%;
  text-align: left;
  padding: 2rem 0;
}

.resultDetail__item-infos-diagram {
  width: 100%;
  overflow: auto;
}
</style>
