import { useState } from "react";
import { Box } from "@mui/material";
import Flow from "./Flow";
import TextArea from "./TextArea";

const Layout = () => {
  const [graph, setGraoh] = useState("");

  const handleGraph = (g) => {
    setGraoh(g);
  };

  return (
    <Box sx={{ display: "flex", height: "100vh" }}>
      <Box sx={{ width: "80%", height: "100%" }}>
        <Flow graph={graph} />
      </Box>
      <Box sx={{ width: "20%", height: "100%" }}>
        <TextArea handleGraph={handleGraph} />
      </Box>
    </Box>
  );
};

export default Layout;
