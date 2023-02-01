<script setup lang="ts">
import { computed } from "vue";
import type { Target } from "@/types/Target";
import ThumbModal from "@/components/targets/modals/ThumbModal.vue";
import EditModal from "@/components/targets/modals/EditModal.vue";

const props = defineProps({
  targets: { type: Array<Target>, required: true },
  checkedTargets: { type: Array<number>, required: true },
});
const emit = defineEmits(["update:targets", "update:checkedTargets"]);
const localTargets = computed({
  get() {
    return props.targets;
  },
  set(localTargets) {
    emit("update:targets", localTargets);
  },
});

const localCheckedTargets = computed({
  get() {
    return props.checkedTargets;
  },
  set(localTargets) {
    emit("update:checkedTargets", localTargets);
  },
});

function deleteTargets() {
  var targets = [...localTargets.value];
  const checkedTargets = [...localCheckedTargets.value];
  if (checkedTargets.length === 0) {
    alert("Please select atleast one target");
    return;
  }
  targets = targets.filter((t) => !checkedTargets.includes(t.id));

  // Replace with delete call and refresh
  // For some reason you must refresh the checkedTargets as well or else it doesnt refresh
  localTargets.value = targets;
  localCheckedTargets.value = [];
}

function mergeTargets() {
  var targets = [...localTargets.value];
  const checkedTargets = [...localCheckedTargets.value];
  if (checkedTargets.length < 2) {
    alert("Please select atleast two targets");
    return;
  }
  console.log(targets, checkedTargets);

  // Get list of targets to merge
  var mergeTargets = targets.filter((t) => checkedTargets.includes(t.id));
  console.log(mergeTargets);

  // Sort targets by number of target regions they have
  mergeTargets = mergeTargets.sort((a, b) =>
    a.regions.length > b.regions.length ? 1 : -1
  );
  console.log(mergeTargets);

  // Grab biggest one, this is the one the others will be merged into
  mergeTargets.shift();
  console.log(mergeTargets);

  // Replace with merge call and refresh
  targets = targets.filter((t) => !mergeTargets.includes(t));
  console.log(targets);

  localTargets.value = targets;
  localCheckedTargets.value = [];
}
</script>

<template>
  <ul class="flex py-2 bg-gray-800/90 text-white font-sans text-l rounded-b-lg">
    <li class="mx-8 font-semibold">
      <h2 class="p-1">Target Operations:</h2>
    </li>
    <li class="mx-8 hover:bg-red-400 rounded-md">
      <button class="p-1" @click="mergeTargets()">Merge</button>
    </li>
    <li class="mx-8 hover:bg-red-400 rounded-md">
      <EditModal
        v-model:targets="localTargets"
        v-model:checkedTargets="localCheckedTargets"
      />
    </li>
    <li class="mx-8 hover:bg-red-400 rounded-md">
      <ThumbModal
        v-model:targets="localTargets"
        v-model:checkedTargets="localCheckedTargets"
      />
    </li>
    <li class="mx-8 hover:bg-red-400 rounded-md">
      <button class="p-1" @click="deleteTargets()">Delete</button>
    </li>
  </ul>
</template>
