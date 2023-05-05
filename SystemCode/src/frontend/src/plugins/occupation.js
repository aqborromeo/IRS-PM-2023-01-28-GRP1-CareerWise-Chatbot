// import get from "lodash.get";

export const careerPathsToGraph = (careerPaths) => {
  if (Array.isArray(careerPaths)) {
    const nodes = {};
    const links = Array(careerPaths.length);
    const entities = ["source", "target"];

    for (let i = 0; i < careerPaths.length; i++) {
      const path = careerPaths[i];
      links[i] = {
        source: path.source.id,
        target: path.target.id,
        value: path.difference,
      };

      // Add source and/or target to list of nodes
      for (let j = 0; j < entities.length; j++) {
        const entityType = entities[j];
        const node = path[entityType];
        if (node) {
          const id = node.id;
          if (!nodes[id]) {
            nodes[id] = {
              name: node.title,
              n: parseInt(node.experienceMedian),
              grp: node.jobZone,
              id: node.id,
            };
          }
        }
      }
    }

    return {
      nodes: Object.values(nodes),
      links,
    };
  }
  return {
    nodes: [],
    links: [],
  };
};

// Settings for flow diagram

export const experiences = {
  1: { min: 0, max: 0 },
  2: { min: 1 / 12, max: 1 / 12 },
  3: { min: 1 / 12, max: 3 / 12 },
  4: { min: 3 / 12, max: 6 / 12 },
  5: { min: 6 / 12, max: 1 },
  6: { min: 1, max: 2 },
  7: { min: 2, max: 4 },
  8: { min: 4, max: 6 },
  9: { min: 6, max: 8 },
  10: { min: 8, max: 10 },
  11: { min: 10, max: 10 },
};

const displayMonthYear = (number) => {
  if (number < 1) {
    const month = number * 12;
    return { number: month, unit: "mth" };
  }
  return { number: number, unit: "yr" };
};

const displayExperienceDuration = (params) => {
  const { min, max } = params;
  const minParams = displayMonthYear(min);
  const maxParams = displayMonthYear(max);
  return min === max
    ? `${minParams.number}${minParams.unit}`
    : `${`${minParams.number}${
        minParams.unit === maxParams.unit ? "" : minParams.unit
      }`} - ${`${maxParams.number} ${maxParams.unit}`} experience`;
};

const colors = [
  "#fafa6e",
  "#f4ce6a",
  "#eda466",
  "#e57c63",
  "#dc616b",
  "#d36088",
  "#c95fa1",
  "#be60b3",
  "#a561b2",
  "#8962a6",
  "#756598",
  "#6b6a89",
];

const getColor = (i) => {
  return i >= 1 && i <= 12 ? colors[i + 1] : colors[0];
};

export const careerPathsToSankey = (sourceData) => {
  if (Array.isArray(sourceData)) {
    const labels = {};
    const data = Array(sourceData.length);
    const entities = ["source", "target"];

    for (let i = 0; i < sourceData.length; i++) {
      const path = sourceData[i];
      data[i] = {
        from: path.source.id,
        to: path.target.id,
        flow: path.difference,
      };

      // Add source and/or target to list of nodes
      for (let j = 0; j < entities.length; j++) {
        const entityType = entities[j];
        const node = path[entityType];
        if (node) {
          const id = node.id;
          if (!labels[id]) {
            labels[id] = node.title;
          }
        }
      }
    }

    return {
      data: {
        datasets: [
          {
            label: "Career Path",
            data,
            colorFrom: (c) => {
              return getColor(sourceData[c.dataIndex].source.experienceMedian);
            },
            colorTo: (c) => {
              return getColor(sourceData[c.dataIndex].target.experienceMedian);
            },
            colorMode: "gradient",
            labels,
            size: "max",
          },
        ],
      },
      options: {
        plugins: {
          tooltip: {
            callbacks: {
              label: (c) => {
                const source = sourceData[c.dataIndex].source;
                const sourceExp =
                  experiences[
                    sourceData[c.dataIndex].source.experienceMedian
                  ] || experiences[1];

                const target = sourceData[c.dataIndex].target;
                const targetExp =
                  experiences[
                    sourceData[c.dataIndex].target.experienceMedian
                  ] || experiences[1];
                return `${source.title} (${displayExperienceDuration(
                  sourceExp
                )})  →  ${target.title} (${displayExperienceDuration(
                  targetExp
                )})`;
              },
            },
          },
        },
      },
    };
  }
};
