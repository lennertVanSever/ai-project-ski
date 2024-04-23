document.addEventListener("DOMContentLoaded", function () {
  var cy; // Declare `cy` outside to make it accessible globally within this function
  let startNode = null;
  let endNode = null;

  // Function to clear previous highlighted path
  function clearHighlighted() {
    if (cy) {
      cy.$(".highlighted").removeClass("highlighted");
    }
  }

  // Function to fetch and display path
  function fetchAndDisplayPath(start, end) {
    if (!start || !end) return; // Ensure both start and end are set

    fetch(
      `http://127.0.0.1:5001/find_path?start=${start}&end=${end}&time=480&weather_weight=0.1&difficulty_weight=9.5&waiting_time_weight=0.5`
    )
      .then((response) => response.json())
      .then((pathData) => {
        clearHighlighted(); // Clear existing path highlights
        if (pathData.path && pathData.path.length > 1) {
          pathData.path.forEach((nodeId, index, array) => {
            if (index < array.length - 1) {
              let source = array[index];
              let target = array[index + 1];
              let edge = cy
                .edges()
                .filter(`edge[source="${source}"][target="${target}"]`);
              edge.addClass("highlighted"); // Add a class to existing edges
            }
          });
        }
      })
      .catch((error) => console.error("Error loading the path:", error));
  }

  fetch(
    "http://127.0.0.1:5001/graph?weather_weight=2.0&difficulty_weight=1.5&waiting_time_weight=1.0"
  )
    .then((response) => response.json())
    .then((data) => {
      cy = cytoscape({
        container: document.getElementById("cy"), // container to render in

        layout: {
          name: "preset", // using preset layout to use specified positions
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
          {
            selector: ".highlighted",
            style: {
              "line-color": "#f00",
              "target-arrow-color": "#f00",
              width: 6,
            },
          },
        ],

        elements: data,
      });

      // Set initial start and end nodes if provided in the data or just default
      startNode = cy.nodes()[0].data("id"); // default to first node
      endNode = cy.nodes()[1].data("id"); // default to second node
      fetchAndDisplayPath(startNode, endNode); // Fetch initial path

      // Handle node taps
      cy.on("tap", "node", function (evt) {
        const nodeId = this.data("id");

        if (startNode && endNode) {
          startNode = nodeId;
          endNode = null;
        } else if (endNode === null && startNode) {
          endNode = nodeId;
        }
        if (startNode && endNode) {
          fetchAndDisplayPath(startNode, endNode);
        }
      });
    })
    .catch((error) => console.error("Error loading the data:", error));
});
