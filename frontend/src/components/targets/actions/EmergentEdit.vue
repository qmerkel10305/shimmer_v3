<script setup lang="ts">
import type { Target } from "@/types/Target";
import type { PropType } from "vue";
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
</script>

<template>
  <div class="flex pt-2">
    <b>Notes:</b>
    <textarea
      class="bg-gray-200 rounded-md mx-1 h-max flex-1 resize-none h-fit"
      v-model="target.notes"
    ></textarea>
  </div>
</template>
