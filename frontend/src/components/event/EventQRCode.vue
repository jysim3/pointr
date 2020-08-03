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
    canvas.style.height = '15rem'
    canvas.style.width = '15rem'
  }
};
</script>