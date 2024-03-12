document.addEventListener("DOMContentLoaded", function () {
  var cy = cytoscape({
    container: document.getElementById("cy"),

    layout: {
      name: "preset",
    },

    style: [
      {
        selector: "node",
        style: {
          "background-color": "#666",
          label: "data(id)",
          "text-valign": "center",
          color: "#fff",
          "text-outline-width": 2,
          "text-outline-color": "#888",
        },
      },
      {
        selector: "edge",
        style: {
          width: 3,
          "line-color": "#ccc",
          "target-arrow-color": "#ccc",
          "target-arrow-shape": "triangle",
          "curve-style": "bezier",
          label: "data(label)",
          "text-margin-y": -10,
          "text-background-color": "#ffffff",
          "text-background-opacity": 0.5,
          "text-background-shape": "roundrectangle",
          "text-background-padding": 3,
          color: "#000",
          "font-size": "10px",
          "edge-text-rotation": "autorotate",
        },
      },
    ],

    elements: {
      nodes: [
        { data: { id: "Slope 1" }, position: { x: 100, y: 100 } },
        { data: { id: "Slope 2" }, position: { x: 300, y: 50 } },
        { data: { id: "Slope 3" }, position: { x: 500, y: 100 } },
        { data: { id: "Lift A" }, position: { x: 100, y: 400 } },
        { data: { id: "Lift B" }, position: { x: 300, y: 450 } },
        { data: { id: "Lift C" }, position: { x: 500, y: 400 } },
      ],
      edges: [
        {
          data: {
            source: "Lift A",
            target: "Slope 1",
            label: "Easy, 5m, Sunny, 2m",
          },
        },
        {
          data: {
            source: "Lift B",
            target: "Slope 2",
            label: "Medium, 7m, Snow, 5m",
          },
        },
        {
          data: {
            source: "Lift C",
            target: "Slope 3",
            label: "Hard, 10m, Windy, 3m",
          },
        },
        { data: { source: "Slope 1", target: "Lift B", label: "Return" } },
        { data: { source: "Slope 2", target: "Lift C", label: "Return" } },
        { data: { source: "Slope 3", target: "Lift A", label: "Return" } },
      ],
    },
  });
});
