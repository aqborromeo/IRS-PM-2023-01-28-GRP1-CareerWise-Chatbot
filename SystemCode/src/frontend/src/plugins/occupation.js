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
