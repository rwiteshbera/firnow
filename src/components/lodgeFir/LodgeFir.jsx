import React from "react";
import { useState } from "react";
import { IconButton, TextField } from "@mui/material";
import Autocomplete from "@mui/material/Autocomplete";
import { Typography } from "@mui/material";
import { Button } from "@mui/material";
import { Stack } from "@mui/material";
import { Box } from "@mui/material";
import { Container } from "@mui/material";
import axios from "axios";

import "./lodgeStyle.css";

const LodgeFir = () => {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileUpload = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = () => {
    const formData = new FormData();
    formData.append("file", selectedFile);
    axios
      .post("/api/upload", formData)
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  };
  return (
    <>
      <h2 className="form_title">Lodge Fir</h2>
      <div className="form_lodge">
        <TextField
          variant="outlined"
          placeholder="Write your name"
          className="form_text"
        />
        <br />
        <br />
        <TextField
          variant="outlined"
          placeholder="Write the name of accused one"
          className="form_text"
        />
        <br />
        <br />
        <TextField
          variant="standard"
          row={3}
          multiline={2}
          className="form_desc"
          placeholder="  Write the description of crime"
          InputProps={{
            disableUnderline: true,
          }}
        ></TextField>
        <br />
        <br />
        <Autocomplete
          disablePortal
          id="combo-box-demo"
          options={district}
          className="selection_box"
          renderInput={(params) => (
            <TextField {...params} label="Select your District" />
          )}
        />
        <br />
        <Autocomplete
          disablePortal
          id="combo-box-demo"
          options={thana}
          className="selection_box"
          renderInput={(params) => (
            <TextField {...params} label="Select your Thana" />
          )}
        />
        <br />
        <Container
          sx={{
            boxShadow: "0 10px 15px -3px rgba(0, 0, 0, 0.1)",
            borderRadius: "0.75rem",
            fontFamily:
              "ui-sans-serif, system-ui, sans-serif, Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol, Noto Color Emoji",
            background: "rgb(255, 255, 255)",
            display: "flex",
            flexDirection: "column",
            width: "100%",
            maxWidth: "650px",
          }}
        >
          <Stack
            sx={{
              justifyContent: "space-between",
              alignItems: "center",
              width: "100%",
              padding: "12px",
              " @media(max-width:479px)": { padding: "16px 18px" },
            }}
            spacing="0px"
            direction="row"
          >
            <Typography
              variant="h3"
              sx={{
                fontSize: "20px",
                " @media(max-width:479px)": { fontSize: "18px" },
              }}
            >
              Attach proof file
            </Typography>
          </Stack>
          <Box sx={{ padding: "12px", width: "100%" }}>
            <Stack
              sx={{
                borderRadius: "0.375rem",
                border: "1px dashed rgb(204, 204, 204)",
                padding: "14px",
                width: "100%",
                alignItems: "center",
              }}
              spacing="20px"
            >
              <img
                src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZlcnNpb249IjEuMSIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHdpZHRoPSI1MTIiIGhlaWdodD0iNTEyIiB4PSIwIiB5PSIwIiB2aWV3Qm94PSIwIDAgNTEyIDUxMiIgc3R5bGU9ImVuYWJsZS1iYWNrZ3JvdW5kOm5ldyAwIDAgNTEyIDUxMiIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSIgY2xhc3M9IiI+PGNpcmNsZSByPSIyNTYiIGN4PSIyNTYiIGN5PSIyNTYiIGZpbGw9IiNkY2RjZGMiIHNoYXBlPSJjaXJjbGUiIHRyYW5zZm9ybT0ibWF0cml4KDEsMCwwLDEsMCwwKSI+PC9jaXJjbGU+PGcgdHJhbnNmb3JtPSJtYXRyaXgoMC41MTk5OTk5OTk5OTk5OTk5LDAsMCwwLjUxOTk5OTk5OTk5OTk5OTksMTIyLjg4MDAwMDAwMDAwMDAyLDEyMi44ODAwMDAwMDAwMDAwMikiPjxwYXRoIGQ9Ik00NjcgMjExSDMwMVY0NWMwLTI0Ljg1My0yMC4xNDctNDUtNDUtNDVzLTQ1IDIwLjE0Ny00NSA0NXYxNjZINDVjLTI0Ljg1MyAwLTQ1IDIwLjE0Ny00NSA0NXMyMC4xNDcgNDUgNDUgNDVoMTY2djE2NmMwIDI0Ljg1MyAyMC4xNDcgNDUgNDUgNDVzNDUtMjAuMTQ3IDQ1LTQ1VjMwMWgxNjZjMjQuODUzIDAgNDUtMjAuMTQ3IDQ1LTQ1cy0yMC4xNDctNDUtNDUtNDV6IiBmaWxsPSIjOWY5ZjlmIiBvcGFjaXR5PSIxIiBkYXRhLW9yaWdpbmFsPSIjMDAwMDAwIiBjbGFzcz0iIj48L3BhdGg+PC9nPjwvc3ZnPg=="
                width="35px"
                height="35px"
              />
              <Typography
                variant="p"
                sx={{ fontSize: "14px", fontWeight: "600" }}
              >
                Drop your files here to attach them
              </Typography>
              <input type="file" onChange={handleFileUpload} />
              <Button
                variant="contained"
                type="submit"
                onChange={handleFileUpload}
                sx={{
                  backgroundColor: "#0d2036",
                  color: "rgb(255, 255, 255)",
                  fontSize: "14px",
                  fontWeight: "700",
                  justifyContent: "center",
                  alignItems: "center",
                  padding: "8px 12px",
                  textTransform: "none",
                }}
              >
                Upload
              </Button>
              
              
            </Stack>
          </Box>
        </Container>
        <br />
        <br />
        <div className="submit_div">
          <button type="submit" onClick={handleUpload} className="submit_btn">
            Lodge FIR
          </button>
        </div>
      </div>
      <br />
      <br />
      <br />
      <br />
    </>
  );
};
const district = [
  { label: "Hooghly" },
  { label: "Howrah" },
  { label: "Kolkata" },
  { label: "Bakura" },
  { label: "Other" },
];

const thana = [
  { label: "Hooghly - Uttarpara" },
  { label: "Kolkata - ParkStreet" },
  { label: "Other" },
];

export default LodgeFir;
