"use client";

import Image from "@/components/image";

export default function Images() {
  const to_server = new WebSocket("ws://localhost:8000/ws");
  to_server.addEventListener("open", (_) => {
    console.log("Connected to server");
    to_server.send("Hello server");
    // ask for flight id images
  });

  to_server.addEventListener("message", (event) => {
    console.log(`Received message ${event.data}`);
  });
  to_server.addEventListener(
    "close",
    (event) => console.log(`Socket closed ${event.data}`),
  );
  to_server.addEventListener(
    "error",
    (event) => console.log(`Error logged ${event.data}`),
  );
  return (
    <main>
      <section className="grid grid-cols-3">
        <Image />
        <Image />
        <Image />
        <Image />
      </section>
    </main>
  );
}
