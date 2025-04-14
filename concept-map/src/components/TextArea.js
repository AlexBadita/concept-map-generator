import { useState } from "react";
import { TextField, Button, Box } from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import { styled } from "@mui/material/styles";

const VisuallyHiddenInput = styled("input")({
  clip: "rect(0 0 0 0)",
  clipPath: "inset(50%)",
  height: 1,
  overflow: "hidden",
  position: "absolute",
  bottom: 0,
  left: 0,
  whiteSpace: "nowrap",
  width: 1,
});

const TextArea = ({ handleGraph }) => {
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (event) => {
    setText(event.target.value);
  };

  const handleFileChange = (event) => {
    const uploadedFile = event.target.files[0];
    if (uploadedFile && uploadedFile.type !== "application/pdf") {
      alert("Only PDF files are allowed.");
      return;
    }
    if (uploadedFile && uploadedFile.size > 5 * 1024 * 1024) {
      alert("File size must be less than 5 MB.");
      return;
    }
    setFile(uploadedFile);
  };

  const setGraph = (g) => {
    handleGraph(g);
  };

  const handleSubmit = async () => {
    if (!text) {
      alert("Please enter text");
      return;
    }

    setIsLoading(true);
    try {
      // Prepare the form data
      const formData = new FormData();
      formData.append("text", text);
      if (file) {
        formData.append("file", file);
      }

      // Send the request to the backend
      const response = await fetch("http://127.0.0.1:5000/send-data", {
        mode: "cors",
        method: "POST",
        body: formData,
      });

      // Check if the response is successful
      if (!response.ok) {
        const errorMessage = `Error: ${response.status} ${response.statusText}`;
        alert(errorMessage);
        return;
      }

      // Parse the response JSON
      const result = await response.json();

      // Extract the "graph" value from the response and pass it to setGraph
      if (result.success && result.graph) {
        setGraph(result.graph);
      } else {
        alert("Unexpected response format or missing graph data.");
      }

      // Clear the file input
    } catch (error) {
      // Handle any errors that occur during the fetch
      console.error("Error submitting data:", error);
      alert("An error occurred while submitting the data. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box
      sx={{
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        p: 2,
        boxSizing: "border-box",
      }}
    >
      <TextField
        label="Enter your text"
        variant="outlined"
        value={text}
        onChange={handleChange}
        multiline
        fullWidth
        maxRows={27}
        sx={{
          height: "90%",
          "& .MuiInputBase-root": {
            height: "100%",
            display: "flex",
            alignItems: "start",
          },
          mb: 1,
        }}
        inputProps={{ style: { textAlign: "justify" } }}
      />
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <Button
          variant="contained"
          color="primary"
          onClick={handleSubmit}
          sx={{ mt: 2 }}
          disabled={isLoading}
        >
          {isLoading ? "Submitting..." : "Submit"}
        </Button>
        <Button
          component="label"
          role={undefined}
          variant="contained"
          tabIndex={-1}
          startIcon={<CloudUploadIcon />}
          sx={{ mt: 2 }}
        >
          Upload file
          <VisuallyHiddenInput type="file" onChange={handleFileChange} />
        </Button>
      </Box>
    </Box>
  );
};

export default TextArea;
