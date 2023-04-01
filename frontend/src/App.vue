<script setup lang="ts">
import { RouterView } from "vue-router";
import NavBar from "./components/NavBar.vue";
</script>

<template>
  <div
    class="bg-red-600 bg-arc-logo bg-cover bg-no-repeat flex flex-col h-screen"
  >
    <header>
      <NavBar />
    </header>
    <RouterView />
  </div>
</template>
