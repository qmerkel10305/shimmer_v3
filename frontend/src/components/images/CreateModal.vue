<script setup lang="ts">
import { TargetRegion } from "@/types/Region";
import { ref, onMounted, onUpdated, defineEmits } from "vue";

const canvas = ref<HTMLCanvasElement | null>(null);
var context: CanvasRenderingContext2D;
const props = defineProps({
  image: { type: HTMLImageElement, required: true },
  targetRegion: { type: TargetRegion, required: true },
});
const emit = defineEmits(["submitTarget", "resetTarget"]);

onMounted(() => {
  context = canvas.value?.getContext("2d")!;
});

onUpdated(() => {
  const img = props.image;
  const tr = props.targetRegion;
  context.drawImage(
    img,
    tr.top_left.x,
    tr.top_left.y,
    tr.width(),
    tr.height(),
    0,
    0,
    canvas.value?.width!,
    canvas.value?.height!
  );
});

function submit_target() {
  // api call create target
  props;
  emit("submitTarget");
}
</script>

<template>
  <div
    class="absolute inset-0 flex items-center justify-center bg-gray-700 bg-opacity-50"
  >
    <div class="max-w-2xl p-6 bg-white rounded-md shadow-xl text-black">
      <div class="flex items-center justify-between">
        <h3 class="text-2xl">Submit Target?</h3>
        <ExitButton @click="emit('resetTarget')" class="ml-2" />
      </div>
      <div class="mt-4 flex">
        <canvas class="max-w-xs aspect-square" ref="canvas"></canvas>
        <div class="px-2 grid place-items-center">
          <button
            class="px-10 py-2 text-red-100 bg-red-600 rounded"
            @click="submit_target()"
          >
            Submit
          </button>
          <button
            class="px-10 py-2 text-red-800 border border-red-600 rounded"
            @click="emit('resetTarget')"
          >
            Submit but in white
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
