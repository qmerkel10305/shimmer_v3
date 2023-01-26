<script setup lang="ts">
import { RouterLink } from "vue-router";
</script>

<template>
  <main>
    <div class="grid grid-cols-2 content-evenly h-screen justify-items-center">
      <div class="font-sans text-left text-3xl">
        <h2>Flight Number: x</h2>
        <h2>Date: Jan 3rd, 2023</h2>
        <h2>Images: 203</h2>
        <h2>Targets: 8</h2>
      </div>
      <ul class="flex flex-col text-black text-3xl">
        <li class="bg-white hover:bg-red-400 rounded-md mb-3">
          <RouterLink to="/images/next" class="p-5" active-class="active" exact
            >Images</RouterLink
          >
        </li>
        <li class="bg-white hover:bg-red-400 rounded-md">
          <RouterLink to="/targets" class="p-5" active-class="active" exact
            >Targets</RouterLink
          >
        </li>
      </ul>
    </div>
  </main>
</template>
