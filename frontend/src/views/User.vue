<template>
  <div id="home-container">
    <h1>Thanks for attending, {{this.username}}</h1>
    <div id="container">
      <h2>Events you've attended</h2>
      <div id="table-container">
        <table cellspacing="0" id="attendance-table">
          <tr>
            <th>Event name</th>
            <!-- <th>Points</th> -->
          </tr>
          <tr v-for="(event,index) in events" :key="index">
            <td class="td-name">{{ event.name }}</td>
            <!-- <td class="td-points">{{ event.points }}</td> -->
          </tr>
        </table>
      </div>
    </div>
  </div>
</template>
<script>
import { fetchAPI } from "@/util.js";
export default {
  name: "User",
  props: {
    zID: String
  },
  data() {
    return {
      username: "",
      events: []
    };
  },
  created() {
    fetchAPI(`/api/user?zID=${this.zID}`, "GET").then(j => {
      console.log(j); // eslint-disable-line
      this.events = j.events;
      this.username = j.name;
    });
  }
};
</script>
<style scoped>

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
  background-color: var(--c-primary);
  color: white;
  font-weight: 400;
  padding: 1rem;
}

tr {
  font-size: 1.5rem;
  text-align: left;
  border: 1px solid var(--c-secondary-dark);
}

td {
    padding: 0.5rem 1rem;
}

.td-name {
    background: white;
}
.td-points {
    background: var(--c-secondary-light);
}
</style>