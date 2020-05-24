
<template>
<div>
      <div class="searchBar">
        <input
        class="input"
        type="text"
        v-model="searchText"
        placeholder="Search for events/societies"
        @focusin="showSuggested = true"
        @focusout="showSuggested = false"
        />
        <transition name="fade">
            <div v-show="showSuggested" class="autocomplete-items">
                <div @click="selectSuggested(m)" v-for="(m, i) in matched" :key="i">
                    <strong>{{m}}</strong>
                </div>
            </div>
        </transition>
      </div>
      </div>
</template>

<script>
export default {
    name: "NavBarSearch",
    components: {
    },
    data() {
        return {
        searchText: "",
        searchData: [],
        showSuggested: false
        };
    },
    computed: {

        matched() {
            return [
            'hihi',
            'boop']
        }
    },
    methods: {
        selectSuggested(v) {
            this.showSuggested = false
            this.searchText = v
        },
    },
    
}
</script>
<style scoped>
.searchBar {
    flex-grow: 1;
    margin: 0 50px;
    max-width: 300px;
    position: relative;
    display: flex;
}
.searchBar input {
    width: 100%
}
.autocomplete-items {
  position: absolute;
  border: 1px solid #d4d4d4;
  border-bottom: none;
  border-top: none;
  z-index: 99;
  /*position the autocomplete items to be the same width as the container:*/
  top: 100%;
  left: 0;
  right: 0;
}
.autocomplete-items div {
  padding: 10px;
  cursor: pointer;
  background-color: #fff;
  border-bottom: 1px solid #d4d4d4;
}
.autocomplete-items div:hover {
    background-color: #f3f3f3;
}
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s;
}
.fade-enter,
.fade-leave-to {
  transform: translateY(-3px);
  opacity: 0;
}
</style>