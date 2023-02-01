<script setup lang="ts">
import { ref } from "vue";
import type { Target } from "@/types/Target";
import ExitButton from "../common/ExitButton.vue";

const props = defineProps({
  targets: { type: Array<Target>, required: true },
  checkedTargets: { type: Array<number>, required: true },
});
var show = ref(false);
defineEmits(["update:targets", "update:checkedTargets"]);

function show_modal() {
  // const targets = [...props.targets];
  const checkedTargets = [...props.checkedTargets];
  if (checkedTargets.length !== 1) {
    alert("Please select only one target");
    return;
  }
  show.value = true;
}
</script>

<template>
  <button class="p-1" @click="show_modal()" @keyup.esc="show = false">
    Edit
  </button>
  <div
    v-show="show"
    class="absolute inset-0 flex items-center justify-center bg-gray-700 bg-opacity-50"
  >
    <div class="max-w-2xl p-6 bg-white rounded-md shadow-xl text-black">
      <div class="flex items-center justify-between">
        <h3 class="text-2xl">Edit Target</h3>
        <ExitButton v-model="show" class="ml-2" />
      </div>
    </div>
  </div>
</template>
