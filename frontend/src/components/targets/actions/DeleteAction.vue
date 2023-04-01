<script setup lang="ts">
import type { Target } from "@/types/Target";

const props = defineProps({
  targets: { type: Array<Target>, required: true },
  checkedTargets: { type: Array<number>, required: true },
});
const emit = defineEmits(["update:targets", "update:checkedTargets"]);

function deleteTargets() {
  var targets = [...props.targets];
  const checkedTargets = [...props.checkedTargets];
  if (checkedTargets.length === 0) {
    alert("Please select atleast one target");
    return;
  }
  targets = targets.filter((t) => !checkedTargets.includes(t.id));

  emit("update:targets", targets);
  emit("update:checkedTargets", []);
}
</script>

<template>
  <button class="p-1 hover:bg-red-400 mx-8 rounded-md" @click="deleteTargets()">
    Delete
  </button>
</template>
