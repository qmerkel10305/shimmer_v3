<script setup lang="ts">
import { computed } from "vue";
import type { Target } from "@/types/Target";
import ThumbModal from "@/components/targets/actions/ThumbModal.vue";
import EditModal from "@/components/targets/actions/EditModal.vue";
import MergeAction from "@/components/targets/actions/MergeAction.vue";
import DeleteAction from "@/components/targets/actions/DeleteAction.vue";

const props = defineProps({
  targets: { type: Array<Target>, required: true },
  checkedTargets: { type: Array<number>, required: true },
});
const emit = defineEmits(["update:targets", "update:checkedTargets"]);
const targets = computed({
  get() {
    return props.targets;
  },
  set(targets) {
    emit("update:targets", targets);
  },
});

const checkedTargets = computed({
  get() {
    return props.checkedTargets;
  },
  set(checkedTargets) {
    emit("update:checkedTargets", checkedTargets);
  },
});
</script>

<template>
  <ul class="flex py-2 bg-gray-800/90 text-white font-sans text-l rounded-b-lg">
    <li class="mx-8 font-semibold">
      <h2 class="p-1">Target Operations:</h2>
    </li>
    <li>
      <MergeAction
        v-model:targets="targets"
        v-model:checkedTargets="checkedTargets"
      />
    </li>
    <li>
      <EditModal
        v-model:targets="targets"
        v-model:checkedTargets="checkedTargets"
      />
    </li>
    <li>
      <ThumbModal
        v-model:targets="targets"
        v-model:checkedTargets="checkedTargets"
      />
    </li>
    <li>
      <DeleteAction
        v-model:targets="targets"
        v-model:checkedTargets="checkedTargets"
      />
    </li>
  </ul>
</template>
