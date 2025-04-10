import { useCallback, useEffect } from "react";
import ReactFlow, {
  applyNodeChanges,
  applyEdgeChanges,
  useNodesState,
  useEdgesState,
  addEdge,
  Controls,
  Background,
} from "react-flow-renderer";

const Flow = ({ graph }) => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  console.log("Flow", graph);
  useEffect(() => {
    if(graph){
      setNodes(graph.nodes);
      setEdges(graph.edges);
      console.log("Nodes: ", graph.nodes);
      console.log("Edges: ", graph.edges);
    }
  }, [graph]);

  const onConnect = useCallback(
    (connection) => setEdges((eds) => addEdge(connection, eds)),
    [setEdges]
  );

  return (
    <div style={{ width: "100%", height: "100%" }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        style={{ width: "100%", height: "100%" }}
        fitView
      >
        <Controls />
        <Background />/
      </ReactFlow>
    </div>
  );
};

export default Flow;
