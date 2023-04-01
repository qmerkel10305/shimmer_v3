import { ref } from "vue";
import type { TargetRegion } from "./Region";

export interface Target {
  thumb: string;
  id: number;
  type: string;
  regions: TargetRegion[];
  letter?: string;
  letter_color?: string;
  shape?: string;
  shape_color?: string;
  orientation?: number;
  notes?: string;
}

export const COLORS = [
  "black",
  "blue",
  "brown",
  "gray",
  "green",
  "orange",
  "purple",
  "red",
  "white",
  "yellow",
];

export const SHAPES = ref([
  "circle",
  "semicircle",
  "quarter_circle",
  "square",
  "rectangle",
  "trapezoid",
  "triangle",
  "pentagon",
  "hexagon",
  "octagon",
  "star",
  "cross",
]);

export const TYPES = ref(["Standard", "Emergent"]);
