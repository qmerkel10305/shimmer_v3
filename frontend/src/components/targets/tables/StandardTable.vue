<script setup lang="ts">
import { computed } from "vue";
import type { Target } from "@/types/Target";

const props = defineProps({
  targets: { type: Array<Target>, required: true },
  modelValue: { type: Array<number>, required: true },
});
const emit = defineEmits(["update:modelValue"]);

const standardTargets = computed(() => {
  return props.targets.filter((t) => {
    return t.type === "Standard";
  });
});

const checkedTargets = computed({
  get() {
    return props.modelValue;
  },
  set(localCheckedTargets) {
    emit("update:modelValue", localCheckedTargets);
  },
});

function capitalize(s: string | undefined) {
  if (s == undefined) {
    return "";
  }
  return s[0].toUpperCase() + s.slice(1);
}
</script>

<template>
  <table class="border min-w-full divide-y divide-black border-black">
    <thead class="bg-gray-200/[.85] font-bold">
      <tr class="">
        <th>Checkbox</th>
        <th>Target Picture</th>
        <th>Target ID</th>
        <th>Target Regions</th>
        <th>Target Shape</th>
        <th>Shape Color</th>
        <th>Shape Letter</th>
        <th>Letter Color</th>
        <th>Target Orientation</th>
      </tr>
    </thead>
    <tbody class="bg-white/[.85] divide-y divide-slate-900">
      <tr v-for="t in standardTargets" :key="t.id">
        <td>
          <input type="checkbox" :value="t.id" v-model="checkedTargets" />
        </td>
        <td class="grid place-items-center p-1">
          <img :src="t.thumb" class="max-w-xs" />
        </td>
        <td>{{ t.id }}</td>
        <td>{{ t.regions.map((tr) => tr.id) }}</td>
        <td>{{ capitalize(t.shape) }}</td>
        <td>{{ capitalize(t.shape_color) }}</td>
        <td>{{ capitalize(t.letter) }}</td>
        <td>{{ capitalize(t.letter_color) }}</td>
        <td>{{ t.orientation }}</td>
      </tr>
    </tbody>
  </table>
</template>
