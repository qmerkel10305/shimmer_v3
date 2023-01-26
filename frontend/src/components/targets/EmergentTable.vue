<script setup lang="ts">
import { computed } from "vue";
import type { Target } from "@/interfaces/TargetInterface";

const props = defineProps({
  targets: { type: Array<Target>, required: true },
});

const emergentTargets = computed(() => {
  return props.targets.filter((t) => {
    return t.type === "Emergent";
  });
});
</script>

<template>
  <table class="border min-w-full divide-y divide-black border-black">
    <thead class="bg-gray-200/85 font-bold">
      <tr class="">
        <th>Checkbox</th>
        <th>Target Picture</th>
        <th>Target ID</th>
        <th>Target Regions</th>
        <th>Notes</th>
      </tr>
    </thead>
    <tbody class="bg-white/85 divide-y divide-slate-900">
      <tr v-for="t in emergentTargets" :key="t.id">
        <td><input type="checkbox" /></td>
        <td class="grid place-items-center">
          <img :src="t.thumb" class="max-w-xs" />
        </td>
        <td>{{ t.id }}</td>
        <td>{{ t.regions }}</td>
        <td>{{ t.notes }}</td>
      </tr>
    </tbody>
  </table>
</template>
