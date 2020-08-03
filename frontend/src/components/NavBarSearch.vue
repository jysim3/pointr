
<template>
  <div class="d-flex justify-content-center">
    <div class="col-6">
      <input
        v-model="searchText"
        class="input w-100"
        type="text"
        placeholder="Search for events/societies"
        @focusin="searchAction"
        @focusout="showSuggested = false"
      >
      <transition name="fade">
        <div
          v-show="showSuggested"
          class="autocomplete-items"
        >
          <div
            v-for="(m, i) in matched"
            :key="i"
            @click="selectSuggested(m)"
          >
            <strong>{{ m.label }}</strong>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
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
      if (this.searchText === '') {
        return
      }
      return this.searchData
        .filter(v => v.label.toUpperCase().includes(this.searchText.toUpperCase()))
        .sort().slice(0,5)
    }
  },
  methods: {
    searchAction() {
      if (this.searchData.length === 0 ) {
        const url = [
          '/api/event/upcoming',
          '/api/society/all'
        ]
        Promise.all(url.map(v => axios.get(v)))
          .then(([events, societies]) => {
            const eventData = events.data
            const societiesData = societies.data
            this.searchData = this.searchData.concat(eventData.data.map(v => ({
              label: v.name,
              _link: `/event/${v.id}`
            })))
            this.searchData = this.searchData.concat(societiesData.data.map(v => ({
              label: v.name,
              _link: `/society/${v.id}`
            })))
          })
      }
      this.showSuggested = true

    },
    selectSuggested(v) {
      this.showSuggested = false
      this.searchText = v.label
      this.$router.push(v._link)
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
@media only screen and (max-width: 900px) {
  .searchBar {
    display: none;
  }
}
</style>