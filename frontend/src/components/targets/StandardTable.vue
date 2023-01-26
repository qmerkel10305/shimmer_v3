<script setup lang="ts">
import { computed } from "vue";
import type { Target } from "@/interfaces/TargetInterface";

const props = defineProps({
  targets: { type: Array<Target>, required: true },
});

const standardTargets = computed(() => {
  return props.targets.filter((t) => {
    return t.type === "Standard";
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
        <th>Target Shape</th>
        <th>Shape Color</th>
        <th>Shape Letter</th>
        <th>Letter Color</th>
        <th>Target Orientation</th>
      </tr>
    </thead>
    <tbody class="bg-white/85 divide-y divide-slate-900">
      <tr v-for="t in standardTargets" :key="t.id">
        <td><input type="checkbox" /></td>
        <td class="grid place-items-center">
          <img :src="t.thumb" class="max-w-xs" />
        </td>
        <td>{{ t.id }}</td>
        <td>{{ t.regions }}</td>
        <td>{{ t.shape }}</td>
        <td>{{ t.shape_color }}</td>
        <td>{{ t.letter }}</td>
        <td>{{ t.letter_color }}</td>
        <td>{{ t.orientation }}</td>
      </tr>
    </tbody>
  </table>
</template>
