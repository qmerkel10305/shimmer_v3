<script setup lang="ts">
import { reactive, ref } from "vue";
import type { Target } from "@/types/Target";
import StandardTable from "@/components/targets/tables/StandardTable.vue";
import EmergentTable from "@/components/targets/tables/EmergentTable.vue";
import ActionBar from "@/components/targets/ActionBar.vue";

var targets: Target[] = reactive([
  {
    thumb: "/temp/8.jpg",
    id: 0,
    type: "Standard",
    regions: [
      {
        top_left: { x: 0, y: 0 },
        bottom_right: { x: 0, y: 0 },
        target_id: 0,
        image_id: 0,
        id: 0,
      },
    ],
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
    regions: [
      {
        top_left: { x: 0, y: 0 },
        bottom_right: { x: 0, y: 0 },
        target_id: 1,
        image_id: 0,
        id: 1,
      },
      {
        top_left: { x: 0, y: 0 },
        bottom_right: { x: 0, y: 0 },
        target_id: 1,
        image_id: 0,
        id: 3,
      },
    ],
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
    regions: [
      {
        top_left: { x: 0, y: 0 },
        bottom_right: { x: 0, y: 0 },
        target_id: 2,
        image_id: 0,
        id: 2,
      },
      {
        top_left: { x: 0, y: 0 },
        bottom_right: { x: 0, y: 0 },
        target_id: 2,
        image_id: 0,
        id: 4,
      },
      {
        top_left: { x: 0, y: 0 },
        bottom_right: { x: 0, y: 0 },
        target_id: 2,
        image_id: 0,
        id: 5,
      },
    ],
    notes: "This dumbass is just in a field",
  },
]);

var checkTargets = ref(Array<number>());
</script>

<template>
  <ActionBar v-model:targets="targets" v-model:checkedTargets="checkTargets" />
  <div class="table-auto min-w-full text-center">
    <h1 class="text-black text-xl text-left font-bold">Standard:</h1>
    <StandardTable :targets="targets" v-model="checkTargets" />
    <h1 class="text-black text-xl text-left font-bold">Emergent:</h1>
    <EmergentTable :targets="targets" v-model="checkTargets" />
  </div>
</template>
