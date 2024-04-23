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

    const weights = getWeights();
    const weightParams = `start=${start}&end=${end}&time=480&weather_weight=${weights.weather_weight}&difficulty_weight=${weights.difficulty_weight}&waiting_time_weight=${weights.waiting_time_weight}`;

    fetch(`http://127.0.0.1:5001/find_path?${weightParams}`)
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
              edge.addClass("highlighted");
            }
          });
        }
      })
      .catch((error) => console.error("Error loading the path:", error));
  }

  // Get current weight settings from sliders
  function getWeights() {
    return {
      weather_weight: document.getElementById("weather-weight").value,
      difficulty_weight: document.getElementById("difficulty-weight").value,
      waiting_time_weight: document.getElementById("waiting-time-weight").value,
    };
  }

  // Updates the graph with new data from the server without reinitializing the entire graph
  function updateGraphData(data) {
    let existingNodes = new Set(cy.nodes().map((node) => node.id())); // Track existing nodes
    let existingEdges = new Set(cy.edges().map((edge) => edge.id())); // Track existing edges

    cy.startBatch();

    // Update nodes
    data.nodes.forEach((nodeData) => {
      if (existingNodes.has(nodeData.data.id)) {
        cy.getElementById(nodeData.data.id).data(nodeData.data);
        existingNodes.delete(nodeData.data.id); // Mark this node as updated
      } else {
        cy.add({ group: "nodes", data: nodeData.data });
      }
    });

    // Remove nodes that were not updated
    existingNodes.forEach((nodeId) => {
      cy.getElementById(nodeId).remove();
    });

    // Update edges
    data.edges.forEach((edgeData) => {
      if (existingEdges.has(edgeData.data.id)) {
        cy.getElementById(edgeData.data.id).data(edgeData.data);
        existingEdges.delete(edgeData.data.id); // Mark this edge as updated
      } else {
        cy.add({ group: "edges", data: edgeData.data });
      }
    });

    // Remove edges that were not updated
    existingEdges.forEach((edgeId) => {
      cy.getElementById(edgeId).remove();
    });

    cy.endBatch();
  }

  // Refresh graph and path when slider values change
  function refreshGraph() {
    const weights = getWeights();
    const weightParams = `weather_weight=${weights.weather_weight}&difficulty_weight=${weights.difficulty_weight}&waiting_time_weight=${weights.waiting_time_weight}`;

    fetch(`http://127.0.0.1:5001/graph?${weightParams}`)
      .then((response) => response.json())
      .then((data) => {
        updateGraphData(data);
        if (startNode && endNode) {
          fetchAndDisplayPath(startNode, endNode);
        }
      })
      .catch((error) => console.error("Error loading data:", error));
  }

  // Initialize Cytoscape, setup sliders and initial graph
  fetch(
    "http://127.0.0.1:5001/graph?weather_weight=2.0&difficulty_weight=1.5&waiting_time_weight=1.0"
  )
    .then((response) => response.json())
    .then((data) => {
      cy = cytoscape({
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

      document.querySelectorAll("input[type=range]").forEach((input) => {
        input.addEventListener("input", () => {
          document.getElementById(input.id + "-display").textContent =
            input.value;
          refreshGraph();
        });
      });

      // Set initial start and end nodes if provided in the data or just default
      startNode = cy.nodes()[0].data("id");
      endNode = cy.nodes()[1].data("id");
      fetchAndDisplayPath(startNode, endNode); // Fetch initial path

      // Node tap event to set start and end for path fetching
      cy.on("tap", "node", function (evt) {
        const nodeId = this.data("id");
        if (!startNode || startNode === nodeId) {
          startNode = nodeId;
          endNode = null; // Reset end if same node tapped or no end set
        } else {
          endNode = nodeId;
        }
        if (startNode && endNode) {
          fetchAndDisplayPath(startNode, endNode);
        }
      });
    })
    .catch((error) =>
      console.error("Error loading initial graph data:", error)
    );
});
