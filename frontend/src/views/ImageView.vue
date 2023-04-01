<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { Point } from "@/types/Point";
import type { Image } from "@/types/Image";
import { TargetRegion } from "@/types/Region";
import CreateModal from "@/components/images/CreateModal.vue";
const MIN_SELECTION_SIZE = 0.1;

const route = useRoute();
const router = useRouter();

const canvas = ref<HTMLCanvasElement | null>(null);
var showModal = ref(false);
var context: CanvasRenderingContext2D;
const imgHTML = new Image();
imgHTML.onload = render;
var img: Image;
var image_id: number;
var xDifference: number;
var yDifference: number;
var imageHeight: number;
var imageWidth: number;
var locked = false;

var selection: TargetRegion | null;
var modalRegion: TargetRegion;

function offsetHeaderHeight(x: number): number {
  return x - 50;
}

watch(
  () => route.params.id,
  (id) => {
    handleId(id.toString());
  }
);

onMounted(() => {
  context = canvas.value?.getContext("2d")!;
  handleId(route.params.id.toString());
  context.fillStyle = "rgba(127, 255, 127, 0.3)";

  // V-On key handlers do not work on canvas because the browser does not allow a canvas to be focussed
  window.addEventListener("keydown", keyHander);
});

onUnmounted(() => {
  window.removeEventListener("keydown", keyHander);
});

function handleId(id: string) {
  if (id === "next") {
    //Get next api
    image_id = 0;
    router.push(`/images/${image_id}`);
  } else {
    image_id = parseInt(id);
    //Get Image api
    img = {
      id: 0,
      targets: [],
    };
    //imgHTML.src = `api/image/${image.id}/img.jpg`
    imgHTML.src = "/temp/flight_95_im00153.jpg";
  }
}

function render() {
  if (canvas.value != null) {
    const corrected_height = offsetHeaderHeight(window.innerHeight);
    // Set image height and width and canvasElement height and width to the height and width of the window
    // Image height and width will be reassigned later
    imageHeight = canvas.value.height = corrected_height;
    imageWidth = canvas.value.width = window.innerWidth;
    context.clearRect(0, 0, imageWidth, imageHeight);

    // Calculates image and widow ratio to determine which dimension (height or width) we need to scale
    const imageRatio = imgHTML.width / imgHTML.height;
    const windowRatio = imageWidth / imageHeight;

    // If the image has a larger width than height then reset the width
    if (imageRatio < windowRatio) {
      imageWidth = corrected_height * imageRatio;
    } else {
      // If the image has a larger height than width then reset the height
      imageHeight = window.innerWidth / imageRatio;
    }

    // Calculate the offset needed for each dimension
    xDifference = (window.innerWidth - imageWidth) / 2;
    yDifference = (corrected_height - imageHeight) / 2;

    context?.drawImage(
      imgHTML,
      xDifference,
      yDifference,
      imageWidth,
      imageHeight
    );

    // Render Target Regions
    img.targets.forEach((tr: TargetRegion) => {
      renderTargetRegion(tr);
    });

    if (
      selection != null &&
      Math.abs(selection.width()) > 0 &&
      Math.abs(selection.height()) > 0
    ) {
      renderTargetRegion(selection);
    }
  }
}

function renderTargetRegion(tr: TargetRegion) {
  context.fillStyle = "rgba(127, 255, 127, 0.3)";
  const x1 = tr.top_left.x * (imageWidth / imgHTML.width) + xDifference;
  const y1 = tr.top_left.y * (imageHeight / imgHTML.height) + yDifference;
  const x2 = tr.bottom_right.x * (imageWidth / imgHTML.width) + xDifference;
  const y2 = tr.bottom_right.y * (imageHeight / imgHTML.height) + yDifference;
  context.fillRect(x1, y1, x2 - x1, y2 - y1);
}

function mouseDown(event: MouseEvent) {
  if (locked) {
    // Exit if the target classifier window is showing
    return;
  }

  // Doesn't allow targets to be drawn in regions where the picture isn't when mouse is clicked
  const corrected_y = offsetHeaderHeight(event.y);
  if (
    event.x < xDifference ||
    corrected_y < yDifference ||
    event.x > xDifference + imageWidth ||
    corrected_y > yDifference + imageHeight
  ) {
    return;
  }

  const point = new Point(
    Math.round((event.x - xDifference) * (imgHTML.width / imageWidth)),
    Math.round((corrected_y - yDifference) * (imgHTML.height / imageHeight))
  );

  img.targets.forEach((tr: TargetRegion) => {
    if (tr.contains(point)) {
      showSubmission(tr);
      return;
    }
  });

  selection = new TargetRegion(point, point, img.id);
}

function mouseMove(event: MouseEvent) {
  if (selection == null) {
    return;
  }

  let [x, y] = bindSelectionToCanvas(event);

  selection.bottom_right = new Point(
    Math.round((x - xDifference) * (imgHTML.width / imageWidth)),
    Math.round((y - yDifference) * (imgHTML.height / imageHeight))
  );

  render();
}

function mouseUp(event: MouseEvent) {
  if (selection == null) {
    return;
  }

  let [x, y] = bindSelectionToCanvas(event);

  selection.bottom_right = new Point(
    Math.round((x - xDifference) * (imgHTML.width / imageWidth)),
    Math.round((y - yDifference) * (imgHTML.height / imageHeight))
  );

  if (selection.top_left.delta(selection.bottom_right) < MIN_SELECTION_SIZE) {
    selection = null;
    return;
  }
  if (selection.top_left.x > selection.bottom_right.x) {
    // This ensures a is smaller than b
    const x_temp = selection.top_left.x;
    selection.top_left.x = selection.bottom_right.x;
    selection.bottom_right.x = x_temp;
  }
  if (selection.top_left.y > selection.bottom_right.y) {
    // This ensures a is smaller than b
    const y_temp = selection.top_left.y;
    selection.top_left.y = selection.bottom_right.y;
    selection.bottom_right.y = y_temp;
  }
  showSubmission(selection);
  render();
  selection = null;
}

function keyHander(event: KeyboardEvent) {
  if (locked) {
    // Exit if the target classifier window is showing
    return;
  }

  const key = event.key;
  if (key === "Enter") {
    loadNextImage(event);
  }

  if (key === "ArrowUp") {
    navigationMenu();
  }

  if (key == "ArrowLeft") {
    router.push(`/images/${image_id - 1}`);
  }

  if (key == "ArrowRight") {
    router.push(`/images/${image_id + 1}`);
  }
}

function loadNextImage(event: KeyboardEvent) {
  // api get next image
  event;
  router.push(`/images/${image_id + 1}`);
}

function navigationMenu() {
  const id_string = prompt("Image id number?", "0");
  if (id_string != null) {
    const id = parseInt(id_string);
    router.push(`/images/${id}`);
  }
}

function bindSelectionToCanvas(event: MouseEvent): [number, number] {
  let x: number, y: number;
  const corrected_y = offsetHeaderHeight(event.y);
  // Checks to see if x coordinate is greater than image width plus offset, if so sets x to edge of image
  if (event.x > imageWidth + xDifference) {
    x = imageWidth + xDifference;
  } else if (event.x < xDifference) {
    // Checks to see if x coordinate is in the offset, if so sets x to beginning of image
    x = xDifference;
  } else {
    // Valid x coordinate
    x = event.x;
  }

  // Checks to see if y coordinate is greater than image height plus offset, if so sets y to edge of image
  if (corrected_y > imageHeight + yDifference) {
    y = imageHeight + yDifference;
  } else if (corrected_y < yDifference) {
    // Checks to see if y coordinate is in the offset, if so sets y to beginning of image
    y = yDifference;
  } else {
    // Valid y coordinate
    y = corrected_y;
  }

  return [x, y];
}

function submitTarget() {
  resetTarget();
  // get image
  render();
}

function resetTarget() {
  // logic if targetregion in image, send delete
  showModal.value = false;
  locked = false;
}

function showSubmission(tr: TargetRegion) {
  modalRegion = tr;
  locked = true;
  showModal.value = true;
}
</script>

<template :key="$route.params.id">
  <canvas
    class="min-w-full h-screen overflow-hidden"
    ref="canvas"
    @mousedown="mouseDown"
    @mousemove="mouseMove"
    @mouseup="mouseUp"
  ></canvas>
  <CreateModal
    v-show="showModal"
    :image="imgHTML"
    :target-region="modalRegion"
    @submit-target="submitTarget"
    @reset-target="resetTarget"
  ></CreateModal>
</template>
