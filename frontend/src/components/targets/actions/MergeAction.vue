<script setup lang="ts">
import type { Target } from "@/types/Target";

const props = defineProps({
  targets: { type: Array<Target>, required: true },
  checkedTargets: { type: Array<number>, required: true },
});
const emit = defineEmits(["update:targets", "update:checkedTargets"]);

function mergeTargets() {
  var targets = [...props.targets];
  const checkedTargets = [...props.checkedTargets];
  if (checkedTargets.length < 2) {
    alert("Please select atleast two targets");
    return;
  }

  // Get list of targets to merge
  var mergeTargets = targets.filter((t) => checkedTargets.includes(t.id));

  // Sort targets by number of target regions they have
  mergeTargets = mergeTargets.sort((a, b) =>
    a.regions.length > b.regions.length ? 1 : -1
  );

  // Grab biggest one, this is the one the others will be merged into
  mergeTargets.shift();

  // Replace with merge call and refresh
  targets = targets.filter((t) => !mergeTargets.includes(t));

  emit("update:targets", targets);
  emit("update:checkedTargets", []);
}
</script>

<template>
  <button class="p-1 hover:bg-red-400 mx-8 rounded-md" @click="mergeTargets()">
    Merge
  </button>
</template>
