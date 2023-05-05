<!-- <template>
  <div>
    <div class="title"></div>
    <div ref="arcDiagram" class="arc-diagram"></div>
  </div>
</template>

<script setup>
import { ref, defineProps, onMounted } from "vue";
import * as d3 from "d3";

const props = defineProps({
  currentItem: {
    type: Object,
    default: () => {
      return null;
    },
  },
  data: {
    type: Object,
    default: () => {
      return null;
    },
  },
});

const arcDiagram = ref(null);

const constructArc = (element) => {
  const width_dim = 800;
  const height_dim = 1200;
  const data = props.data;

  // Refer to D3 documentation: https://d3-graph-gallery.com/graph/arc_template.html
  // set the dimensions and margins of the graph
  // const margin = { top: 0, right: 30, bottom: 50, left: 60 },
  //   width = width_dim - margin.left - margin.right,
  //   height = height_dim - margin.top - margin.bottom;

  // set the dimensions and margins of the graph
  var margin = { top: 20, right: 30, bottom: 20, left: 200 },
    width = width_dim - margin.left - margin.right,
    height = height_dim - margin.top - margin.bottom;

  // append the svg object to the body of the page
  var svg = d3
    .select(element)
    .append("svg")
    .attr("width", "100%")
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  // Read dummy data

  // List of node names
  var allNodes = data.nodes.map(function (d) {
    return d.name;
  });

  // A linear scale to position the nodes on the X axis
  var y = d3.scalePoint().range([0, height]).domain(allNodes);

  // Add the circle for the nodes
  svg
    .selectAll("mynodes")
    .data(data.nodes)
    .enter()
    .append("circle")
    .attr("cx", 50)
    .attr("cy", function (d) {
      return y(d.name);
    })
    .attr("r", 8)
    .style("fill", function (d) {
      return d.id === props.currentItem?.id ? "#69b3a2" : "#88bbf2";
    });

  // And give them a label
  svg
    .selectAll("mylabels")
    .data(data.nodes)
    .enter()
    .append("text")
    .attr("x", 20)
    .attr("y", function (d) {
      return y(d.name);
    })
    .text(function (d) {
      return d.name;
    })
    .style("width", "200px")
    .style("word-break", "break-word")
    .style("text-anchor", "end")
    .style("display", "inline-block")
    .style("alignment-baseline", "end");

  // Add links between nodes. Here is the tricky part.
  // In the input data, links are provided between nodes -id-, NOT between node names.
  // So have to do a link between this id and the name
  var idToNode = {};
  data.nodes.forEach(function (n) {
    idToNode[n.id] = n;
  });
  // Cool, now if I do idToNode["2"].name I've got the name of the node with id 2

  // Add the links
  svg
    .selectAll("mylinks")
    .data(data.links)
    .enter()
    .append("path")
    .attr("d", function (d) {
      let start = y(idToNode[d.source].name); // X position of start node on the X axis
      let end = y(idToNode[d.target].name); // X position of end node
      return [
        "M",
        50,
        start, // the arc starts at the coordinate x=start, y=height-30 (where the starting node is)
        "A", // This means we're gonna build an elliptical arc
        ((start - end) / 2) * 4,
        ",", // Next 2 lines are the coordinates of the inflexion point. Height of this point is proportional with start - end distance
        (start - end) / 2,
        0,
        0,
        ",",
        start < end ? 1 : 0,
        50,
        ",",
        end,
      ] // We always want the arc on top. So if end is before start, putting 0 here turn the arc upside down.
        .join(" ");
    })
    .style("fill", "none")
    .attr("stroke", "black");
};

onMounted(() => {
  constructArc(arcDiagram.value);
});
</script>

<style scoped></style> -->
