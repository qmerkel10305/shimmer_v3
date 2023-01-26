<script setup lang="ts">
import { reactive } from "vue";
import type { Target } from "@/interfaces/TargetInterface";
import StandardTable from "@/components/targets/StandardTable.vue";
import EmergentTable from "@/components/targets/EmergentTable.vue";

const targets: Target[] = reactive([
  {
    thumb: "/temp/8.jpg",
    id: 0,
    type: "Standard",
    regions: [1, 2, 3],
    letter: "C",
    letter_color: "Yellow",
    shape: "Semi Circle",
    shape_color: "Orange",
    orientation: 0,
  },
  {
    thumb: "/temp/8.jpg",
    id: 1,
    type: "Standard",
    regions: [1, 2, 3],
    letter: "C",
    letter_color: "Yellow",
    shape: "Semi Circle",
    shape_color: "Orange",
    orientation: 0,
  },
  {
    thumb: "/temp/8.jpg",
    id: 2,
    type: "Emergent",
    regions: [1, 2, 3],
    notes: "This dumbass is just in a field",
  },
]);
</script>

<template>
  <div class="table-auto min-w-full text-center">
    <h1 class="text-black text-xl text-left font-bold">Standard:</h1>
    <StandardTable :targets="targets" />
    <h1 class="text-black text-xl text-left font-bold">Emergent:</h1>
    <EmergentTable :targets="targets" />
  </div>
</template>
