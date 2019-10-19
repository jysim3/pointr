<template>
  <div id="home-container">
    <h1>Thanks for attending, {{this.username}}</h1>

    <div id="container">
      <h2>Events you attended</h2>
      <div id="table-container">
        <table cellspacing="0" id="attendance-table">
          <tr>
            <th>Event name</th>
            <th>Points</th>
          </tr>
          <tr v-for="(event,index) in events" :key="index">
            <td class="td-name">{{ event.name }}</td>
            <td class="td-points">{{ event.points }}</td>
          </tr>
        </table>
      </div>
    </div>
  </div>
</template>
<script>
import { fetchAPI } from "@/util.js";
export default {
  name: '',
  props: {
    zid: String
  },
  data() {
    return {
      username: "Steven",
      events: []
    };
  },
  mounted() {
    fetchAPI(`/api/user?zID=${this.zid}`, "GET")
    .then(j => {
      console.log(j); // eslint-disable-line
      this.events = j.events;
      this.username = j.name;
    });
  }
};
</script>
<style scoped>
@import "../assets/style.css";

#home-container {
  background-color: var(--primary-yellow);
  width: 100vw;
  height: 100vh;
}

#table-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 2rem 0;
}

h1 {
    margin-top: 0;
    padding-top: 2rem;
    margin-bottom: 3rem;
}

h2 {
    text-align: center;
}

table {
  width: 40%;
  margin: 0;
  padding: 0;
}

th {
  font-size: 1.75rem;
  text-align: left;
  background-color: var(--dark-grey);
  color: white;
  font-weight: 400;
  padding: 1rem;
}

tr {
  font-size: 1.5rem;
  text-align: left;
  border: 1px solid var(--dark-grey);
}

td {
    padding: 0.5rem 1rem;
}

.td-name {
    background: white;
}
.td-points {
    background: var(--bgc-grey);
}
</style>