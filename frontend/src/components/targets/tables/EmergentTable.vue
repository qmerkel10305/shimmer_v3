<script setup lang="ts">
import { computed } from "vue";
import type { Target } from "@/types/Target";

const props = defineProps({
  targets: { type: Array<Target>, required: true },
  modelValue: { type: Array<number>, required: true },
});
const emit = defineEmits(["update:modelValue"]);

const emergentTargets = computed(() => {
  return props.targets.filter((t) => {
    return t.type === "Emergent";
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
</script>

<template>
  <table class="border min-w-full divide-y divide-black border-black">
    <thead class="bg-gray-200/[.85] font-bold">
      <tr class="">
        <th>Checkbox</th>
        <th>Target Picture</th>
        <th>Target ID</th>
        <th>Target Regions</th>
        <th>Notes</th>
      </tr>
    </thead>
    <tbody class="bg-white/[.85] divide-y divide-slate-900">
      <tr v-for="t in emergentTargets" :key="t.id">
        <td>
          <input type="checkbox" :value="t.id" v-model="checkedTargets" />
        </td>
        <td class="grid place-items-center p-1">
          <img :src="t.thumb" class="max-w-xs" />
        </td>
        <td>{{ t.id }}</td>
        <td>{{ t.regions.map((tr) => tr.id) }}</td>
        <td>{{ t.notes }}</td>
      </tr>
    </tbody>
  </table>
</template>
