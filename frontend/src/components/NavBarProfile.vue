<template>
<div class="routes-more-wrapper">
          <i
            @click="toggleMore"
            class="material-icons routes-display-more"
          >{{ displayMore ? 'expand_less' : 'expand_more' }}</i>

          <transition name="slide-fade">
            <div
              ref="routes-more"
              class="routes-more"
              v-if="displayMore"
              @focusout="toggleMore"
              tabindex="0"
            >
              <router-link :to="'/user/' + this.zID" class="routes-more-profile">
                <img
                  src="https://st3.depositphotos.com/6672868/14376/v/450/depositphotos_143767633-stock-illustration-user-profile-group.jpg"
                />
                <div class="routes-more-profile-text">
                  <div class="routes-more-profile-text-title">{{ name }}</div>
                  <span>{{ zID }}</span>
                </div>
              </router-link>
              <hr />
              <div class="routes-more-link">Profile</div>
              <router-link :to="{name:'changePassword'}" class="routes-more-link">Change Password</router-link>
              <div @click="signOut" class="routes-more-link">Log out</div>
            </div>
          </transition>
    
    </div>
</template>
<script>
export default {
    name: "NavBarProfile",
    data(){ return{ 
        "displayMore": false
    }},
    computed: {
        zID () {  return this.$store.getters['user/zID'] },
        name () { return this.$store.getters['user/name'] }
    },
    methods: {
        signOut() { this.$store.dispatch('user/signOut')},
        toggleMore() {
        this.displayMore = !this.displayMore;
        this.$nextTick(() => {
            console.log(this.displayMore); //eslint-disable-line
            if (this.displayMore) this.$refs["routes-more"].focus();
        });
        }
    }
    
}
</script>
<style scoped>
.routes-display-more {
  cursor: pointer;
  color: #82BF4B;
}
.routes-more-wrapper {
  position: relative;
}
.routes-more:focus {
  outline: none;
}
.routes-more {
  width: 200px;
  position: absolute;
  top: 2rem;
  right: 0;
  background-color: white;
  padding: 1rem;
  border-radius: 5px;
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s;
}
.slide-fade-enter,
.slide-fade-leave-to {
  transform: translateY(-30px);
  opacity: 0;
}

.routes-more-profile {
  display: flex;
  align-items: center;
  box-shadow: none;
}
.routes-more-profile-text {
  margin-left: 1rem;
  display: flex;
  flex-direction: column;
}
.routes-more-profile-text-title {
  font-weight: bold;
  display: block;

  color: black;
}
.routes-more-profile > img {
  width: 50px;
  border-radius: 25px;
}
.routes-more > hr {
  margin-top: 1rem;
}
.routes-more-link {
  padding-left: 1rem;
  padding-top: 1rem;
  cursor: pointer;
  display: block;
  color: black;
}
.routes-more-link:hover {
  color: black;
  font-weight: bold;
}
</style>