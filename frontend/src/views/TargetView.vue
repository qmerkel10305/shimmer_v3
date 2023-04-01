<script setup lang="ts">
import { reactive, ref } from "vue";
import type { Target } from "@/types/Target";
import { Point } from "@/types/Point";
import StandardTable from "@/components/targets/tables/StandardTable.vue";
import EmergentTable from "@/components/targets/tables/EmergentTable.vue";
import ActionBar from "@/components/targets/ActionBar.vue";
import { TargetRegion } from "@/types/Region";

var targets: Target[] = reactive([
  {
    thumb: "/temp/8.jpg",
    id: 0,
    type: "Standard",
    regions: [new TargetRegion(new Point(0, 0), new Point(0, 0), 0, 0, 0)],
    letter: "C",
    letter_color: "yellow",
    shape: "semicircle",
    shape_color: "orange",
    orientation: 0,
  },
  {
    thumb: "/temp/8.jpg",
    id: 1,
    type: "Standard",
    regions: [
      new TargetRegion(new Point(0, 0), new Point(0, 0), 0, 1, 1),
      new TargetRegion(new Point(0, 0), new Point(0, 0), 0, 1, 3),
    ],
    letter: "C",
    letter_color: "yellow",
    shape: "semicircle",
    shape_color: "orange",
    orientation: 0,
  },
  {
    thumb: "/temp/8.jpg",
    id: 2,
    type: "Emergent",
    regions: [
      new TargetRegion(new Point(0, 0), new Point(0, 0), 0, 2, 2),
      new TargetRegion(new Point(0, 0), new Point(0, 0), 0, 2, 4),
      new TargetRegion(new Point(0, 0), new Point(0, 0), 0, 2, 5),
    ],
    notes: "Example target sitting in field",
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
