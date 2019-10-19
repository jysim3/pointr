<template>
  <div>
    <ul>
      <li v-for="(attendee, index) in attendees" :key="index">
        {{ attendee }}
        <!-- EDIT ICON -->
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="48"
          height="48"
          viewBox="0 0 48 48"
        >
          <title>ic_edit_48px</title>
          <g fill="#111111">
            <path
              d="M6 34.5V42h7.5l22.13-22.13-7.5-7.5L6 34.5zm35.41-20.41c.78-.78.78-2.05 0-2.83l-4.67-4.67c-.78-.78-2.05-.78-2.83 0l-3.66 3.66 7.5 7.5 3.66-3.66z"
            />
          </g>
        </svg>
        <!-- DELETE ICON -->
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48">
          <title>ic_close_48px</title>
          <g fill="#111111">
            <path
              d="M38 12.83L35.17 10 24 21.17 12.83 10 10 12.83 21.17 24 10 35.17 12.83 38 24 26.83 35.17 38 38 35.17 26.83 24z"
            />
          </g>
        </svg>
      </li>
    </ul>
  </div>
</template>

<script>
// import fetchAPI from '@/util.js'
// import { apiURL } from "@/util.js"

export default {
  name: "Attendees",
  props: ["eid", "attendees"],
  mounted() {}
};
</script>

<style>
</style>