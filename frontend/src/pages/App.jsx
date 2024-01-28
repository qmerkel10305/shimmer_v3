import { Autocomplete, TextField, Typography } from "@mui/material";

export default function App() {
  return (
    <main className="flex flex-col items-center w-screen h-screen justify-center">
      <Typography variant="h3" className="italic">
        Shimmer
      </Typography>
      <Autocomplete
        disablePortal
        id="combo-box-demo"
        options={["something"]}
        sx={{ width: 300 }}
        renderInput={(params) => <TextField {...params} label="Flight Id" />}
        freeSolo
      />
    </main>
  );
}
