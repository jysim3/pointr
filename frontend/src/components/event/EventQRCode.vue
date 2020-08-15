<template>
  <div>
    <canvas id="qr-canvas" />
  </div>
</template>

<script>
import QRCode from "qrcode";

export default {
  name: "EventQRCode",
  props: {
    eventID: {
      type: String,
      required: true
    }
  },
  mounted() {
    // Generating and adding QRCode to canvas
    const canvas = document.getElementById("qr-canvas")
    const url = window.location.href;
    
    QRCode.toCanvas(canvas, url);
  }
};
</script>
<style scoped>
canvas {
  height: 100% !important;
  width: 100% !important;
  object-fit: contain;
}
</style>