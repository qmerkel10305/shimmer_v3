<script setup lang="ts">
import type { Target } from "@/types/Target";
import type { PropType } from "vue";
import { COLORS, SHAPES } from "@/types/Target";
import { computed } from "vue";

const props = defineProps({
  modelValue: { type: Object as PropType<Target>, required: true },
});
const emit = defineEmits(["update:modelValue"]);

const target = computed({
  get() {
    return props.modelValue;
  },
  set(target) {
    emit("update:modelValue", target);
  },
});
function capitalize(s: string) {
  return s[0].toUpperCase() + s.slice(1);
}
</script>

<template>
  <div class="flex pt-2">
    <b>Orientation:</b>
    <input
      class="bg-gray-200 rounded-md mx-1 h-max flex-1 resize-none h-fit"
      v-model="target.orientation"
      type="number"
      maxlength="3"
    />
  </div>
  <div class="flex pt-2">
    <b>Shape:</b>
    <select
      v-model="target.shape"
      class="bg-gray-200 rounded-md mx-1 h-max flex-1 resize-none h-fit"
    >
      <option v-for="s in SHAPES" :value="s" :key="s">
        {{ capitalize(s) }}
      </option>
    </select>
  </div>
  <div class="flex pt-2">
    <b>Shape Color:</b>
    <select
      v-model="target.shape_color"
      class="bg-gray-200 rounded-md mx-1 h-max flex-1 resize-none h-fit"
    >
      <option v-for="c in COLORS" :value="c" :key="c">
        {{ capitalize(c) }}
      </option>
    </select>
  </div>
  <div class="flex pt-2">
    <b>Letter:</b>
    <input
      class="bg-gray-200 rounded-md mx-1 h-max flex-1 resize-none h-fit"
      v-model="target.letter"
      maxlength="1"
    />
  </div>
  <div class="flex pt-2">
    <b>Letter Color:</b>
    <select
      v-model="target.letter_color"
      class="bg-gray-200 rounded-md mx-1 h-max flex-1 resize-none h-fit"
    >
      <option v-for="c in COLORS" :value="c" :key="c">
        {{ capitalize(c) }}
      </option>
    </select>
  </div>
</template>
