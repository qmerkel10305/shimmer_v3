import { Autocomplete, TextField, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";

export default function Navigator({ size, defaultValue }) {
  const navigate = useNavigate();

  return (
    <Autocomplete
      disablePortal
      id="combo-box-demo"
      options={["something", "another"]}
      sx={{ width: 300 }}
      renderInput={(params) => <TextField {...params} label="Flight Id" />}
      onChange={(event) => {
        let flightId = event.target.textContent;
        console.log(flightId);
        navigate("/shimmer", { state: { flightId } });
      }}
      size={size}
      defaultValue={defaultValue}
      disableClearable
    />
  );
}
