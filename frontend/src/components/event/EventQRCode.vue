<template>
  <canvas ref="qr-canvas" />
</template>

<script>
import QRCode from "qrcode";

export default {
  name: "EventQRCode",
  props: {
    url: {
      type: String,
      required: true
    }
  },
  watch: {
    url(n) {
      QRCode.toCanvas(this.$refs['qr-canvas'], n);
    }
  },
  mounted() {
    QRCode.toCanvas(this.$refs['qr-canvas'], this.url);
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