
<template>
    <div class="imgDiv">
        <input type="file" style="display:none" 
        ref="fileInput" 
        @change="onFileSelected"
        accept="image/png, image/jpeg"/>
        <img 
        :src="src"
        @error="imgAlt"
        />
        <div class="edit"
        v-if="updateURL"
        @click="changePhoto"
        > 
            
            <i class="material-icons"> edit </i>
        </div>
    </div>
  
</template>

<script>
import axios from 'axios'
export default {
    props: {
        src: {
            type: String,
            required: true
        },
        updateURL: {
            type: String,
        },
        updateFieldName: {
            type: String,
            default: 'logo'
        }
    },
    data() {
        return {
        }

    },
    methods: {
        imgAlt(event) {
            event.target.src = "https://thumbs.dreamstime.com/b/default-avatar-profile-icon-social-media-user-vector-default-avatar-profile-icon-social-media-user-vector-portrait-176194876.jpg"
        },
        changePhoto(){
            this.$refs['fileInput'].click()
        },
        onFileSelected(event) {
            const selectedFile = event.target.files[0]
            const fd = new FormData()
            fd.append(this.updateFieldName, selectedFile, selectedFile.name)
            axios.patch(this.updateURL,fd, )
            .then(() => {
                this.$emit('update')
            })

        }
    }

}
</script>

<style scoped>
.imgDiv {
    position: relative;
}
img {

    width: 150px;
    object-fit: cover;
    height: 150px;
    box-shadow: 0 0rem 2rem 0rem rgba(59, 59, 95, 0.3);
    border-radius: 150px;
    flex-shrink: 0;

    position: relative;


}
.edit {
    content: '\A';
    position: absolute;
    width: 100%; height:100%;
    top:0; left:0;
    background:rgba(0,0,0,0.6);
    border-radius: 150px;
    opacity: 0;
    cursor: pointer;
}
.edit:hover {
    opacity: 1;
}
.edit > i {
    display: block;
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    color: white;
}
</style>