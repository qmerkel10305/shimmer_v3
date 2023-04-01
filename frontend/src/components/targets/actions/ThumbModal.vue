<script setup lang="ts">
import { ref } from "vue";
import type { Target } from "@/types/Target";
import type { TargetRegion } from "@/types/Region";
import ExitButton from "@/components/common/ExitButton.vue";

const props = defineProps({
  targets: { type: Array<Target>, required: true },
  checkedTargets: { type: Array<number>, required: true },
});
var show = ref(false);
var regions = ref<TargetRegion[]>();
defineEmits(["update:targets", "update:checkedTargets"]);

function show_modal() {
  const targets = [...props.targets];
  const checkedTargets = [...props.checkedTargets];
  if (checkedTargets.length !== 1) {
    alert("Please select only one target");
    return;
  }
  regions.value = (
    targets.find((t) => t.id === checkedTargets[0]) as Target
  ).regions;
  show.value = true;
}

function select_thumb(region: TargetRegion) {
  // Replace with call to backend
  console.log(region.id);
  show.value = false;
}

function close_modal() {
  show.value = false;
}
</script>

<template>
  <button
    class="p-1 hover:bg-red-400 mx-8 rounded-md"
    @click="show_modal()"
    @keyup.esc="show = false"
  >
    Thumbnail
  </button>
  <div
    v-show="show"
    class="absolute inset-0 flex items-center justify-center bg-gray-700 bg-opacity-50"
  >
    <div class="max-w-2xl p-6 bg-white rounded-md shadow-xl text-black">
      <div class="flex items-center justify-between">
        <h3 class="text-2xl">Select Thumbnail</h3>
        <ExitButton @click="close_modal()" class="ml-2" />
      </div>
      <div class="mt-4 flex justify-center">
        <div v-for="r in regions" :key="r.id">
          <img
            src="/temp/8.jpg"
            class="max-w-xs p-2 hover:bg-gray-300 cursor-pointer rounded-md"
            @click="select_thumb(r)"
          />
        </div>
      </div>
    </div>
  </div>
</template>
