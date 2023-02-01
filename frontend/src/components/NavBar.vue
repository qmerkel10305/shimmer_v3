<script setup lang="ts">
import { RouterLink } from "vue-router";
</script>

<template>
  <nav class="bg-black font-sans text-2xl">
    <ul class="flex py-2">
      <li class="mx-8">
        <RouterLink
          to="/"
          class="text-white font-mono"
          active-class="active"
          exact
          ><span style="color: red">Sh</span>immer
        </RouterLink>
      </li>
      <li class="mr-6">
        <RouterLink
          to="/images/next"
          class="text-white hover:bg-red-400 rounded-sm"
          active-class="active"
          exact
          >Images
        </RouterLink>
      </li>
      <li class="mr-6">
        <RouterLink
          to="/targets"
          class="text-white hover:bg-red-400 rounded-sm"
          active-class="active"
          exact
          >Targets
        </RouterLink>
      </li>
    </ul>
  </nav>
</template>
