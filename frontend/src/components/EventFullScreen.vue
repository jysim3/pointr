
<template>
    <div class="fullscreen" ref="fullscreen-div">
      <div class="left">
        <a @click="$emit('exitFullScreen')" class="material-icons">chevron_left</a>
        <div class="left-after"> </div>
        <div>
            <img class="logo" src="../assets/logo.png" alt="pointr logo" />
            <button @click="share" class="btn btn-primary">Share full screen picture</button>
            </div>
        <div></div>
      </div>
      <div class="right">

      </div>
      <div class="right-content">
        <h3> Welcome </h3>
        <h3>to</h3>
        <h1>{{name}}</h1>
        by<h3 class="societies">{{ this.eventSoc }}</h3>
        <hr/>
        <h3> Mark your attendance </h3>
        <h3>@</h3>
        <h3 class="primary">pointr.live</h3>
        <div class="options">
            <h3>Option 1:</h3>
            <div class="box"> 
                <h3> Scan the QR code to sign in </h3>
                <EventQRCode :eventID="this.eventID" />
            </div>
        </div>
        <div class="options">
            <h3>Option 2:</h3>
            <div class="box"> 
                <h3>Head to <span class="primary">pointr.live/event/{{this.eventID}}</span> to sign in</h3>
            </div>
        </div>
    </div>
    </div>
</template>

<script>
import EventQRCode from "@/components/event/EventQRCode.vue";
import html2canvas from 'html2canvas'
import { saveAs } from 'file-saver'
export default {
    props: {
        eventID: {
            required: true,
            type: String
        },
        name: {
            required: true,
            type: String
        },
        eventSoc: {
            required: true,
            type: String
        }
    },
    components: {
        EventQRCode,
    },
    methods: {
        share() {
            html2canvas(this.$refs['fullscreen-div'], {
                backgroundColor: '#f7f7f7',
                width: 1579,
                height: 1047,
                windowWidth: 1579,
                windowHeight: 1047,
                
            })
            .then(v => {
                v.toBlob(b => {
                    saveAs(b, `${this.name}.png`)
                })
            })

        }
    }
}
</script>

<style scoped>

.fullscreen {
  z-index: 1;
  height: 100%;
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  right: 0;
}
.left,.right {
    height: 100%;
    background: var(--c-secondary);
    position: relative;
}
.left {
    float: left;
    position: fixed;
    background-image:  url(/img/unsw.780d0411.jpg);
    width: calc(50%);
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    align-items: center;
}
.left div {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
img {
    width: 50%;
}
.right, .right-content {

    float: right;
    width: calc(50% - 20px);
    padding-top: 2rem;
    text-align: center;
}
.right {
    position: fixed;
    right: 0;
    z-index: -1;
}
.societies {
    color: rgb(143, 106, 0);
    margin-top: 1rem;
}
.right * {
    font-weight: bold;
    font-family: KollectifBold;
}
h1 {
    font-family: Kollektif;
    color: var(--c-primary);
    font-size: 4rem;
}
h3 {
    font-size: 2rem;
    color: black;
}
.left-after {
    position: absolute;
    top: 0;
    width: 0;
    height: 0;
}
.left-after {
    left: calc(100% - 100px);
    border-top: 100vh solid transparent;
    border-right: 100px solid var(--c-secondary);
}
hr {
    border-color: black;
    border-radius: 0;
    border-width: 1px;
    margin: 4rem 0;
}
.options {
    margin-top: 2rem;
    display: flex;
    align-items: center;
}
.options h3 {
    margin-right: 1rem;
}
a {
    position: fixed;
    font-size: 3rem;
    position: absolute;
    top: 0;
    left: 0;
    z-index: 2;
    color: white;
}
</style>