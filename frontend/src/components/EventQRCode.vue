<template>
  <div>
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
    const url = `${window.location.host}/e/${this.eid}`
    QRCode.toCanvas(canvas, url);
    // canvas.style.height = '10rem'
    // canvas.style.width = '10rem'
    // console.log(url) //eslint-disable-line
  }
};
</script>

<style>
</style>