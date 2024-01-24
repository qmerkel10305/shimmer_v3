"use client";

import Link from "next/link";
import TextField from "@mui/material/TextField";
import Autocomplete from "@mui/material/Autocomplete";

export default function Home() {
  return (
    <main className="">
      <Link href="/images">images</Link>
      <Autocomplete
        disablePortal
        id="combo-box-demo"
        options="first"
        sx={{ width: 300 }}
        renderInput={(params) => <TextField {...params} label="Movie" />}
      />
    </main>
  );
}
