<script setup lang="ts">
import { RouterView } from "vue-router";
import NavBar from "./components/NavBar.vue";
</script>

<template>
  <div
    class="h-screen bg-red-600 bg-arc-logo bg-cover bg-no-repeat overflow-hidden"
  >
    <header>
      <NavBar />
    </header>
    <RouterView />
  </div>
</template>
