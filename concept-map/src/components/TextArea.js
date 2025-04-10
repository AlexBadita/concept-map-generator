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

  const handleChange = (event) => {
    setText(event.target.value);
  };

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const setGraph = (g) => {
    handleGraph(g);
  };

  const handleSubmit = async () => {
    if (text) {
      const formData = new FormData();
      formData.append("text", text);
      if (file) {
        formData.append("file", file);
      }
      const response = await fetch("http://127.0.0.1:5000/send-data", {
        mode: "cors",
        method: "POST",
        body: formData,
      });
      console.log(response);
      const result = await response.json();
      console.log("Recieved: ", result);
      setFile(null);
      setGraph(result);
    } else {
      alert("Please enter text");
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
        >
          Submit
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
