<template>
  <div id="qr-container">
    <canvas id="qr-canvas"></canvas>
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
    canvas.style.height = '20rem'
    canvas.style.width = '20rem'
  }
};
</script>

<style>
#qr-container {
  display: inline-block;
}

#qr-canvas {
  border-radius: var(--border-radius);
}

</style>