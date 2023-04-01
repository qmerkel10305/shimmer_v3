<script setup lang="ts">
import { ref, computed } from "vue";
import type { Target } from "@/types/Target";
import ExitButton from "@/components/common/ExitButton.vue";
import EmergentEdit from "@/components/targets/actions/EmergentEdit.vue";
import StandardEdit from "@/components/targets/actions/StandardEdit.vue";
import { TYPES } from "@/types/Target";

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

var show = ref(false);
var target = ref<Target>({
  thumb: "",
  id: 0,
  type: "",
  regions: [],
});
var org_target: Target;
var target_index: number;

function show_modal() {
  const constTargets = [...targets.value];
  const constCheckedTargets = [...checkedTargets.value];
  if (constCheckedTargets.length !== 1) {
    alert("Please select only one target");
    return;
  }
  target_index = constTargets.findIndex((t) => t.id === constCheckedTargets[0]);
  if (target_index === -1) {
    alert("Target not found");
    return;
  }
  target.value = constTargets[target_index];
  org_target = { ...target.value };
  show.value = true;
  checkedTargets.value = [];
}

function cancel_modal() {
  const constTargets = [...targets.value];
  Object.assign(constTargets[target_index], org_target);
  targets.value = constTargets;
  exit_modal();
}

function exit_modal() {
  show.value = false;
}
</script>

<template>
  <button
    class="p-1 hover:bg-red-400 mx-8 rounded-md"
    @click="show_modal()"
    @keyup.esc="cancel_modal()"
  >
    Edit
  </button>
  <div
    v-show="show"
    class="absolute inset-0 flex items-center justify-center bg-gray-700 bg-opacity-50"
  >
    <div class="max-w-2xl p-6 bg-white rounded-md shadow-xl text-black">
      <div class="flex items-center justify-between">
        <h3 class="text-2xl">Edit Target</h3>
        <ExitButton @click="cancel_modal()" class="ml-2" />
      </div>
      <div class="mt-4 flex">
        <img :src="target.thumb" class="max-w-xs" />
        <div class="px-2">
          <div><b>Target Id:</b> {{ target.id }}</div>
          <div>
            <b>Target Regions:</b> {{ target.regions.map((tr) => tr.id) }}
          </div>
          <div class="flex">
            <b>Target Type:</b>
            <select v-model="target.type" class="bg-gray-200 rounded-md mx-1">
              <option v-for="t in TYPES" :value="t" :key="t">
                {{ t }}
              </option>
            </select>
          </div>
        </div>
      </div>
      <EmergentEdit v-if="target.type === 'Emergent'" v-model="target" />
      <StandardEdit v-if="target.type === 'Standard'" v-model="target" />
      <div class="py-2 flex">
        <button
          class="px-6 py-2 text-red-100 bg-red-600 rounded"
          @click="exit_modal()"
        >
          Save
        </button>
        <button
          class="px-6 ml-2 text-red-800 border border-red-600 rounded"
          @click="cancel_modal()"
        >
          Cancel
        </button>
      </div>
    </div>
  </div>
</template>
