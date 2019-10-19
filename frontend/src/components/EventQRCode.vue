<template>
  <div id="qr-container">
    <canvas id="qr-canvas"></canvas>
  </div>
</template>

<script>
import QRCode from "qrcode";

export default {
  name: "EventQRCode",
  props: ["eid"],
  mounted() {
    // Generating and adding QRCode to canvas
    const canvas = document.getElementById("qr-canvas")
    const url = `${window.location.host}/#/e/${this.eid}`
    QRCode.toCanvas(canvas, url);
    canvas.style.height = '15rem'
    canvas.style.width = '15rem'
    // console.log(url) //eslint-disable-line
  }
};
</script>

<style>
#qr-container {
  display: inline-block;
}
</style>