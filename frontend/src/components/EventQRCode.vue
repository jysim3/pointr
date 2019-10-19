<template>
  <div>
    <canvas id="qr-canvas"></canvas>
    <h1>{{ this.eid }}</h1>
  </div>
</template>

<script>
import QRCode from "qrcode";

export default {
  name: "EventQRCode",
  props: ["eid"],
  mounted() {
    // const generateQR = async text => {
    //   await QRCode.toDataURL(text)
    //   // try {
    //   //   console.log();
    //   // } catch (err) {
    //   //   console.error(err);
    //   // }
    // };

    // const addQRCode = async text => {
    //   const canvas = document.getElementById("qr-canvas")
    //   const qrcode = generateQR(text)
    //   canvas.appendChild(qrcode)
    // }

    // addQRCode(this.eid)
    const canvas = document.getElementById("qr-canvas")
    const url = `${window.location.host}/e/${this.eid}`
    QRCode.toCanvas(canvas, url);
    console.log(url) //eslint-disable-line
  }
};
</script>