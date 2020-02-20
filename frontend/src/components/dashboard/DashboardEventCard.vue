<template>
  <div>
      <p>{{ eventData.name }}</p>
      <p>{{ eventData.location }}</p>
      <p>{{ eventData.date }}</p>
  </div>
</template>

<script>
export default {
    name: 'DashboardEventCard',
    props: {
        eventData: Object
        /* 
        eventData: {
            name,
            date,
            location,
            societyName,
            societyID,
        }
        */
    }
}
</script>

<style>

</style>